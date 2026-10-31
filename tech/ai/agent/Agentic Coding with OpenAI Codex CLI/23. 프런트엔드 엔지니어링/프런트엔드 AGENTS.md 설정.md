# 프런트엔드 AGENTS.md 설정

프런트엔드 작업에서 에이전트가 저지르는 실수는 대부분 조용하다. 컴파일은 되는데 프로젝트 관례와 어긋나 있어서, 나중에 리뷰나 디버깅 단계에서야 드러난다. 이 문서는 그런 조용한 실패를 AGENTS.md로 어떻게 막는지, 그리고 완료 기준을 어떻게 에이전트의 피드백 루프로 바꾸는지 정리한다.

배경은 22장에서 만든 Run or Relax 서비스다. 22장의 백엔드는 시간과 시간표를 받아 Audley End 역의 다음 출발 열차와 판정(RUN 또는 relax)을 돌려주는, 얼굴 없는 API였다. 23장은 그 API를 호출해 전광판을 그리는 React와 TypeScript 프런트엔드를 Codex CLI로 만든다.

---

## 1. 프런트엔드에서 실수가 더 위험한 이유

백엔드 에이전트가 틀린 SQL을 만들면 테스트가 바로 깨진다. 프런트엔드는 다르다. 에이전트가 엉뚱한 패키지 매니저를 쓰거나, 훅 기반 코드베이스에 클래스 컴포넌트를 넣거나, Vitest 러너에 Jest 단언문을 쓰더라도 일단 컴파일은 된다. 그래서 문제가 늦게 보이고, 원인을 추적하기도 어렵다. 이 장의 핵심 주제가 바로 이 조용한 실패다. 함께 따라오는 어려움으로는 툴체인 불일치, 아무것도 증명하지 못하는 테스트, 접근성 부채, 디자인을 코드로 옮기는 일이 있다.

책은 React와 TypeScript를 예로 들지만, 특정 라이브러리 이야기가 아니다. 조용한 실패가 일찍 드러나도록 Codex CLI를 설정하는 방법이 주제다.

## 2. 학습 목표

이 장을 끝내면 다음을 할 수 있어야 한다.

- 흔한 툴체인 불일치를 막는 프런트엔드 AGENTS.md 작성
- 프롬프트 하나로 타입이 붙은 React 컴포넌트와 같은 위치의 Vitest 테스트 만들기
- 백엔드의 타입 계약을 React에서 받아, 판별 유니온(discriminated union)으로 분기해 API 모양을 양쪽에서 강제하기
- 합성 이벤트가 아니라 실제 사용자 상호작용을 다루는 Vitest와 Testing Library 테스트 만들기
- UI와 API에 걸친 기능에 탐색자/작업자 서브에이전트 패턴 적용
- 접근성 점검을 반복 가능한 스킬로 자동화
- 비전 입력과 Figma의 MCP 서버로 디자인을 코드로 옮기기
- 브라우저 사용 검증 루프의 지연과 토큰 비용이 값어치를 하는 때를 판단

## 3. 백엔드보다 질문이 많아진다

22장에서 AGENTS.md가 에이전트의 추측을 막는 가장 효율 좋은 수단이라고 했는데, 프런트엔드에서는 그 중요성이 더 커진다. 지켜야 할 관례가 많고, 어긴 흔적은 더 조용하기 때문이다. 예를 들면 모노레포가 pnpm을 쓰는데 npm install을 실행하거나, 배럴 파일이 이름 있는 export를 기대하는데 default export를 쓰거나, Vitest로 옮겼는데 jest.fn()을 쓰는 식이다. 하나하나는 사소하지만 쌓이면 리뷰가 느려지고 관례가 갈라지며, 에이전트를 자율적으로 돌리게 해 주는 신뢰가 닳는다.

프런트엔드 AGENTS.md는 백엔드에서는 암묵적으로 넘어가도 되는 다섯 가지 질문에 답해야 한다.

| 번호 | 질문 | 왜 필요한가 |
| --- | --- | --- |
| 1 | 패키지 매니저는 무엇이고 정확한 명령은 무엇인가 | npm, yarn, pnpm 혼용을 막는다 |
| 2 | React 버전은 무엇이고 어떤 패턴을 허용하거나 금지하는가 | 버전별 권장 패턴이 다르다 |
| 3 | 컴포넌트 라이브러리는 무엇이고 기본 부품은 어떻게 설치하고 확장하는가 | 생성 파일을 건드리는 사고를 막는다 |
| 4 | 테스트 프레임워크는 무엇이고 단위 테스트와 e2e의 경계는 어디인가 | 러너끼리 충돌하지 않게 한다 |
| 5 | 에이전트가 절대 넘으면 안 되는 파일 시스템 경계는 어디인가 | 보호할 디렉터리를 고정한다 |

