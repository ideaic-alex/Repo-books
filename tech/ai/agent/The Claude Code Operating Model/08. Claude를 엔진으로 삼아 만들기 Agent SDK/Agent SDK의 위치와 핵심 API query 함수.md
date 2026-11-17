# Agent SDK의 위치와 핵심 API query 함수

앞 장까지는 Claude Code를 "쓰는" 방법이었다. CLAUDE.md, 서브에이전트, 스킬(Skills, 재사용 가능한 작업 지침 묶음), 훅(Hooks, 도구 실행 전후에 끼어드는 자동 규칙), MCP 서버, 헤드리스 모드(터미널 없이 `claude -p`로 실행하는 방식)는 모두 이미 만들어진 틀 안에서 설정으로 동작을 넓히는 방법이다. 이 장의 Agent SDK는 출발점이 다르다. 개발자가 사용자가 아니라 애플리케이션을 만드는 사람이 되어, Claude Code의 핵심 능력을 자기 프로그램 안에 부품처럼 넣는다.

이 문서는 책의 도입 사례, Agent SDK가 놓이는 위치, 설치 방법, 그리고 SDK의 입구인 `query` 함수를 다룬다. 계산기에 비유하면 헤드리스 모드는 정해진 버튼만 누르는 "계산기 사용"이고, Agent SDK는 계산기의 동작 규칙을 직접 짜는 "계산기 프로그래밍"이다.

---

## 1. 도입 사례: 도구 사용에서 제품 만들기로

앞 장에서 샤오쉐가 Claude Code를 CI/CD 파이프라인에 붙여 PR 자동 리뷰와 보고서 생성을 해냈다. 팀 반응이 좋자 제품 매니저가 더 앞선 요구를 낸다. 비개발 동료가 사용자 스토리만 입력하면 시스템이 관련 코드 모듈을 찾고, 구현 난이도를 평가하고, 고쳐야 할 파일 목록을 뽑아 주는 사내 도구다.

헤드리스 모드로 일부는 해결되지만 본질이 명령줄 도구라서 터미널에 익숙하지 않은 제품 매니저에게는 문턱이 높다. 필요한 것은 입력 양식, 진행 상황 표시, 이력 추적이 있는 웹 화면이다. 즉 "도구를 쓰는 일"이 아니라 "제품을 만드는 일"이 된다. 팀의 조언자인 Kage의 정리가 이 장의 한 줄 요약이다. 헤드리스 모드는 매개변수로 Claude를 움직이고, Agent SDK는 코드로 Claude를 지휘한다.

## 2. Agent SDK의 위치: 설정에서 코드로

| 구분 | 지금까지(Claude Code 사용) | Agent SDK |
|---|---|---|
| 개발자의 역할 | 사용자. 정해진 틀 안에서 설정으로 확장 | 애플리케이션 제작자 |
| 제어 대상 | 설정 파일(CLAUDE.md, 훅 JSON 등) | 언제 Claude를 띄울지, 어떤 매개변수를 넘길지, 중간 단계를 어떻게 엮을지, 여러 턴의 상태를 어떻게 관리할지를 모두 코드로 |
| 결과물 | 더 잘 맞춘 Claude Code | Claude를 지능 엔진으로 삼은 새 애플리케이션 |

원서 그림 8.1은 CLAUDE.md에서 Agent SDK까지 이어지는 진화 경로를 보여 준다. 계층이 깊어질수록 제어 단위가 잘고 맞춤 정도가 높아진다. Agent SDK는 그 사슬의 끝에 있어서 유연성이 가장 크지만 엔지니어링 복잡도도 가장 높다. 이 점은 기억해 둘 만하다. 유연성과 복잡도는 같이 올라간다.

## 3. 제공 형태와 설치

Agent SDK는 Python판과 TypeScript/JavaScript판이 있고 기능은 동등하다. 2025년 말을 기준으로 패키지 이름이 `claude-code-sdk`에서 `claude-agent-sdk`로 공식 변경되었다. 위치를 더 정확히 드러내려는 개명이다. 같은 맥락에서 옵션 클래스 이름도 `ClaudeCodeOptions`에서 `ClaudeAgentOptions`로 바뀌었다.

```
pip install claude-agent-sdk
npm install @anthropic-ai/claude-agent-sdk
```

옛 이름으로 된 자료를 만나면 새 이름으로 바꿔 읽으면 된다.

## 4. 핵심 API: query 함수

