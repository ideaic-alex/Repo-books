# 실습: 데이터베이스 연결과 사용자 정의 MCP 서버

두 가지 실습을 다룬다. 첫째는 가장 흔한 요구인 "Claude가 데이터베이스를 직접 조회하게 하기"로, PostgreSQL MCP 서버 설정 한 번이면 끝난다. 둘째는 기존 서버로 부족할 때 TypeScript나 Python SDK로 나만의 MCP 서버를 만드는 일로, 할 일(to-do) 관리 서버가 예제다. 두 실습에서 공통으로 건지는 교훈은 보안(읽기 전용 계정)과 로그 출력 위치(stderr)다.

---

## 1. 실습 1: 데이터베이스 연결

먼저 PostgreSQL MCP 서버를 설정한다. 핵심은 `.mcp.json`에 서버 이름 postgres, 명령 `npx`, 인자 `["-y", "@modelcontextprotocol/server-postgres"]`, 환경 변수 `DATABASE_URL`을 `${DATABASE_URL:-postgresql://localhost:5432/mydb}` 형태로 넣는 것이다. 환경 변수가 없으면 로컬 기본 주소를 쓴다.

설정이 끝나면 자연어로 지시하면 된다. 원서 대화 예시는 이렇다. 사용자가 "지난달 주문 수와 총액을 조회해 줘"라고 하면 Claude가 "postgres MCP 서버의 sql_query 도구를 호출"하고, 지난달(2025년 12월) 주문 1,234건, 총액 $456,789.00, 평균 주문액 $370.21, 전월 대비 12.3% 증가라는 결과를 돌려준다.

이 과정에서 Claude는 조회 요구를 스스로 알아차리고, Postgres MCP 서버를 찾아, SQL을 만들어 실행하고, 결과를 정리해 돌려준다. 사용자는 SQL 문법을 몰라도 되고 DB 클라이언트를 열거나 데이터를 손으로 내보낼 필요도 없다.

### 핵심 보안 원칙: 읽기 전용 계정

데이터베이스 연결에는 읽기 전용 계정만 써야 한다. 원서는 읽기 전용 허용 목록(allowlist)이 올바른 기본값이라고 설명한다. DROP TABLE 같은 문장은 테이블과 모든 행을 파괴하고, 조회와 달리 다시 실행해도 피해를 되돌릴 수 없다. 이 비대칭 때문에 쓰기는 파괴적인 것으로 취급해 허용 목록에서 제외한다.

## 2. 실습 2: 사용자 정의 MCP 서버 만들기

기존 MCP 서버로 요구를 못 채울 때(사내 API 연동, 특정 형식의 데이터 처리 도구 등)는 TypeScript나 Python SDK로 전용 서버를 만든다. 원서의 TypeScript 예시는 할 일 목록 서버로, MCP 서버의 기본 골격을 보여 준다.

### 2-1. TypeScript 서버의 구성

| 구성 요소 | 내용 |
|---|---|
| 가져오기 | `@modelcontextprotocol/sdk`의 McpServer, StdioServerTransport, 그리고 스키마 검증용 zod |
| 저장소 | 메모리 안의 todos 배열(id, text, done) |
| 서버 인스턴스 | `new McpServer({ name: "todo-server", version: "1.0.0" })` |
| 도구 todo_add | 설명 "Add a new todo item", 입력 `{ text: z.string().describe("The todo text") }`, 무작위 id를 만들어 todos에 넣고 "Added: id - text"를 돌려준다 |
| 도구 todo_list | 설명 "List all todo items", 입력 없음. 비었으면 "No todos found.", 있으면 `[x]` 또는 `[ ]` 표시와 id, 텍스트를 줄마다 돌려준다 |
| 리소스 stats | 설명 "Server statistics". total, completed, pending 개수를 mimeType `application/json`으로 돌려준다 |
| 시작 | StdioServerTransport를 만들어 server.connect(transport)하고 시작 로그는 console.error로 낸다 |

