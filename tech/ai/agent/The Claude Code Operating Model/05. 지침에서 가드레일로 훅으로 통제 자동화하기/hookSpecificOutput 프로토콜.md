# hookSpecificOutput 프로토콜

훅 스크립트가 Claude와 시스템에게 자기 판단을 전하는 방식, 곧 stdout으로 내보내는 JSON의 모양을 정리한다. 핵심은 hookSpecificOutput 객체 안에 이벤트 이름과 결정, 이유, 추가 컨텍스트를 담는 것이다. 이 약속을 알아야 뒤의 실습 스크립트가 왜 그렇게 생겼는지 읽힌다.

---

## 1. 새 형식과 옛 형식

PreToolUse 훅의 출력 형식은 2025년에 크게 바뀌었다. 이전 버전은 최상위에 decision과 reason 필드를 두었고, 새 버전은 hookSpecificOutput 객체 안에 중첩한 permissionDecision 형식을 권장한다. 지금은 두 형식이 모두 지원되지만 새 코드는 새 규격을 따라야 한다.

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "This command attempts to delete a protected system directory",
    "additionalContext": "Protected path patterns: /etc, /usr, /var"
  }
}
```

필드의 뜻은 다음과 같다.

| 필드 | 뜻 |
|---|---|
| hookEventName | 이 출력이 어느 이벤트에 대한 것인지(여기서는 PreToolUse) |
| permissionDecision | 허용 여부 결정. 값은 아래 네 가지 |
| permissionDecisionReason | 결정의 이유. 막을 때는 사용자와 Claude가 이유를 알 수 있게 반드시 구체적으로 쓴다 |
| additionalContext | Claude의 컨텍스트에 주입될 추가 정보 |

## 2. permissionDecision의 네 값

- **allow**: 권한 시스템을 건너뛰고 바로 실행한다.
- **deny**: 실행을 막는다.
- **ask**: 결정을 사용자에게 넘긴다.
- **defer**: 평소의 권한 흐름에 맡긴다.

이 중 ask는 미묘하지만 실용적이다. 자동으로 거절하지 않고 "나는 확신이 없으니 사람이 결정하라"는 태도를 전한다. 판정이 애매한 명령(예를 들어 패턴에 완전히 걸리지는 않으나 수상한 명령)에 알맞다. 참고(노트 작성자): 이 예는 원서에 없는 설명용 보충이다.

PreToolUse에서 입력을 다시 쓰고 싶다면 permissionDecision을 allow로 두고 hookSpecificOutput 아래에 updatedInput 객체를 함께 넣는다(1번 문서의 `--dry-run` 예). 이는 네 번째 결정값이 아니다.

## 3. additionalContext: 효율적인 피드백 순환

additionalContext 필드는 모든 이벤트 유형에 적용되며, 내용은 Claude의 컨텍스트에 주입된다. 이것이 효율적인 피드백 순환을 만든다. 예를 들어 PostToolUse 훅이 정적 분석(lint) 결과를 additionalContext로 되먹이면, Claude가 그 정보를 받고 문제를 스스로 고친다. 이 과정에 사람이 개입하지 않는다. 5번 문서의 lint 피드백 순환이 이 원리를 쓴다.

## 4. PermissionRequest 출력

PermissionRequest 이벤트는 권한 대화상자가 뜨려 할 때 발동하며, 출력은 `hookSpecificOutput` 아래 `hookEventName: "PermissionRequest"`와 `decision` 객체(`behavior`, `updatedPermissions`)로 구성된다. 원서 예시는 behavior를 "allow"로, updatedPermissions를 빈 객체로 둔다. 이것으로 사용자 확인이 필요한 요청을 프로그램으로 승인하거나 거부한다.

## 5. 모든 이벤트에 공통인 최상위 필드

모든 이벤트가 다음 공통 필드를 지원한다. 원서 예시는 줄바꿈이 깨져 있어 의미대로 복원했다.

```json
{
  "continue": false,
  "stopReason": "Security violation detected, session terminated",
  "suppressOutput": false,
  "systemMessage": "Warning: This operation has been blocked by the security policy"
}
```

- **continue: false**: "비상 브레이크"다. 현재 어느 이벤트 단계이든 Claude의 처리를 즉시 종료시킨다. stopReason에 종료 사유를 적는다.
- **systemMessage**: 이 필드의 내용은 사용자에게 바로 표시되며 Claude에게는 전달되지 않는다.
- suppressOutput: 원서는 예시에만 보이고 별도 설명은 없다(참고(노트 작성자): 이름으로 보아 출력 표시를 억제하는 용도로 짐작되나 원서는 설명하지 않는다).

## 6. 최상위 decision: block

Stop과 SubagentStop 훅은 최상위에 `"decision": "block"`과 `"reason"`을 돌려주어 종료를 막는다(5번 문서의 테스트 관문과 6번 문서의 SubagentStop 예). 이는 위의 옛 형식 필드와 같은 모양이다. 어떤 이벤트에서 어느 형식을 쓰는지 정리하면 다음과 같다. 이 표는 원서의 예시 코드를 근거로 노트 작성자가 정리한 것이다.

| 이벤트 | 원서 예시가 쓰는 출력 |
|---|---|
| PreToolUse | hookSpecificOutput.permissionDecision (deny, allow) |
| PostToolUse | hookSpecificOutput.additionalContext |
| Stop, SubagentStop | 최상위 decision: "block"과 reason |
| SubagentStart | hookSpecificOutput.additionalContext (hookEventName: SubagentStart) |

## 7. 종료 코드와 JSON의 관계

종료 코드 0이면 stdout JSON을 해석하고, 2면 stderr 내용이 차단 사유로 Claude에게 전달된다(2번 문서). 그래서 stdout은 JSON 결정 전용으로 비워 두고 디버그 문구는 stderr로 보내야 한다(7번 문서). 원서 보안 실습 스크립트는 차단 시 JSON을 출력한 뒤 exit 2로 끝내는데, 종료 코드 2의 설명대로라면 이때 전달되는 것은 stderr다. 스크립트가 같은 이유를 stderr에도 한 줄 남기는 것(`echo "BLOCKED: $pattern" >&2`)은 그 때문으로 이해된다. 참고(노트 작성자): exit 2일 때 stdout JSON을 시스템이 해석하는지는 원서가 명시하지 않으므로, 이유를 stderr에도 남기는 방식이 안전하다고 읽었다.

---

## 8. 핵심 정리

- 새 규격은 hookSpecificOutput 중첩 형식이고, 옛 최상위 decision/reason도 아직 지원되지만 새 코드는 새 규격을 쓴다.
- permissionDecision은 allow, deny, ask, defer. 입력 재작성은 updatedInput으로 별도 처리한다.
- additionalContext는 Claude의 컨텍스트로 들어가 lint 결과 같은 피드백 순환을 만든다.
- continue: false는 비상 브레이크이고, systemMessage는 사용자에게만 보인다.

<br>
<br>
<br>

[The Claude Code Operating Model](../)