SDK의 입구는 `query` 함수다. 헤드리스 모드의 입구가 `claude -p "prompt"`라면 `query`는 그것의 프로그램판이다. 차이는 반환 방식이다. 최종 결과 하나를 돌려주지 않고, 비동기 메시지 스트림(작업 중 생기는 메시지를 순서대로 흘려 보내는 통로)을 돌려준다.

### 4-1. 진입점은 두 가지

| 진입점 | 상태 | 쓰는 때 |
|---|---|---|
| `query()` | 무상태. 호출할 때마다 새 세션을 연다 | 일회성 작업. 이 장의 모든 예제 |
| `ClaudeSDKClient` | 상태 유지. 여러 번 주고받는 동안 세션을 쥐고 있다 | 3턴 전의 말도 기억해야 하는 프로세스 내 대화형 비서 |

둘 다 사용자 정의 도구와 훅을 지원한다. 차이는 능력이 아니라 세션이 사는 기간이다. 이 장의 예제는 각각 독립적이라 `query()`만 쓴다.

### 4-2. Python 예제의 구조

코드 분석 예제는 세 부분으로 이뤄진다. 먼저 `ClaudeAgentOptions`에 `max_turns=5`(최대 5턴), `allowed_tools=["Read", "Grep", "Glob"]`(읽기 계열 도구만 허용), `system_prompt`("코드 아키텍처 분석가")를 정한다. 다음에 `async for message in query(prompt=..., options=options)`로 스트림을 돈다. 마지막으로 메시지가 `AssistantMessage`이면 내용 블록 중 `text`가 있는 것을 바로 출력하고, `ResultMessage`이면 `total_cost_usd`로 총비용을 찍는다.

```python
async for message in query(prompt="Analyze src/auth/", options=options):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if hasattr(block, 'text'):
                print(block.text, end="", flush=True)
    elif isinstance(message, ResultMessage):
        print(f"Cost: ${message.total_cost_usd:.4f}")
```

참고(노트 작성자): 위 코드는 원서 예제를 줄여 옮긴 것이다. 원서 코드는 `AssistantMessage`와 `ResultMessage`를 import하는 줄이 빠져 있고, 프롬프트 문자열이 줄바꿈된 채 인쇄되어 있다. 추출본에서 따옴표와 들여쓰기가 일부 깨져 있어 문맥으로 복원했다.

### 4-3. TypeScript 예제의 차이

구조는 같고 문법과 이름 규칙이 다르다. 옵션 키가 `maxTurns`, `allowedTools`, `systemPrompt`처럼 카멜 케이스이고, 스트림은 `for await (const message of query({...}))`로 돈다. 메시지 종류는 클래스 검사 대신 `message.type === 'assistant'`, `'result'`로 가른다. 비용 필드는 `totalCostUsd`다. 두 언어 모두 필드 이름이 스네이크 케이스(Python)와 카멜 케이스(TypeScript)로 갈린다는 점만 주의하면 된다.

### 4-4. 비동기 제너레이터가 주는 이점

`query`는 비동기 제너레이터(결과를 하나씩 내어 주는 함수)다. Claude가 전체 작업을 끝낼 때까지 기다리지 않고, 메시지가 생길 때마다 즉시 넘겨준다. 효과는 두 가지다.

- 웹 애플리케이션에서는 Claude의 사고 과정을 프런트엔드로 흘려 보내 Claude.ai 같은 타자기 효과를 낼 수 있다.
- CI/CD에서는 Claude가 아직 실행 중이어도 이미 나온 출력을 처리하기 시작할 수 있다.

---

## 5. 핵심 정리

- Agent SDK는 Claude Code를 "쓰는" 단계에서 "내 앱의 부품으로 넣는" 단계로 넘어가는 도구다. 제어는 설정이 아니라 코드로 한다.
- 패키지는 `claude-agent-sdk`(Python)와 `@anthropic-ai/claude-agent-sdk`(TypeScript)이며, 옛 이름 `claude-code-sdk`, `ClaudeCodeOptions`는 개명 전 이름이다.
- `query()`는 무상태 비동기 스트림이고, 대화 기억이 필요하면 `ClaudeSDKClient`를 쓴다.
- 스트림 덕분에 실시간 화면 갱신이 가능하다. 한 번에 결과를 받는 헤드리스와의 가장 큰 차이다.

<br>
<br>
<br>

[The Claude Code Operating Model](../)