```typescript
const server = new McpServer({ name: "todo-server", version: "1.0.0" });
server.tool("todo_add", "Add a new todo item",
  { text: z.string().describe("The todo text") },
  async ({ text }) => { /* todos에 추가 후 결과 텍스트 반환 */ });
const transport = new StdioServerTransport();
await server.connect(transport);
console.error("MCP Server started");   // 로그는 stderr로
```

원서 코드의 추출 상태는 좋지 않다. stats 리소스 블록 안에 "Start the server"와 `async function main()`, `StdioServerTransport` 줄이 끼어들었고, 뒤쪽에는 "Focus on checking for security vulnerabilities, logic errors, and performance issues." 같은 코드 리뷰 프롬프트 문장이 섞여 있다. 이는 다른 대목의 문장이 조판 과정에서 섞인 것으로 보여 제외했고, 위 표는 각 도구·리소스의 정의 순서와 주석으로 구성을 복원한 것이다. 코드는 핵심만 줄여 실었다.

### 2-2. 주목할 설계 포인트 세 가지

- **도구 설명이 중요하다**: `server.tool()`의 두 번째 매개변수인 설명 문자열이 Claude가 언제 이 도구를 부를지 판단하는 핵심 근거다. 설명이 분명하고 정확할수록 Claude가 의도를 정확히 파악해 알맞은 도구를 부른다.
- **타입 안전성과 검증**: 입력 매개변수는 Zod 스키마로 정의한다. 엄격한 타입 안전성을 주고 런타임에 매개변수를 자동 검증해 잘못된 데이터가 들어오는 것을 막는다.
- **로그 출력 규칙**: 디버그 로그는 stdout이 아니라 `console.error`로 stderr에 낸다. stdout 채널은 JSON-RPC 메시지 전송 전용이라, 일반 로그가 섞이면 프로토콜 파싱이 실패한다. 이는 5장의 훅 스크립트 디버그 출력 원칙과 같다.

### 2-3. Python 구현

Python도 간결하다. `mcp.server`의 Server와 `mcp.server.stdio`의 stdio_server를 가져와 `Server("todo-server")`를 만들고, `@server.tool("todo_add")`와 `@server.tool("todo_list")` 데코레이터로 도구를 정의한다. 함수의 독스트링("Add a new to-do item", "List all to-do items")이 도구 설명 역할을 한다. 주 함수는 `async with stdio_server() as (read_stream, write_stream)` 안에서 `server.run(read_stream, write_stream)`을 호출하고, `asyncio.run(main())`으로 시작한다. 예시의 `generate_id()`는 정의되어 있다고 가정한 함수다.

원서 Python 코드 역시 `todo_list` 부분에서 `return "No todos found."`와 `"\n".join(` 줄이 중복되고, `import asyncio` 들여쓰기가 깨져 있다. 중복은 조판 오류로 보아 한 번만 읽었고 들여쓰기는 문맥으로 복원했다.

### 2-4. 설정 파일에 등록

개발이 끝나면 설정 파일에 서버를 등록한다. 컴파일한 서비스를 띄우는 예시는 서버 이름 my-todo에 `command: "node"`, `args: ["./mcp-server/build/index.js"]`를 둔다. Python 프로젝트라면 command를 python으로 바꾼다.

---

## 3. 핵심 정리

- DB 연결은 postgres MCP 서버 설정 하나로 되고, 이후 자연어로 요청하면 Claude가 SQL 생성과 실행을 맡는다. 연결 계정은 반드시 읽기 전용으로 한다. 쓰기(DROP 등)는 되돌릴 수 없어 허용 목록에서 뺀다.
- 사용자 정의 서버는 SDK로 만든다. 도구(todo_add, todo_list)와 리소스(stats)를 정의하고 stdio로 연결한다.
- 도구 설명 문자열이 Claude의 도구 선택 근거이고, Zod 스키마가 입력을 검증한다.
- 로그는 반드시 stderr로 내야 한다. stdout이 오염되면 JSON 파싱 오류가 난다.
- 만든 서버는 `.mcp.json`에 command와 args로 등록한다.

<br>
<br>
<br>

[The Claude Code Operating Model](../)
