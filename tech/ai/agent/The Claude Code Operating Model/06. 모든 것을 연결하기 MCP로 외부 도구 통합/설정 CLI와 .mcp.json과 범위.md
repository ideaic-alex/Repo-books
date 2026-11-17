# 설정: CLI, .mcp.json, 범위

MCP 서버를 Claude Code에 연결하는 방법은 두 가지다. 명령줄의 claude mcp 명령으로 빠르게 추가하거나, 설정 파일 `.mcp.json`을 직접 고치는 것이다. CLI 명령은 결국 이 파일을 다루는 도구이므로 파일 구조를 알면 세밀한 설정이 가능하다. 이 문서는 명령 모음, 파일 구조, 환경 변수 치환, 설정 위치별 범위, 그리고 비밀을 Git에 올리지 않는 방법을 정리한다.

---

## 1. CLI로 빠르게 설정하기

`claude mcp` 명령 세트로 MCP 서버 설정을 관리한다. 원서 예시를 용도별로 풀어 쓴다.

| 목적 | 명령(핵심) | 설명 |
|---|---|---|
| 로컬 stdio 서버 추가 | `claude mcp add filesystem npx -y @modelcontextprotocol/server-filesystem /workspace` | 작업 디렉터리를 /workspace로 한 로컬 파일 시스템 서비스 |
| 원격 HTTP 서버 추가 | `claude mcp add --transport http company-jira https://jira.company.com/mcp` | 사내 Jira 서비스에 연결 |
| 사용자 수준(전역) 서버 추가 | `claude mcp add --scope user github -- npx -y @modelcontextprotocol/server-github` | 모든 프로젝트에 적용되는 사용자 설정에 GitHub 서비스 추가 |
| 인증이 있는 서버 추가 | `claude mcp add --transport http --header "Authorization: Bearer ${TOKEN}" api https://api.example.com/mcp` | 사용자 정의 HTTP 헤더로 인증 토큰 전달 |
| 목록 | `claude mcp list` | 현재 설정된 MCP 서버 전체 보기 |
| 연결 시험 | `claude mcp test github` | 지정 서버의 연결 상태와 사용 가능 여부 확인 |
| 삭제 | `claude mcp remove github` | 지정 서버 설정 제거 |

`--scope user`는 사용자 수준 설정을, `--transport http`는 전송 방식을 지정하는 옵션이다. 원서 명령은 줄바꿈 때문에 일부 줄이 쪼개져 추출되었으나 옵션 이름과 인자 순서는 그대로 읽힌다.

## 2. .mcp.json 구조

`claude mcp` 명령은 본질적으로 `.mcp.json` 설정 파일을 조작한다. 원서 예시의 핵심 구조는 다음과 같다. 최상위 키는 mcpServers이고 그 아래에 서버 이름별 항목이 있다.

```json
{
  "mcpServers": {
    "filesystem": { "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"],
      "env": {} },
    "company-jira": { "type": "http", "url": "https://jira.company.com/mcp",
      "headers": { "Authorization": "Bearer ${JIRA_TOKEN}" } },
    "postgres": { "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": { "DATABASE_URL": "${DB_URL:-postgresql://localhost:5432/mydb}" } }
  }
}
```

두 가지 유형이 보인다. stdio 서버는 `command`, `args`, `env`를 쓰고, 원격 서버는 `type: "http"`, `url`, `headers`를 쓴다. 원서 코드는 줄바꿈이 어긋나 있어 한 항목씩 다시 정렬해 적었다.

## 3. 환경 변수 치환: 가장 중요한 기능

설정 파일에서 가장 중요한 기능은 환경 변수 치환이다.

- `${VAR_NAME}`: 실행 시점에 자리표시자를 해당 환경 변수의 값으로 바로 바꾼다.
- `${VAR_NAME:-default_value}`: 환경 변수 VAR_NAME이 설정되지 않았으면 지정한 기본값을 쓴다.

이 기능으로 API 키나 DB 비밀번호 같은 민감 정보를 mcp.json에 직접 쓰지 않고 운영체제 환경 변수나 .env 파일에 둘 수 있다. 설정 파일에는 실제 비밀이 아니라 변수 참조(`${JIRA_TOKEN}` 같은)만 들어 있으므로, 자격 증명 유출 걱정 없이 mcp.json을 Git 저장소에 커밋해 팀과 공유해도 된다.

## 4. 설정 파일 위치와 범위

mcp.json의 적용 범위는 위치에 따라 다르다(표 6.1).

| 위치 | 범위 | 적용 시나리오 |
|---|---|---|
| `.mcp.json`(프로젝트 루트 디렉터리) | 프로젝트 수준 | 현재 프로젝트에만 적용. 특정 코드베이스에 묶인 팀 공유 서비스(프로젝트의 DB 연결, 특정 사내 도구)에 알맞다. 보통 Git에 커밋한다 |
| `~/.claude/` 디렉터리 | 모든 프로젝트, 사용자 수준 | 모든 프로젝트에 적용. 개인용 범용 도구(개인 파일 시스템 접근, 전역 코드 검색 도구)에 알맞다. 사용자 홈 디렉터리에 있어 프로젝트에 따라 바뀌지 않는다 |

### 개인 자격 증명 분리

개인 GitHub 토큰처럼 특정 MCP 서버의 자격 증명을 Git에 올리면 안 될 때는, 자격 증명 부분을 `.claude/settings.local.json`(이미 .gitignore로 제외됨)에 저장하고 서버의 기본 구성은 팀 공유용 mcp.json에 둘 수 있다.

참고(노트 작성자): 원서는 `.claude/settings.local.json`에 자격 증명 부분을 저장한다고만 쓰고 구체적인 키 구조는 보이지 않는다. 앞 절의 환경 변수 치환과 함께 쓰는 것이 가장 단순한 방법으로 읽히지만, 구체적 설정 형식은 원서에 없으므로 공식 문서를 확인해야 한다.

---

## 5. 핵심 정리

- 서버 추가·확인은 `claude mcp add`, `list`, `test`, `remove`로 한다. 옵션은 `--transport http`, `--scope user`, `--header`다.
- CLI는 `.mcp.json`(최상위 mcpServers)을 다루는 도구다. stdio는 command, args, env, 원격은 type, url, headers를 쓴다.
- `${VAR}`와 `${VAR:-기본값}` 치환 덕에 비밀은 환경 변수에 두고 설정 파일만 안전하게 커밋한다.
- 프로젝트 루트의 `.mcp.json`은 팀 공유, `~/.claude/`는 개인 전역이다. 개인 자격 증명은 `.claude/settings.local.json`으로 분리한다.

<br>
<br>
<br>

[The Claude Code Operating Model](../)
