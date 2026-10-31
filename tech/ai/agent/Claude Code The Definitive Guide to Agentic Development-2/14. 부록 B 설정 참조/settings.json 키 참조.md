# settings.json 키 참조

settings.json은 Claude Code의 동작을 파일로 정해 두는 설정 파일이다. 이 문서는 부록 B에 나온 키를 기능별로 묶어서, 각 키가 무슨 일을 하는지와 타입, 기본값을 정리한다. 권한 규칙, 환경 변수, 모델, 인증, 세션 동작, 화면 표시, 파일 추천까지 다룬다.

샌드박스, 어트리뷰션, 플러그인, MCP 승인, 관리자 전용 키는 분량이 많아서 별도 문서로 나눴다. 키를 찾을 때는 이 문서에서 큰 범주를 확인하고 필요한 문서로 넘어가면 된다.

---

## 1. JSON 스키마로 자동완성 받기

settings.json 맨 위에 `$schema` 줄을 넣으면, JSON 스키마를 지원하는 에디터에서 자동완성과 실시간 검증을 받을 수 있다. 키 이름을 잘못 적었을 때 바로 표시해 주므로 설정 파일을 손으로 쓸 때 넣어 두는 편이 좋다.

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": { ... },
  "env": { ... }
}
```

## 2. 권한 규칙(permissions)

권한 규칙은 어떤 도구를 물어보지 않고 허용할지, 매번 물어볼지, 아예 막을지를 정한다.

| 키 | 타입 | 설명 |
|---|---|---|
| `permissions.allow` | string[] | 프롬프트 없이 자동 승인하는 도구 |
| `permissions.ask` | string[] | 사용자 확인이 필요한 도구 |
| `permissions.deny` | string[] | 항상 막는 도구 |

규칙은 `Tool` 또는 `Tool(specifier)` 형태로 쓰고, 글롭(glob) 패턴을 쓸 수 있다. 글롭은 `*` 같은 와일드카드로 여러 이름을 한꺼번에 가리키는 표기다.

평가 순서는 Deny, Ask, Allow 순이다. 모든 범위(scope)를 통틀어 가장 먼저 일치한 규칙이 적용된다. 그래서 어느 한 곳에서 deny로 막아 둔 것은 다른 곳에서 allow를 걸어도 열리지 않는다.

규칙 예시는 다음과 같다.

- `Bash(npm test)`: 특정 bash 명령 하나
- `Write(*.env)`: 파일 패턴
- `mcp__server__tool`: MCP 도구
- `Bash(git *)`: 와일드카드를 쓴 명령 묶음

## 3. 환경 변수와 훅, 모델

| 키 | 타입 | 설명 |
|---|---|---|
| `env` | object | Claude의 환경에 주입하는 키-값 쌍 |
| `hooks` | object | 이벤트와 핸들러를 연결하는 매핑 (훅 문서 참고) |
| `model` | string | 기본으로 쓸 모델 식별자 |
| `availableModels` | string[] | 선택할 수 있는 모델 목록 |

`env`는 settings.json 안에서 환경 변수를 정해 두는 방법이다. Claude Code 자체를 조절하는 환경 변수는 별도 문서에서 정리한다. `availableModels`는 사용자가 고를 수 있는 모델의 범위를 좁힐 때 쓴다.

## 4. 인증과 자격 증명

| 키 | 타입 | 설명 |
|---|---|---|
| `apiKeyHelper` | string | 인증 값을 만들어 내는 사용자 스크립트로, `/bin/sh`로 실행한다. 이 값은 모델 요청 때 `X-Api-Key`와 `Authorization: Bearer` 헤더로 보낸다 |
| `awsAuthRefresh` | string | AWS 자격 증명을 갱신하려고 `.aws` 디렉터리를 수정하는 스크립트 |
| `awsCredentialExport` | string | AWS 자격 증명을 JSON으로 출력하는 스크립트 |
| `forceLoginMethod` | string | 로그인 방식을 제한한다. `claudeai`(Claude.ai 계정) 또는 `console`(API 과금 계정) |
| `forceLoginOrgUUID` | string | 로그인 때 자동으로 고를 조직의 UUID. `forceLoginMethod`와 함께 써야 한다 |

`apiKeyHelper`는 키를 파일에 박아 두지 않고 스크립트가 그때그때 발급하게 하고 싶을 때 쓴다. 로그인 관련 두 키는 보통 조직이 계정 사용 방식을 통일하려고 관리자 범위에서 건다.

## 5. 세션과 동작

| 키 | 타입 | 설명 |
|---|---|---|
| `cleanupPeriodDays` | number | 이 기간보다 오래 활동이 없는 세션을 시작할 때 삭제한다. 기본값 30. 0이면 즉시 정리한다 |
| `language` | string | 응답에 쓸 언어. 예: `"japanese"`, `"spanish"`, `"french"` |
| `outputStyle` | string | 출력 스타일을 지정해 시스템 프롬프트를 조정한다 |
| `plansDirectory` | string | 플랜 파일을 저장할 위치. 프로젝트 루트 기준 상대 경로이며 기본값은 `~/.claude/plans` |
| `showTurnDuration` | boolean | "Cooked for 1m 6s" 같은 턴 소요 시간 메시지를 보여 줄지 정한다. 기본값 true |
| `teammateMode` | string | 에이전트 팀의 팀원을 어떻게 보여 줄지 정한다. `auto`(tmux나 iTerm2에서는 분할 창 선택), `in-process`, `tmux` |

세션 기록은 `cleanupPeriodDays` 기준으로 지워진다는 점을 기억해 두자. 오래된 세션을 다시 열어 쓸 일이 있다면 이 값을 늘려야 한다.

## 6. UI와 화면 표시

| 키 | 타입 | 설명 |
|---|---|---|
| `autoUpdatesChannel` | string | 릴리스 채널. `"stable"`은 약 일주일 지난 버전이라 회귀 버그를 피할 수 있고, `"latest"`는 가장 최신 버전이다. 기본값 `"latest"` |
| `spinnerTipsEnabled` | boolean | 작업 중 스피너에 팁을 보여 준다. 기본값 true |
| `spinnerVerbs` | object | 스피너 동사를 바꾼다. `mode`는 `"replace"`(내 동사만 사용) 또는 `"append"`(기본 동사와 섞기), `verbs`는 string[] |
| `terminalProgressBarEnabled` | boolean | Windows Terminal과 iTerm2에서 터미널 진행 막대를 켠다. 기본값 true |
| `prefersReducedMotion` | boolean | 스피너, 반짝임 같은 UI 애니메이션을 줄이거나 끈다. 접근성용 |

안정성이 중요한 팀이라면 `autoUpdatesChannel`을 `"stable"`로 두는 것이 한 가지 방법이다. 일주일 정도 늦게 받는 대신 막 나온 버전의 회귀를 피할 수 있다.

## 7. 파일 추천(File Suggestion)

`@`로 파일 경로를 자동완성할 때의 동작을 정하는 키들이다.

| 키 | 타입 | 설명 |
|---|---|---|
| `fileSuggestion` | object | 큰 모노레포에서 `@` 파일 경로 자동완성을 대신하는 사용자 스크립트 |
| `respectGitignore` | boolean | `@` 파일 선택기가 `.gitignore` 패턴을 따를지 정한다. 기본값 true |

`fileSuggestion` 스크립트는 stdin으로 `query` 필드가 든 JSON을 받는다. 그리고 stdout에 파일 경로를 줄바꿈으로 구분해 출력한다. 파일이 아주 많은 모노레포에서 기본 검색이 느리거나 원하는 결과를 못 줄 때, 직접 만든 검색 로직을 끼워 넣는 용도다.

<br>
<br>
<br>

[Claude Code The Definitive Guide to Agentic Development-2](../)
