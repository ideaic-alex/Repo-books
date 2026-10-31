# 플러그인과 MCP 승인 설정

플러그인과 MCP 서버는 외부 코드를 Claude Code에 끌어들이는 통로다. 그래서 settings.json에는 어떤 것을 켜고, 어떤 것을 승인하고, 어떤 것을 막을지 정하는 키가 따로 있다. 이 문서는 플러그인 활성화, 프로젝트 `.mcp.json` 서버 승인, 그리고 관리자 전용 키를 정리한다.

---

## 1. 플러그인 설정

| 키 | 타입 | 설명 |
|---|---|---|
| `enabledPlugins` | string[] | 켜 둘 플러그인 식별자. `plugin-name@marketplace-name` 형식 |
| `extraKnownMarketplaces` | object[] | 추가로 인정할 플러그인 마켓플레이스 소스. 신뢰 경계를 명시한다 |

플러그인의 훅은 플러그인 루트 디렉터리 안의 `hooks/hooks.json`에 정의한다. 이 훅 정의에는 선택 사항으로 최상위 `description` 필드를 넣을 수 있다. 플러그인 스크립트는 `${CLAUDE_PLUGIN_ROOT}` 변수로 자기 디렉터리를 가리킨다. 플러그인이 어디에 설치되든 번들된 스크립트를 찾을 수 있게 하는 장치다.

마켓플레이스 소스를 적는 형식은 MCP 설정 문서의 "플러그인 마켓플레이스 소스" 표에 있다.

## 2. MCP 서버 승인

프로젝트 루트의 `.mcp.json`에 정의된 MCP 서버는 팀원이 저장소를 받으면 함께 따라온다. 그래서 이 서버들을 자동으로 믿을지는 사용자 설정으로 따로 정한다.

| 키 | 타입 | 설명 |
|---|---|---|
| `enableAllProjectMcpServers` | boolean | 프로젝트 `.mcp.json`에 정의된 모든 MCP 서버를 자동 승인한다 |
| `enabledMcpjsonServers` | string[] | `.mcp.json` 중 승인할 서버를 지정한다. 예: `["memory", "github"]` |
| `disabledMcpjsonServers` | string[] | `.mcp.json` 중 거부할 서버를 지정한다 |

전부 승인하는 `enableAllProjectMcpServers`는 편하지만, 저장소에 들어온 모든 서버를 믿는다는 뜻이다. 신뢰할 서버만 `enabledMcpjsonServers`에 이름으로 적는 쪽이 더 안전하다.

## 3. 관리자 전용(Managed-Only) 설정

아래 키는 관리자(managed) 범위에서 조직이 거는 정책용이다. 사용자나 프로젝트가 바꾸지 못하게 막는 것이 목적이다.

| 키 | 타입 | 설명 |
|---|---|---|
| `strictKnownMarketplaces` | boolean | 승인된 마켓플레이스의 플러그인만 허용한다 |
| `allowManagedHooksOnly` | boolean | 사용자, 프로젝트, 플러그인 훅을 막고 관리자와 SDK 훅만 실행한다 |
| `allowManagedPermissionRulesOnly` | boolean | 사용자와 프로젝트 설정이 allow, ask, deny 권한 규칙을 정의하지 못하게 한다 |
| `disableAllHooks` | boolean | 모든 훅과 사용자 정의 상태 표시줄을 끈다 |
| `allowedMcpServers` | object[] | 사용자가 설정할 수 있는 MCP 서버의 허용 목록. 정의하지 않으면 제한이 없고, 빈 배열이면 전면 차단(lockdown)이다. 거부 목록이 우선한다 |
| `deniedMcpServers` | object[] | 모든 범위에서 명시적으로 막을 MCP 서버의 거부 목록 |

`allowedMcpServers`의 세 가지 상태를 구분해야 한다.

- 값을 정의하지 않으면 MCP 서버에 제한이 없다.
- 빈 배열 `[]`이면 아무 서버도 설정할 수 없는 전면 차단이다.
- 서버를 나열하면 그 목록 안의 서버만 설정할 수 있다.

어떤 경우든 `deniedMcpServers`에 있는 서버는 막힌다. 허용 목록과 거부 목록이 겹치면 거부가 이긴다.

## 4. 이 키들이 필요한 상황

관리자 전용 키는 보안 정책을 조직 전체에 강제하고 싶을 때 쓴다. `allowManagedHooksOnly`는 관리자와 SDK 훅만 돌게 하고, `allowManagedPermissionRulesOnly`는 사용자와 프로젝트 설정이 권한 규칙을 정하지 못하게 한다.

관리자 범위가 설정 우선순위에서 가장 높다는 점, 그리고 장치 관리 체계가 없는 조직을 위한 서버 관리 설정은 설정 범위 문서에서 설명한다.

<br>
<br>
<br>

[Claude Code The Definitive Guide to Agentic Development-2](../)
