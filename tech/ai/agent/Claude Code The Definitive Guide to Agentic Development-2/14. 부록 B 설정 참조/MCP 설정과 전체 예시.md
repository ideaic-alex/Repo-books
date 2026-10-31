# MCP 설정과 전체 예시

이 문서는 프로젝트 루트의 `.mcp.json` 형식, 관리자용 MCP 허용/거부 키, 플러그인 마켓플레이스 소스 표기법, 그리고 지금까지의 키를 한 파일에 모은 settings.json 전체 예시를 다룬다. MCP는 Claude Code에 외부 도구와 데이터를 연결하는 규격이다.

---

## 1. .mcp.json 형식

`.mcp.json`은 프로젝트 루트에 두고, `mcpServers` 아래에 서버를 이름별로 적는다. 서버는 내 컴퓨터에서 실행 파일로 띄우는 로컬 서버와, URL로 접속하는 원격 서버 두 가지로 쓴다.

```json
{
  "mcpServers": {
    "server-name": {
      "command": "node",
      "args": ["path/to/server.js"],
      "env": {
        "API_KEY": "${ENV_VAR_NAME}"
      },
      "cwd": "./optional-working-directory"
    },
```

이어서 원격 서버는 `url`과 `headers`로 적는다.

```json
    "remote-server": {
      "url": "https://mcp.example.com/sse",
      "headers": {
        "Authorization": "Bearer ${TOKEN}"
      }
    }
  }
}
```

비밀 값은 파일에 직접 쓰지 않고 `${ENV_VAR_NAME}`, `${TOKEN}`처럼 환경 변수를 끌어다 쓰는 방식이다. `.mcp.json`은 저장소에 커밋되는 파일이므로 이렇게 해야 키가 새지 않는다.

## 2. 서버 설정 필드

| 필드 | 타입 | 필수 | 설명 |
|---|---|---|---|
| `command` | string | 예 (로컬) | 실행할 파일 |
| `args` | string[] | 아니오 | 명령 인자 |
| `env` | object | 아니오 | 환경 변수. `${VAR}` 치환을 지원한다 |
| `cwd` | string | 아니오 | 서버 프로세스의 작업 디렉터리 |
| `url` | string | 예 (원격) | 원격 서버의 SSE 엔드포인트 |
| `headers` | object | 아니오 | 원격 연결에 쓸 HTTP 헤더 |

로컬 서버는 `command`가 필수이고, 원격 서버는 `url`이 필수다.

## 3. 관리자용 MCP 설정

| 키 | 타입 | 설명 |
|---|---|---|
| `mcpServers.allowlist` | string[] | 여기 있는 서버만 설정할 수 있다 |
| `mcpServers.denylist` | string[] | 여기 있는 서버는 막는다 |

앞의 관리자 전용 설정 문서에 나온 `allowedMcpServers`, `deniedMcpServers`도 허용/거부 목록이다. 원문은 두 표기의 관계를 따로 설명하지 않으므로, 실제로 쓸 때는 사용하는 버전의 공식 문서를 확인한다.

## 4. 플러그인 마켓플레이스 소스

플러그인을 어디서 가져올지 적는 표기법이다. `접두어:값` 형태다.

| 소스 종류 | 형식 |
|---|---|
| Git 호스팅 플랫폼 | `githost:org/repo` |
| Git URL | `git:https://example.com/repo.git` |
| npm | `npm:package-name` |
| URL | `url:https://example.com/plugin.tar.gz` |
| 파일 | `file:/path/to/plugin` |
| 디렉터리 | `directory:/path/to/plugin-dir` |
| 호스트 패턴 | `host:*.internal.company.com` |

호스트 패턴(`host:`)은 와일드카드로 도메인을 지정하는 표기다. 원문에는 이 표기의 용도 설명이 없다.

## 5. settings.json 전체 예시

앞에서 본 키를 한 파일에 모은 예시다. 길어서 세 덩어리로 나눈다. 첫 덩어리는 스키마, 권한, 환경 변수다. allow에는 테스트와 린트, git 명령과 읽기 도구를 두고, deny에는 `.env` 쓰기와 `secrets/` 읽기를 둔다.

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(npm test)",
      "Bash(npm run lint)",
      "Bash(git *)",
      "Read",
      "Glob",
      "Grep"
    ],
    "deny": ["Write(.env)", "Write(.env.*)", "Read(secrets/**)"]
  },
  "env": { "NODE_ENV": "development", "LOG_LEVEL": "info" },
```

두 번째 덩어리는 모델, 언어, 업데이트 채널, 표시 옵션, 샌드박스다.

```json
  "model": "claude-opus-4-6",
  "language": "english",
  "autoUpdatesChannel": "stable",
  "showTurnDuration": true,
  "spinnerVerbs": {
    "mode": "append",
    "verbs": ["Pondering", "Crafting"]
  },
```

이어서 샌드박스 설정이다.

```json
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker", "git"],
    "network": {
      "allowedDomains": ["registry.npmjs.org", "api.github.com"]
    }
  },
```

세 번째 덩어리는 어트리뷰션과 PreToolUse 훅이다(원문 예시를 이어 붙인 것이다). PR 문구는 "Generated with Claude Code"로 두고, Bash 도구가 실행되기 전에 `validate-bash.sh`를 돌린다.

```json
  "attribution": {
    "commit": "Generated with Claude Code\n\nCo-Authored-By: Claude <noreply@anthropic.com>",
    "pr": "Generated with Claude Code"
  },
```

마지막으로 훅 설정이다.

```json
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "handler": {
          "type": "command",
          "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/validate-bash.sh"
        }
      }
    ]
  }
}
```

이 예시는 한 파일에 권한, 환경, 모델, 표시, 샌드박스, 어트리뷰션, 훅을 모두 묶을 수 있다는 점을 보여 준다. 실제로는 범위 문서에서 설명한 기준대로 팀 공통 항목은 Project에, 개인 취향은 User에 나눠 두는 것이 좋다.

<br>
<br>
<br>

[Claude Code The Definitive Guide to Agentic Development-2](../)
