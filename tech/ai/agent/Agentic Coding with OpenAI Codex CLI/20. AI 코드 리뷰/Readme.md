# AI 코드 리뷰

코드 리뷰는 지식을 퍼뜨리고 버그를 일찍 잡고 팀의 기준을 지키는 일이지만, 끝없이 반복되는 일이기도 하다. Codex CLI의 리뷰 기능은 로컬 터미널, 풀 리퀘스트, CI 파이프라인의 세 층에서 동작한다. 이 장은 각 표면을 설정하는 법과 서로 연결하는 법, 그리고 사람의 판단이 꼭 필요한 곳에 사람을 남겨 두는 법을 다룬다.

AI 리뷰가 잘 잡는 문제와 못 보는 문제를 구분하는 데서 출발해, `/review` 명령, AGENTS.md 리뷰 지침, codex-action 기반 PR 자동 리뷰, 구조화 출력과 교차 모델 리뷰, 3단계 성숙도 모델까지 이어진다.

---

## 1. 핵심 요점

- AI 리뷰는 보안 안티패턴, 린터가 못 보는 정확성 문제, AGENTS.md로 정한 관례 위반처럼 피로에 민감한 항목에 강하고, 아키텍처와 의도와 조직 내 트레이드오프는 사람이 판단해야 한다.
- c-CRAB 벤치마크에서 네 에이전트를 합쳐도 과제의 약 40%만 풀렸다. AGENTS.md의 리뷰 체크리스트와 여러 모델의 병용이 이 격차를 줄이는 방법이다.
- 에이전트가 쓴 PR은 설명과 코드가 어긋나는 경우가 있으므로, PR 설명은 계획이 아니라 diff에서 만들고 AI 리뷰를 사람 승인 없는 머지 관문으로 쓰지 않는다.
- `/review`는 브랜치 비교, 미커밋 변경, 커밋 리뷰, 사용자 지정 지침의 네 모드를 가진 읽기 전용 명령이며, `review_model`로 리뷰 전용 모델을 고를 수 있다.
- `## Review guidelines`에는 린터가 잡는 스타일 규칙을 넣지 않고, P0~P2 심각도와 함께 보안과 정확성 규칙을 적는다. 하위 디렉터리의 AGENTS.md로 민감한 패키지 규칙을 겹쳐 쓴다.
- `openai/codex-action`과 `--output-schema`로 신뢰도 점수가 붙은 JSON 지적을 얻고, 자동 PR 코멘트는 P0와 P1로 제한한다. Codex와 Claude Code의 지적을 합치면 서로의 사각지대를 메운다.
- 리뷰-수정 루프는 수동 리뷰, 자율 stop 훅, 다중 AI 거버넌스의 3단계로 성숙하며, 프로젝트의 위험도에 맞는 단계를 고른다.

---

## 2. 문서 목록

- [AI 리뷰가 잘하는 일과 못하는 일](AI%20%EB%A6%AC%EB%B7%B0%EA%B0%80%20%EC%9E%98%ED%95%98%EB%8A%94%20%EC%9D%BC%EA%B3%BC%20%EB%AA%BB%ED%95%98%EB%8A%94%20%EC%9D%BC.md): 강점과 한계, c-CRAB 벤치마크, 리뷰 체크리스트
- [에이전트 PR 신뢰 문제](%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20PR%20%EC%8B%A0%EB%A2%B0%20%EB%AC%B8%EC%A0%9C.md): 설명과 코드의 불일치 연구, CodeRabbit 수치, diff 기반 설명 생성과 훅 검증
- [리뷰 모델 설정과 review 명령](%EB%A6%AC%EB%B7%B0%20%EB%AA%A8%EB%8D%B8%20%EC%84%A4%EC%A0%95%EA%B3%BC%20review%20%EB%AA%85%EB%A0%B9.md): review_model, 엄격도 조정, /review의 네 가지 모드
- [PR 자동 리뷰와 codex-action](PR%20%EC%9E%90%EB%8F%99%20%EB%A6%AC%EB%B7%B0%EC%99%80%20codex-action.md): GitHub 클라우드 리뷰와 GitHub Actions 워크플로 읽기
- [구조화 출력과 교차 모델 리뷰](%EA%B5%AC%EC%A1%B0%ED%99%94%20%EC%B6%9C%EB%A0%A5%EA%B3%BC%20%EA%B5%90%EC%B0%A8%20%EB%AA%A8%EB%8D%B8%20%EB%A6%AC%EB%B7%B0.md): output-schema, 플랫폼별 구현, Codex와 Opus의 적대적 리뷰 흐름도
- [AGENTS.md 리뷰 지침과 프로젝트별 설정](AGENTS.md%20%EB%A6%AC%EB%B7%B0%20%EC%A7%80%EC%B9%A8%EA%B3%BC%20%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%EB%B3%84%20%EC%84%A4%EC%A0%95.md): Review guidelines 작성법, 겹쳐 쓰기, 프로젝트 유형별 설정표
- [사람과 AI 협업과 3단계 성숙도](%EC%82%AC%EB%9E%8C%EA%B3%BC%20AI%20%ED%98%91%EC%97%85%EA%B3%BC%203%EB%8B%A8%EA%B3%84%20%EC%84%B1%EC%88%99%EB%8F%84.md): 협업 패턴 세 가지와 리뷰-수정 루프의 성숙도 모델
- [요약](%EC%9A%94%EC%95%BD.md): 20장의 핵심 열 가지
- [연습 문제](%EC%97%B0%EC%8A%B5%20%EB%AC%B8%EC%A0%9C.md): 훅, 지침, 워크플로, 보정 감사, 협업 설계, 다중 AI 구성

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
