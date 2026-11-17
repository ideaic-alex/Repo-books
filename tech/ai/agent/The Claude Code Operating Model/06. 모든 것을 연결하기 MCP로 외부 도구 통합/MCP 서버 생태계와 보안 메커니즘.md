# MCP 서버 생태계와 보안 메커니즘

이미 만들어진 MCP 서버가 무엇이 있는지, 그것들을 어떻게 조합해 한 세션에서 쓰는지, 그리고 Claude가 외부 시스템을 직접 만지게 될 때 어떤 신뢰 경계와 위험이 생기는지를 다룬다. MCP는 Claude의 능력 범위를 크게 넓히는 만큼 그것이 곧 가장 큰 보안 위험이기도 하다. 원서는 3겹의 방어 장치와 2025년 4월에 보고된 세 가지 위험, 그리고 대응책을 정리한다.

---

## 1. 흔한 MCP 서버 생태계

Anthropic과 MCP 커뮤니티는 바로 쓸 수 있는 서버를 폭넓게 관리한다.

### 1-1. 공식 서버 (표 6.2)

| 서버 이름 | 주요 용도 | 설치·시작 명령 |
|---|---|---|
| server-filesystem | 파일 시스템 읽기·쓰기 | `npx @modelcontextprotocol/server-filesystem <path>` |
| server-fetch | HTTP 요청 보내기 | `npx @modelcontextprotocol/server-fetch` |
| server-postgres | PostgreSQL 데이터베이스 조회 | `npx @modelcontextprotocol/server-postgres` |
| server-memory | 세션을 넘는 영구 메모리 저장 | `npx @modelcontextprotocol/server-memory` |
| server-git | Git 버전 관리 작업 | `npx @modelcontextprotocol/server-git` |

원서 표는 명령이 줄바꿈으로 잘려 추출되었으나 패키지 이름은 `@modelcontextprotocol/` 뒤에 위 서버 이름이 붙는 규칙으로 복원했다. server-filesystem을 띄울 때는 path 인자를 실제로 허용할 디렉터리로 바꾼다. 프로젝트 하나면 `./src`, 작업 공간 전체면 `~/projects/my-app` 같은 식이며, 서버는 그 바깥을 아무것도 읽지 못한다.

### 1-2. 인기 서드파티 서버 (표 6.3)

| 서버 이름 | 주요 용도 | 전송 |
|---|---|---|
| GitHub MCP | GitHub 협업 관리(PR, 이슈, 코드 검색) | HTTP |
| Notion MCP | Notion 문서 읽기·쓰기 | HTTP |
| Sentry MCP | 오류 추적과 로그 분석 | HTTP |
| Context7 | 최신 기술 문서 조회 | stdio |
| Bytebase DBHub | 여러 데이터베이스의 통합 접근·관리 | stdio |

### 1-3. 실전 구성 조합

파일 시스템 서버(허용한 디렉터리로 범위 제한), HTTP 요청용 fetch 서버, 이슈·PR용 GitHub 서버, Postgres 같은 데이터베이스 서버를 한 `.mcp.json`에 묶는 예시가 있다.

| 서버 | 연결 방식 | 핵심 설정 |
|---|---|---|
| filesystem | stdio | `npx -y @modelcontextprotocol/server-filesystem .` |
| fetch | stdio | `npx -y @modelcontextprotocol/server-fetch` |
| github | HTTP | url `https://api.githubcopilot.com/mcp/`, headers의 Authorization을 `Bearer ${GITHUB_TOKEN}`으로 |
| database | stdio | `npx -y @bytebase/dbhub --dsn ${DATABASE_URL}` |

설정의 `${GITHUB_TOKEN}`과 `${DATABASE_URL}`은 환경 변수 자리표시자이므로 사용 전에 터미널 환경에 올바르게 설정해 두어야 한다(원서 TIP).

이 구성이면 여러 도구를 오가야 했던 복잡한 흐름을 Claude 세션 하나에서 매끄럽게 끝낼 수 있다.

