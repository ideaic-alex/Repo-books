# 실습 1 GitHub Actions 자동 코드 리뷰

이제 이론을 실제 워크플로(workflow, GitHub Actions에서 자동 실행 절차를 적은 YAML 파일)로 옮긴다. Anthropic이 제공하는 GitHub Actions 연동은 두 가지다. 하나는 공식 액션(anthropics/claude-code-action@v1)으로, 캡슐화가 잘 되어 설정이 쉽다. 다른 하나는 CLI를 직접 호출하는 방식으로, 더 유연하고 세밀한 제어가 가능하다. 이 문서는 두 방식의 설정 항목과 단계를 빠짐없이 적는다. 단순한 리뷰는 공식 액션으로 충분하고, 병합 차단 여부 판정이나 파일 종류별 차별 전략 같은 복잡한 논리가 필요하면 CLI 직접 호출을 쓴다.

---

## 1. 공식 액션 사용하기

### 1-1. 준비

Claude Code에는 편리한 설치 명령이 있다. 대화형 모드에서 `/install-github-app`을 실행하면 GitHub 앱 설치, Secrets 설정, 워크플로 파일 생성까지 전 과정을 안내한다. 수동으로 하려면 GitHub 저장소의 Settings, Secrets, Actions로 가서 `ANTHROPIC_API_KEY`를 추가하고 워크플로 파일 `.github/workflows/claude-review.yml`을 만든다.

### 1-2. 워크플로 구성

| 항목 | 값 |
|---|---|
| name | Claude PR Review |
| on.pull_request.types | opened, synchronize, reopened |
| on.issue_comment.types | created |
| concurrency.group | `${{ github.workflow }}-${{ github.event.pull_request.number }}` |
| concurrency.cancel-in-progress | true (같은 PR의 새 커밋이 오면 실행 중인 이전 작업을 자동 취소해 자원 절약) |
| jobs.review.runs-on | ubuntu-latest |
| jobs.review.if | `github.event_name == 'pull_request' \|\| contains(github.event.comment.body, '@claude')` (PR 관련 이벤트이거나 댓글에 "@claude"가 있을 때만 실행) |
| checkout 단계 | `fetch-depth: 0` (diff 분석을 위해 전체 이력을 가져옴) |
| 액션 | `anthropics/claude-code-action@v1` |
| with.anthropic_api_key | `${{ secrets.ANTHROPIC_API_KEY }}` |
| with.prompt | 보안 취약점(SQL 인젝션, XSS, 하드코딩된 민감 정보 등), 처리되지 않은 예외와 경계 사례, 성능 위험(N+1 쿼리, 메모리 누수 위험) 세 가지를 검토하고 `## Review Report` 아래 `### Critical (Must Fix)`, `### Warning (Recommended Fix)`, `### Suggestion (Optional Optimization)` 형식으로 보고하라 |
| with.claude_args | `--allowedTools "Read,Grep,Glob"`, `--max-turns 10`, `--model claude-sonnet-4-6` |

```yaml
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    prompt: |
      Please review the code changes in this PR ... (보안, 예외·경계 사례, 성능)
    claude_args: >-
      --allowedTools "Read,Grep,Glob"
      --max-turns 10
      --model claude-sonnet-4-6
```

원서 YAML은 들여쓰기가 모두 사라진 채 추출되었고, checkout 단계의 `- uses: actions/checkout@v4`와 `with:` 줄이 빠진 채 `fetch-depth: 0`만 남아 있다. 이 노트는 GitHub Actions 문법과 앞뒤 문맥으로 복원했다. 특히 checkout 단계는 원서 두 번째 예시(직접 CLI 호출)에서 `actions/checkout@v4`에 `fetch-depth: 0`을 준 형태와 같다고 보고 맞춰 적었다.

### 1-3. 주목할 세 가지

- **이중 트리거 모드**: 공식 액션 v1은 트리거 모드를 자동으로 감지한다.
  - 에이전트 모드(Agent Mode): 설정에 `prompt` 매개변수를 주면 작동한다. PR이 만들어지거나 갱신될 때마다 Claude가 미리 정한 리뷰 작업을 자동으로 수행한다.
  - 태그 모드(Tag Mode): 사용자가 PR 댓글에서 `@claude`를 멘션하면 작동한다. Claude가 팀원처럼 특정 질문에 대화식으로 답한다.
  - 두 모드는 같은 워크플로 파일 안에서 충돌 없이 함께 쓸 수 있다.
- **매개변수 전달 방식**: v1은 설정 구조를 크게 단순화했다. 모든 Claude Code CLI 매개변수를 `claude_args` 필드로 통일해 넘긴다. 베타 버전에 있던 `max_turns`, `allowed_tools` 같은 독립 필드는 폐기되어 더는 지원하지 않는다.
- **동시성 제어 전략**: `cancel-in-progress: true`로 효율적인 동시성 제어를 한다. 같은 PR에 커밋이 연속으로 푸시되면 실행 중인 이전 작업을 자동 취소하고 가장 최근 커밋이 일으킨 리뷰만 남긴다. 중복 실행을 피하고 API 호출 비용을 아낀다.

참고(노트 작성자): `issue_comment` 이벤트에서는 `github.event.pull_request`가 보통 비어 있어 이 concurrency 그룹 키가 PR 번호로 구분되지 않을 수 있다. 원서에 없는 관찰이므로 적용 전에 확인한다.

## 2. CLI 직접 호출

