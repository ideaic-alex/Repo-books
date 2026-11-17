# 실습 코드 분석 웹 서비스와 SDK 대 헤드리스 CLI 선택

지금까지 배운 query, 옵션, 메시지 처리를 한데 합친 코드 분석 서비스 실습이다. 명령줄로 시뮬레이션하는 스크립트에서 시작해 FastAPI 기반 SSE(Server-Sent Events, 서버가 클라이언트로 데이터를 계속 밀어 보내는 방식) 스트리밍 서비스로 확장한다. 이어서 Agent SDK와 헤드리스 CLI 중 무엇을 고를지 판단 기준을 정리한다.

---

## 1. 코드 분석 에이전트 서비스

함수 `analyze_codebase(directory, focus="general")`는 지정한 디렉터리의 코드를 분석한다. `focus`는 `security`, `performance`, `quality`, `general` 중 하나다.

### 1-1. 초점별 시스템 프롬프트

| focus | 지시 내용 |
|---|---|
| security | SQL 인젝션, XSS, 하드코딩된 민감 정보, 접근 제어 부재 등 |
| performance | N+1 쿼리, 메모리 누수, 중복 계산, 캐싱 전략 부재 등 |
| quality | 이름 짓기, 중복, 테스트 커버리지. 린터가 이미 강제하는 것은 건너뜀 |
| general | 보안, 성능, 코드 품질, 아키텍처 건전성을 아우른 종합 리뷰 |

### 1-2. 옵션 구성

옵션은 앞에서 배운 안전 설정이 그대로 모여 있다. 이것이 이 실습의 가장 중요한 학습 포인트다.

- `model="claude-sonnet-4-6"`, `max_turns=15`, `max_budget_usd=0.50`: 턴과 비용 상한
- `allowed_tools=["Read", "Grep", "Glob"]`와 `permission_mode="plan"`: 읽기 전용이라 분석만 한다
- `cwd=directory`: 대상 디렉터리에서 작업
- `system_prompt`: `claude_code` 프리셋에 초점별 지시를 `append`

```python
options = ClaudeAgentOptions(model="claude-sonnet-4-6", max_turns=15,
    max_budget_usd=0.50, allowed_tools=["Read", "Grep", "Glob"],
    permission_mode="plan", cwd=directory,
    system_prompt={"type": "preset", "preset": "claude_code", "append": focus_prompt})
```

### 1-3. 스트리밍과 결과 수집

스트림을 돌며 assistant의 텍스트 블록은 `output_text`에 모으고 바로 출력한다(원서 주석: 실제 웹 서비스에서는 여기서 SSE 이벤트를 `yield`한다). 도구 호출은 `tools_used`에 이름을 담는다. `ResultMessage`에서는 `session_id`, `cost_usd`, `turns`, `duration_ms`, `success`(오류가 아니면 참)를 `metadata`로 만든다. 반환은 `report`(텍스트를 줄바꿈으로 이은 것), `tools_used`, `metadata`다.

`main()`은 명령줄 인수로 디렉터리와 초점을 받아(기본 `.`과 `general`) 분석을 돌린 뒤 상태, 비용, 소요 시간, 턴 수, 사용한 도구를 출력한다. 원서 주석은 실제 도구라면 디렉터리 경로를 해석하고 존재 여부를 확인해야 한다고 지적한다.

참고(노트 작성자): 원서 코드에는 알아볼 만한 오류가 여럿 있다. 스트림 처리의 `if` 블록 들여쓰기가 한 단계 어긋나 있고(추출 문제일 수 있다), `main()`에서 정의되지 않은 변수 `meta`를 쓰며, 같은 함수의 다른 줄은 `result['metadata']`를 쓴다. 의도는 `result['metadata']`로 읽는 것이다. 또 `print` 줄의 f-string이 줄바꿈으로 끊겨 있다. 실습 때 그대로 복사하지 말고 이 점들을 바로잡아야 한다.

## 2. FastAPI와 SSE로 확장하기

실제 웹 서비스에서는 쿼리의 비동기 제너레이터를 SSE에 바로 연결해 지연이 적은 실시간 푸시를 한다. 원서가 강조하는 것은 코드 형태다. 요청을 처리하는 비동기 핸들러가 에이전트의 메시지 스트림을 돌면서 조각이 도착할 때마다 클라이언트로 전달한다. 실행이 끝날 때까지 기다리지 않으므로 프런트엔드는 빈 로딩 화면 대신 작업이 진행되는 모습을 그대로 그린다.

