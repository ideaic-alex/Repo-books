# 파이썬용 AGENTS.md 작성

Python 프로젝트에서 설정 하나만 고른다면 AGENTS.md가 가장 효과가 크다. 이 파일이 없으면 Codex CLI는 그럴듯하지만 틀린 선택을 한다. `uv add` 대신 `pip install`을 쓰고, `uv run pytest` 대신 `python -m pytest`를 돌리고, 프로젝트가 pyproject.toml을 쓰는데 `setup.cfg`나 `.flake8`을 만든다. 하나하나는 고치면 되지만 쌓이면 신뢰가 깎이고 환경이 서서히 어긋난다.

---

## 1. 루트 AGENTS.md가 답해야 할 네 가지

루트 AGENTS.md는 네 질문에 답해야 한다. 어떤 패키지 매니저를 쓰는가, 테스트 명령은 무엇인가, 린트와 포맷 명령은 무엇인가, 작업이 끝났다는 기준은 무엇인가. 다음은 Run or Relax용으로 쓴 예다.

```markdown
# AGENTS.md
## Environment
- Python package manager: uv, never use `pip` directly
- All tool invocations must go through `uv run`
- To add a dependency: `uv add <package>`; dev: `uv add --dev <package>`
- Python version: 3.14 (see `.python-version` or `pyproject.toml`)
## Testing
- Run tests: `uv run pytest tests/ -v`
- Run a single test file: `uv run pytest tests/test_foo.py -v`
- Run with coverage: `uv run pytest --cov=src --cov-report=term-missing`
- All new code must have pytest coverage, with no exceptions
```

```markdown
## Linting and formatting
- Lint: `uv run ruff check . --fix`
- Format: `uv run ruff format .`
- Type check: `uv run mypy src/` (stable default; `uv run ty check` once `ty` leaves beta)
- Run all checks before marking a task done: lint → format → type check → tests
## Commit conventions
- Conventional Commits: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`
- Do not commit `uv.lock` changes unless dependency versions were intentionally updated
```

여기 나온 uv, ruff, mypy, pytest는 이 책이 고른 예제 스택일 뿐 처방이 아니다. 핵심은 팀이 실제로 쓰는 도구에 이름을 붙여 에이전트가 짐작하지 않게 하는 것이다. poetry나 hatch, black, pyright, unittest로 바꿔도 파일의 모양은 똑같다. AGENTS.md는 환경과 기술 스택에 맞춰 달라지는 문서라는 것이 요점이고, 이 장이 위 스택을 쓰는 것은 우연이다.

## 2. "완료하기 전에"라는 문구

"before marking a task done"(작업을 끝났다고 표시하기 전에)이라는 구절이 중요하다. 이 구절이 없으면 에이전트는 프롬프트의 글자 그대로만 만족시키고, 동작을 확인하지 않은 채 멈춘다. 이 구절이 있으면 Codex CLI는 린트, 포맷, 타입 검사, 테스트를 "끝"의 정의로 받아들인다.

## 3. 설정 항목 참조표

| 항목 | 권장 값 | 왜 중요한가 |
|---|---|---|
| 패키지 매니저 | uv | uv.lock 기준으로 해석하고 설치해서 개발자와 CI 사이의 환경 어긋남을 없앤다 |
| 테스트 명령 | `uv run pytest tests/ -v` | uv가 관리하는 환경을 거치고, `-v`로 테스트 이름이 보여 진단이 쉽다 |
| 커버리지 명령 | `uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=90` | 하한선으로 커버리지 후퇴를 막고, term-missing으로 빠진 줄을 바로 보여 준다 |
| 린트 명령 | `uv run ruff check . --fix` | 자동 수정으로 기계적인 리뷰 지적을 없애고, `--fix`는 안전한 변환만 적용한다 |
| 포맷 명령 | `uv run ruff format .` | Black을 대체하며 결과가 결정적이고, 큰 코드베이스에서도 1초 안쪽이다 |
| 타입 검사 | `uv run mypy src/` (또는 `uv run ty check`) | mypy가 안정적인 기본값이며 완료 게이트가 돌리는 도구다. Astral의 Rust 기반 ty는 집필 시점에 베타다 |
| 완료 게이트 | 린트, 포맷, 타입 검사, 테스트 | 순서를 명시해 일부만 하고 끝내는 것을 막는다 |
| 커밋 스타일 | Conventional Commits | 변경 로그 자동 생성과 시맨틱 버저닝이 가능해진다 |

## 4. 서비스가 커질 때: 중첩 오버라이드

Run or Relax는 지금은 서비스 하나다. 만약 시드 데이터 대신 실제 지연 정보를 가져오는 별도 워커가 생긴다면, 루트 AGENTS.md는 공통 규칙을 유지하고 그 폴더 안의 중첩 파일이 달라지는 부분만 담는다. Codex CLI는 범위 순서대로 합치며 더 깊은 파일이 이긴다.

```markdown
# src/delay_feed/AGENTS.md
## Service-specific overrides
- This is a background worker, not an HTTP service: no route handlers here
- It writes `data/delays.json`; it must never reach into `src/departures/`
- Integration tests poll a stub feed: `uv run pytest tests/integration/ -m integration`
- Unit tests only: `uv run pytest tests/unit/`
```

중첩 파일에는 달라지는 점만 둔다. 도구 체인 전체를 파일마다 반복하면 루트 규칙이 바뀔 때 서로 어긋난다.

## 5. /init으로 내 파일 검증하기

Codex CLI에서 `/init`을 실행하면 실제 프로젝트 구조를 바탕으로 AGENTS.md 시작본이 만들어진다. 이것을 내가 쓴 파일과 diff로 비교해 보자. 생성본이 나와 다른 테스트 경로, 도구 설정, 디렉터리를 적어 놓았다면, Codex가 달리 추측했을 규칙을 하나 찾아낸 것이다. 세션 도중에 문제가 되기 전에 미리 잡을 수 있다.

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
