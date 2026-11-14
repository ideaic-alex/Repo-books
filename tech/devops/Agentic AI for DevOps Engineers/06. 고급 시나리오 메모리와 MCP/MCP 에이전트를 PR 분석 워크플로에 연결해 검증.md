# MCP 에이전트를 PR 분석 워크플로에 연결해 검증

이 실습은 워크플로가 로컬 diff 아티팩트를 만들어 쓰던 경로를 MCP 기반 조회로 바꾼다. 그러면서 JSON 검증, PR 댓글, 아티팩트 보관, 리스크 게이트는 그대로 유지한다. 완성 워크플로는 원서 저장소의 finish/.github/workflows/pr-code-quality-agent.yml에 있다.

통합은 세 묶음의 설정에 달려 있다. GitHub 권한, 모델과 토큰 설정, MCP PR 맥락이다. 시험은 정상 경로와 권한 실패를 둘 다 확인해서, 에이전트나 MCP의 실패와 뒤쪽 GitHub 인가 실패를 구분할 수 있게 한다.

---

## 1. 워크플로 구성

단계는 원서의 번호를 따랐다.

1. 작업 저장소에 .github/workflows/pr-code-quality-agent.yml을 만든다. 이름은 PR Code Quality Agent (MCP)이고 트리거는 pull_request다. 최종 댓글 단계에 필요한 최소 권한은 contents 읽기, pull-requests 쓰기, issues 쓰기다.
2. 잡 analyze_pr_with_mcp(ubuntu-latest)의 환경 변수를 다음과 같이 정확히 맞춘다.

| 변수 | 값 |
|---|---|
| AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT | 저장소 시크릿 |
| PR_ANALYSIS_TOKEN | secrets.PR_ANALYSIS_TOKEN (MCP 서버용) |
| MCP_PR_OWNER, MCP_PR_REPO, MCP_PR_NUMBER | github.repository_owner, 이벤트의 저장소 이름, 이벤트의 PR 번호 |
| MCP_SERVER_PROJECT | mcp/DevOps.McpServer |
| PR_RISK_GATE | high (리스크 게이트 임계값) |

3. 단계는 Checkout, Setup .NET(10.0.x), artifacts 폴더 만들기, 파일 기반 에이전트 실행(`dotnet run --file ai/agents/PRCodeQualityAgent.cs > artifacts/pr-analysis.json`, 앞에 `set -euo pipefail`), 에이전트가 JSON 결과 파일을 만들었는지 확인(`test -f`, 내용을 cat)이다.
4. actions/github-script와 기본 제공 secrets.GITHUB_TOKEN을 써서 검증된 JSON을 파싱하고, 표지가 붙은 PR 댓글 하나를 만들거나 갱신(upsert)하며, 설정한 임계값을 평가한다. 원서의 요점은 PR_ANALYSIS_TOKEN은 MCP 서버용이고, 워크플로의 댓글 단계에는 기본 제공 secrets.GITHUB_TOKEN이 맞는 토큰이라는 것이다. 이름이 같은 두 토큰의 역할이 다르다.
5. 리스크 게이트 로직은 다음과 같다. PR_RISK_GATE 값(소문자로 변환, 기본 high)이 low, medium, high 중 하나인지 보고 아니면 "Invalid PR_RISK_GATE value"로 실패한다. 순위는 low 1, medium 2, high 3이다. 전체 위험도의 순위가 임계값 순위 이상이거나, 이슈 중 심각도 순위가 임계값 이상인 것이 하나라도 있으면(blockingIssue) 실패 처리하고 "PR blocked by risk gate" 메시지를 낸다.

```javascript
const shouldFail = overallRiskRank >= order[gate] || blockingIssue;
if (shouldFail) core.setFailed(`PR blocked by risk gate. overallRisk=${overallRisk}, threshold=${gate}`);
```

6. 리스크 게이트가 실패해도 아티팩트를 올린다. `if: always()`로 artifacts/ 폴더를 pr-analysis-artifacts 이름으로 올리고, 파일이 없으면 경고한다. 그다음 워크플로, 서버, 에이전트 변경을 커밋하고 푸시한 뒤 검증용 PR을 연다.

### 1-1. 5장 게이트와의 차이

5장의 pr-diff-ai-analysis 워크플로 게이트는 별도 잡에서 위험도가 high이고 신뢰도가 0.70 이상일 때만 실패시켰다. 6장 워크플로의 게이트는 신뢰도를 보지 않고, 전체 위험도나 개별 이슈의 심각도가 PR_RISK_GATE 임계값 이상이면 실패시킨다. 임계값을 low나 medium으로 낮추면 더 엄격해진다. 이 비교는 두 장의 본문을 대조해 정리한 것이다. 원서는 6장 게이트가 신뢰도를 쓰지 않는다고 따로 말하지 않았고, 발췌된 코드에 신뢰도 비교가 없다는 근거로 적었다.

원서 코드의 줄바꿈이 일부 깨져 있어서 위 게이트 로직은 보이는 줄을 기준으로 복원했다.

## 2. 시험: 권한 실패를 거쳐 성공까지

단계는 원서 번호를 따랐다.

