# 스킬 생태계: 스킬 쓰기와 활용

9장의 훅이 에이전트의 생애 주기를 제어하는 도구였다면, 스킬은 에이전트에게 새로운 일을 하는 방법을 가르치는 도구다. 이 장은 커뮤니티 스킬을 찾고 설치하고 조합하는 소비자 쪽과, 직접 스킬을 쓰고 description을 다듬고 호출 정책을 정해 배포하는 생산자 쪽을 함께 다룬다.

후반부에서는 스킬을 설치 가능한 단위로 묶는 Codex 플러그인 마켓플레이스, 설치 정책을 통한 기업 거버넌스, 스킬과 플러그인을 엮은 워크플로 패턴과 실제 사례를 살펴본다.

---

## 1. 핵심 요점

- 스킬은 SKILL.md가 든 디렉터리이며, 시작 때는 name과 description만 읽고 본문과 보조 파일은 필요할 때만 읽는 점진적 공개 방식이다.
- SKILL.md는 AGENTS.md와 함께 AAIF가 관리하는 열린 표준이라서 Codex CLI, Claude Code, Cursor 등에서 고치지 않고 쓸 수 있다.
- 탐색 순서는 프로젝트, 사용자, 관리자, 시스템이다. 팀 스킬은 `.agents/skills/`에 커밋하고, 설치한 스킬은 서드파티 코드처럼 검토한다.
- description은 라우팅 규칙이므로 핵심 동작, 트리거 동의어, 명시적 제외를 넣는다. 영향이 큰 스킬은 `agents/openai.yaml`에서 `allow_implicit_invocation: false`로 막는다.
- 스킬 크기는 5단계로 가늠하고, 먼저 손으로 해 본 뒤 SKILL.md로 옮기며, `skills-ref` 검증과 3층 평가로 품질을 확인한다.
- 플러그인은 스킬, 앱 커넥터, MCP 서버 설정을 묶고, marketplace.json의 설치 정책(INSTALLED_BY_DEFAULT, AVAILABLE, NOT_AVAILABLE)으로 거버넌스를 건다.
- 조합은 개별 스킬 안이 아니라 AGENTS.md, 상위 스킬, 플러그인 매니페스트에서 하고, 스킬 하나는 책임 하나에 집중한다.

---

## 2. 문서 목록

- [스킬의 개념과 표준](%EC%8A%A4%ED%82%AC%EC%9D%98%20%EA%B0%9C%EB%85%90%EA%B3%BC%20%ED%91%9C%EC%A4%80.md): 스킬의 구조, 점진적 공개, agentskills.io 표준, 보안 주의
- [스킬 찾기와 설치와 관리](%EC%8A%A4%ED%82%AC%20%EC%B0%BE%EA%B8%B0%EC%99%80%20%EC%84%A4%EC%B9%98%EC%99%80%20%EA%B4%80%EB%A6%AC.md): 카탈로그, 설치 명령, 탐색 순서, 끄기, 호출 정책, 스킬 대 MCP 대 훅 비교
- [SKILL.md 작성 규칙](SKILL.md%20%EC%9E%91%EC%84%B1%20%EA%B7%9C%EC%B9%99.md): 디렉터리 구조, frontmatter 필드와 name 규칙, 3단계 로딩, description 쓰는 법
- [openai.yaml과 스킬 만들어 배포하기](openai.yaml%EA%B3%BC%20%EC%8A%A4%ED%82%AC%20%EB%A7%8C%EB%93%A4%EC%96%B4%20%EB%B0%B0%ED%8F%AC%ED%95%98%EA%B8%B0.md): 호출 정책과 MCP 의존성, 검증과 공개, 5단계 크기 기준, 작성 순서
- [스킬 평가하기](%EC%8A%A4%ED%82%AC%20%ED%8F%89%EA%B0%80%ED%95%98%EA%B8%B0.md): 3층 평가 구조, description 평가, Skillgrade와 Skill Creator V2, CI 연결
- [플러그인과 마켓플레이스](%ED%94%8C%EB%9F%AC%EA%B7%B8%EC%9D%B8%EA%B3%BC%20%EB%A7%88%EC%BC%93%ED%94%8C%EB%A0%88%EC%9D%B4%EC%8A%A4.md): plugin.json 구조, 마켓플레이스 탐색 순서, 설치 정책, 수명 주기 명령
- [워크플로 조합과 사례](%EC%9B%8C%ED%81%AC%ED%94%8C%EB%A1%9C%20%EC%A1%B0%ED%95%A9%EA%B3%BC%20%EC%82%AC%EB%A1%80.md): 조합 패턴 세 가지, 번들 훅, 확장 우선 구조, Nx와 codex-pr-body와 Elves와 Google Agent Skills 사례
- [요약](%EC%9A%94%EC%95%BD.md): 장 끝 Summary 아홉 항목 정리
- [연습 문제](%EC%97%B0%EC%8A%B5%20%EB%AC%B8%EC%A0%9C.md): 팀 관례 스킬, description 보정, 로컬 마켓플레이스 실습

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
