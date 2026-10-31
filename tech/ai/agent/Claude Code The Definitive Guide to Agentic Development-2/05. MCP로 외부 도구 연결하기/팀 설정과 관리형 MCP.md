# 팀 설정과 관리형 MCP

MCP 서버 설정은 한 사람이 고생해서 맞춰 두면 팀 전체가 혜택을 보는 종류의 일이다. 이 문서는 설정 파일을 어떻게 팀이 공유하는지, 비밀 값은 어디에 두는지, 조직이 허용할 서버를 어떻게 통제하는지를 설명한다. 기업 환경에서 새 팀원이 저장소를 받자마자 올바른 MCP 환경을 갖추면서도 정체불명의 서버는 붙지 못하게 하는 구성이 목표다.

---

## 1. .mcp.json으로 설정 모으기

MCP 서버는 프로젝트 루트의 `.mcp.json`에 설정한다. 이 파일은 버전 관리(git)에 커밋하는 것이 좋다. 한 사람이 MCP 설정을 알아내면 나머지 팀원은 저장소를 받는 것만으로 같은 설정을 얻는다.

```json
{
  "mcpServers": {
    "analytics": {
      "command": "node",
      "args": ["./mcp-servers/analytics/index.js"],
      "env": {
        "DB_CONNECTION": "${ANALYTICS_DB_URL}"
      }
    }
  }
}
```

### 비밀 값은 환경 변수로

위 예시의 `${ANALYTICS_DB_URL}`처럼 환경 변수 치환(interpolation)을 쓰면 자격 증명을 파일에 직접 적지 않고도 참조할 수 있다. `.mcp.json`에는 구조만 들어가고, 실제 비밀 값은 각 개발자의 환경에 둔다. 그래서 파일을 저장소에 커밋해도 비밀이 새지 않는다.

## 2. 관리형 MCP: 허용 목록과 차단 목록

기업은 관리형 설정(managed settings)으로 허용할 MCP 서버를 제한할 수 있다.

- **허용 목록**: 관리형 설정의 `allowedMcpServers`. 설정할 수 있는 서버를 이 목록에 있는 것으로만 제한한다.
- **차단 목록**: `deniedMcpServers`. 특정 서버를 막는다.

이 장치는 개발자가 임의의 외부 서비스를 Claude Code 세션에 연결하는 일을 막는다. 조직에 데이터 분류 정책이 있다면 의미 있는 통제 수단이다.

허용/차단은 설정 단계에서 작동한다. 어떤 서버가 허용 목록에 없다면, 프로젝트의 `.mcp.json`에 무엇이 적혀 있든 Claude Code는 그 서버에 연결하지 않는다. 이는 2장에서 설명한 권한 범위 계층과 같은 덮어쓰기 규칙이다. 관리형 설정이 이긴다.

## 3. 프로젝트 서버 승인 흐름을 정하는 설정 세 가지

프로젝트의 `.mcp.json`에 정의된 서버를 어떻게 승인할지는 사용자 수준 설정 세 가지로 정한다.

| 설정 키 | 역할 | 사용 시점 |
|---|---|---|
| `enableAllProjectMcpServers` | 프로젝트 `.mcp.json`의 모든 MCP 서버를 자동 승인 | 작업하는 저장소를 믿고 마찰을 없애고 싶을 때 `true` |
| `enabledMcpjsonServers` | 자동 승인할 서버 이름 목록. 예: `["memory", "github"]` | 일부 서버만 확인 없이 연결하고 싶을 때 |
| `disabledMcpjsonServers` | 거부할 서버 이름 목록. 예: `["filesystem"]` | 특정 서버를 절대 연결하지 않을 때 |

세부 동작은 다음과 같다.

- `enableAllProjectMcpServers`의 기본값은 `false`다. 이 경우 서버를 하나씩 직접 승인해야 한다.
- `enabledMcpjsonServers`에 없는 서버는 여전히 승인을 물어본다.
- `disabledMcpjsonServers`에 있는 서버는 프로젝트 `.mcp.json`이 정의하더라도 연결되지 않는다.

## 4. 조직에 배포하는 흐름

이 설정들은 조직 단위 배포에서 힘을 발휘한다. 팀은 프로젝트에 필요한 서버를 모두 담은 `.mcp.json`을 버전 관리에 커밋한다. 그리고 관리형 설정에서 그 서버들만 허용 목록에 넣고 나머지는 차단 목록에 둔다.

그러면 새 팀원은 저장소를 클론하는 것만으로 MCP 설정을 자동으로 받는다. 그리고 관리형 설정이 정체 모를 서버가 끼어드는 일을 막아 준다.

## 5. 정리

- `.mcp.json`은 프로젝트 루트에 두고 커밋한다.
- 자격 증명은 `${변수명}` 치환으로 참조하고, 값은 개발자 개별 환경에 둔다.
- 관리형 설정의 `allowedMcpServers`와 `deniedMcpServers`가 프로젝트 설정보다 우선한다.
- 프로젝트 서버 승인은 `enableAllProjectMcpServers`, `enabledMcpjsonServers`, `disabledMcpjsonServers` 세 가지로 조절한다.
- 팀 설정은 저장소가 전파하고, 조직 통제는 관리형 설정이 맡는 이중 구조로 운영한다.

<br>
<br>
<br>

[Claude Code The Definitive Guide to Agentic Development-2](../)
