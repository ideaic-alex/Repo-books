# 부록 A 명령어 참조

Claude Code를 쓸 때 자주 찾게 되는 명령어, 플래그, 슬래시 명령, 단축키, 권한 설정, Vim 모드를 한곳에 모아 둔 참조 부록이다. 처음부터 읽는 장이라기보다 필요할 때 펼쳐 보는 사전에 가깝다.

이 노트는 같은 내용을 용도별로 다시 묶었다. 시작 방식, 세션 플래그, 헤드리스 출력, 권한, 슬래시 명령, 단축키, 배시 모드, 세션 선택기와 Vim 모드 순서다.

---

## 1. 핵심 요점

- **시작 방식**: `claude`는 대화형, `claude -p "task"`는 한 번 실행하고 끝나는 헤드리스 모드이고, `-c`는 최근 대화를, `-r`은 ID나 이름으로 고른 세션을 이어 간다.
- **세션 플래그**: `--fork-session`으로 기록을 유지한 채 새 세션으로 갈라지고, `--from-pr`로 PR에 연결된 세션을 다시 열며, `--session-name`으로 이름을 붙인다.
- **헤드리스 출력**: `--output-format`은 text, json, stream-json 중에서 고르고, `--max-turns`, `--budget-tokens`, `--fallback-model`로 실행 한도와 대비책을 정한다.
- **권한 모드 다섯 가지**: Plan(읽기 전용), Default, Auto-accept edits, Full auto-accept, Bypass permissions 순으로 자율성이 커지며, Bypass는 샌드박스에서만 쓴다.
- **권한 규칙**: `Tool` 또는 `Tool(specifier)` 문법과 glob을 쓰고(`Bash(git *)`), MCP 도구는 `mcp__<server>__<tool>` 패턴으로 지정한다.
- **슬래시 명령과 단축키**: `/compact`, `/context`, `/rewind`, `/resume` 같은 명령과 Shift+Tab, Esc Esc, Ctrl+B 같은 단축키로 세션 도중 대부분을 조작한다.
- **배시 모드와 백그라운드**: `!` 접두로 셸 명령을 바로 실행하고, Ctrl+B로 오래 걸리는 작업을 백그라운드로 보낸다.
- **편집 편의**: `/terminal-setup`으로 줄바꿈 키를 설치하고, `/vim`으로 Vim 모드를 켠다.

---

## 2. 문서 목록

- [CLI 명령어와 시작 방식](CLI%20%EB%AA%85%EB%A0%B9%EC%96%B4%EC%99%80%20%EC%8B%9C%EC%9E%91%20%EB%B0%A9%EC%8B%9D.md): claude, -p, -c, -r 등 시작과 재개 명령
- [세션과 입력 플래그](%EC%84%B8%EC%85%98%EA%B3%BC%20%EC%9E%85%EB%A0%A5%20%ED%94%8C%EB%9E%98%EA%B7%B8.md): 세션 이어 가기, 갈라지기, 모델과 에이전트 지정, 팀 표시 방식
- [시스템 프롬프트와 출력 제어 플래그](%EC%8B%9C%EC%8A%A4%ED%85%9C%20%ED%94%84%EB%A1%AC%ED%94%84%ED%8A%B8%EC%99%80%20%EC%B6%9C%EB%A0%A5%20%EC%A0%9C%EC%96%B4%20%ED%94%8C%EB%9E%98%EA%B7%B8.md): 시스템 프롬프트 교체와 덧붙이기, 출력 형식, 턴과 토큰 한도
- [권한 플래그와 권한 모드](%EA%B6%8C%ED%95%9C%20%ED%94%8C%EB%9E%98%EA%B7%B8%EC%99%80%20%EA%B6%8C%ED%95%9C%20%EB%AA%A8%EB%93%9C.md): 허용과 거부 플래그, 권한 모드 다섯 가지, 도구 이름과 규칙 문법
- [슬래시 명령 모음](%EC%8A%AC%EB%9E%98%EC%8B%9C%20%EB%AA%85%EB%A0%B9%20%EB%AA%A8%EC%9D%8C.md): 슬래시 명령 전체 표와 용도별 정리
- [키보드 단축키와 여러 줄 입력](%ED%82%A4%EB%B3%B4%EB%93%9C%20%EB%8B%A8%EC%B6%95%ED%82%A4%EC%99%80%20%EC%97%AC%EB%9F%AC%20%EC%A4%84%20%EC%9E%85%EB%A0%A5.md): 단축키 세 묶음과 여러 줄 입력 방법
- [배시 모드와 백그라운드 작업](%EB%B0%B0%EC%8B%9C%20%EB%AA%A8%EB%93%9C%EC%99%80%20%EB%B0%B1%EA%B7%B8%EB%9D%BC%EC%9A%B4%EB%93%9C%20%EC%9E%91%EC%97%85.md): `!` 접두, 백그라운드 실행, 프롬프트 제안, 작업 목록
- [세션 선택기와 Vim 모드](%EC%84%B8%EC%85%98%20%EC%84%A0%ED%83%9D%EA%B8%B0%EC%99%80%20Vim%20%EB%AA%A8%EB%93%9C.md): 세션 선택기 키와 Vim 모드 이동 및 편집 명령

<br>
<br>
<br>

[Claude Code The Definitive Guide to Agentic Development-2](../)
