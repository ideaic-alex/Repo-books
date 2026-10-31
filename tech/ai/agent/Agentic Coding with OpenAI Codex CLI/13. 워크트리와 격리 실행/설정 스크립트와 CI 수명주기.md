# 설정 스크립트와 CI 수명주기

워크트리를 막 만들면 소스 파일만 있고 돌아가는 환경은 없다. 또 CI에서는 워크트리 생성부터 삭제까지 사람 손 없이 자동으로 돌아가야 한다. 이 문서는 워크트리 설정 스크립트, CI용 수명주기 스크립트, GitHub Actions 예시, 병렬 매트릭스 작업을 다룬다.

---

## 1. 워크트리 설정 스크립트

환경 준비가 안 된 워크트리에서는 에이전트가 빠진 의존성을 찾느라 턴을 낭비한다. 워크트리를 만든 직후에 돌릴 스크립트로 해결한다.

```bash
#!/usr/bin/env bash
# .codex/worktree-setup.sh
set -euo pipefail
cd "$1" # 첫 번째 인자로 워크트리 경로를 받는다
npm ci
npm run db:migrate
```

스크립트가 멈춰 에이전트를 무한정 막지 않도록 타임아웃 래퍼를 붙인다.

```bash
timeout 120 .codex/worktree-setup.sh ".codex/worktrees/$TASK_ID"
```

설정 비용이 큰 프로젝트(큰 의존성 트리, 느린 데이터베이스 시딩)라면 `node_modules`를 심볼릭 링크로 걸거나 공유 패키지 캐시를 써서 워크트리끼리 산출물을 재사용하는 방법도 있다.

정리 정책도 정해 둬야 한다. 브랜치가 병합되거나 버려졌을 때 워크트리를 어떻게 할지다. 가장 단순한 정책은 즉시 삭제다. 실패한 에이전트 실행을 디버깅하려면 워크트리를 보관용 디렉터리로 옮겨 두고 최종 상태를 살펴본 뒤 직접 지운다.

## 2. CI에서의 수명주기

CI에서는 작업 단계 시작 때 만들고, 쓰고, 결과와 상관없이 끝에 지우는 과정이 완전히 자동이어야 한다.

### 기본 수명주기 스크립트

```bash
#!/usr/bin/env bash
set -euo pipefail
TASK_ID="${1:?task id required}"
BRANCH="codex/${TASK_ID}"
WORKTREE_PATH=".codex/worktrees/${TASK_ID}"
git worktree add "$WORKTREE_PATH" -b "$BRANCH"
trap 'git worktree remove --force "$WORKTREE_PATH"; git branch -D "$BRANCH"' EXIT
codex --cd "$WORKTREE_PATH" "$TASK_PROMPT"
```

`trap ... EXIT` 관용구 덕분에 에이전트가 0이 아닌 상태로 끝나거나 CI 러너가 중단돼도 정리가 실행된다. `git worktree remove`의 `--force`는 워크트리에 커밋하지 않은 변경이 있을 때 필요하다. CI에서는 정리 단계가 실패하게 두기보다 그 변경을 버리는 편이 보통 낫다.

## 3. GitHub Actions 예시

원서의 예시는 단계 네 개로 이루어진다. 핵심 줄만 옮긴다.

```yaml
- uses: actions/checkout@v5
  with:
    fetch-depth: 0 # worktrees need full history
- name: Provision worktree   # task_id 생성 후 git worktree add
- name: Run Codex agent      # codex --cd ".codex/worktrees/<task_id>" "<프롬프트>"
- name: Push task branch
  if: success()
- name: Cleanup worktree
  if: always()
```

- 작업 ID는 `github.run_id`와 `github.run_attempt`를 이어 sha256 해시를 낸 뒤 앞 8자를 쓰고, `GITHUB_OUTPUT`으로 다음 단계에 넘긴다.
- 푸시 단계는 `if: success()`라서 성공했을 때만 `git -C` 로 워크트리에서 `codex/<task_id>` 브랜치를 origin에 올린다.
- 정리 단계는 `if: always()`로 실패해도 돌고, `git worktree remove --force`와 `git branch -D` 뒤에 `|| true`를 붙여 정리 실패가 작업 전체를 깨뜨리지 않게 한다.

체크아웃 단계의 `fetch-depth: 0`을 눈여겨봐야 한다. 얕은 클론은 리베이스나 일부 워크트리 작업에 필요한 히스토리가 모자란다. 전체 fetch가 너무 느린 저장소라면 `--depth` 대신 `--filter=blob:none`(블롭 없는 클론)을 쓴다.

러너가 작업 사이에 워크스페이스를 재사용하는 환경(자체 호스팅 러너 풀에서 흔하다)에서는 이전 작업의 정리 단계가 건너뛰어지면 낡은 워크트리 등록 정보가 쌓일 수 있다. 각 작업 시작 때, 새 워크트리를 만들기 전에 `git worktree prune`을 실행해서 더는 없는 디렉터리의 등록을 지운다.

## 4. 병렬 매트릭스 작업

GitHub Actions의 매트릭스 작업은 "에이전트 하나, 워크트리 하나" 원칙에 자연스럽게 들어맞는다.

```yaml
strategy:
  matrix:
    task:
      - "migrate user service to async/await"
      - "add rate limiting to the API gateway"
      - "write property-based tests for the parser"
  max-parallel: 3
```

매트릭스의 각 갈래는 별도 러너에서 돌기 때문에 기본으로 진짜 파일 시스템 격리가 된다. 공유 객체 데이터베이스는 원격 origin이고, 모든 에이전트가 각자 따로 push한다. 공유되는 로컬 상태가 없고, 실행 중에 조율할 일도 없으며, 끝난 뒤에 PR로 병합하면 된다.

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
