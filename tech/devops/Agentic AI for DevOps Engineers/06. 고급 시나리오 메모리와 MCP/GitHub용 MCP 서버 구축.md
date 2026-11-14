# GitHub용 MCP 서버 구축

이 실습은 완성된 강의 구현을 바탕으로 .NET 10 stdio MCP 서버를 만든다. 서버는 읽기 도구 두 개(github_get_pull_request, github_list_pull_request_files)와 통제된 쓰기 도구 하나(github_add_pull_request_comment)를 노출한다. 이 장에서 PR 품질 에이전트가 쓰는 도구는 파일 목록 조회뿐이다. 쓰기 도구는 기능 범위와 토큰 권한이 쓸 수 있는 동작을 어떻게 좌우하는지 보이려고 일부러 넣었다.

설계의 핵심은 모델이 도구를 고르되, GitHub 토큰과 요청 구성과 외부 부작용은 MCP 서버가 쥔다는 점이다. 이 분리가 연동을 감사 가능하고 제한된 상태로 유지하는 중심이다.

---

## 1. 아키텍처

GitHub Actions 러너가 에이전트 프로세스를 호스팅한다. 에이전트는 MCP 클라이언트를 만들어, 표준 입력과 출력(stdio)으로 로컬 서버를 실행한다. MCP 클라이언트와 서버 사이에는 JSON-RPC 메시지가 오간다. 서버는 일반 C# 코드를 실행해 GitHub REST API를 호출하고 결과를 클라이언트에 돌려준다. 이 경계가 모델의 추론과, 자격 증명과 외부 부작용을 처리하는 승인된 구현을 갈라놓는다.

전체 흐름은 이렇다(원서 그림 6.6의 설명).

1. PR 이벤트가 워크플로를 트리거하고, 워크플로가 에이전트와 서버의 입력을 설정한다.
2. 에이전트가 MCP 도구로 PR 파일을 가져온다.
3. 간결한 파일 목록을 만들고, 로컬의 모델용 도구로 관련 있는 패치만 살핀다.

이 구조는 GitHub 연동 로직을 한곳에 모으고, 모델에 API 직접 접근을 주지 않고도 다른 에이전트가 같은 서버를 재사용하게 해 준다.

C# MCP SDK는 로컬 stdio와 원격 HTTP 전송을 지원한다. 이 장은 에이전트와 서버가 같은 잡 안에서 도므로 stdio를 쓴다. 클라이언트가 서버 프로세스를 띄우고 표준 입출력으로 통신하므로, 서버는 표준 출력을 프로토콜 메시지 전용으로 비워 두고 진단 메시지는 표준 오류로 써야 한다.

## 2. 서버 프로젝트 만들기

완성본은 원서 저장소 finish/mcp/DevOps.McpServer에 있다. 단계는 원서 번호를 따랐다.

1. MCP 작업용 기능 브랜치를 만들고 finish 샘플 디렉터리에서 터미널을 연다.
2. 완성 워크플로와 같은 경로에 서버 프로젝트를 만든다.

```
dotnet new console -n DevOps.McpServer -o mcp/DevOps.McpServer
```

3. 프로젝트 파일을 과정 저장소가 고정한 패키지 버전으로 바꾼다. 출력 형식은 Exe, 대상은 net10.0, ImplicitUsings와 Nullable은 enable이다. 패키지는 Microsoft.Extensions.Hosting 10.0.3, Microsoft.Extensions.Http 10.0.3, ModelContextProtocol 1.0.0이다. 원서는 ModelContextProtocol 1.0.0이 이 구현에서 net10.0을 대상으로 하는 안정 버전이라고 적는다.
4. Program.cs를 다음 구성으로 바꾼다.

   - 로깅은 표준 오류로 돌린다(`LogToStandardErrorThreshold = LogLevel.Trace`). 표준 출력의 프로토콜 트래픽이 유효한 JSON-RPC로 유지되기 때문이다.
   - 환경 변수 PR_ANALYSIS_TOKEN을 읽어 GitHubAuthOptions 레코드로 싱글턴 등록하고, GitHubTooling도 싱글턴으로 등록한다.
   - GitHubApiClient용 HttpClient를 등록한다. 기준 주소는 GitHub API, 타임아웃 30초, User-Agent 설정, Accept는 vnd.github+json, API 버전 헤더 X-GitHub-Api-Version은 2022-11-28이다. 토큰이 있으면 Bearer 인증 헤더를 붙인다.
   - MCP 서버를 `AddMcpServer().WithStdioServerTransport().WithToolsFromAssembly()` 체인으로 등록한 뒤 실행한다.

```csharp
builder.Services.AddMcpServer().WithStdioServerTransport().WithToolsFromAssembly();
```

WithToolsFromAssembly는 현재 어셈블리에서 McpServerToolType이 붙은 클래스를 찾아 도구로 등록한다. 이로써 호스트가 stdio로 실행되고 어셈블리에서 도구를 발견하도록 구성되었다.

## 3. GitHub API 클라이언트 구현

다음 층은 인증이 필요한 GitHub REST 호출을 한곳에 모아, 도구 메서드마다 전송, 오류 처리, 토큰 관리를 중복하지 않게 한다. 파일은 mcp/DevOps.McpServer/GitHub/GitHubApiClient.cs이고 완성본은 원서 저장소에 있다. 이 클라이언트는 다음을 한곳에 모은다.

