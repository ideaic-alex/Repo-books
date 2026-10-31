# AGENTS.md 리뷰 지침과 프로젝트별 설정

AGENTS.md는 팀의 리뷰 기준을 Codex CLI가 모든 표면(로컬 `/review`, GitHub 클라우드 리뷰, codex-action)에서 자동으로 읽는 형태로 담는다. 이 문서는 `## Review guidelines` 섹션을 쓰는 법, 하위 디렉터리에서 규칙을 겹쳐 쓰는 법, 그리고 프로젝트 유형별 권장 설정표를 정리한다.

AGENTS.md는 Linux Foundation 산하 Agentic AI Foundation(AAIF)이 관리하는 열린 표준이다. AAIF는 2025년 12월 Anthropic, Block, OpenAI가 공동 창립해 도구 간 AI 에이전트 설정을 표준화하려는 단체다.

---

## 1. 적용 범위와 우선순위

`## Review guidelines` 섹션은 그 문서의 범위 안에 있는 파일에 대한 모든 리뷰 패스에 적용된다. 루트의 AGENTS.md는 프로젝트 전체에 적용된다. `payments/AGENTS.md`는 `payments/` 아래 모든 파일에 적용되고, 그 파일들에 대해서는 루트보다 우선한다. 이 계층 덕에 저장소 수준에는 일반 기준을, 민감한 하위 시스템에는 전문 기준을 두면서 일반 규칙을 중복해서 쓰지 않아도 된다.

## 2. 잘 짜인 리뷰 지침 예

```markdown
## Review guidelines
- Flag any use of `eval()` or `exec()` as P0.
- Flag direct SQL string concatenation as P0; require parameterised queries.
- Every new HTTP route must use the authentication middleware. Flag violations as P0.
- Do not log PII or user-identifiable data at any log level. Flag violations as P1.
- Treat typos in public-facing documentation as P1.
- New public API methods without docstrings are P1.
- Flag inconsistent error-handling patterns as P2.
```

각 항목은 무엇을 찾을지와 심각도를 함께 적는다. 심각도를 정해 두면 자동 PR 코멘트의 P0/P1 필터와 맞물린다. 마지막 항목은 같은 모듈 안에 예외와 에러 반환이 섞여 있는 경우를 가리킨다.

## 3. 무엇을 넣지 않는가

눈여겨볼 점은 스타일 규칙, import 순서, 포매팅이 빠져 있다는 것이다. 이런 것은 린터 설정에 속한다. 리뷰 지침에 섞으면 신호 대 잡음 비율이 나빠지고, 사람이든 AI든 리뷰어가 지적을 건너뛰도록 길들이게 된다.

## 4. 하위 디렉터리에서 규칙 겹쳐 쓰기

규정 준수 의무가 있는 패키지에는 루트를 건드리지 않고 규칙을 추가한다. 결제 패키지 예시는 다음과 같다.

```markdown
<!-- payments/AGENTS.md -->
## Review guidelines
- Flag any hardcoded card numbers, CVVs, or full PANs as P0 immediately.
- All payment amounts must use the Money type from `lib/money`. Flag raw
  floating-point arithmetic on monetary values as P0.
- Every new payment flow must have a corresponding integration test.
  Flag additions to `payments/flows/` without a matching test file as P1.
```

카드 번호, CVV, 전체 PAN이 코드에 박혀 있으면 즉시 P0, 금액은 `lib/money`의 Money 타입만 쓰고 부동소수점 연산은 P0, 새 결제 흐름에는 통합 테스트가 있어야 하며 없으면 P1이라는 내용이다.

## 5. 프로젝트 유형별 권장 설정 (표 20-1)

프로젝트의 위험 특성에 따라 쓰는 표면, 우선순위, 문턱, 사람이 집중할 곳이 달라진다.

| 프로젝트 유형 | 권장 표면 | AGENTS.md 우선순위 | 엄격도 문턱 | 사람 리뷰의 초점 |
| --- | --- | --- | --- | --- |
| 공개 API 서비스 | pre-commit + 자동 PR 리뷰 | P0: 인증 우회, 인젝션, 데이터 유출. P1: 입력 검증 누락, 문서 없는 엔드포인트 | P0는 커밋 차단, P1은 머지 전 필수 | API 계약의 정확성, 하위 호환성 |
| 내부 도구 | 대화형 /review + 민감한 PR에 수동 `@codex review` | P0: 자격 증명 노출, 확인 없는 파괴적 작업. P1: 에러 처리 누락 | P0는 권고만, 자동 머지 관문 없음 | 사용성, 운영 안전성 |
| 데이터 파이프라인 | 자동 PR 리뷰 + CI codex-action | P0: 마이그레이션 없는 스키마 변경, 로그의 PII. P1: 외부 데이터 null 검사 누락, 하드코딩된 배치 크기 | P0는 CI 차단, P1은 코멘트로 노출 | 데이터 품질 계약, 상하류 영향 |
| 프런트엔드 애플리케이션 | pre-commit + 자동 PR 리뷰 | P0: XSS 경로, 토큰의 안전하지 않은 저장. P1: 접근성 퇴행, 로딩/에러 상태 누락 | P0는 커밋 차단, P1은 머지 전 검토 | UX 일관성, 인터랙션 설계 |
| 보안 민감 라이브러리 | pre-commit + 자동 PR 리뷰 + 전문가 수동 리뷰 | P0: 다른 유형의 모든 항목과 암호 오용. P1: 확립된 패턴에서 벗어난 모든 것 | P0는 커밋과 CI 차단, P1은 명시적 승인 필요 | 위협 모델 정합성, 부채널 노출 |
| 레거시 현대화 | 리팩터링 세션 중 대화형 /review | P0: 동작을 깨는 변경, 사라진 에러 경로. P1: 레거시 안티패턴을 다시 들여오는 새 코드 | P0는 커밋 차단, P1은 추적용 기록 | 기존 동작과의 동등성, 점진적 범위 |

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
