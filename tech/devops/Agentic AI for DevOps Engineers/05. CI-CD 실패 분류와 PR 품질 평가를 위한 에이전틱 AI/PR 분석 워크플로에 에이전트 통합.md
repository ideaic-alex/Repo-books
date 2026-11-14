# PR 분석 워크플로에 에이전트 통합

앞 문서에서 만든 PRCodeQualityAgent를 GitHub Actions 워크플로에 붙인다. 이 워크플로는 PR이 열리거나(opened), 새 커밋이 올라오거나(synchronize), 다시 열리거나(reopened), 수동으로 실행될 때마다 에이전트를 돌린다. 분석 결과를 아티팩트로 올리고, PR에 댓글을 달고, 모델이 충분한 신뢰도로 고위험 발견을 내놓으면 리스크 게이트(위험 관문)를 적용한다.

원서 저장소의 스캐폴드는 finish/.github/workflows/pr-diff-ai-analysis.yml에 있다. 여기서 설명하는 버전은 MCP_PR_* 변수와 PR_ANALYSIS_TOKEN을 에이전트 실행 전에 설정하도록 MCP 기반 에이전트에 맞춘 것이다.

---

## 1. 워크플로 파일과 트리거

파일은 .github/workflows/pr-diff-ai-analysis.yml이고 이름은 PR Diff AI Analysis다.

- 트리거: pull_request의 opened, synchronize, reopened 유형과 workflow_dispatch.
- 권한: contents는 read, pull-requests는 read, issues는 write. PR 댓글은 이슈 댓글 API로 달리므로 issues 쓰기 권한이 필요하다(이 연결은 노트 작성자의 보충이며, 원서는 권한 값만 제시한다).
- 동시성(concurrency): 그룹 이름은 `pr-diff-ai-` 뒤에 PR 번호(없으면 ref)를 붙인 값이고 cancel-in-progress는 true다. 같은 PR에 새 푸시가 오면 진행 중이던 이전 분석을 취소한다.

## 2. analyze-pr-diff 작업

작업 이름은 Analyze PR Diff이고 ubuntu-latest에서 실행한다. 위험도, 신뢰도, 요약을 작업 출력(overall-risk, confidence, summary)으로 노출해 뒤의 리스크 게이트가 쓰게 한다. 출력 값은 extract 단계에서 온다.

| 순서 | 단계 | 하는 일 |
|---|---|---|
| 1 | Checkout | actions/checkout@v4, fetch-depth 0으로 전체 이력을 가져옴 |
| 2 | Setup .NET | actions/setup-dotnet@v4, 버전 10.0.x |
| 3 | Build PR diff artifact | artifacts/pr.diff 생성 |
| 4 | Run PRCodeQualityAgent | 에이전트 실행, 결과를 artifacts/pr-analysis.json에 저장하고 jq로 JSON 유효성 확인 |
| 5 | Extract analysis outputs | jq로 overallRisk, confidence, summary를 뽑아 GITHUB_OUTPUT에 기록 |
| 6 | Upload analysis artifacts | pr.diff와 pr-analysis.json을 pr-diff-ai-analysis 이름으로 업로드 |
| 7 | Upsert PR comment | 숨은 표지로 댓글 하나를 만들거나 갱신 |

### 2-1. diff 아티팩트 만들기

pull_request 이벤트라면 기준 브랜치를 얕게 가져와(`git fetch --no-tags --prune --depth=1 origin <base_ref>`) 기준 브랜치와 현재 커밋 사이의 diff를 `artifacts/pr.diff`로 저장한다. 다른 이벤트(수동 실행)라면 HEAD~1과 HEAD 사이의 diff를 쓰고 실패해도 계속 간다. diff가 비었으면 파일에 `# empty diff` 한 줄을 넣는다. 스크립트는 `set -euo pipefail`로 시작한다.

