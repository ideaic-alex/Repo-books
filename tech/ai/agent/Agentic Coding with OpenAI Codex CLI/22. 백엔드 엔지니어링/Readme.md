# 백엔드 엔지니어링

앞 장들이 이미 있는 코드를 리뷰하고 옮기고 고치는 이야기였다면, 22장부터 24장까지는 아무것도 없는 상태에서 서비스를 만들어 운영까지 올린다. 22장은 그 첫 단계로 Python과 FastAPI로 백엔드 서비스와 API를 만든다. 예제는 Audley End에서 Liverpool Street로 가는 열차의 출발 안내판 Run or Relax이고, 지금 시각과 시간표를 보고 RUN(뛰어라)인지 relax(여유 부려도 된다)인지 판정한다.

이 장의 질문은 FastAPI 코드를 어떻게 짜느냐가 아니라, Codex CLI가 우리 팀의 방식대로 짜게 하려면 어떻게 설정하느냐이다. Python은 정적 타입 언어보다 에이전트가 받는 피드백이 약하므로, 장 대부분이 그 틈을 메우는 AGENTS.md, pyproject.toml, 훅 설정이다.

---

## 1. 핵심 요점

- Python은 타입 오류가 늦게 드러나고, 환경이 흘러가고, import 부수 효과가 숨고, 목이 쉽고, 비동기에 소리 없는 모서리가 있어 에이전트의 피드백 루프가 약하다. 이 장의 모든 레시피는 이 다섯 틈 중 하나를 막는다.
- AGENTS.md에 패키지 매니저, 테스트, 린트와 포맷, 완료 기준을 적고 모든 실행을 `uv run`으로 거치게 하면 "엉뚱한 도구" 실수 대부분이 사라진다.
- pytest는 픽스처 위치, 마커, 커버리지 하한을 말로 알려 줘야 한다. 생성된 테스트는 현재 동작을 베끼기만 할 수 있으므로 소스만큼 꼼꼼히 리뷰한다.
- 타입 힌트와 독스트링은 스타일을 정해 줘야 일관되게 나온다. 설명 없는 `Any` 금지와 Google 스타일 독스트링이 핵심이다.
- pyproject.toml이 uv, ruff, mypy, pytest 설정의 단일 기준이고, `.python-version`까지 적어 두면 에이전트가 짐작할 것이 없어진다.
- 훅 세 개(PostToolUse 린트, Stop 테스트 게이트, UserPromptSubmit 낡은 명령 차단)가 도구 규율을 에이전트의 기억에 기대지 않고 강제한다. Stop 훅은 JSON 출력 규칙 때문에 `>&2`와 `--no-sync`, `UV_CACHE_DIR` 처리가 필요하다.
- FastAPI와 비동기 규칙(async 핸들러, `Depends()`, `response_model`, 블로킹 I/O 금지)도 AGENTS.md에 적는다. CORS는 브라우저가 등장해야 드러나므로 프롬프트와 테스트로 미리 못 박는다.
- 판정 규칙(`WALK_MINUTES` 14, `RUN_MINUTES` 8)은 순수 함수로 두고 경계를 이름으로 드러내는 테스트로 고정한다. `GET /departures` 계약이 23장과 24장의 기반이 된다.

---

## 2. 문서 목록

- [만들 서비스 소개](%EB%A7%8C%EB%93%A4%20%EC%84%9C%EB%B9%84%EC%8A%A4%20%EC%86%8C%EA%B0%9C.md): Run or Relax의 목적, 판정 규칙의 두 경계, HTTP 계약, 프로젝트 구조, 응답 모델
- [파이썬이 에이전트에게 어려운 이유](%ED%8C%8C%EC%9D%B4%EC%8D%AC%EC%9D%B4%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%EC%97%90%EA%B2%8C%20%EC%96%B4%EB%A0%A4%EC%9A%B4%20%EC%9D%B4%EC%9C%A0.md): 피드백 루프를 약하게 만드는 다섯 가지 틈과 방어책
- [파이썬용 AGENTS.md 작성](%ED%8C%8C%EC%9D%B4%EC%8D%AC%EC%9A%A9%20AGENTS.md%20%EC%9E%91%EC%84%B1.md): 루트 AGENTS.md가 답할 네 가지, 설정 참조표, 중첩 오버라이드, /init 검증
- [pytest와 테스트 생성](pytest%EC%99%80%20%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EC%83%9D%EC%84%B1.md): 픽스처 찾기, 커버리지 기준, 마커, 테스트 자동 확장과 함정
- [타입 힌트와 독스트링 자동화](%ED%83%80%EC%9E%85%20%ED%9E%8C%ED%8A%B8%EC%99%80%20%EB%8F%85%EC%8A%A4%ED%8A%B8%EB%A7%81%20%EC%9E%90%EB%8F%99%ED%99%94.md): 타입 스타일 규칙, Any 금지, Google 스타일 독스트링과 D100
- [uv, ruff 도구 체인과 훅](uv%2C%20ruff%20%EB%8F%84%EA%B5%AC%20%EC%B2%B4%EC%9D%B8%EA%B3%BC%20%ED%9B%85.md): pyproject.toml 단일 기준, 설정 여섯 가지, 훅 세 개와 Stop 명령의 이유
- [FastAPI 규칙과 API 만들기](FastAPI%20%EA%B7%9C%EC%B9%99%EA%B3%BC%20API%20%EB%A7%8C%EB%93%A4%EA%B8%B0.md): FastAPI와 비동기 규칙, 프롬프트, CORS, 판정 함수와 로더, 시드 데이터, 실행
- [요약](%EC%9A%94%EC%95%BD.md): 22장 핵심 일곱 가지
- [연습 문제](%EC%97%B0%EC%8A%B5%20%EB%AC%B8%EC%A0%9C.md): 기준선 점검부터 API 만들기까지 다섯 가지 실습과 풀이 방향

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