리뷰 결과에 따라 PR 병합을 막을지 정하거나, 리뷰 보고서를 일반 댓글이 아니라 공식 PR 댓글로 게시하거나, 파일 종류별로 다른 리뷰 전략을 쓰는 등 복잡한 논리가 필요하면 Claude CLI를 직접 호출한다. 파일은 `.github/workflows/advanced-review.yml`이다.

### 2-1. 트리거와 권한

| 항목 | 값 |
|---|---|
| name | Advanced AI Review |
| on.pull_request.types | opened, synchronize |
| on.pull_request.paths | `'src/**'` (src/ 아래가 바뀔 때만 트리거) |
| concurrency | 위와 같은 그룹, cancel-in-progress: true |
| permissions | contents: read, pull-requests: write, issues: write |

### 2-2. 단계별 내용

| 순서 | 단계 | 핵심 내용 |
|---|---|---|
| 1 | actions/checkout@v4 | `fetch-depth: 0` |
| 2 | actions/setup-node@v4 | `node-version: "20"` |
| 3 | Install Claude Code | `npm install -g @anthropic-ai/claude-code` |
| 4 | Get changed files (id: changed) | `git diff --name-only origin/${{ github.base_ref }}...HEAD`로 변경 파일을 구해 `files`(공백 구분)와 `count`를 `$GITHUB_OUTPUT`에 기록 |
| 5 | Run Claude Review (id: review) | 아래 설명 |
| 6 | Post Review Comment | actions/github-script@v7, review.md를 읽어 `issues.createComment`로 댓글 게시 |
| 7 | Gate on critical issues | review.md에서 판정 표식을 찾아 실패 처리 |

**5단계**의 env는 `ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}`, `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC: "1"`, `CHANGED_FILES: ${{ steps.changed.outputs.files }}`다. 실행 명령은 다음 옵션들로 구성된다. 프롬프트는 변경된 파일을 검토하되 보안 취약점, 논리 오류, 성능 문제에 집중하고 모든 문제에 파일명과 줄 번호를 주며, 응답을 `<VERDICT>request_changes</VERDICT>` 또는 `<VERDICT>approved</VERDICT>` 중 정확히 한 줄의 판정 줄로 끝내라고 요구한다.

```bash
claude -p "Review the following changed files: $CHANGED_FILES ... <VERDICT>...</VERDICT>" \
  --output-format json --max-turns 10 --max-budget-usd 0.50 \
  --model claude-sonnet-4-6 --allowedTools "Read,Grep,Glob" > review.json
jq -r '.result' review.json > review.md
echo "cost=$(jq -r '.total_cost_usd' review.json)" >> $GITHUB_OUTPUT
echo "is_error=$(jq -r '.is_error' review.json)" >> $GITHUB_OUTPUT
```

결과는 review.json으로 저장한 뒤 jq로 `.result`를 review.md에 쓴다. 원서 주석은 리뷰를 셸이나 JS 문자열에 끼워 넣지 말고 파일에 써서 넘기라고 한다(인젝션 방지). 이어서 `total_cost_usd`를 `cost`, `is_error`를 `is_error` 출력으로 기록한다.

**6단계**는 env의 `COST`에 `${{ steps.review.outputs.cost }}`를 받고, review.md를 읽어 `## Claude Code Review` 제목 아래 본문과 `---` 구분선, `*Cost: $<비용> | Automated by Claude Code*` 꼬리말이 달린 댓글을 PR에 단다.

**7단계**는 `grep -qF "<VERDICT>request_changes</VERDICT>" review.md`가 참이면 `::error::Claude requested changes`를 출력하고 `exit 1`로 워크플로를 실패시킨다. 원서의 주의는 "critical"이라는 단어를 맨 grep으로 찾지 말고 명시적 표식(sentinel)을 쓰라는 것이다. 이 단어는 "no critical issues"나 "non-critical"처럼 거의 모든 리뷰에 나오기 때문이다.

### 2-3. 이 방식이 주는 세 가지 능력

- **비용 투명성**: 리뷰마다의 구체적 비용이 댓글에 바로 표시된다.
- **품질 관문**: 심각한(Critical급) 문제가 감지되면 워크플로가 자동 실패해 PR 병합을 막는다(구현은 판정 표식 방식).
- **경로 필터링**: paths 매개변수로 src/ 디렉터리 변경 때만 리뷰를 트리거한다.

### 2-4. CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC

이 환경 변수는 CI/CD의 표준 모범 사례다. 자동 업데이트 확인, 오류 보고, 텔레메트리(사용 데이터) 전송 같은 비필수 기능을 자동화 환경에서 한꺼번에 끈다(5번 문서에서 개별 변수와 함께 다시 정리한다).

---

## 3. 핵심 정리

- 공식 액션: `anthropics/claude-code-action@v1` + `ANTHROPIC_API_KEY` 시크릿. 설치 보조는 `/install-github-app`.
- v1은 CLI 매개변수를 모두 `claude_args`로 전달한다. 베타의 `max_turns`, `allowed_tools` 필드는 폐기되었다.
- prompt가 있으면 에이전트 모드, 댓글의 `@claude`는 태그 모드이며 한 파일에서 공존한다.
- `concurrency`의 `cancel-in-progress: true`로 이전 실행을 취소해 비용을 아낀다.
- CLI 직접 호출: checkout(fetch-depth 0), setup-node(20), npm 설치, 변경 파일 추출, `claude -p`(`--output-format json`, `--max-turns 10`, `--max-budget-usd 0.50`, `--allowedTools "Read,Grep,Glob"`), 댓글 게시, `<VERDICT>` 판정 표식 기반 관문.
- 권한은 `contents: read`, `pull-requests: write`, `issues: write`로 최소화한다.

<br>
<br>
<br>

[The Claude Code Operating Model](../)
