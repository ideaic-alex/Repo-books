# 에이전트 실패 진단과 디버깅

설정을 제대로 해 두어도 에이전트는 틀린 결과를 내거나, 루프에 빠지거나, AGENTS.md를 조용히 무시하거나, 일을 끝내기도 전에 컨텍스트 윈도를 다 써 버린다. 5장에서 신뢰 모델(승인 모드, 샌드박스, 권한 단계)을 세웠지만, 이 장은 그럼에도 문제가 터졌을 때 어떻게 복구할지를 다룬다.

세션 기록을 거꾸로 읽어 어긋난 지점을 찾는 법부터, `codex doctor`, `codex sandbox`, `codex execpolicy check`, `codex debug models` 같은 오프라인 진단, `RUST_LOG` 추적, 컨텍스트 과부하와 명세 이탈 대응, 3단계 관측 스택까지 정리한다. 마지막에는 싼 점검부터 하는 진단 체크리스트로 묶는다.

---

## 1. 핵심 요점

- 세션 기록(`~/.codex/sessions/`의 JSONL)을 끝에서부터 거꾸로 읽으면 어긋난 지점을 찾을 수 있고, `jq`로 실패와 승인 결정을 뽑는다.
- `-a untrusted -s read-only`는 에이전트가 아무것도 실행하지 않은 채 계획만 보여 주는 점검 모드이고, `/status`, `/debug-config`, `/feedback`은 TUI 안에서 바로 쓰는 진단 도구다.
- AGENTS.md는 실패해도 에러가 없으므로 `RUST_LOG=codex_core=debug` 추적으로 로딩을 확인하고, 위치, 인코딩, 지침 위치를 점검한다.
- `codex doctor`, `codex sandbox`, `codex execpolicy check`, `codex debug models`는 세션을 띄우지 않고 설정, 샌드박스, 규칙, 모델 문제를 가려낸다.
- 컨텍스트가 70~80%에 이르면 `/compact`로 압축하거나 새 세션을 시작하고, 폭주 세션은 Ctrl-C를 한 번만 눌러 멈춘 뒤 `git stash`로 복구한다.
- 출력이 원래 명세에서 서서히 벗어나는 명세 이탈은 SLUMP 점검으로 찾고, 명세를 다시 붙이거나 `/goal`로 재고정한다.
- 관측은 로컬 롤아웃, OpenAI Platform Traces, OTLP 외부 내보내기의 3단계로 나뉘며 서로 보완한다.
- 체크리스트는 설정, 인증, 샌드박스, 규칙, 모델, 추적, 롤아웃, 피드백 순으로 싼 것부터 한다.

---

## 2. 문서 목록

- [세션 기록으로 원인 찾기](%EC%84%B8%EC%85%98%20%EA%B8%B0%EB%A1%9D%EC%9C%BC%EB%A1%9C%20%EC%9B%90%EC%9D%B8%20%EC%B0%BE%EA%B8%B0.md): 롤아웃 JSONL 읽는 법, 진단용 승인 모드, `/status`, `/debug-config`, `/feedback`
- [세션 전 점검 codex doctor와 인증](%EC%84%B8%EC%85%98%20%EC%A0%84%20%EC%A0%90%EA%B2%80%20codex%20doctor%EC%99%80%20%EC%9D%B8%EC%A6%9D.md): 세션 시작 전 진단과 인증 실패 분리
- [AGENTS.md 로딩 실패 진단](AGENTS.md%20%EB%A1%9C%EB%94%A9%20%EC%8B%A4%ED%8C%A8%20%EC%A7%84%EB%8B%A8.md): 로딩 확인 방법과 조용히 실패하는 패턴
- [샌드박스와 실행 정책 오프라인 검증](%EC%83%8C%EB%93%9C%EB%B0%95%EC%8A%A4%EC%99%80%20%EC%8B%A4%ED%96%89%20%EC%A0%95%EC%B1%85%20%EC%98%A4%ED%94%84%EB%9D%BC%EC%9D%B8%20%EA%B2%80%EC%A6%9D.md): `codex sandbox`, `.rules`, `codex execpolicy check`
- [컨텍스트 과부하와 폭주 세션 복구](%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%20%EA%B3%BC%EB%B6%80%ED%95%98%EC%99%80%20%ED%8F%AD%EC%A3%BC%20%EC%84%B8%EC%85%98%20%EB%B3%B5%EA%B5%AC.md): 과부하 증상, 중단과 롤백, SLUMP 명세 이탈 점검
- [RUST_LOG 추적과 codex debug](RUST_LOG%20%EC%B6%94%EC%A0%81%EA%B3%BC%20codex%20debug.md): 모듈별 로그, JSON 로그, `codex debug models`
- [3단계 관측 스택과 트레이스 활용](3%EB%8B%A8%EA%B3%84%20%EA%B4%80%EC%B8%A1%20%EC%8A%A4%ED%83%9D%EA%B3%BC%20%ED%8A%B8%EB%A0%88%EC%9D%B4%EC%8A%A4%20%ED%99%9C%EC%9A%A9.md): 롤아웃, Platform Traces, OTLP와 실전 쿼리 (그림 18-1 포함)
- [진단 체크리스트](%EC%A7%84%EB%8B%A8%20%EC%B2%B4%ED%81%AC%EB%A6%AC%EC%8A%A4%ED%8A%B8.md): 여덟 단계 진단 절차와 증상별 출발점
- [요약](%EC%9A%94%EC%95%BD.md): 장 요약 열 가지
- [연습 문제](%EC%97%B0%EC%8A%B5%20%EB%AC%B8%EC%A0%9C.md): 실습 다섯 문제와 풀이 방향

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
