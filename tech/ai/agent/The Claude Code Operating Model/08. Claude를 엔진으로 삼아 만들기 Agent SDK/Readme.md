# Claude를 엔진으로 삼아 만들기 Agent SDK

이 장은 Claude Code를 쓰는 사람에서 Claude를 부품으로 넣어 제품을 만드는 사람으로 넘어가는 길을 다룬다. 먼저 Agent SDK가 헤드리스 모드와 어떻게 다른지, 입구인 `query` 함수가 어떤 메시지 스트림을 돌려주는지 본다. 이어서 `ClaudeAgentOptions`의 권한 모드와 도구 권한 패턴, 세션 이어 가기와 사용자 정의 도구, 훅과 4계층 보안 방어, 구조화된 출력을 익힌다.

마지막으로 코드 분석 웹 서비스 실습과 SDK 대 헤드리스 CLI 선택 기준을 정리한다. 원서의 코드에는 인쇄 오류가 있어 본문에서 그 부분을 밝혔다.

---

## 1. 핵심 요점

- Agent SDK는 설정이 아니라 코드로 Claude를 제어한다. 유연성이 가장 크지만 엔지니어링 복잡도도 가장 높다.
- `query()`는 무상태 비동기 스트림이고, 맥락을 유지하는 대화에는 `ClaudeSDKClient`를 쓴다. 패키지 이름은 `claude-agent-sdk`다.
- 메시지는 system/init, assistant, user, result 네 종류이며 result의 `subtype`으로 성공, 턴 초과, 예산 초과, 실행 오류, 구조화 출력 실패를 가른다.
- 권한 모드는 default, acceptEdits, plan, bypassPermissions 네 가지이고, `Bash(git diff *)` 같은 패턴으로 도구 허용 범위를 좁힌다.
- `resume`은 세션 맥락을 잇고 `fork_session=True`는 원본을 보존한 채 갈라 쓴다.
- 사용자 정의 도구는 프로세스 내 MCP 서버이며 이름은 `mcp__{server_name}__{tool_name}` 형식이다.
- 4계층 보안은 permission_mode, allowed_tools, canUseTool, PreToolUse 훅이다.
- 단일 단계 CI와 셸 자동화는 헤드리스 CLI, 앱과 도구와 세션과 동시성은 Agent SDK가 맞다.

---

## 2. 문서 목록

- [Agent SDK의 위치와 핵심 API query 함수](Agent SDK의 위치와 핵심 API query 함수.md): 도입 사례, 설정에서 코드로의 전환, 설치, query와 ClaudeSDKClient
- [메시지 유형 해석](메시지 유형 해석.md): system/init, assistant, user, result와 subtype 표, 메시지 처리 패턴
- [ClaudeAgentOptions와 권한 모드·도구 권한 패턴](ClaudeAgentOptions와 권한 모드·도구 권한 패턴.md): 옵션 항목, 네 가지 권한 모드, 도구 패턴 매칭
- [세션 관리와 사용자 정의 도구](세션 관리와 사용자 정의 도구.md): resume과 fork, @tool, Pydantic 검증, 설계 원칙
- [SDK 훅과 4계층 보안 방어, 구조화된 출력](SDK 훅과 4계층 보안 방어, 구조화된 출력.md): PreToolUse, PostToolUse, 셸 훅 비교, canUseTool, JSON Schema
- [실습 코드 분석 웹 서비스와 SDK 대 헤드리스 CLI 선택](실습 코드 분석 웹 서비스와 SDK 대 헤드리스 CLI 선택.md): 분석 서비스, FastAPI와 SSE, 선택 표, 프로덕션 과제
- [요약과 핵심 개념](요약과 핵심 개념.md): 장 전체 흐름, 핵심 개념 표, 자주 놓치는 점, 생각해 볼 질문

<br>
<br>
<br>

[The Claude Code Operating Model](../)