1. GitHub Copilot에게 샘플 장바구니 데이터를 만들게 한다. 새 엔드포인트 api/cart에 샘플 장바구니를 가져오는 메서드를 추가한다.
2. 변경을 커밋하고 푸시해 새 PR을 만든다.
3. 실행 결과를 확인한다. 원서의 초기 시험에서는 댓글 upsert 단계에서 403 권한 오류로 실패했다. 오류 본문은 MCP와 에이전트 쪽은 정상 동작했고, 댓글 업로드만 GitHub 권한 문제로 거부되었음을 확인해 준다. 원인은 앞의 리팩터링에서 권한이 제대로 유지되지 않은 것이었다.

원서는 이 실패가 중요하다고 짚는다. 성공한 MCP 분석과 실패한 워크플로 부작용을 분리해서 보여 주기 때문이다. 403이 댓글 게시 중에 나왔으므로, 도구 실행과 뒤쪽 GitHub 권한은 따로 진단해야 한다는 교훈이다.

4. 워크플로 권한을 고치고 커밋해 푸시한다. 이 변경은 병합된 뒤에야 효력이 있으므로(pull_request 이벤트의 워크플로는 기준 브랜치의 정의를 쓰는 점 때문으로 보이나, 원서는 이유를 적지 않았다) 현재 PR을 squash and merge하고 브랜치를 지운다.
5. main으로 전환해 최신 변경을 받고, 새 브랜치를 만든다. 예: testing/mcp-integration.
6. GitHub Copilot에게 새 더미 엔드포인트, 예를 들어 결제 요약 엔드포인트를 만들게 하고, 커밋하고 푸시해 새 PR을 연다.
7. 실행을 확인한다. 이번에는 잡이 성공적으로 끝난다. PR 분석 댓글이 발견된 이슈의 표로 보이는데, 앞선 댓글 스타일에서 서식이 바뀐 것이다. 검증된 에이전트 출력이 PR에서 일관된 발견 사항 표로 그려졌다.
8. 최종적으로 main에 squash and merge해 MCP 통합을 마무리한다.

참고(노트 작성자): 4번의 괄호 속 이유는 원서 설명이 아니라 노트 작성자의 추측이다. 원서는 "병합된 뒤에야 효력이 있다"고만 적었다.

## 3. 확장 연습

원서가 제시하는 확장 과제는 책 앞에서 소개한 다른 에이전트나 워크플로에 같은 MCP 서버를 적용하는 것이다. 완성된 확장은 다음을 충족해야 한다.

- 필요한 최소 도구를 식별한다.
- 최소 권한을 유지한다.
- 도구 인자와 결과를 검증한다.
- 도구를 쓸 수 없는 상황을 처리한다.
- 워크플로가 기대한 아티팩트나 PR 댓글을 여전히 만드는지 확인한다.
- MCP로 대체한 직접 GitHub API 연동이 있다면 문서로 남긴다.

권한을 넓히거나 검증을 약화하지 않고 같은 MCP 경계를 다른 워크플로에 적용하는 것이 요점이다.

## 4. 장 요약

원서의 요약을 풀어 쓰면 이렇다. 이 장은 DevOps 에이전트에 오래 남는 메모리와 표준화된 도구 접근을 더했다. 메모리를 쓰는 ChatOps 워크플로는 GitHub 이슈에서 승인된 저장소 선호를 불러오고, PR 내용을 신뢰하지 않으며, 구조화된 메모리 후보를 뽑고, 명시적 스키마, 길이, 범위, 비밀 금지 목록 검사를 통과한 항목만 쓴다. GitHub 이슈 장부는 워크플로 수준 메모리를 보여 주지만, 운영 설계에는 더 강한 출처, 보존, 동시성, 거버넌스 통제가 필요하다.

이어 ModelContextProtocol 1.0.0으로 .NET 10 MCP 서버를 만들었다. 서버는 좁게 범위가 정해진 GitHub 도구를 노출하고, stdio로 Postman에서 검증했으며, McpClient를 통해 PR 품질 에이전트에 연결했다. 최종 워크플로는 MCP 맥락을 주고, 파일 기반 에이전트를 돌리고, JSON 출력을 검증하고, 구조화된 PR 댓글을 갱신하고, 결정론적 리스크 게이트를 적용하고, 아티팩트를 보관한다. 이 패턴들은 운영 환경의 인가, 검증, 감사 통제를 지키면서 능력을 키운다.

## 5. 핵심 정리

- 워크플로의 권한은 contents 읽기, pull-requests 쓰기, issues 쓰기이고, 토큰은 둘로 나뉜다. MCP 서버용은 PR_ANALYSIS_TOKEN, 댓글용은 secrets.GITHUB_TOKEN이다.
- 리스크 게이트는 PR_RISK_GATE 임계값(기본 high)과 전체 위험도 및 이슈 심각도를 비교하고, 게이트 실패에도 아티팩트는 올린다.
- 첫 시험의 403은 댓글 단계에서 났고, 이는 MCP와 에이전트가 아닌 워크플로 권한 문제로 분리해서 진단했다.
- 권한 수정 후 새 PR에서는 성공하고, 분석 댓글이 발견 사항 표로 나타났다.
- 확장 과제는 최소 도구, 최소 권한, 인자와 결과 검증, 도구 장애 처리를 지키며 MCP를 다른 워크플로에 적용하는 것이다.

<br>
<br>
<br>

[Agentic AI for DevOps Engineers](../)