| 기능 | 동작 |
|---|---|
| 인증 검사 | EnsureAuthenticated. 토큰이 비면 "PR_ANALYSIS_TOKEN is not set..." 예외 |
| GET (GetJson) | 상대 경로 앞의 슬래시를 떼고 헤더만 받은 시점에 응답을 처리. 실패 시 상태 코드, 이유, 남은 호출 한도(X-RateLimit-Remaining)와 Retry-After를 경고 로그에 남기고 본문과 함께 예외를 던짐 |
| POST (PostJson) | 인증을 내부에서 다시 확인하고 JSON 본문을 보냄. 204 NoContent면 `{"status":"ok"}`를 돌려주고, 실패하면 본문과 함께 예외 |

GetJson은 읽기 도구가 요청 전에 EnsureAuthenticated를 부른 뒤 호출하며, PostJson은 같은 검사를 내부에서 한다. 돌려주는 JsonElement는 JsonDocument가 해제되기 전에 복제해서(Clone) 반환한다.

실패를 조용히 삼키지 않고 실행 가능한 오류로 위로 올리는 점이 중요하다. 5장에서 본 도구 취약성과 거짓 확신을 막는 설계다. 이 연결은 노트 작성자의 해석이다.

## 4. MCP 도구 정의

API 클라이언트는 GitHub로 가는 통제된 경로를 주지만, 승인된 동작이 이름 붙은 도구로 노출되기 전에는 MCP 클라이언트가 발견할 수 없다. 파일은 mcp/DevOps.McpServer/GitHub/GitHubTooling.cs다. 클래스에 McpServerToolType을, 공개 도구 메서드마다 McpServerTool을 붙인다. 아래 이름은 에이전트가 쓰는 정확한 이름이며 클라이언트 호출과 반드시 일치해야 한다.

| 도구 이름 | 하는 일 | 인자 |
|---|---|---|
| github_get_pull_request | PR 번호로 제목, 본문, 상태, 작성자, head/base 참조를 가져옴 | owner, repo, number |
| github_list_pull_request_files | 변경 파일의 이름, 상태, 추가/삭제 줄 수, patch를 나열 | owner, repo, number, page(기본 1), perPage(기본 100, 최대 100) |
| github_add_pull_request_comment | PR 대화에 이슈 댓글로 댓글을 추가(쓰기) | owner, repo, number, body(마크다운 댓글 본문) |

모든 도구는 먼저 EnsureAuthenticated를 부른다. 조회 경로는 각각 `repos/{owner}/{repo}/pulls/{number}`, `repos/{owner}/{repo}/pulls/{number}/files?page=..&per_page=..`이고, 댓글은 `repos/{owner}/{repo}/issues/{number}/comments`에 POST한다. 댓글 도구는 호출할 때 PR 번호와 저장소를 정보 로그로 남긴다.

처음 두 도구는 읽기 작업이다. github_add_pull_request_comment는 상태를 바꾸는 작업이므로 토큰과 워크플로가 댓글 생성을 의도적으로 허용할 때만 켜야 한다. 각 인자에는 설명(Description) 특성이 붙어 있어, 모델과 클라이언트가 도구를 정확히 이해하는 근거가 된다.

## 5. 빌드하고 확인하기

아래 명령으로 finish 샘플 디렉터리에서 서버를 빌드한다.

```
dotnet build mcp/DevOps.McpServer/DevOps.McpServer.csproj
```

빌드에 성공하면 앱 호스트와 DevOps.McpServer.dll이 mcp/DevOps.McpServer/bin/Debug/net10.0 아래에 생긴다. 컴파일은 서버가 구조적으로 건전하다는 것만 확인할 뿐이다. MCP 클라이언트가 실행하고, 도구를 발견하고, 인자를 바인딩하고, 응답을 받을 수 있는지는 보장하지 않는다. 그래서 다음 문서에서 에이전트와 분리해 이 프로토콜 동작을 따로 시험한다.

참고(노트 작성자): 원서의 코드 목록은 줄바꿈과 따옴표가 일부 깨져 있었고(특히 Accept 헤더 값과 문자열 보간 부분), 단계 번호도 코드 블록 사이에서 다시 1부터 시작하는 등 어긋나 있었다. 위 설명은 코드의 구조와 본문 문장을 근거로 복원했다. 정확한 코드는 원서 저장소의 finish/mcp 폴더를 확인하는 것이 안전하다.

## 6. 핵심 정리

- 서버는 도구 세 개(읽기 둘, 쓰기 하나)를 노출하고, 모델은 도구를 고르지만 토큰과 요청과 부작용은 서버가 쥔다.
- stdio 전송이라서 표준 출력은 프로토콜 전용이고 로그는 표준 오류로 보낸다.
- GitHub 토큰은 환경 변수 PR_ANALYSIS_TOKEN으로 받고, 없으면 도구 호출이 명확한 오류로 실패한다.
- GitHubApiClient가 인증, GET, POST, 타임아웃, 응답 파싱, 오류를 한곳에 모은다.
- 도구 이름은 에이전트의 클라이언트 호출과 정확히 일치해야 한다.
- 쓰기 도구는 토큰과 워크플로가 허용할 때만 켠다. 빌드 성공만으로는 프로토콜 동작이 검증되지 않는다.

<br>
<br>
<br>

[Agentic AI for DevOps Engineers](../)
