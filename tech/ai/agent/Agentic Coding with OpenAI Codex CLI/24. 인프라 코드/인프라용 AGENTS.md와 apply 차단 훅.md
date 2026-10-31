# 인프라용 AGENTS.md와 apply 차단 훅

인프라 저장소는 애플리케이션 저장소와 관례가 다르다. 이 문서는 인프라 전용 AGENTS.md에 무엇을 적는지, 그 금지 사항을 훅(hook)으로 어떻게 강제하는지, 그리고 이 파일을 저장소 어디에 두는지를 설명한다.

---

## 1. 인프라 AGENTS.md의 내용

원서가 보여 주는 AGENTS.md는 크게 세 덩어리다. 테스트 명령, 관례, 금지 사항이다.

**테스트 명령**

| 목적 | 명령 |
| --- | --- |
| 포맷 | `terraform fmt -recursive` |
| 문법 검사 | `terraform init -backend=false` 후 `terraform validate` |
| 변경 미리보기 | `terraform plan -out=tfplan` |
| 린트 | `tflint --init` 후 `tflint` (Google 룰셋, `--init`은 TFLint 플러그인 캐시에 씀) |
| 보안 스캔 | `checkov -d . --compact` |

**관례**

- 프로바이더는 google, 실행 환경은 Cloud Run, 정적 자산은 Cloud Storage.
- 모든 리소스 이름은 `{project}-{env}-{resource}` 규칙을 따른다.
- 변수는 `variables.tf`, 출력은 `outputs.tf`에 둔다.
- 원격 상태는 `backend.tf`(GCS 백엔드)에 설정하며 절대 고치지 않는다.
- 계산된 값은 인라인 식이 아니라 `locals` 블록에 둔다.
- 서비스마다 서비스 계정을 하나씩 쓰고 기본 Compute 서비스 계정은 쓰지 않는다.
- `.terraform.lock.hcl`은 커밋하고 gitignore에 넣지 않는다. 프로바이더 버전을 고정하는 파일이기 때문이다.

**금지 사항**

- `terraform apply`, `terraform destroy`, `gcloud run deploy`를 실행하지 않는다.
- `.terraform.lock.hcl`을 직접 수정하지 않는다.
- `modules/shared/` 아래 파일은 명시적 승인 없이 건드리지 않는다.
- 자격 증명, 토큰, 비밀 값을 커밋하지 않는다.

핵심은 `terraform apply` 금지다. 원서는 이 금지를 `gcloud run deploy`까지 넓힌다. 이 명령도 새 리비전을 운영에 곧장 밀어 넣어 같은 경계를 넘기 때문이다. 애플리케이션 코드는 테스트를 돌려도 안전하지만, 이 명령들은 즉시 되돌릴 수 없는 영향을 낸다. 에이전트는 계획하고 검증하고 제안하며, 검토와 적용은 사람이 한다.

## 2. 문서에 적은 금지는 제안일 뿐이다

AGENTS.md에만 적어 두면 그 금지는 부탁에 가깝다. 에이전트는 이를 읽고 대개 따르지만, 운이 나쁜 날에는 `terraform apply`를 그냥 실행한다. 폭발 반경이 운영 환경인 명령에 "대개"로는 부족하다. 그래서 훅(9장)을 함께 쓴다. 훅이 해당 명령을 아예 막아서 부탁을 벽으로 바꾼다.

`PreToolUse` 훅은 셸 명령이 실행되기 전에 불리고, 0이 아닌 값으로 종료해 그 명령을 거부할 수 있다. 훅 설정은 이렇다.

```json
{
  "hooks": {
    "PreToolUse": [{
      "hooks": [{
        "type": "command",
        "command": "bash .codex/scripts/block-apply.sh",
        "statusMessage": "Checking for apply-boundary violations…",
        "timeout": 5
      }]
    }]
  }
}
```

스크립트는 실행하려는 명령을 읽어서 실제 인프라를 바꿀 만한 것을 거부한다.

