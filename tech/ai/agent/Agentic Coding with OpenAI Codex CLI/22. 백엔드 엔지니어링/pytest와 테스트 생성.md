# pytest와 테스트 생성

pytest는 사실상 Python의 표준 테스트 러너다. 그런데 픽스처가 어디 있는지, 마커가 어떻게 쓰이는지 듣지 못한 에이전트에게는 관례가 뻔하지 않다. 이런 세부를 AGENTS.md에 적어 두느냐에 따라, 문법만 맞고 쓸모없는 테스트를 만드는 작성자가 되기도 하고 기존 테스트 묶음에 자연스럽게 끼는 작성자가 되기도 한다.

---

## 1. 픽스처 찾기

가장 흔한 실수는 Codex CLI가 `conftest.py`에 이미 있는 픽스처를 또 만드는 것이다. 지시 한 덩어리로 막을 수 있다.

```markdown
## pytest conventions
- Shared fixtures are in `tests/conftest.py`: check there before creating new ones
- The `timetable` fixture loads the seeded JSON; reuse it instead of reading files
  or calling the clock inside a test
- Per-service fixtures live in `tests/<service>/conftest.py`
- Use pytest-asyncio with `asyncio_mode = "auto"`: no manual `@pytest.mark.asyncio`
- HTTP client fixtures use `httpx.AsyncClient` with ASGI transport, not `requests`
```

FastAPI 같은 비동기 프레임워크를 쓰는 팀은 보통 pyproject.toml에 이렇게 설정한다.

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
addopts = "--tb=short -q"
```

AGENTS.md에 이 메모가 없으면 Codex CLI는 모든 비동기 테스트에 `@pytest.mark.asyncio`를 붙인다. diff만 보면 맞는 코드 같지만 프로젝트 관례를 어긴 것이다.

## 2. 커버리지 기준과 테스트 마커

커버리지 하한과 테스트 종류를 명시한다.

```markdown
## Coverage
- Minimum coverage: 90% overall, 100% for `src/departures/verdict.py`
- Do not add `# pragma: no cover` without a comment explaining why
## Test markers
- @pytest.mark.unit: no I/O, runs in CI on every push
- @pytest.mark.integration: requires Docker services, runs in CI on PR only
- @pytest.mark.slow: long-running; skip locally with `-m "not slow"`
- Default local command: `uv run pytest -m "unit" -q`
```

판정 규칙 파일 `verdict.py`는 절대 후퇴하면 안 되는 규칙이라 100%로 못 박았다. 이렇게 적어 두면 Codex CLI가 새 테스트 파일을 만들 때 알맞은 마커를 붙인다. 통합 테스트가 실수로 unit 마커를 달면 푸시할 때마다 데이터베이스 호출이 끼어들어, CI에 대한 신뢰를 갉아먹는 느리고 불안정한 실패가 생긴다.

## 3. 테스트 자동 확장

Codex CLI가 pytest에서 가장 믿을 만하게 기여하는 일은 기존 코드의 커버리지를 늘리는 것이다. 예를 들어 이런 프롬프트가 있다. "src/departures/timetable.py의 공개 함수 중 커버리지가 없는 것마다 프로젝트의 timetable 픽스처를 써서 pytest 테스트를 추가해 줘." AGENTS.md가 정확하면 결과가 좋다. 에이전트가 `tests/conftest.py`에서 픽스처를 읽고, `pyproject.toml`에서 마커 정의를 확인하고, 기존 구조에 맞게 테스트를 만든다.

## 4. 대량 생성의 함정

대량으로 만든 테스트는 바로 통과하지만 엉뚱한 것을 검증하는 경우가 있다. 동작이 올바른지가 아니라 지금 동작이 재현되는지를 확인하는 테스트다. 생성된 테스트도 생성된 소스 코드만큼 꼼꼼히 리뷰해야 한다. 이를테면 `None`이 버그인 상황에서 `result == None`을 단언하는 테스트는, 테스트가 없는 것보다 나쁘다.

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