## 4. 예시 AGENTS.md

책은 React 19 컴파일러를 쓰는 Next.js 15 프로젝트용 설정으로 다섯 질문에 모두 답한다. 구성은 다음과 같다. 코드블록에는 핵심 줄만 옮겼다.

```markdown
## Stack
- React 19 with TypeScript strict mode
- Next.js 15 (App Router), static export (`output: "export"`)
- Tailwind CSS v4, shadcn/ui
- Vitest + Testing Library, Playwright
- pnpm (never npm install or yarn)
```

Next.js는 정적 내보내기(`output: "export"`)로 빌드한다. 전광판이 서버 런타임 없이 정적 파일로만 배포된다는 뜻이다. React 19는 2024년 12월에 정식 출시됐고, 자동 메모이제이션을 해 주는 React 컴파일러가 핵심 기능이다. 이 때문에 useMemo와 useCallback을 쓰는 권장 방식이 바뀌었다.

나머지 섹션은 다음과 같다.

- **Backend**: 22장 FastAPI 서비스의 `GET /departures`를 브라우저가 직접 호출한다. 기본 주소는 환경 변수 `NEXT_PUBLIC_DEPARTURES_API_URL`이고 값이 없으면 `http://localhost:8000`을 쓴다. 호출이 다른 출처(cross-origin)이므로 백엔드가 전광판 출처에 대한 CORS 헤더를 보내야 한다.
- **Commands**: `pnpm dev`(개발 서버, 3000 포트), `pnpm test`(Vitest), `pnpm test:e2e`(Playwright), `pnpm build`, `pnpm lint`(ESLint와 Prettier 점검), `pnpm tsc --noEmit`(타입 검사).
- **Architecture**: `/app`은 페이지, `/components/ui`는 shadcn/ui 기본 부품, `/components`는 애플리케이션 컴포넌트, `/lib`는 유틸리티와 데이터 호출, `/tests`는 Vitest, `/e2e`는 Playwright.
- **Component conventions**: 함수형 컴포넌트만 쓴다. useMemo와 useCallback은 기본으로 추가하지 않고 컴파일러를 믿는다. 급하지 않은 상태 갱신에는 `startTransition`을 쓴다. 서버 컴포넌트를 우선하고 상호작용이 필요할 때만 `"use client"`를 쓴다. shadcn/ui 컴포넌트는 `pnpm dlx shadcn@latest add <component>`로 설치한다. 컴포넌트 파일은 이름 있는 export만 쓴다.
- **TypeScript**: strict 모드, `any`와 `@ts-ignore` 금지. 타입을 좁힐 때는 캐스팅 대신 `satisfies`를 쓴다. API 응답 모양에는 모두 명시적 타입을 붙인다.
- **Constraints**: `/components/ui`는 직접 수정하지 않는다. 프로덕션 코드에 `console.log`를 넣지 않는다. Tailwind 유틸리티 클래스만 쓰고 인라인 스타일과 CSS-in-JS는 쓰지 않는다.
- **Completion criteria**: `pnpm build`가 에러 없이 통과, `pnpm test`가 모두 통과, `pnpm tsc --noEmit`이 에러 0.

## 5. 눈여겨볼 세 줄

**useMemo/useCallback 금지.** 이 한 줄이 없으면 Codex CLI는 비싼 계산마다 방어적으로 메모이제이션을 두른다. 동작은 하지만 쓸데없이 장황한 코드가 나온다. React 컴파일러(예전 이름 React Forget)는 빌드 때 컴포넌트와 훅을 자동으로 메모이제이션하므로, 손으로 useMemo나 useCallback을 더하면 이중 메모이제이션이 된다. 에이전트가 낡은 React 17 시절 성능 패턴을 따라 하는 것을 이 줄이 막는다.

**`/components/ui` 직접 수정 금지.** 이 파일들은 shadcn CLI가 만들고 관리하는 생성 파일이지 우리가 소유한 소스가 아니다. 직접 고치면 재생성 흐름이 깨진다. 이를 강한 제약으로 적어 두면 Codex CLI가 기본 부품을 "개선"하면서 생기는 조용한 훼손을 막는다.

**완료 기준 섹션.** 이 섹션이 AGENTS.md를 스타일 가이드에서 피드백 루프로 바꾼다. Codex CLI는 작업 끝에 목록의 명령을 실행하고 통과할 때까지 반복한다. 기준이 없으면 언제 끝났는지를 에이전트가 스스로 추론해야 하는데, 추론은 하지만 늘 정확하지는 않다.

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