```bash
#!/usr/bin/env bash
# .codex/scripts/block-apply.sh
set -euo pipefail
payload="$(cat)"   # PreToolUse JSON, 실행할 명령이 들어 있다
if printf '%s' "$payload" \
  | grep -qE 'terraform[[:space:]]+(apply|destroy)|gcloud[[:space:]]+run[[:space:]]+deploy'; then
  echo "Blocked: apply/destroy/deploy cross the apply boundary. A human runs these." >&2
  exit 2
fi
```

이제 지시를 어겨도 경계는 유지된다. 에이전트는 계획과 검증은 얼마든지 할 수 있지만, 운영을 건드리는 종류의 명령은 문 앞에서 거부된다. 그 명령은 사람이 에이전트 바깥에서 의식적으로 실행한다. 같은 훅은 `kubectl delete`나 `gcloud sql`처럼 팀이 막고 싶은 되돌릴 수 없는 명령 어디에나 확장할 수 있다.

## 3. 샌드박스 모드: 읽기 전용에서 시작한다

인프라 작업의 가장 안전한 출발점은 읽기 전용 샌드박스(`-s read-only`)다. 이 모드에서 에이전트는 모듈을 읽고, 계획을 만들고, 변경을 제안할 수 있지만 파일을 쓰거나 명령을 실행하지 못한다. 에이전트가 테라폼 파일을 직접 쓸 준비가 되었을 때만 `workspace-write`로 올린다. 이 쓰기 단계에서는 에이전트가 명령을 실행할 수 있으므로, 금지를 믿는 것이 아니라 강제해야 한다. 그때 `PreToolUse` 훅이 마지막 안전망이 된다.

## 4. 인프라 AGENTS.md는 어디에 두는가

단일 언어 저장소라면 이 파일이 루트 AGENTS.md가 된다. 하지만 Run or Relax는 단일 언어가 아니다. 루트에는 22장에서 만든 파이썬용 AGENTS.md가 있고, `frontend/`에는 23장의 리액트용 AGENTS.md가 있어서 각자 자기 도구 체인을 다룬다. 인프라용은 이들과 같은 종류의 세 번째 파일이며, 루트가 아니라 자기 디렉터리에 둔다.

```text
run-or-relax/
├── AGENTS.md            # Python: uv, pytest, ruff (22장)
├── src/departures/      # FastAPI 서비스
├── frontend/
│   └── AGENTS.md        # React: pnpm, vitest (23장)
└── infra/
    ├── AGENTS.md        # Terraform: validate, tflint, checkov, apply 금지
    └── modules/         # cloud_run, site, ...
```

Codex CLI는 AGENTS.md 파일을 범위 순서대로 합치고 가장 깊은 파일이 이긴다(22장의 중첩 덮어쓰기 동작). 그래서 `infra/` 아래 파일은 에이전트가 인프라 작업을 할 때만 적용된다.

이 범위 나누기는 겉치레가 아니다. 루트 파일은 "모든 도구는 `uv run`으로 돌리고 `pytest`가 초록이면 끝"이라고 말하는데, 테라폼에는 정확히 틀린 규칙이다. 인프라 관례를 루트에 두면 저장소의 3분의 2에서 파이썬 규칙과 모순된다. `infra/`에 두면 HCL을 쓰는 곳에서만 `terraform validate`와 apply 금지가 적용되고, 파이썬과 리액트 규칙은 그 근처에 오지 않는다.

그리고 이 파일에는 다른 점만 적는다. Conventional Commits나 비밀 커밋 금지처럼 모두에게 공통인 관례는 루트에서 물려받는다. 그래서 인프라 AGENTS.md에는 테라폼과 스캐너 명령, 그리고 무엇보다 `apply`, `destroy`, `gcloud run deploy` 금지처럼 인프라에만 해당하는 내용만 둔다. 나머지를 반복하면 루트가 바뀔 때 두 파일이 어긋난다.

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
