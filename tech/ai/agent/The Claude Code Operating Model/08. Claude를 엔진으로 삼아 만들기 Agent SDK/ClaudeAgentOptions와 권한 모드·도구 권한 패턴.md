# ClaudeAgentOptions와 권한 모드·도구 권한 패턴

`ClaudeAgentOptions`는 Claude의 동작을 조절하는 핵심 설정 객체다. 헤드리스 CLI의 명령줄 매개변수를 프로그래밍 인터페이스로 바꾼 것이라, 값을 코드에서 동적으로 정할 수 있다. 사용자 역할에 따라 권한 모드를 바꾸거나 작업 종류에 따라 모델을 바꾸는 일이 가능해진다. 이름은 이전 버전의 `ClaudeCodeOptions`에서 바뀐 것이다.

이 문서는 옵션의 주요 항목을 묶어 살피고, 가장 중요한 보안 장치인 권한 모드와 도구 권한 패턴 문법을 다룬다.

---

## 1. 옵션 항목 한눈에 보기

원서의 구성 예제는 옵션을 주제별로 나눠 보여 준다.

| 묶음 | 항목 | 설명 |
|---|---|---|
| 모델·실행 제어 | `model` | 쓸 모델 버전(예: `claude-sonnet-4-6`) |
| | `max_turns` | 최대 상호작용 턴 수. 무한 루프 방지 |
| | `max_budget_usd` | 비용 상한. 소프트 한도라서 턴 사이에 검사하므로, 진행 중인 턴은 끝까지 간다 |
| 도구 권한 | `allowed_tools` | 허용 목록(화이트리스트). 열거한 도구만 쓴다 |
| | `disallowed_tools` | 금지 목록(블랙리스트). 보통 허용 목록보다 우선하거나 보완한다 |
| 권한 모드 | `permission_mode` | `default`, `acceptEdits`, `plan`, `bypassPermissions` |
| 프롬프트 | `system_prompt` | 직접 문자열을 주거나 프리셋에 덧붙인다 |
| 작업 환경 | `cwd`, `env` | 에이전트의 작업 디렉터리, 주입할 환경 변수 |
| 세션 | `resume` | 지정한 `session_id`의 맥락을 이어받는다 |
| 구조화 출력 | `output_format` | JSON Schema에 맞는 출력을 강제 |
| MCP 연동 | `mcp_servers` | 외부 MCP 서버를 동적으로 띄워 연결 |

주의할 점이 두 가지 있다. 첫째, `max_budget_usd`는 엄격한 차단이 아니라 "턴 사이에 확인하는 소프트 한도"다. 한 턴이 비싸게 끝날 수 있으므로 한도를 넉넉한 안전선으로 이해해야 한다. 둘째, `system_prompt`에는 `{"type": "preset", "preset": "claude_code", "append": "..."}` 형태가 있다. Claude Code의 기본 시스템 프롬프트를 그대로 쓰면서 뒤에 지시(원서 예: SQL 인젝션 취약점을 꼭 확인하라)를 덧붙이는 방식이다.

```python
options = ClaudeAgentOptions(
    model="claude-sonnet-4-6", max_turns=10, max_budget_usd=1.0,
    allowed_tools=["Read", "Grep", "Glob", "Write"],
    disallowed_tools=["Bash"], permission_mode="default",
    mcp_servers={"db": {"command": "python", "args": ["./db_server.py"]}},
)
```

참고(노트 작성자): 위는 원서 예제 중 일부 항목만 골라 한 덩어리로 줄인 것이다. 원서에서는 줄마다 주석이 달려 있고 `system_prompt`, `cwd`, `env`, `resume`, `output_format` 항목도 함께 나온다.

## 2. 권한 모드 자세히 보기

권한 모드는 Agent SDK 애플리케이션의 핵심 보안 방어선이다. 파일 쓰기나 명령 실행처럼 위험할 수 있는 작업을 만났을 때 Claude가 어떻게 행동할지를 정한다(원서 표 8.2).

