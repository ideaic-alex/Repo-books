# MCP 사용하기와 제공하기

MCP는 에이전트가 GitHub, 데이터베이스, 브라우저 같은 외부 시스템과 하나의 공용 규약으로 대화하게 해 주는 표준이다. 이 장은 Codex CLI가 MCP 서버를 가져다 쓰는 방법과, 반대로 Codex CLI 자신을 MCP 서버로 내주는 방법을 모두 다룬다.

서버를 하나 붙일 때마다 쓸 수 있는 능력이 늘지만 컨텍스트 윈도도 그만큼 소모된다. 그래서 어떤 서버와 도구를 켤지 고르는 일이 곧 컨텍스트 관리라는 관점이 장 전체를 이끈다. 쓰기 연동의 안전, 장애 대응, 디버깅까지 운영 관점도 함께 정리한다.

---

## 1. 핵심 요점

- MCP는 에이전트와 도구를 잇는 열린 표준이며, 호스트, 클라이언트, 서버의 3단 구조로 돌아간다.
- 도구 어노테이션(readOnlyHint, destructiveHint 등)은 승인 시스템이 호출 경로를 정하는 근거가 된다. 직접 만들 때는 보수적으로 정직하게 단다.
- enabled_tools 허용 목록, enabled 토글, 프로필 범위 설정, 짧은 도구 설명으로 컨텍스트 비용을 관리한다.
- 모델이 잘 아는 작업은 gh, curl, psql 같은 CLI가 더 싸다. 구조화된 스키마와 런타임 강제 안전장치가 필요할 때 MCP를 쓴다.
- Python FastMCP로 서버를 쉽게 만들 수 있고, 연결 전에 MCP Inspector로 따로 테스트한다.
- `codex mcp-server`로 Codex CLI를 서버로 내놓으면 codex와 codex-reply 도구로 에이전트 간 위임이 가능하다.
- 쓰기 연동에는 명시적 어노테이션, 승인 통제, 멱등성, 감사 로그의 네 원칙이 필요하다.
- 기업 환경에서는 서버 허용 목록과 자격 증명 격리를 지키고, 장애에 대비해 타임아웃과 디버깅 절차를 갖춘다.

---

## 2. 문서 목록

- [MCP 기본 개념](MCP%20%EA%B8%B0%EB%B3%B8%20%EA%B0%9C%EB%85%90.md): MCP란 무엇인지, 호스트·클라이언트·서버 구조, 도구 어노테이션
- [자주 쓰는 서버 연결하기](%EC%9E%90%EC%A3%BC%20%EC%93%B0%EB%8A%94%20%EC%84%9C%EB%B2%84%20%EC%97%B0%EA%B2%B0%ED%95%98%EA%B8%B0.md): GitHub, Context7, Playwright, Postgres 설정과 도구 선택
- [컨텍스트 비용 관리](%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%20%EB%B9%84%EC%9A%A9%20%EA%B4%80%EB%A6%AC.md): MCP 대 CLI 판단 기준과 비용을 줄이는 네 가지 방법
- [기업 환경의 MCP](%EA%B8%B0%EC%97%85%20%ED%99%98%EA%B2%BD%EC%9D%98%20MCP.md): 서버 범위 지정, 자격 증명 격리, 엘리시테이션
- [간단한 MCP 서버 만들기](%EA%B0%84%EB%8B%A8%ED%95%9C%20MCP%20%EC%84%9C%EB%B2%84%20%EB%A7%8C%EB%93%A4%EA%B8%B0.md): FastMCP 최소 서버, Codex 연결, Inspector 테스트
- [Codex CLI를 MCP 서버로 쓰기](Codex%20CLI%EB%A5%BC%20MCP%20%EC%84%9C%EB%B2%84%EB%A1%9C%20%EC%93%B0%EA%B8%B0.md): codex mcp-server, 두 도구, 위임 패턴
- [운영 환경의 MCP](%EC%9A%B4%EC%98%81%20%ED%99%98%EA%B2%BD%EC%9D%98%20MCP.md): 쓰기 안전, 장애 대응, 원격과 컨테이너 서버, 디버깅
- [요약](%EC%9A%94%EC%95%BD.md): 장의 아홉 가지 핵심 정리
- [연습 문제](%EC%97%B0%EC%8A%B5%20%EB%AC%B8%EC%A0%9C.md): 세 개의 연습 문제와 풀이 방향

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