흥미로운 점은 이 diff 파일을 에이전트가 직접 읽지는 않는다는 것이다. 원서는 에이전트가 diff 경로를 인자로 받을 필요가 없다고 말한다. PR 파일을 MCP 서버를 통해 읽기 때문이다. pr.diff는 사람이 확인할 수 있는 아티팩트로 남는다(이 해석은 노트 작성자의 것).

### 2-2. 에이전트 실행 단계

환경 변수는 시크릿과 이벤트 값으로 채운다.

| 변수 | 값의 출처 |
|---|---|
| AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT | 저장소 시크릿(`<값은 시크릿에만 저장>`) |
| PR_ANALYSIS_TOKEN | secrets.GITHUB_TOKEN |
| MCP_PR_OWNER | github.repository_owner |
| MCP_PR_REPO | github.event.repository.name |
| MCP_PR_NUMBER | github.event.pull_request.number |
| MCP_SERVER_PROJECT | mcp/DevOps.McpServer |

실행 명령은 `dotnet run --file ai/agents/PRCodeQualityAgent.cs > ./artifacts/pr-analysis.json` 다음에 `jq . ./artifacts/pr-analysis.json > /dev/null`이다. jq가 오류 없이 끝나야 JSON이 유효하다는 뜻이다.

원서 주의: workflow_dispatch로 테스트할 때는 PR 컨텍스트가 없다. 수동 실행은 MCP_PR_OWNER, MCP_PR_REPO, MCP_PR_NUMBER 값을 워크플로 입력이나 환경 변수로 임시로 제공한 뒤에만 쓰거나, 실제 PR 이벤트로 에이전트를 시험해야 한다.

### 2-3. 출력 추출

extract 단계는 `jq -r '.overallRisk // "unknown"'`처럼 기본값을 두고 세 값을 뽑는다. 위험도 기본값은 unknown, 신뢰도 기본값은 0, 요약 기본값은 빈 문자열이다. 요약은 여러 줄일 수 있어서 `summary<<EOF ... EOF` 형식으로 GITHUB_OUTPUT에 쓴다. 이렇게 하면 게이트가 아티팩트를 다시 파싱하지 않고 평가할 수 있다.

### 2-4. 아티팩트 업로드

원본 diff와 검증된 JSON 분석을 올린다. `if-no-files-found`는 error다. 리스크 게이트가 나중에 실패해도 에이전트 출력을 확인할 수 있게 하려는 설계다.

### 2-5. PR 댓글 만들기 또는 갱신(upsert)

pull_request 이벤트에서만 `actions/github-script@v7`로 댓글을 단다. 댓글 본문 맨 위에 숨은 HTML 주석 표지 `<!-- pr-diff-ai-analysis -->`를 넣고, 제목은 "AI PR Diff Analysis", 그 아래 분석 JSON을 코드 펜스로 감싼다. 스크립트는 PR의 기존 댓글을 페이지 단위(100개씩)로 모두 훑어 사용자 유형이 Bot이고 본문에 표지가 있는 댓글을 찾는다. 있으면 그 댓글을 갱신하고 없으면 새로 만든다. 새 푸시(synchronize)마다 댓글이 쌓이는 것을 막는 방법이다.

## 3. risk-gate 작업

리스크 게이트는 별도의 작업이다. 이름은 Risk Gate이고 `needs: analyze-pr-diff`로 분석 작업 뒤에 실행되며, 조건은 이벤트가 pull_request일 때다. 에이전트가 high 위험을 보고하고 신뢰도가 설정된 임계값 이상일 때만 실패한다.

게이트의 로직은 다음과 같다.

1. 작업 출력에서 위험도와 신뢰도를 받는다.
2. 신뢰도가 숫자 형식(정규식 `^[0-9]+(\.[0-9]+)?$`)이 아니거나 없으면 0으로 두고 메시지를 남긴다.
3. 임계값은 0.70이다.
4. 위험도가 high이고 신뢰도가 임계값 이상이면 "High risk changes detected..." 메시지를 내고 `exit 1`로 실패한다. 부동소수 비교에는 awk를 쓴다.
5. 그 외에는 통과 메시지를 낸다.