| 모드 | 동작 | 적합한 상황 |
|---|---|---|
| `default` | 표준 상호작용. 파일 쓰기나 셸 실행 같은 위험 작업은 외부 확인(보통 콜백이나 사람의 개입)을 기다린다 | 사용자를 마주하는 웹 앱, 대화형 CLI 도구 |
| `acceptEdits` | 반자동. 파일 편집은 자동 수락하지만 Bash 실행, 네트워크 요청 등은 계속 확인을 요구한다 | 자동 수정 스크립트, 코드 포맷팅 파이프라인 |
| `plan` | 읽기 전용·계획 모드. 모든 수정 금지. 파일 읽기, 코드 분석, 계획 출력만 가능하고 쓰기와 명령 실행은 못 한다 | 코드 리뷰, 아키텍처 분석, 취약점 스캔 |
| `bypassPermissions` | 완전 신뢰. 모든 권한 검사를 건너뛰고 `rm -rf`, `curl` 같은 고위험 명령까지 자동 실행 | 엄격히 격리된 CI 컨테이너, 샌드박스 환경 |

### 2-1. bypassPermissions에 대한 Kage의 경고

CI/CD에서 `bypassPermissions`는 사람의 확인이 필요 없어 편해 보인다. 그러나 이는 Claude에게 파일 삭제, 설정 변경, 네트워크 요청 시작을 포함한 모든 명령 실행 권한을 주는 것이다. 실행 환경이 완전히 격리되어 있다고 확신할 때만 켜야 한다. 원서가 드는 격리 조건은 컨테이너 배포, 읽기 전용 파일 시스템, 네트워크 차단이다.

### 2-2. 모드를 고르는 기준

모드는 "위험 작업을 누가 승인하는가"로 고른다. 사람이 앞에 있으면 `default`, 편집만 믿어도 되면 `acceptEdits`, 아예 아무것도 바꾸면 안 되면 `plan`, 승인할 사람도 없고 환경 자체가 안전한 우리에 갇혀 있으면 `bypassPermissions`다. 이 장의 실습 서비스가 `plan`을 쓰는 이유도 분석만 하고 파일은 건드리지 않기 때문이다.

## 3. 도구 권한 패턴 매칭

`allowed_tools`는 헤드리스 CLI와 같은 패턴 매칭 문법을 지원한다. 도구 이름만 쓰면 그 도구 전체를 허용하고, 괄호 안에 패턴을 넣으면 인수까지 제한한다.

```python
allowed_tools=["Read", "Grep", "Glob",
    "Bash(git diff *)",       # git diff 명령만
    "Bash(npm test *)",       # npm test 명령만
    "mcp__database__query"]   # MCP database 서버의 query 도구만
```

세 가지 형태를 구분해 두자.

- 내장 도구: `Read`, `Grep`, `Glob`처럼 이름만 쓴다.
- 인수 제한: `Bash(git diff *)`처럼 Bash 전체를 열지 않고 특정 명령 모양만 허용한다. 최소 권한(필요한 만큼만 주는 원칙)을 실천하는 방법이다.
- MCP 도구: `mcp__서버이름__도구이름` 형식이다. 이 형식은 다음 문서의 사용자 정의 도구에서도 그대로 쓴다.

---

## 4. 핵심 정리

- `ClaudeAgentOptions`는 헤드리스 CLI 매개변수의 프로그래밍판이며, 값을 코드에서 동적으로 바꿀 수 있는 것이 장점이다.
- `max_turns`와 `max_budget_usd`로 폭주를 막되, 예산은 소프트 한도임을 기억한다.
- 권한 모드 네 가지는 기본 자세를 정하는 장치이며, 격리가 확인되지 않으면 `bypassPermissions`는 쓰지 않는다.
- `Bash(git diff *)` 같은 패턴으로 허용 범위를 명령 단위까지 좁힌다.

<br>
<br>
<br>

[The Claude Code Operating Model](../)
