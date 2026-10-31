# 기업 환경의 MCP

회사 단위로 Codex CLI를 쓰면 어떤 MCP 서버를 허용할지, 누가 쓸 수 있는지, 서버가 어떤 자격 증명을 들고 있는지를 통제해야 한다. 이 문서는 서버 허용 범위 관리, 자격 증명 격리, 그리고 서버가 사용자에게 되묻는 엘리시테이션(elicitation)을 다룬다.

---

## 1. 서버 범위 정하기

플랫폼 팀이 배포하는 관리형(managed) config.toml에서 문서화된 `mcp_servers.<id>.enabled` 키로 허용할 서버를 선언한다. 검증하지 않은 서버는 명시적으로 끄거나 아예 적지 않는다.

```toml
# Managed config: only these servers run; everything else is disabled by default.
[mcp_servers.github]
enabled = true
# ... command, args, env, enabled_tools as needed
[mcp_servers.context7]
enabled = true
# ...
[mcp_servers.unvetted_server]
enabled = false
```

Codex CLI의 설정 계층 구조상 개발자 로컬 config.toml이 개별 키를 덮어쓸 수는 있다. 하지만 기준선은 플랫폼 팀의 관리형 설정이다. 민감한 서버에 `enabled = false`를 명시해 두면 팀 차원에서 실수로 다시 켜지는 일을 막는다. 관리형 설정을 어떻게 배포하는지, 프로젝트 범위 재정의가 팀 정책과 어떻게 상호작용하는지 등 기업 배포 전체 구조는 17장에서 다룬다.

## 2. 자격 증명 격리

MCP 서버의 자격 증명(API 토큰, 데이터베이스 URL)도 다른 비밀 값과 같은 방식으로 다뤄야 한다. 실행 시점에 서버 프로세스에 주입하고 설정 파일에 커밋하지 않는다.

- 서버가 기대하는 환경 변수 이름 그대로를 Codex CLI 시작 전에 설정하는 방법이 가장 낫다.
- 또는 운영체제의 비밀 저장소에서 값을 읽은 뒤 MCP 서버를 exec로 띄우는 런처(래퍼)를 쓴다.
- `${GITHUB_TOKEN}` 같은 셸식 자리 표시자가 config.toml 안에서 확장될 것이라고 가정하지 않는다. 사용 중인 Codex CLI 버전이 그 동작을 명시적으로 문서화한 경우가 아니라면 그렇다.

## 3. 엘리시테이션

엘리시테이션은 서버가 세션 도중에 사용자에게 추가 정보를 요청하는 MCP 기능이다. 빠진 매개변수를 물어보거나, 파괴적인 작업 전에 확인을 받거나, 모호한 질의에 대한 설명을 요청하는 데 쓴다. 이 기능은 세분화된 승인 정책(granular approval policy)의 `mcp_elicitations` 승인 범주로 제어한다.

## 4. 점검 목록

- 허용한 서버만 enabled = true이고 나머지는 false이거나 없는가
- 토큰이 config.toml에 적혀 있지 않고 프로세스 환경으로 들어가는가
- 자리 표시자가 확장되지 않은 채 서버에 그대로 전달되고 있지 않은가
- 엘리시테이션 승인 범주를 정책에서 의도한 대로 설정했는가

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
