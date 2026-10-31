# GitHub Actions 기본 패턴

GitHub에서는 `openai/codex-action` 액션을 쓰면 Codex CLI를 파이프라인에 쉽게 붙일 수 있다. 이 문서는 그 액션과 이를 바탕으로 한 네 가지 패턴(PR 요약, 자동 코드 리뷰, 머지 때 테스트 생성, 의존성 업데이트 에이전트)을 설명한다. 워크플로 예시는 핵심 줄만 옮기고 나머지는 말로 풀었다.

---

## 1. openai/codex-action

이 액션은 `codex exec`에 GitHub 환경에 맞는 기본값을 입혀 놓은 것이다. CLI 설치, 시크릿(secret) 주입, 출력 노출을 대신 해 준다. 결과 메시지는 `steps.<id>.outputs.final-message`로 뒤 단계에서 읽는다.

### 가장 간단한 연동: 읽기 전용 PR 요약

처음 저장소에 도입할 때 가장 안전한 방식이다. Codex CLI가 바뀐 내용을 쉬운 말로 설명하고, 다음 단계가 그 요약을 PR 댓글로 단다. 에이전트는 코드를 읽기만 하고, 유일한 쓰기인 댓글은 에이전트가 아니라 GitHub API가 처리한다. 그래서 위험이 작다.

```yaml
- uses: openai/codex-action@v1
  id: codex
  with:
    prompt: "Summarize what changed in this PR in three bullet points"
    sandbox: read-only
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

댓글 게시는 `actions/github-script@v7`로 한다. `github.rest.issues.createComment`를 호출하고, 본문(`body`)은 환경 변수 `CODEX_OUTPUT`(값은 `${{ steps.codex.outputs.final-message }}`)에서 가져온다.

## 2. 모든 PR에 자동 코드 리뷰

가장 효과가 큰 첫 패턴이다. PR이 열리거나 갱신되는 순간 1차 리뷰가 달린다. 잡이 diff를 만들고, Codex CLI에 구조화된 비평(논리 오류, 에러 처리 누락, 보안 우려, 테스트 커버리지 공백)을 요청하고, 결과를 댓글로 올린다. 읽기 전용으로 돌리므로 조언 수준에 머문다. 사람 리뷰어에게 문제를 알려 줄 뿐 코드를 건드리지 않는다. 리뷰 대기 시간이 병목인 팀에서 특히 유용하다. 사람이 PR을 열 때 에이전트의 1차 검토가 이미 기다리고 있기 때문이다.

### 이 절이 다루는 범위

여기서는 파이프라인 배선만 다룬다. 언제 잡이 뜨는지, diff 범위를 어떻게 잡는지, 결과를 어떻게 돌려주는지다. 리뷰 내용을 읽을 만하게 만드는 방법은 20장의 주제다. AI 리뷰가 믿을 만하게 잡는 결함 종류와 판단하지 못하는 종류, AGENTS.md에 넣는 `## Review guidelines` 블록, `/review` 명령 모드, 여러 에이전트의 적대적 리뷰가 거기서 나온다. 아래 짧은 프롬프트는 20장에서 만드는 리뷰 기준의 자리 표시자로 보면 된다. 파이프라인은 같고 비평의 품질은 20장에서 나온다.

### 워크플로 뼈대

- 트리거: `pull_request`의 `opened`, `synchronize`, `reopened`
- 권한: `contents: read`, `pull-requests: write`
- 체크아웃: `actions/checkout@v4`에 `fetch-depth: 0`(전체 이력, diff를 만들려면 필요)
- diff 생성: 아래 한 줄

```yaml
- name: Generate diff
  run: git diff origin/${{ github.base_ref }}...HEAD > /tmp/pr.diff
```

- 리뷰 실행: `openai/codex-action@v1`, `sandbox: read-only`. 프롬프트는 "시니어 엔지니어로서 PR을 리뷰하라, diff는 `/tmp/pr.diff`에 있다, (1) 논리 오류 (2) 에러 처리 누락 (3) 보안 우려 (4) 테스트 커버리지 공백을 찾고 GitHub 마크다운으로 간결하게 쓰라"는 내용이다.
- 댓글 게시: `github-script`로 `### Codex Review` 제목 아래에 `CODEX_OUTPUT`을 붙여 올린다.

PR 내용을 프롬프트에 직접 끼워 넣지 않고 diff를 파일로 쓴 뒤 프롬프트에서는 파일 경로만 가리킨다는 점에 주목한다. 이유는 `CI 에이전트 안전 전략과 관측.md`의 안전 원칙에서 설명한다. 문서만 바뀐 PR은 건너뛰도록 `paths` 필터를 달아 두면 불필요한 실행을 줄일 수 있다.

