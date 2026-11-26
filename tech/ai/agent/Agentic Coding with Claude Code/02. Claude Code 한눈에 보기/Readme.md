# Claude Code 한눈에 보기

2장은 작은 Next.js 프로젝트 HookHub를 만들며 Claude Code가 실제로 어떻게 일하는지 익히는 실습 장이다. /init으로 CLAUDE.md를 만들고, 권한 시스템과 Playwright MCP를 써 보고, 계획 모드로 스펙을 쓴 뒤 그 스펙으로 메인 페이지를 구현한다. 여기서 만든 HookHub는 책 끝까지 이어지는 공통 실습 재료다.

---

## 1. 핵심 요점

- 프로젝트에서 처음 할 일은 /init이다. Claude가 코드베이스를 훑어 기술 스택과 구조를 CLAUDE.md에 담고, 이후 요청마다 이 파일을 먼저 읽는다.
- 파일을 만들거나 편집할 때마다 Claude는 권한을 묻는다. 안전한 에이전트형 코딩을 위해 이 통제를 유지한다.
- claude mcp add 명령으로 Playwright MCP를 사용자 범위(-s user)로 연결하고, /mcp로 연결을 확인한다. 외부 도구도 사용할 때 권한을 묻는다.
- Cursor 규칙은 Claude Code에서도 쓸 수 있다. 다만 memory 폴더에 둔 CLAUDE.md는 자동으로 로드되지 않으므로 필요할 때 불러오도록 따로 설정해야 한다.
- 스펙 주도 설계에서는 계획 모드에서 깊은 추론용 모델(Opus)로 스펙을 쓰게 하고, 구현은 가벼운 모델(Sonnet)에 스펙을 @로 붙여 시킨다.
- 같은 세션을 오래 쓰면 컨텍스트 윈도우가 차서 결과가 나빠진다. 새로 시작하거나 /clear, /compact로 관리한다.
- 최종 구조는 app, components, memory(frontend, spec)이며, 이것이 다음 장을 위한 기준 상태다.

---

## 2. 문서 목록

- [프로젝트 준비와 CLAUDE.md 만들기](프로젝트 준비와 CLAUDE.md 만들기.md): 장의 목표, Next.js 프로젝트 만들기, /init, 권한 시스템, CLAUDE.md의 내용
- [Playwright MCP와 memory 폴더](Playwright MCP와 memory 폴더.md): MCP 연결과 확인, Cursor 규칙으로 만든 프런트엔드 메모리, 자동 로드되지 않는 파일
- [스펙 주도 설계로 메인 페이지 구현](스펙 주도 설계로 메인 페이지 구현.md): 계획 모드에서 스펙 쓰기, 모델 전환, 구현과 결과, 커밋
- [요약과 핵심 개념](요약과 핵심 개념.md): 장 전체 흐름, 핵심 개념 표, 자주 놓치는 점

<br>
<br>
<br>

[Agentic Coding with Claude Code](../)
