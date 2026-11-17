# 실습 2 다단계 CI 파이프라인

실습 1의 리뷰는 한 단계짜리였다. 실제 프로젝트에서는 Claude가 여러 단계에 참여해야 할 수 있다. 먼저 코드 품질을 보고, 다음으로 보안 취약점을 훑고, 마지막으로 테스트 커버리지를 확인하는 식이다. 단계마다 중점 영역, 도구 권한 제한, 비용 예산이 다르다. 이 문서는 세 개의 잡(job, 워크플로 안의 실행 단위)으로 이루어진 다단계 AI 파이프라인의 설정값을 모두 적고, 그 뒤에 숨은 세 가지 설계 원칙(모델 등급화, 예산 등급화, 병렬 실행)을 정리한다.

---

## 1. 워크플로 개요

워크플로 이름은 Multi-Stage AI Pipeline이고, 트리거는 `pull_request`의 `types: [opened, synchronize]`다. 세 잡 모두 `runs-on: ubuntu-latest`이며 `actions/checkout@v4`로 시작하고, env에 `ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}`와 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC: "1"`를 준다. Claude는 `npx @anthropic-ai/claude-code -p ...`로 호출한다(전역 설치 없이 npx로 실행하는 점이 실습 1의 CLI 방식과 다르다).

## 2. 단계별 설정

| 항목 | 1단계 lint-check | 2단계 security-scan | 3단계 coverage-check |
|---|---|---|---|
| 목적 | 빠른 형식 검사 | 심층 보안 검토 | 테스트 커버리지 분석 |
| 의존성(needs) | 없음 | lint-check | lint-check |
| 프롬프트 | src/ 아래 코드가 프로젝트 코딩 표준을 따르는지 확인 | 심층 보안 스캔, OWASP Top 10 중심 | 테스트 커버리지가 부족한 코드 경로 분석 |
| --model | claude-haiku-4-5 | claude-sonnet-4-6 | claude-sonnet-4-6 |
| --max-turns | 3 | 10 | 8 |
| --max-budget-usd | 0.05 | 1.00 | 0.50 |
| --allowedTools | "Read,Grep,Glob" | "Read,Grep,Glob" | "Read,Grep,Glob" |
| --output-format | text | json | text |
| 그 밖 | 없음 | --append-system-prompt와 --json-schema, 결과를 security-report.json으로 저장 | 없음 |

2단계의 `--append-system-prompt`는 "You are an application security expert. Please focus only on security vulnerabilities."다. `--json-schema`는 `vulnerabilities` 배열을 요구하고, 각 항목은 `severity`(string), `description`(string), `file`(string) 필드를 가지며 `severity`와 `description`이 필수다. 최상위 필수 필드는 `vulnerabilities`다. 출력은 `> security-report.json`으로 저장한다.

```yaml
security-scan:
  runs-on: ubuntu-latest
  needs: lint-check          # 형식 검사를 통과한 뒤에만 실행
  steps:
    - uses: actions/checkout@v4
    - run: |
        npx @anthropic-ai/claude-code -p "Conduct an in-depth security scan, focusing on OWASP Top 10" \
          --model claude-sonnet-4-6 --max-turns 10 --max-budget-usd 1.00 \
          --allowedTools "Read,Grep,Glob" --output-format json > security-report.json
```

참고(노트 작성자): 위 코드는 2단계의 골격만 보인 것이며 `--append-system-prompt`와 `--json-schema`, env는 표에 따로 적었다. 원서 YAML은 들여쓰기가 모두 사라져 있고, 일부 줄(`npx ... -p "..." \` 뒤 이어쓰기)이 쪽 경계에서 끊겨 있다. 키 구조와 GitHub Actions 문법에 맞춰 복원했다.

## 3. 세 가지 설계 원칙

### 3-1. 모델 등급화: 일에 맞는 모델

형식 검사나 lint 분류처럼 기계적이고 명세가 분명한 검사는 더 깊은 추론의 덕을 보지 못하므로 Haiku 같은 작고 저렴한 모델로 충분하다. 많은 컨텍스트를 붙들고 추론해야 하는 일(보안 검토, 커버리지 분석)에서는 Sonnet 같은 큰 모델이 값을 한다. 구체적인 모델 이름은 바뀔 것이다. 그러나 방법은 바뀌지 않는다. 같은 작업을 두 등급으로 실제 PR 열 개에 돌려 사람이 검토한 기준선과 결과를 비교하고, 탐지율 차이로 큰 모델이 그 배수만큼 값어치가 있는지 판단한다.

### 3-2. 예산 등급화: 모든 실행에 상한

모든 실행에 `--max-budget-usd`로 상한을 건다. 적정 상한은 책에서 베낄 숫자가 아니다. 프롬프트, 모델, 저장소가 에이전트에게 읽게 만드는 컨텍스트 양에 따라 다르다. 기준선을 잡는 방법은 작업을 열 번 실행해 JSON 출력의 `total_cost_usd`를 읽고, 관찰된 최댓값보다 높게 상한을 두는 것이다. 이 예시의 수치($0.05는 사소한 검사, $1은 깊은 검사)는 저자들이 측정한 규모의 자릿수일 뿐 권장치가 아니다.

### 3-3. 병렬 실행

security-scan과 coverage-check는 둘 다 `needs: lint-check`가 걸려 있어 첫 단계가 끝나야 시작한다. 이 두 단계 사이에는 의존성이 없으므로 GitHub Actions가 자동으로 병렬 실행한다. 1단계가 실패하면 뒤의 두 단계는 돌지 않아, 값싼 검사로 비싼 검사를 걸러 내는 구조이기도 하다. 이 마지막 해석은 `needs`의 의미에서 이끌어 낸 것이며 원서는 병렬 실행만 직접 언급한다.

---

## 4. 핵심 정리

- 세 잡은 lint-check(haiku, 3턴, $0.05, text), security-scan(sonnet, 10턴, $1.00, json + 스키마), coverage-check(sonnet, 8턴, $0.50, text)다. 도구는 모두 읽기 전용(`Read,Grep,Glob`)이다.
- security-scan과 coverage-check는 `needs: lint-check`이므로 1단계 뒤에 병렬로 돈다.
- 모델 등급은 실제 PR 열 개로 탐지율을 비교해 결정하고, 예산 상한은 열 번 실행해 관찰한 `total_cost_usd` 최댓값보다 높게 둔다. 책의 숫자는 규모의 예시일 뿐이다.
- 단계마다 모델, 시스템 프롬프트, 출력 형식, 예산, 라운드를 따로 정한다.

<br>
<br>
<br>

[The Claude Code Operating Model](../)
