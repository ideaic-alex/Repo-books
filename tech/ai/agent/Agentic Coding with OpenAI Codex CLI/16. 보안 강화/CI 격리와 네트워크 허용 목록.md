# CI 격리와 네트워크 허용 목록

CI에서는 실행이 매번 같은 결과를 내야 하고, 밖으로 나가는 네트워크 연결은 명시한 곳으로만 열려 있어야 한다. 이 문서는 사용자 설정의 영향을 걷어 내는 두 플래그, 컨테이너 격리, 관리형 네트워크 허용 목록, 환경별 프로필을 설명한다.

---

## 1. CI 격리: 두 개의 플래그

CI 파이프라인은 결정적인(deterministic) 실행이 필요하다. 아래 두 플래그가 사용자 설정에서 오는 변수를 없앤다.

```bash
codex --ignore-user-config --ignore-rules exec "run the test suite and fix failures"
```

- `--ignore-user-config`는 ~/.codex/config.toml을 아예 로드하지 않는다. 에이전트는 기본값과 CLI로 준 설정만으로 시작한다. CI 러너에 남아 있는 사용자 설정이 파이프라인 동작에 영향을 주지 못한다.
- `--ignore-rules`는 사용자와 프로젝트의 execpolicy `.rules` 파일을 로드하지 않는다. 이 파일은 명령이 실행 정책에 어떻게 맞춰질지를 바꾼다. 대화형으로 쓸 때는 유용하지만 CI에서는 비결정성의 원인이 된다.

두 플래그를 같이 쓰면 러너에 상주하는 사용자 설정이 모두 빠진다. 단 AGENTS.md와 관리형 requirements.toml은 여전히 로드된다. 따라서 이 실행은 완전히 밀폐된(hermetic) 것이 아니라 재현 가능한(reproducible) 것이다.

GitHub Actions 워크플로 예시는 다음과 같다.

```yaml
# .github/workflows/codex-ci.yml
- name: Run Codex agent (clean-room)
  run: |
    codex \
      --ignore-user-config \
      --ignore-rules \
      -a on-request \
      exec "fix the failing tests in src/auth/"
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

중요한 점이 하나 있다. `--ignore-user-config`는 관리형 설정(requirements.toml)을 건너뛰지 않는다. 관리형 규칙은 사용자 취향이 아니라 조직 정책이므로 항상 로드된다. 그래서 클린룸 CI 실행에서도 기업 보안 정책은 계속 적용된다.

## 2. 컨테이너로 가장 강하게 격리

보증 수준이 가장 높아야 하는 상황이라면 최소 파일 시스템만 가진 컨테이너 안에서 Codex CLI를 돌린다. Codex CLI에는 공식 컨테이너 이미지가 없다. 아래 예의 my-codex-image는 직접 만들어야 하는 이미지다. 언어 기반 이미지에서 시작해 Dockerfile에서 `npm install -g @openai/codex`(또는 설치 스크립트)로 Codex를 설치한다.

```bash
docker run --rm \
  -v "$(pwd)/src:/workspace/src:rw" \
  -v "$(pwd)/tests:/workspace/tests:rw" \
  -v "$(pwd)/docs:/workspace/docs:ro" \
  -e OPENAI_API_KEY="$OPENAI_API_KEY" \
  my-codex-image \
  codex exec "fix the failing tests"
```

docs/를 읽기 전용(:ro)으로 마운트했기 때문에, 에이전트가 문서 파일을 쓰려 해도 커널이 거부한다.

## 3. 네트워크 허용 목록

밖으로 네트워크 호출을 할 수 있는 에이전트 시스템은 설정 실수 한 번이면 코드베이스를 유출한다. 방어는 명시적 허용 목록(allowlist)이다.

```toml
# requirements.toml (managed): centralised allowlist
[experimental_network]
enabled = true
allowed_domains = ["api.openai.com", "registry.npmjs.org", "github.com"]
managed_allowed_domains_only = true
```

`managed_allowed_domains_only = true`이면 allowed_domains 밖의 호스트로 나가는 모든 연결이 정책 위반으로 실패한다. 운영 환경에서 원하는 기본 거부 자세가 이것이다.

MCP 서버도 따로 점검한다. 각 서버의 외부 호출이 서버가 내세운 목적 안에 있는지 확인해야 한다. "GitHub 이슈 조회"를 한다면서 외부 분석 엔드포인트로 몰래 연락하는 MCP 서버는 공급망 위험이다. 켜기 전에 MCP 서버의 소스 코드를 검토하고, 그 서버가 꼭 필요로 하는 호스트만 허용 목록에 넣는다.

허용 목록은 다른 공격도 막아 준다. 주입된 지시가 에이전트에게 공격자 URL을 curl로 받아 bash로 넘기라고 시키는 경우다. 그 도메인이 허용 목록에 없으면 페이로드를 가져오기 전에 curl 자체가 실패한다.

네트워크 정책에도 환경별 프로필을 쓴다. 개발 프로필은 허용 목록을 느슨하게, 운영 프로필은 엄격하게 둔다. CI 파이프라인에서는 `codex --profile production exec "..."`처럼 프로필을 지정한다.

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
