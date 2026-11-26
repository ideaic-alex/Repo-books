# MCP, 스킬, 플러그인으로 Claude Code 확장하기

8장은 Claude Code의 기본 기능을 넘어 외부 세계와 연결하는 방법을 다룬다. MCP로 Notion에 문서를 자동 생성하고, 스킬과 플러그인으로 코드 리뷰, 자동 테스트, 문서 파일 생성을 맡기고, GitHub MCP로 프로젝트를 보관한다. 마지막에는 Vercel로 배포하고 Supabase 데이터베이스를 붙여, 내 컴퓨터에서만 돌던 쇼핑 목록 앱을 누구나 접속하는 서비스로 만든다.

---

## 1. 핵심 요점

- MCP는 AI가 외부 데이터와 도구, 서비스에 접속하는 표준 통신 규약이다. API가 기능을 요청하는 창구라면 MCP는 AI가 파일과 데이터베이스를 직접 다루게 한다.
- Claude Code는 MCP 클라이언트이고 MCP 서버가 실제 일을 한다. 서버를 새로 연결하면 기능이 늘어나는 확장 구조다.
- 원격 MCP는 명령 한 줄로 시작하고 인증이 필요하다. 로컬 MCP는 내 컴퓨터에서 명령을 직접 실행하며 인터넷 없이도 된다. `--` 기호가 Claude Code 옵션과 실행 명령을 가른다.
- MCP 설치의 세 단계는 `claude mcp add` 명령, 계정 인증, 프롬프트 사용이다. 설치 명령은 Vibe Index에서 Official MCP 표시를 확인해 복사한다.
- 스킬은 `.claude/skills/스킬이름/SKILL.md`에 저장되며 Claude가 맥락에 따라 자동으로 쓴다. 플러그인은 MCP와 스킬을 묶은 꾸러미이고, 마켓플레이스에서 `/plugin`으로 설치한다.
- GitHub MCP는 토큰 인증으로 설치하며, add, commit, push 과정을 Claude Code가 대신한다. 토큰은 한 번만 보이니 따로 저장하고 비밀로 지킨다.
- Vercel은 GitHub에 올린 코드를 자동 배포한다. 시작 페이지가 `index.html`이 아니면 404 오류가 난다.
- Supabase MCP로 테이블을 만들고 로컬 스토리지 저장을 데이터베이스 저장으로 바꾸면, 여러 기기에서 같은 데이터를 보는 진짜 서비스가 된다.

---

## 2. 문서 목록

- [MCP의 개념과 Notion 연결](MCP의 개념과 Notion 연결.md): MCP와 API의 차이, 클라이언트-서버 모델, Notion MCP 설치와 인증, 연구 노트 자동 생성
- [로컬 MCP와 Sequential Thinking](로컬 MCP와 Sequential Thinking.md): 원격과 로컬 MCP 비교, 설치 명령 해부, 인증, 일반 추론과의 비교 실습
- [스킬과 플러그인, 마켓플레이스](스킬과 플러그인, 마켓플레이스.md): 스킬 만들기와 쓰기, 플러그인과 마켓플레이스, Playwright 테스트, document-skills
- [GitHub MCP로 프로젝트 보관하기](GitHub MCP로 프로젝트 보관하기.md): 토큰 발급, GitHub MCP 설치, 프로젝트 업로드, add와 commit과 push
- [Vercel 배포와 Supabase 데이터베이스 연결](Vercel 배포와 Supabase 데이터베이스 연결.md): 배포와 404 해결, 로컬 스토리지의 한계, Supabase 테이블, 실시간 동기화
- [요약과 핵심 개념](요약과 핵심 개념.md): 장 전체 흐름, 핵심 개념 표, 자주 놓치는 점

<br>
<br>
<br>

[Build with Claude Code](../)
