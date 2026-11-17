# 헤드리스 모드와 CI/CD 통합

이 장은 Claude Code를 대화형 도구에서 사람 없이 돌아가는 자동화 부품으로 바꾸는 헤드리스 모드를 다룬다. 먼저 -p 옵션과 출력 형식, 비용 가드레일, 도구 권한, 실행 제어의 네 축 매개변수를 배우고, 유닉스 파이프라인과 스트리밍 출력, 세션 관리를 익힌다. 이어 GitHub Actions의 공식 액션과 CLI 직접 호출, 다단계 CI 파이프라인을 실습한다.

그다음 프로덕션 환경 변수 체크리스트와 CI에서의 MCP 설정, GitLab CI, Jenkins, 로컬 스크립트로의 이식, 다섯 겹 보안 방어와 4단계 도입 전략, Agent SDK로의 확장을 정리한다. CLI 옵션 이름, 환경 변수 이름, 수치는 원서 표기를 그대로 적었다.

---

## 1. 핵심 요점

- 헤드리스 모드는 `claude -p`로 시작하지만 `--allowedTools` 없이는 승인 대기로 멈춘다. 사람이 하던 권한 승인, 품질 점검, 프로세스 제어를 매개변수로 못 박는 것이 핵심이다.
- 네 축은 출력 형식(`--output-format` text, json, stream-json), 비용(`--max-turns`, `--max-budget-usd`), 도구 권한(`--allowedTools` 화이트리스트 우선), 실행 제어(`--model`, `--fallback-model`, `--append-system-prompt`, `--json-schema`)다.
- stdin 파이프로 다른 도구와 조합하고, 세션은 기본 비저장이라 `--resume`, `--continue`, `--fork-session`으로 맥락을 잇는다.
- GitHub Actions는 공식 액션 `anthropics/claude-code-action@v1`(옵션은 `claude_args`)과 CLI 직접 호출 두 방식이다. 직접 호출은 비용 표시, `<VERDICT>` 판정 관문, 경로 필터링을 준다.
- 다단계 파이프라인은 단계별로 모델(haiku, sonnet), 예산($0.05, $1.00, $0.50), 출력 형식을 달리하고 `needs`로 병렬 실행한다.
- CI에는 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1`, `DISABLE_AUTOUPDATER=1` 등을 설정하고 MCP는 `--mcp-config`와 `--strict-mcp-config`를 쓴다.
- GitLab CI, Jenkins, 로컬 `review.sh`는 같은 옵션 묶음을 재사용한다.
- 방어는 최소 권한, 비밀 관리, 컨테이너 격리, 비용 보호, 감사 로그의 다섯 겹이고, 도입은 관찰자, 조언자, 관문, 능동 수리의 4단계다.

---

## 2. 문서 목록

- [비대화형 전환과 핵심 매개변수 4축](비대화형 전환과 핵심 매개변수 4축.md): -p, 대화형과의 차이, 출력 형식, 비용 가드레일, 도구 권한, 실행 제어
- [유닉스 파이프라인과 스트리밍 출력과 세션 관리](유닉스 파이프라인과 스트리밍 출력과 세션 관리.md): 파이프 조합, stream-json 이벤트, --resume과 --fork-session
- [실습 1 GitHub Actions 자동 코드 리뷰](실습 1 GitHub Actions 자동 코드 리뷰.md): 공식 액션과 직접 CLI 호출 워크플로
- [실습 2 다단계 CI 파이프라인](실습 2 다단계 CI 파이프라인.md): 세 단계 잡, 모델·예산 등급화, 병렬 실행
- [CI 환경 구성 프로덕션 체크리스트와 MCP 설정](CI 환경 구성 프로덕션 체크리스트와 MCP 설정.md): 환경 변수, 완성 템플릿, --mcp-config
- [플랫폼 간 통합 GitLab CI와 Jenkins와 로컬 스크립트](플랫폼 간 통합 GitLab CI와 Jenkins와 로컬 스크립트.md): GitLab CI, Jenkins, review.sh
- [보안 모범 사례와 단계적 도입 전략과 Agent SDK로의 확장](보안 모범 사례와 단계적 도입 전략과 Agent SDK로의 확장.md): 다섯 겹 방어, 4단계 도입, Agent SDK
- [요약과 핵심 개념](요약과 핵심 개념.md): 장 전체 흐름, 핵심 개념 표, 자주 놓치는 점, 토론 질문

<br>
<br>
<br>

[The Claude Code Operating Model](../)
