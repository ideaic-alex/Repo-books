# AGENTS.md 로딩 실패 진단

AGENTS.md는 로딩에 실패해도 에러를 내지 않는다. 에이전트가 지침을 무시하는 것처럼 보일 때, 실제로는 파일이 아예 읽히지 않았거나, 읽혔지만 모델이 따르지 않은 것일 수 있다. 이 문서는 파일이 정말 로드됐는지 확인하는 방법과, 조용히 실패하는 대표적인 패턴을 정리한다.

---

## 1. RUST_LOG로 로딩 확인하기

```bash
RUST_LOG=info,codex_core=debug codex "your task here" 2>&1 | head -50
```

이렇게 실행하면 Codex가 찾아서 합친 지침 파일을 알려 주는 추적 출력이 나온다. 예를 들면 다음과 같은 줄이다.

```text
codex_core: agents_md: found /home/dan/.codex/AGENTS.md (global)
codex_core: agents_md: found /home/dan/projects/myapp/AGENTS.md (project)
codex_core: agents_md: loaded 2 file(s), combined length 847 bytes
```

전역 파일과 프로젝트 파일이 각각 발견되고, 합쳐서 몇 개 파일, 몇 바이트가 로드됐는지 확인할 수 있다. 기대한 파일이 목록에 없다면 경로, 파일 이름의 대소문자(Linux는 대소문자를 구분한다), 인코딩을 점검한다.

AGENTS.md가 로드되지 않아도 명시적인 에러는 나오지 않는다. 그래서 `RUST_LOG=codex_core=debug`처럼 모듈을 지정한 추적이 로딩을 확인하는 가장 믿을 만한 방법이다.

## 2. 조용히 실패하는 대표 패턴

| 패턴 | 설명과 대응 |
|---|---|
| 엉뚱한 디렉터리 | 하위 디렉터리에 AGENTS.md를 만들어 놓고 저장소 루트에서 실행하거나, 그 반대인 경우다. 어디서 실행하는지와 파일 위치를 맞춘다 |
| 인코딩 문제 | BOM 표식이나 섞인 줄바꿈 때문에 파싱이 조용히 실패한다. `file AGENTS.md`로 확인하고 `dos2unix AGENTS.md`로 고친다 |
| 모델의 기존 성향과 충돌하는 지침 | "코드에 주석을 달지 마라"처럼 이유 없는 금지는 잘 먹히지 않는다. "이 프로젝트는 자기 설명적인 변수 이름만을 유일한 문서화 수단으로 쓴다"처럼 이유를 덧붙인다 |
| 너무 깊이 묻힌 지침 | 위쪽에 있는 지침일수록 무게가 실린다. 핵심 지침은 맨 위로 올린다 |

앞의 두 가지(위치와 인코딩)는 파일이 아예 읽히지 않는 문제이고, 뒤의 두 가지는 읽혔는데 효과가 약한 문제다. 로그에 파일이 찍혔는데도 지침이 안 먹는다면 뒤쪽 두 가지를 의심한다.

## 3. 진단 순서

1. `RUST_LOG=codex_core=debug`로 실행해 `agents_md` 줄을 확인한다.
2. 파일이 목록에 없으면 경로와 이름 대소문자, 인코딩을 점검한다.
3. 목록에 있는데 따르지 않으면 지침의 위치(맨 위인지)와 이유를 적었는지 점검한다.

`codex doctor`도 AGENTS.md 파일 탐색을 점검 항목에 포함하므로, 세션 시작 전에 어떤 파일이 로드될지 먼저 볼 수 있다.

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
