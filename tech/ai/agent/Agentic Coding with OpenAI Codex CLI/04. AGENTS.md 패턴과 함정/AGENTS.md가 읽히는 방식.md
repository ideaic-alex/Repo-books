# AGENTS.md가 읽히는 방식

프롬프트는 세션이 끝나면 사라진다. 새 세션은 항상 빈 상태로 시작하기 때문에, "커밋 전에 make test를 돌려라", "src/generated/ 아래 생성 파일은 건드리지 마라" 같은 팀의 약속을 매번 입으로 말해 줘야 한다. 열 명이 하루에 수십 번씩 Codex CLI 세션을 열면 이 반복이 꽤 큰 마찰이 된다.

AGENTS.md는 이 틈을 메우는 일반 Markdown 파일이다. 저장소에 커밋해 두거나 홈 디렉터리에 개인 기본값으로 두면, Codex CLI가 세션을 시작할 때마다 자동으로 읽는다. 이 문서에서는 파일이 어떤 순서로 찾아지고 합쳐지는지, 어떤 모양으로 쓰면 좋은지 정리한다.

---

## 1. AGENTS.md란 무엇인가

AGENTS.md에는 정해진 스키마가 없다. 어떤 Markdown이든 유효하다. 이 파일이 특별한 이유는 내용이 아니라 읽히는 시점에 있다. Codex CLI는 사용자의 프롬프트보다 먼저, 매 실행마다 자동으로 이 파일을 모델 컨텍스트에 넣는다.

원문은 이 파일을 AI 협업자의 "성문 헌법"에 빗댄다. 어떤 작업을 시키든 항상 적용되는 상시 규칙, 프로젝트 관례, 넘지 말아야 할 선을 적어 두는 곳이라는 뜻이다. 3장이 프롬프트 한 번을 잘 쓰는 기술이었다면, 4장은 모든 프롬프트를 반복 없이 더 낫게 만드는 기반 시설을 다룬다.

## 2. 탐색 체인: 넓은 범위에서 좁은 범위로

Codex CLI는 파일시스템을 가장 넓은 범위에서 가장 좁은 범위로 훑으며 찾은 AGENTS.md를 전부 이어 붙여 하나의 지침 묶음을 만든다. 순서는 다음과 같다.

| 단계 | 위치 | 성격 |
|---|---|---|
| 1 | `~/.codex/AGENTS.override.md` 또는 `~/.codex/AGENTS.md` | 개인 전역 기본값 |
| 2 | `<git-root>/AGENTS.override.md` 또는 `<git-root>/AGENTS.md` | 저장소 전체 팀 규칙 |
| 3 | git 루트와 현재 디렉터리 사이 각 디렉터리의 `AGENTS.override.md` 또는 `AGENTS.md` | 중간 경로별 규칙 |
| 4 | `<cwd>/AGENTS.override.md` 또는 `<cwd>/AGENTS.md` | Codex CLI를 실행한 디렉터리의 규칙 |

각 단계에서 `.override.md`가 있으면 같은 단계의 일반 `.md`보다 우선한다. 이어 붙인 결과에서 내용이 충돌하면 더 가까운 파일이 이긴다. 홈 디렉터리 파일은 개인 기본값, 저장소 루트 파일은 팀 기본값, 하위 디렉터리 파일은 서비스별 규칙을 맡고, 각 층은 위쪽 규칙에 덧붙이거나 더 조이거나 뒤집을 수 있다.

> 원서 그림 설명(약 84쪽, 글로 풀어 씀): AGENTS.md 탐색 체인 그림. 전역 파일, 저장소 루트 파일, 중간 디렉터리 파일, 현재 디렉터리 파일 순으로 위에서 아래로 내려가고, 마지막에 하나의 지침 묶음으로 합쳐진다.

그림 4.1은 이 흐름을 위에서 아래로 보여 준다. 맨 위가 전역(개인 기본값), 그다음이 저장소 루트(팀 기본값), 중간 디렉터리들, 현재 디렉터리(서비스별 규칙) 순이다. 위에서 아래로 갈수록 범위가 좁아지고, 네 단계가 마지막에 하나의 지침 묶음으로 합쳐진다. 충돌하면 가까운 파일이 이기고, 각 단계에서는 `.override.md`가 `.md`를 이긴다는 설명이 맨 아래 칸에 적혀 있다.

## 3. 알아 둘 동작 방식

처음부터 알고 있으면 나중에 헤매지 않는 사실이 몇 가지 있다.

- 체인은 실행할 때마다 새로 만들어진다. 캐시가 없으니 파일을 고친 뒤 비워 줄 것도 없다.
- 빈 파일은 조용히 건너뛴다. 체인이 끊기거나 초기화되지 않는다.
- 불러온 파일 전체의 합계 크기는 `project_doc_max_bytes` 설정으로 제한된다. 기본값은 32 KiB이고, 한도를 넘는 부분은 알림 없이 잘린다. 원문은 이 값이 Codex CLI 소스의 `PROJECT_DOC_MAX_BYTES` 상수(32 * 1024)라고 밝힌다.
- 같은 단계에서는 `.override.md`가 일반 `.md`보다 우선한다.

시작점이 현재 디렉터리가 아니라 git 루트라는 점도 중요하다. `services/payments/` 안에서 Codex CLI를 실행해도 탐색은 저장소 루트에서 시작해 중간 디렉터리를 거쳐 현재 위치까지 내려온다. 그래서 저장소 루트의 규칙은 아무리 깊은 하위 디렉터리에서 일해도 항상 적용된다.

## 4. 파일은 어떻게 생겼나

필수 구조는 없다. 그래도 잘 작동하는 파일은 대개 몇 개의 짧은 섹션으로 나뉘고, 모델이 모호함 없이 따를 수 있는 명령형 문장으로 쓰여 있다. 원문의 TypeScript 웹 서비스 예시는 다음 섹션들로 이루어진다.

- 프로젝트 개요: Node.js REST API, TypeScript, Vitest로 테스트, GitHub Actions로 AWS Lambda에 배포한다는 한두 줄 설명
- Commands: `npm run build`, `npm test`(Vitest, 커밋 전에 반드시 통과), `npm run lint`, `npm run typecheck`
- Commit conventions: Conventional Commits 사용(`feat:`, `fix:`, `chore:` 등), 영향받는 모듈로 범위 지정(`feat(cart): add coupon validation`), `main`에 직접 커밋하지 않고 항상 PR로
- Style: TypeScript strict 모드, `any`와 `// @ts-ignore` 금지, import는 그룹 안에서 알파벳순(ESLint가 강제), 비동기 함수는 `Promise<T>`를 명시적으로 반환
- Constraints: `src/generated/`는 OpenAPI로 자동 생성되므로 수정 금지, 새 의존성은 PR 설명에 목록으로 적지 않고는 설치 금지, 새 엔드포인트에는 `tests/integration/`에 통합 테스트 추가

```markdown
# Project: Checkout Service
## Commands
- Build: `npm run build`
- Test: `npm test` (runs Vitest; must pass before any commit)
## Constraints
- Do not modify files under `src/generated/`
```

Commands 섹션은 파일 맨 위에 두는 것이 좋다. Codex CLI는 자기 작업을 검증할 방법을 정할 때 이 섹션을 반복해서 들춰 본다. 테스트 명령을 빨리 찾을수록 명령을 지어낼 가능성이 줄어든다.

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