## 3. 머지 때 테스트 생성

테스트 커버리지 공백을 자동으로 메운다. main에 머지될 때마다 직전 커밋에서 바뀐 소스 파일을 나열하고, 추가·수정된 함수의 단위 테스트를 만들고, 결과를 PR로 연다. 새 테스트는 main에 곧바로 들어가지 않고 리뷰를 거친다. 그래서 생성이 부실해도 대가는 PR 하나 반려일 뿐 테스트 스위트가 깨지는 일은 없다. 기능이 테스트 없이 자주 머지되고 커버리지가 내려가는 코드베이스에 맞는 패턴이다.

핵심 요소는 다음과 같다.

- 트리거: `push`, 브랜치 `main`
- 권한: `contents: write`, `pull-requests: write`
- 체크아웃: `fetch-depth: 2`(직전 커밋과 비교하려고 두 개만 가져온다)
- 변경 파일 추출: `git diff HEAD~1 HEAD --name-only`에서 `ts|js|py|go` 확장자만 고르고 `.test.`나 `_test.`가 들어간 테스트 파일은 뺀다. 목록은 `/tmp/changed-source.txt`에 저장하고 개수를 `count` 출력으로 내보낸다.
- 테스트 생성: `count`가 `'0'`이 아닐 때만 실행한다. 프롬프트는 목록의 각 파일에서 직전 커밋에 추가·수정된 함수의 공개 API를 다루는 단위 테스트를 쓰되 기존 테스트 프레임워크와 관례를 따르라는 내용이다. `sandbox: workspace-write`.
- PR 열기: `peter-evans/create-pull-request@v6`. 브랜치는 `codex/tests-${{ github.sha }}`, 제목은 `test: add generated tests for ${{ github.sha }}`, 본문은 리뷰 후 머지하라는 안내, 레이블은 `codex-generated, tests`.

```yaml
- name: Generate tests
  if: steps.changed.outputs.count != '0'
  uses: openai/codex-action@v1
  with:
    sandbox: workspace-write
```

## 4. 의존성 업데이트 에이전트

단순 버전 올림 봇이 필요로 하는 뒤치다꺼리 없이 의존성을 최신으로 유지한다. 매주 예약된 잡이 안전한 범위(마이너 버전만, 메이저는 절대 올리지 않는다) 안에서 오래된 패키지를 올리고, 테스트를 돌리고, 테스트를 깨는 의존성은 되돌린 다음, 통합 PR 하나를 연다. 기계적 봇과 다른 점은 테스트하고 되돌리는 순환이다. 처리해야 할 버전 올림 더미가 아니라 이미 통과한 업데이트의 초록색 PR을 받는다. 작업이 대부분 기계적이므로 `gpt-5.4-mini`로 실행당 비용을 낮춘다.

- 트리거: 매주 월요일 09시(`cron: '0 9 * * 1'`)와 수동 실행(`workflow_dispatch`)
- 권한: `contents: write`, `pull-requests: write`
- 준비: `actions/setup-node@v4`, `node-version: '22'`
- 에이전트: `sandbox: workspace-write`, `model: gpt-5.4-mini`. 프롬프트는 오래된 npm 의존성을 최신 마이너로 올리고(메이저는 올리지 않음), `npm install`과 `npm test`를 돌리고, 테스트가 실패하면 원인 의존성을 되돌리고, 결과를 `updated`, `skipped`, `failed` 키의 JSON으로 보고하라는 내용이다.
- PR 열기: 브랜치 `codex/deps-${{ github.run_id }}`, 제목 `chore: weekly dependency updates`, 레이블 `dependencies, codex-generated`.

```yaml
sandbox: workspace-write
model: gpt-5.4-mini
```

> 경고: `npm install`은 업데이트된 패키지의 라이프사이클 스크립트(설치 훅)를 실행한다. 악성 패키지가 끼면 러너에서 코드가 돌 수 있다. 그래서 네트워크가 샌드박스된 러너에서, 외부로 나가는 통신(egress)을 npm 레지스트리로만 제한해서 돌려야 한다.

## 5. 네 패턴 한눈에 비교

| 패턴 | 트리거 | 샌드박스 | 에이전트가 쓰는 것 |
| --- | --- | --- | --- |
| PR 요약·리뷰 | `pull_request` | `read-only` | 없음(댓글은 API가 단다) |
| 테스트 생성 | `push` to main | `workspace-write` | 테스트 파일 |
| 의존성 업데이트 | 주간 예약 | `workspace-write` | 의존성 파일 |

세 패턴 모두 에이전트의 결과를 곧바로 main에 넣지 않고 댓글이나 PR이라는 사람이 보는 관문을 거친다.

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