```bash
if [ "$risk" = "high" ] && awk -v c="$confidence" -v t="$threshold" \
   'BEGIN { exit (c >= t) ? 0 : 1 }'; then exit 1; fi
```

신뢰도가 이상한 값일 때 0으로 두는 점이 안전 설계다. 모델이 숫자를 안 주면 게이트가 실패시키지는 않지만, 위험도가 high라는 신호가 있더라도 사람이 댓글과 아티팩트로 확인할 수 있다. 실패시킬지 말지의 정책은 이처럼 코드로 정해 둔다.

## 4. 시험해 보기

1. 명백한 고위험 변경을 도입하는 브랜치를 만든다. 예를 들어 API 응답 모델에서 비밀번호 필드를 반환하거나 하드코딩한다.
2. 그 브랜치에서 PR을 연다.
3. 워크플로가 AI PR Diff Analysis 댓글을 달고, pr-analysis.json을 업로드하고, 출력이 high 위험이며 신뢰도가 0.70 이상일 때 리스크 게이트를 실패시키는지 확인한다.

## 5. 완성된 고리와 주의

완성된 고리는 안전한 수준의 자율성을 가진다. 에이전트가 PR 맥락을 가져오고, 구조화된 리뷰를 만들고, PR에 댓글을 달고, 결정론적 정책 게이트가 워크플로 실패 여부를 결정한다. 코드를 다시 쓰거나, 병합하거나, 배포하거나, 사람 리뷰를 건너뛰지 않는다. 앞 문서의 자율성 수준으로 치면 수준 1(제안)에 가깝고, 게이트가 병합을 막는 역할을 한다는 해석은 노트 작성자의 것이다.

원서의 보안 주의: 이 워크플로는 Azure OpenAI 시크릿과 쓰기 가능한 GITHUB_TOKEN을 쓰므로 먼저 신뢰할 수 있는 내부 PR에만 쓰라고 한다. 포크에서 온 PR은 시크릿을 받지 못할 수 있고, 저장소 설정에 따라 GitHub가 쓰기 권한을 낮출 수도 있다. pull_request_target은 보안상 영향을 명시적으로 가르치고 처리하지 않을 거라면 피하라고 한다.

## 6. 장 요약과 다음 장 예고

원서의 장 요약을 풀어 쓰면 이렇다. 에이전틱 AI가 일반 AI 보조와 다른 점, DevOps 에이전트가 추론, 계획, 메모리, 도구, 검증을 결합한다는 점을 배웠다. 안전하거나 위험한 CI/CD 사용 사례를 살펴보고, CI 로그에서 결정론적 신호를 뽑아 검증된 JSON 분류를 돌려주는 실패 분류 에이전트를 만들었다. 운영 실패의 이유(맥락 손실, 약한 계획, 취약한 도구 인터페이스, 프롬프트 민감성, 과신)를 보고, 관찰에서 제안을 거쳐 검증과 정책 게이트가 갖춰진 뒤에만 통제된 행동을 허용하는 점진적 자율성을 적용했다. 마지막으로 통제된 MCP 경계로 PR 파일을 가져오고, 구조화된 리뷰를 게시하고, 아티팩트를 올리고, 고위험 발견이 신뢰도 기준을 넘을 때만 리스크 게이트를 실패시키는 PR 품질 평가 에이전트를 GitHub Actions 워크플로에 통합했다. 다음 장은 메모리, MCP 기반 표준 도구, 멀티 에이전트 워크플로, 관측 가능성으로 에이전트 능력을 확장한다.

참고(노트 작성자): 원서 YAML과 셸 코드는 추출 과정에서 들여쓰기와 줄바꿈이 사라져 있었다. 위 설명은 단계 순서와 설명 문장을 근거로 복원했으며, 문법 세부(특히 YAML 구조)는 원서 저장소의 finish 폴더 파일로 대조하는 것이 안전하다.

<br>
<br>
<br>

[Agentic AI for DevOps Engineers](../)