```python
@app.post("/api/analyze")
async def analyze(request: AnalyzeRequest):
    async def event_stream():
        async for message in query(prompt=request.prompt, options=options):
            ...  # text 블록은 data: {"type":"text",...}, 결과는 {"type":"done","cost":...}
    return StreamingResponse(event_stream(), media_type="text/event-stream")
```

SSE 한 건은 `data: {JSON}` 뒤에 빈 줄이 오는 형식이다. 텍스트 블록마다 `type: text`, 마지막 `ResultMessage`에서는 `type: done`과 비용을 보낸다. 원서 코드의 f-string이 줄바꿈으로 끊겨 있어 위에는 줄임표로 요약했다. `AnalyzeRequest`의 정의는 원서에도 나오지 않는다.

이 서비스가 처음 도입 사례의 해답이다. 제품 매니저는 터미널 없이 웹 양식으로 요청을 보내고, 진행 상황을 실시간으로 보며, 비용과 소요 시간 같은 메타데이터를 이력에 남길 수 있다.

## 3. Agent SDK와 헤드리스 CLI, 무엇을 고를까

둘 다 Claude를 사람 없이 돌릴 수 있지만 적합한 장면이 갈린다. 잘못 고르면 구조가 쓸데없이 복잡해지거나 기능이 모자라게 된다(원서 표 8.4).

| 상황 | 추천 | 이유 |
|---|---|---|
| CI/CD의 단일 단계 작업 | 헤드리스 CLI | 의존성 없는 배포, YAML에 바로 삽입, Python/Node 런타임 설치 불필요 |
| 셸 스크립트 자동화 | 헤드리스 CLI | 파이프라인 조합에 딱 맞고 단순 |
| 웹/데스크톱 AI 앱 | Agent SDK | 스트리밍(SSE), 세밀한 상태 관리, 프런트엔드 연동 |
| 사용자 정의 도구가 필요 | Agent SDK | `@tool`로 로컬 함수를 등록해 복잡한 업무 로직 순환 |
| 다중 턴 대화·연속 세션 | Agent SDK | 세션 관리 내장, 메시지를 수동으로 이어 붙일 필요 없음 |
| 메시지 흐름의 세밀한 제어 | Agent SDK | 비동기 제너레이터로 조각 단위로 가로채기, 수정, 라우팅 |
| 인스턴스 동시 다수 관리 | Agent SDK | `asyncio.gather` 같은 프로그램 방식 동시성 제어 |

경험칙은 이렇다. 로직이 셸 명령 한두 줄에 들어가면 CLI를 쓴다. 복잡한 분기, 반복, 일괄 데이터 처리, 다른 실행 코드와의 긴밀한 결합이 필요해지면 Agent SDK를 쓴다. 그 지점부터는 셸에 머무는 비용이 얻는 이익보다 커진다. 단서도 있다. 셸이 사람들이 생각하는 것보다 더 많은 일을 해낸다는 점이다.

## 4. 프로덕션 전환 시 챙길 문제 (Kage's notes)

SDK는 AI 앱 제작의 문턱을 낮추지만 "쉽다"가 "단순하다"는 뜻은 아니다. 데모를 프로덕션급으로 올리려면 다섯 가지를 풀어야 한다.

| 과제 | 내용 |
|---|---|
| 오류 재시도 | 네트워크 변동과 API 속도 제한 대응 |
| 비용 추적 | 호출마다 토큰 소비를 모니터링 |
| 사용자 격리 | 서로 다른 사용자의 대화가 섞이지 않게 함 |
| 응답 타임아웃 | 오래 걸리는 작업의 중단 전략 |
| 서킷 브레이커 | 연속 실패 뒤 호출을 자동 중단 |

원서 문장이 서킷 브레이커 설명 중간에서 쪽이 넘어가며 끊겨 있으나, 앞뒤 문맥으로 "연속 실패 후 호출을 자동으로 멈추는 장치"로 복원했다.

---

## 5. 핵심 정리

- 실습 서비스는 `plan` 모드, 읽기 도구 3종, 턴·비용 상한이라는 보수적 설정으로 안전하게 분석만 한다.
- 비동기 제너레이터를 SSE에 연결하면 웹에서 실시간 진행을 보여 줄 수 있다.
- 단일 단계 CI 작업과 셸 스크립트는 헤드리스 CLI, 앱·도구·세션·동시성이 필요하면 Agent SDK다.
- 프로덕션에는 재시도, 비용 추적, 사용자 격리, 타임아웃, 서킷 브레이커가 필수다.

<br>
<br>
<br>

[The Claude Code Operating Model](../)
