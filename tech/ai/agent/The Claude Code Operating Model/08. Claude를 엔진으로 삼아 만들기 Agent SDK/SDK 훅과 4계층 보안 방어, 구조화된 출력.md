# SDK 훅과 4계층 보안 방어, 구조화된 출력

5장의 훅(Hooks)은 JSON 설정 파일로 정의했다. SDK에서는 같은 끼어들기 지점을 코드 안의 콜백 함수로 등록한다. 설정 파일을 오가는 수고가 사라진다. 이 문서는 SDK 훅(PreToolUse, PostToolUse), 셸 훅과의 비교, Agent SDK의 4계층 보안 방어, 그리고 출력 형식을 강제하는 구조화된 출력(Structured Output)을 다룬다.

---

## 1. SDK 훅의 사용 전제

원서가 먼저 밝히는 주의가 하나 있다. Python SDK에서는 `SessionStart`와 `SessionEnd`를 코드 콜백으로 등록할 수 없다. Python의 `HookEvent` 타입에 빠져 있어서, 설정 파일에 선언하는 셸 명령 훅으로만 쓸 수 있다. TypeScript에서는 SDK 콜백으로 등록할 수 있다. 이 문서의 예제가 쓰는 `PreToolUse`와 `PostToolUse`는 두 언어 모두에서 가능하다.

## 2. PreToolUse: 실행 전 차단

AI가 도구를 실제로 실행하기 전에 내용을 검사해 위험하면 즉시 거부하는 세밀한 런타임 보안 장치다. 훅 함수는 `(input_data, tool_use_id, context)`를 받고, 차단하려면 `hookSpecificOutput`에 `permissionDecision: "deny"`와 이유를 담아 돌려준다. 문제가 없으면 빈 딕셔너리 `{}`를 돌려준다.

원서의 두 훅은 이렇다.

| 훅 | 대상 도구 | 검사 내용 |
|---|---|---|
| `block_dangerous_bash` | Bash | 명령에 `rm -rf`, `sudo`, `chmod 777`, `> /dev/`, `mkfs`, `dd if=`가 들어 있으면 거부 |
| `protect_config_files` | Write, Edit | 경로에 `.env`, `secrets`, `production.yaml`, `database/migrations`가 들어 있으면 거부 |

등록은 `hooks={"PreToolUse": [HookMatcher(matcher="Bash", hooks=[block_dangerous_bash]), ...]}`로 하고, Write와 Edit는 각각 matcher를 따로 둔다.

```python
return {"hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": f"Blocked: {pattern}"}}
```

참고(노트 작성자): 문자열 포함 검사는 단순하다는 한계가 있어 우회 표기를 완전히 막지 못한다. 원서도 이를 최종 방어선이 아니라 4계층 중 한 겹으로 둔다.

## 3. PostToolUse: 실행 후 처리

도구가 실행된 뒤에 워크플로를 보강하고 전 과정을 감사한다. 원서는 두 가지를 보여 준다.

- `auto_format_on_write`: Write나 Edit 뒤에 파일 확장자를 보고 포맷터를 호출한다. `.py`는 Black, `.ts`, `.js`, `.tsx`, `.jsx`는 Prettier(`--write`)다.
- `audit_all_tools`: 모든 도구 호출을 JSONL 파일(`agent-audit.jsonl`)에 한 줄씩 덧붙인다. 항목은 시각, 도구 이름, 입력, `tool_use_id`다. matcher를 `"*"`로 두면 전부에 걸린다.

PreToolUse와 PostToolUse는 한 `hooks` 딕셔너리에 함께 등록한다. 원서 코드의 `audit_all_tools`는 `audit_entry` 변수를 만들고 `json.dumps(entry)`로 쓰는데 변수명이 일치하지 않는 오타로 보인다. 설명은 의도(`audit_entry`를 기록)에 맞춰 읽었다.

## 4. 셸 훅과 SDK 훅의 비교

원서 표 8.3의 요점이다.

| 항목 | 셸 훅 | SDK 훅 |
|---|---|---|
| 정의 | `settings.json` 설정 + 셸 스크립트 파일 | Python/TypeScript 함수 |
| 실행 환경 | 독립 하위 프로세스 | 현재 프로세스 안 |
| 데이터 교환 | stdin/stdout으로 JSON 문자열 | 함수 매개변수와 반환 객체 |
| 비동기 | 미지원(동기 블로킹) | `async/await` 네이티브 지원 |
| 디버깅 | 어려움(echo 출력이나 로그 파일에 의존) | 효율적(IDE 중단점, 단계별 실행) |
| 적합한 곳 | Claude Code 대화형, 헤드리스 CLI | SDK로 만든 내장 애플리케이션 |

