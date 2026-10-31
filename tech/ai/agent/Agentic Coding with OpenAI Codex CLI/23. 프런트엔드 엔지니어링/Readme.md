# 프런트엔드 엔지니어링

22장에서 만든 Run or Relax 백엔드는 시간과 시간표를 받아 다음 출발 열차와 RUN 또는 relax 판정을 돌려주는, 얼굴 없는 API였다. 23장은 그 API를 호출해 전광판을 그리는 React와 TypeScript 프런트엔드를 Codex CLI로 만든다.

프런트엔드에서는 에이전트의 실수가 가장 잡기 어렵다. 엉뚱한 패키지 매니저, 훅 코드베이스에 들어온 클래스 컴포넌트, Vitest 러너에 쓴 Jest 단언문은 컴파일이 되기 때문에 조용히 잘못된다. 이 장은 그런 조용한 실패가 일찍 드러나도록 Codex CLI를 설정하는 방법을 다룬다.

---

## 1. 핵심 요점

- 프런트엔드 AGENTS.md는 패키지 매니저, React 버전과 패턴, 컴포넌트 라이브러리, 테스트 경계, 건드리면 안 되는 경로의 다섯 질문에 답해야 한다.
- 완료 기준(`pnpm build`, `pnpm test`, `pnpm tsc --noEmit`)을 적어 두면 에이전트가 통과할 때까지 스스로 반복한다.
- 백엔드의 `"RUN" | "relax"` 유니온을 프런트엔드가 그대로 거울처럼 받으면, 판정이 늘 때 타입 검사가 먼저 실패한다. 다만 런타임 보증은 아니므로 필요하면 Zod 같은 검증을 더한다.
- 컴포넌트는 구체적인 프롬프트로, 반복 패턴은 `$new-component` 같은 스킬로 만든다. 테스트는 시나리오를 적고 fireEvent 대신 userEvent를 쓰게 한다.
- UI와 API에 걸친 기능은 탐색자가 읽고 작업자가 만드는 서브에이전트 패턴으로 컨텍스트 오염을 피한다.
- axe-core를 jest-axe(Vitest)와 @axe-core/playwright(브라우저)로 연결하면 접근성 점검이 재현 가능한 스킬이 된다.
- 디자인은 Figma MCP(베타) 또는 이미지 입력으로 옮기되 간격 토큰은 사람이 확인한다. 브라우저 사용 검증은 지연과 토큰 비용 때문에 시각 작업 마무리에만 쓴다.

---

## 2. 문서 목록

- [프런트엔드 AGENTS.md 설정](%ED%94%84%EB%9F%B0%ED%8A%B8%EC%97%94%EB%93%9C%20AGENTS.md%20%EC%84%A4%EC%A0%95.md): 조용한 실패의 성격, 다섯 질문, 예시 AGENTS.md, 완료 기준
- [프로젝트 만들기와 막힘 해결](%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%20%EB%A7%8C%EB%93%A4%EA%B8%B0%EC%99%80%20%EB%A7%89%ED%9E%98%20%ED%95%B4%EA%B2%B0.md): 스캐폴드 명령, 설정 프롬프트, 정적 내보내기, 막힘 복구표
- [백엔드 연결과 타입 계약](%EB%B0%B1%EC%97%94%EB%93%9C%20%EC%97%B0%EA%B2%B0%EA%B3%BC%20%ED%83%80%EC%9E%85%20%EA%B3%84%EC%95%BD.md): 백엔드 실행, CORS, lib/departures.ts 계약과 그 한계
- [컴포넌트 생성과 전광판 만들기](%EC%BB%B4%ED%8F%AC%EB%84%8C%ED%8A%B8%20%EC%83%9D%EC%84%B1%EA%B3%BC%20%EC%A0%84%EA%B4%91%ED%8C%90%20%EB%A7%8C%EB%93%A4%EA%B8%B0.md): DepartureRow 프롬프트, new-component 스킬, 뷰와 컨테이너 분리
- [테스트 생성과 Playwright 확인](%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EC%83%9D%EC%84%B1%EA%B3%BC%20Playwright%20%ED%99%95%EC%9D%B8.md): 시나리오 지정 테스트, userEvent, playwright-check 스킬
- [탐색자와 작업자 서브에이전트 패턴](%ED%83%90%EC%83%89%EC%9E%90%EC%99%80%20%EC%9E%91%EC%97%85%EC%9E%90%20%EC%84%9C%EB%B8%8C%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%ED%8C%A8%ED%84%B4.md): 컨텍스트 오염, 역할 분담, 그림 23.1, 적용 기준
- [접근성 점검 자동화](%EC%A0%91%EA%B7%BC%EC%84%B1%20%EC%A0%90%EA%B2%80%20%EC%9E%90%EB%8F%99%ED%99%94.md): axe-core, jest-axe, Playwright 점검, accessibility-audit 스킬
- [디자인에서 코드로와 브라우저 검증](%EB%94%94%EC%9E%90%EC%9D%B8%EC%97%90%EC%84%9C%20%EC%BD%94%EB%93%9C%EB%A1%9C%EC%99%80%20%EB%B8%8C%EB%9D%BC%EC%9A%B0%EC%A0%80%20%EA%B2%80%EC%A6%9D.md): Figma MCP와 비전 입력, 작업 유형별 패턴 표, 브라우저 사용 검증
- [요약](%EC%9A%94%EC%95%BD.md): 장 끝 요약 여덟 가지
- [연습 문제](%EC%97%B0%EC%8A%B5%20%EB%AC%B8%EC%A0%9C.md): 다섯 가지 실습과 풀이 방향

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
