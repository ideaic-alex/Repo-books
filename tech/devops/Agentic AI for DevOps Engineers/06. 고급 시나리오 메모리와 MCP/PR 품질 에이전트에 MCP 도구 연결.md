# PR 품질 에이전트에 MCP 도구 연결

서버가 독립적으로 검증되었으니, 5장에서 만든 PR 품질 에이전트가 PR 데이터를 직접 불러오던 경로를 MCP 서버 호출로 바꾼다. 에이전트는 여전히 .NET 10 파일 기반 앱이고, 완성본은 원서 저장소의 finish/ai/agents/PRCodeQualityAgent.cs에 있다.

이 문서는 에이전트 쪽 변경만 다룬다. 워크플로 설정과 최종 시험은 다음 문서에서 다룬다. 바뀌는 부분이 의외로 작다는 점이 핵심이다. 파일 목록을 얻는 출처만 MCP로 바뀌고, 그 뒤의 DiffTools와 검증 로직은 그대로다.

---

## 1. 바뀌는 곳과 그대로인 곳

| 구분 | 내용 |
|---|---|
| 바뀌는 곳 | PR 파일 데이터의 출처. MCP 클라이언트가 github_list_pull_request_files 도구를 호출한다 |
| 그대로인 곳 | 이전 로컬 diff 구현이 쓰던 FileDiffEntry 객체, 모델용 DiffTools 함수, JSON 검증, 대체 JSON |

참고(노트 작성자): 5장 문서에서 설명한 PRCodeQualityAgent는 이미 MCP 클라이언트를 쓰는 형태로 서술되어 있다. 원서 5장은 MCP 서버 프로젝트가 이미 있다고 가정하고 존재 여부만 확인하라고 했고, 서버를 실제로 만드는 과정은 6장에 나온다. 6장은 서버를 만들고 시험한 뒤 에이전트에 연결하는 과정을 다시 짚는 구성이다. 에이전트 코드 설명이 두 장에 겹치는 것은 원서의 구성이다.

## 2. 에이전트 코드 변경 단계

원서의 번호를 따랐다.

1. 소스는 ModelContextProtocol 1.0.0 패키지를 고정하고(`#:package ModelContextProtocol@1.0.0`) 클라이언트와 프로토콜 네임스페이스(ModelContextProtocol.Client, ModelContextProtocol.Protocol)를 가져온다.
2. 워크플로가 주는 MCP PR 입력을 읽고 검증한다. MCP_PR_OWNER, MCP_PR_REPO, MCP_PR_NUMBER가 없으면 예외로 일찍 실패하고, PR 번호가 정수가 아니면 "MCP_PR_NUMBER must be an integer." 예외를 던진다.
3. MCP 클라이언트를 만들고, github_list_pull_request_files를 호출하고, 돌아온 JSON 배열로 기존 diff 도구를 초기화한다. 이어서 파일 목록(최대 250개)과 고위험 후보(상위 20개)를 만든다.
4. CreateMcpClientAsync는 stdio로 서버 프로젝트를 띄운다. MCP_SERVER_PROJECT의 기본값은 완성 샘플이 쓰는 경로 mcp/DevOps.McpServer다. 전송 설정은 이름 "DevOps MCP Server", 명령 dotnet, 인자 `run --project <서버 프로젝트>`다.
5. 클라이언트 래퍼 GitHubMcp를 구현한다. 정확한 서버 도구 이름, 딕셔너리 형태의 인자, TextContentBlock 결과 처리를 쓴다.

```csharp
var result = await client.CallToolAsync("github_list_pull_request_files",
    new Dictionary<string, object?> { ["owner"] = owner, ["repo"] = repo, ["number"] = number },
    cancellationToken: ct);
```

결과에서 텍스트 블록(TextContentBlock)만 골라 내용을 줄바꿈으로 합친 뒤 JSON으로 파싱한다. 텍스트 블록이 하나도 없으면 "MCP tool returned no text content." 예외를 던진다. 도구가 빈 결과를 조용히 돌려줘도 성공으로 넘어가지 않게 하는 방어다(이 해석은 노트 작성자의 것).

6. DiffTools.InitializeFromPullRequestFiles를 고친다. 돌아온 files 배열을 순회해 filename, additions, deletions, patch를 읽고, 이전 로컬 diff 구현이 쓰던 것과 같은 FileDiffEntry 객체를 만든다. 이전의 파일 로딩과 파싱 경로는 이제 MCP 응답이 PR 데이터의 출처이므로 제거한다.

## 3. 자식 프로세스의 환경 변수 주의

이 구현에서 stdio 자식 프로세스는 워크플로 환경을 그대로 물려받으며, 여기에는 PR_ANALYSIS_TOKEN도 들어 있다. 원서는 운영 호스트라면 서버에 필요한 환경 변수만 넘기고, 관련 없는 자격 증명을 자식 프로세스에 노출하지 말라고 경고한다. 최소 권한 원칙이 환경 변수에도 적용된다는 뜻이다.

## 4. 다음 단계

에이전트가 이제 MCP로 PR 데이터를 가져오므로, 남은 일은 GitHub Actions 잡을 설정하고, 결정론적 출력 검사를 유지하고, 기존 리스크 게이트를 적용하는 것이다.

## 5. 핵심 정리

- 바뀌는 것은 PR 파일의 출처뿐이고, DiffTools와 검증과 대체 JSON은 그대로 쓴다.
- 도구 이름은 서버의 `github_list_pull_request_files`와 정확히 같아야 하고 인자는 딕셔너리로 넘긴다.
- 결과는 텍스트 블록에서 JSON으로 파싱하고, 텍스트가 없으면 예외로 실패한다.
- 이전 로컬 파일 로딩 경로는 제거한다.
- stdio 자식 프로세스가 환경 변수를 물려받는 점은 운영에서 필요한 변수만 넘기도록 좁혀야 한다.

<br>
<br>
<br>

[Agentic AI for DevOps Engineers](../)