선택 기준은 간단하다. Claude Code를 그대로 쓴다면 셸 훅, SDK로 맞춤 앱이나 서비스 연동, 복잡한 자동화 흐름을 만든다면 SDK 훅이다.

## 5. 4계층 보안 방어

Agent SDK는 네 겹의 심층 방어(defense in depth)를 둔다. 안쪽에서 바깥으로 보지 말고 "넓은 틀에서 좁은 검사 순서"로 보면 쉽다.

| 계층 | 하는 일 | 성격 |
|---|---|---|
| 1. `permission_mode` | 전체 기본 자세를 정한다 | 전역 기준선 |
| 2. `allowed_tools` | 존재할 도구 자체를 제한해 불필요한 도구를 없앤다 | 도구 범위 |
| 3. `canUseTool` 콜백 | 호출 때마다 인수 맥락을 보고 허용 여부를 정한다 | 호출별 문, SDK 고유 |
| 4. `PreToolUse` 훅 | 실행 직전의 마지막 결정적 검문. 가장 세밀한 인수 검사, 입력 보정, 감사 기록 | 최종 검문소 |

원서는 일반적인 애플리케이션에서는 허용 목록과 권한 모드가 방어의 대부분을 맡는다고 덧붙인다. 즉 네 겹이 모두 같은 무게는 아니다.

### 5-1. canUseTool의 철자

런타임 권한 콜백은 SDK 고유 기능이다. 매개변수 철자가 Python은 `can_use_tool`, TypeScript는 `canUseTool`이다. 원서 본문의 일반론은 TypeScript형으로 쓰지만 Python 예제는 `can_use_tool`을 등록한다. 직접 입력할 때는 설명이 아니라 코드를 따르라는 안내다.

### 5-2. 게이트키퍼 예제

원서의 `can_use_tool(tool_name, tool_input)`은 두 장면을 막는다. 하나는 Write와 Edit의 경로에 `.env`나 `secrets`가 들어간 경우를 `{"allowed": False, "reason": ...}`로 거부하는 것이다. 다른 하나는 Bash가 허용 목록에 있더라도 `curl`, `wget`, `ssh` 같은 네트워크 명령이 들어 있으면 거부하는 것이다. 문제가 없으면 `{"allowed": True}`를 돌려준다. 이를 `permission_mode="acceptEdits"`, 허용 도구 5종, `can_use_tool=can_use_tool`, PreToolUse 감사 훅과 한 옵션에 묶어 네 겹을 모두 세운다.

## 6. 구조화된 출력

앱을 만들 때는 자유 서술 대신 구조화된 데이터가 필요한 경우가 많다. `output_format={"type": "json_schema", "schema": ...}`를 주면 Claude가 JSON Schema에 맞는 출력을 낸다.

| 구분 | Python | TypeScript |
|---|---|---|
| 스키마 정의 | Pydantic `BaseModel` + `model_json_schema()` | Zod `z.object(...)` + `z.toJSONSchema()` |
| 옵션 키 | `output_format` | `outputFormat` |
| 결과 위치 | `ResultMessage.structured_output` | 동일 개념 |

원서의 `SecurityReport` 모델은 `summary`(문자열), `issues`(딕셔너리 목록: severity, file, line, description 구조), `risk_score`(0.0~10.0 실수)를 가진다. 결과가 오면 `SecurityReport.model_validate(message.structured_output)`로 검증된 객체를 얻어 타입 안전하게 쓴다. TypeScript 예제는 `severity`를 `critical`, `high`, `medium`, `low`로 고정하는 enum으로, `riskScore`를 0~10 숫자로 제한한다.

초기 출력이 검증에 실패하면 SDK가 자동으로 재시도한다. 최대 재시도 횟수는 내부 정책이 정하며 원서가 수치를 밝히지 않는다. 한도를 넘겨도 실패하면 `error_max_structured_output_retries` 오류가 돌아온다.

---

## 7. 핵심 정리

- SDK 훅은 설정 파일 대신 코드 콜백이며, Python의 SessionStart/SessionEnd는 콜백이 불가해 설정 파일 셸 훅으로만 쓴다.
- PreToolUse는 `permissionDecision: "deny"`로 실행 전에 막고, PostToolUse는 포맷팅과 감사 로그에 쓴다.
- 4계층은 permission_mode, allowed_tools, canUseTool, PreToolUse 훅 순이며 현실에서는 앞의 둘이 무게를 많이 진다.
- 구조화된 출력은 JSON Schema를 강제하고, 실패하면 자동 재시도 후 전용 오류를 낸다.

<br>
<br>
<br>

[The Claude Code Operating Model](../)
