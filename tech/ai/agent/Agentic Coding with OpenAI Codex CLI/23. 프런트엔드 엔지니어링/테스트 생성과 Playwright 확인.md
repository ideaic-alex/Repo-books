# 테스트 생성과 Playwright 확인

React 프로젝트에서 단위 테스트의 표준 도구는 Vitest와 Testing Library다. Codex CLI는 컴포넌트 소스가 있으면 이런 테스트를 정확하게 만들어 내지만, 품질은 프롬프트가 얼마나 구체적이냐에 달렸다. 이 문서는 시나리오를 지정하는 테스트 프롬프트, fireEvent와 userEvent의 차이, 브라우저 검증용 playwright-check 스킬을 정리한다.

---

## 1. 시나리오를 적어 주기

"이 컴포넌트 테스트 써 줘"라고 하면 커버리지가 나온다. 시나리오를 지정해야 쓸모 있는 테스트가 나온다. 책의 전광판 테스트 프롬프트는 여섯 가지를 지정한다.

**DepartureBoardView (순수 렌더링)**

1. 출발마다 행이 하나씩 그려진다.
2. RUN 출발에는 RUN 배지, relax 출발에는 relax 배지가 보인다.
3. 빈 목록에는 빈 상태("no more trains today")가 보인다.

**DepartureBoard (컨테이너, fetchDepartures를 mock)**

4. 로딩 스켈레톤이 보이고, 프로미스가 풀리면 행이 보인다.
5. fetchDepartures가 거부되면 에러 상태가 보인다.
6. 폴링 간격마다 다시 가져오고 마지막 갱신 시각이 넘어간다.

여기에 상호작용에는 Testing Library의 userEvent, 폴링에는 가짜 타이머를 쓰고, 고정된 `now`를 넘겨 실제 시계를 읽지 않게 하며, fireEvent는 쓰지 말라는 조건을 붙인다.

## 2. userEvent를 지정하는 이유

fireEvent는 합성 DOM 이벤트 하나를 쏘는 반면, userEvent는 포커스, 블러, 키보드 순서까지 포함해 실제 브라우저의 동작을 흉내 낸다. 예를 들어 userEvent는 pointerdown, mousedown, focus, click처럼 이벤트 순서 전체를 재현하므로, 이벤트 순서에 기대는 컴포넌트를 테스트할 때 차이가 난다. fireEvent로 쓴 테스트는 실제 상호작용이라면 실패할 상황에서도 통과할 수 있다. Codex CLI는 두 API를 다 알고 있으니, 우리 코드베이스가 어느 쪽을 쓰는지 사람이 알려 줘야 한다.

## 3. playwright-check 스킬

종단 간(e2e) 테스트에는 Playwright 스킬로 브라우저 검증 루프를 만든다. `.agents/skills/playwright-check/SKILL.md`의 내용은 다음과 같다.

```markdown
---
name: playwright-check
description: Verify UI changes by running Playwright browser tests
---
1. Start the development server: `pnpm dev &`
2. Wait for readiness: `npx wait-on http://localhost:3000`
3. Run: `pnpm test:e2e --grep "<component name>"`
4. If no test exists, create a minimal one: navigate to the
   page, assert key elements render, check for no console
   errors, test mobile (375px) and desktop (1280px) viewports
5. Report the outcome and any failures
```

스킬 끝에는 컴포넌트나 페이지를 바꾼 뒤 작업 완료로 표시하기 전에 항상 이걸 돌리라는 지시가 붙는다. 시각적 정확성이 중요한 프롬프트에서는 스킬을 이름으로 가리키면 된다. 예를 들어 "헤더에 검색창을 추가해라. 구현한 뒤 `$playwright-check`로 모바일과 데스크톱 구간에서 제대로 그려지는지 확인하라"고 쓴다.

## 4. 운영상 주의

Playwright 테스트는 개발 서버가 떠 있어야 하므로 세션이 이어지는 동안 포트 하나와 프로세스 하나를 쓴다. CI에서는 3000 포트가 비어 있어야 하고, 세션이 끝나면 `pnpm dev`가 깨끗이 종료되는지 확인해야 한다. 2단계의 wait-on이 필수인 이유는, 이게 없으면 서버가 아직 시작을 끝내지 못한 상태에서 Playwright가 404를 맞고 거짓 실패를 내기 때문이다.

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