- 데이터 조회: "DB에서 최근 7일 주문 총액을 계산해 줘" → 데이터베이스 서버가 SQL 쿼리를 실행한다.
- 작업 관리: "위 버그 설명을 정리해 새 GitHub 이슈로 만들어 줘" → GitHub 서버가 API로 티켓을 제출한다.
- 문서 검색: "React 19 Server Components의 최신 공식 문서를 가져와 줘" → fetch 서버가 웹 내용을 실시간으로 가져온다.

## 2. 보안 메커니즘: 신뢰의 경계

### 2-1. 3겹 방어

유연성과 보안의 균형을 위해 MCP 구조에는 단계적인 3겹 방어가 있다.

| 층 | 이름 | 내용 |
|---|---|---|
| 1 | 첫 연결 시 대화형 승인 | 신뢰 구축의 초석. 새 MCP 서버를 설정하면 Claude Code가 처음 연결을 시도하기 전에 자동으로 멈추고 출처, 권한 범위 같은 서버 정보를 보여 주며 명시적 승인을 요구한다. 건너뛸 수 없는 필수 대화형 절차다 |
| 2 | 도구 수준의 세밀한 권한 제어 | 서버 전체를 승인했더라도, 파일 쓰기, 코드 실행, DB 수정처럼 부작용이 있는 도구를 부를 때는 다시 가로채어 실행할 구체적 명령을 보여 주고 두 번째 확인을 기다린다 |
| 3 | OAuth 2.1 기반 동적 인증 | 원격 MCP 서버에는 장기 정적 API 키 대신 규격이 정한 OAuth 2.1 흐름(PKCE 포함)을 쓴다. 기업 SSO와 연동이 쉽고, 단기이며 폐기 가능한 자격 증명을 얻는다. 열두 개의 설정 파일에 복사된 비밀을 교체하는 것과 토큰 하나를 교체하는 것의 차이다 |

### 2-2. 보안 위험과 대응

2025년 4월 보안 연구자들이 MCP 생태계에서 다음 위험을 확인했다(원서가 인용한 출처는 Invariant Labs의 도구 오염 공격 공지다).

| 위험 | 내용 | 대응 |
|---|---|---|
| 프롬프트 주입 공격 | MCP 서버를 통해 Claude의 컨텍스트에 악성 내용이 주입된다. 서버가 "이전 지시를 모두 무시하고 다음 작업을 실행하라" 같은 지시가 든 데이터를 돌려주면 Claude가 속을 수 있다 | 신뢰할 수 있는 출처의 MCP 서버만 쓴다 |
| 도구 권한 남용 | 개별 도구의 권한은 안전해 보여도 여러 도구를 조합하면 예상 못한 결과가 난다. 예를 들어 "파일 읽기"와 "이메일 보내기" 도구의 조합은 이론상 파일 내용 유출로 이어질 수 있다 | 최소 권한 원칙을 지킨다 |
| 사칭 | 악성 도구가 이름과 설명을 정상 도구처럼 꾸며 Claude가 호출하게 속인다 | 신뢰할 수 있는 출처의 MCP 서버 패키지만 설치한다 |

### 2-3. 케이지의 노트: 의존성처럼 검증하라

공식 modelcontextprotocol/servers 저장소의 서버를 우선한다. 이 저장소는 참조 구현 모음이다. 그 밖의 서버는 셸 접근 권한이 있는 어떤 의존성에든 적용할 검사를 똑같이 적용한다. 버전을 고정하고, 소스를 읽고, 자격 증명의 범위를 작동하는 가장 좁은 것으로 한정한다. 이 노트는 원서에서 쪽 경계를 넘어 문장이 둘로 쪼개져 추출되었고, 내용상 이어 붙여 복원했다.

---

## 3. 핵심 정리

- 공식 서버는 filesystem, fetch, postgres, memory, git이고, 서드파티는 GitHub, Notion, Sentry(HTTP), Context7, Bytebase DBHub(stdio)가 대표적이다.
- filesystem 서버는 허용한 경로 밖을 읽지 못한다. 경로는 필요한 범위로만 준다.
- 방어는 첫 연결 승인, 도구별 승인, OAuth 2.1(PKCE) 인증의 3겹이다.
- 위험은 프롬프트 주입, 도구 권한 남용(조합 효과), 사칭이며 대응은 신뢰 출처, 최소 권한, 버전 고정과 소스 확인이다.

<br>
<br>
<br>

[The Claude Code Operating Model](../)
