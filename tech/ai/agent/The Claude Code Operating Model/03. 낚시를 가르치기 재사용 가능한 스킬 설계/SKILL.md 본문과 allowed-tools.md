# SKILL.md 본문과 allowed-tools

앞 문서에서 frontmatter의 트리거와 권한 통제를 이해했으니, 이제 SKILL.md의 본문 설계로 넘어간다. 책은 여기가 스킬이 실제로 힘을 발휘하는 곳이라고 말한다. 핵심 사고방식은 "SKILL.md는 저장소가 아니라 라우터(router, 요청을 알맞은 곳으로 안내하는 길잡이)"라는 것이다.

이 문서는 라우터 사고, 계약형 참조, 500줄 규칙과 리팩터링 신호, 그리고 allowed-tools로 행동을 통제하는 방법(권한 설계 템플릿, Bash 접두어 문법, 과잉 권한의 위험)을 다룬다.

---

## 1. 라우터 사고: 저장소가 아니라 길잡이

흔한 오해는 SKILL.md를 "지식 저장소"로 보고 관련 정보를 전부 욱여넣는 것이다. 올바른 설계는 SKILL.md에 핵심 절차와 라우팅 표만 두고, 상세 지식은 참조하는 여러 파일에 나눠 두는 것이다.

### 1-1. Quick Reference 표

라우팅 설계의 핵심 기법은 Quick Reference 표다. 책의 재무 분석 예는 다음과 같다.

```markdown
## Quick Reference
| Analysis Type | Trigger Keywords | Reference Resource |
| Revenue Analysis | revenue, sales, turnover | reference/revenue.md |
| Cost Analysis | cost, expense, expenditure | reference/costs.md |
| Profitability Analysis | profit, gross margin, net margin | reference/profitability.md |
```

이 표는 세 줄에 약 50토큰밖에 들지 않으면서 Claude를 안내한다. 책은 표가 분석 유형, 트리거 키워드, 참조 자원을 한눈에 보여 주며, Claude가 파일 전체를 한 줄씩 읽고 "매출 질문이면 revenue.md를 보라"는 식으로 추론하게 하는 방식보다 정보 밀도가 최대 10배 높다고 설명한다.

참고(노트 작성자): 책 본문은 이 표가 "다섯 가지 핵심 차원"의 라우팅 기준을 안내한다고 쓰지만, 예시 표의 열은 세 개이며 다섯 가지가 무엇인지는 적혀 있지 않다.

### 1-2. 계약형 참조

보조 파일을 참조할 때는 경로만 나열하지 말고 "계약"을 세워야 한다. Claude가 세 가지를 분명히 알아야 하기 때문이다.

- 언제 로드하는가(트리거 시점)
- 어디를 보는가(자원 위치)
- 무엇을 얻는가(기대 산출)

| 구분 | 예 | 평가 |
|---|---|---|
| 약한 참조 | See `reference/revenue.md` for more details. | Claude가 언제 로드할지, 로드해서 무엇을 할지 알 수 없다 |
| 계약형 참조 | When the user asks about revenue growth, ARPU, or revenue composition: → Load `reference/revenue.md` for calculation formulas and industry benchmarks. | 조건, 경로, 기대 내용이 모두 명시됨 |

책은 이 사상이 서브에이전트 파이프라인의 "인수인계 계약"과 같다고 연결한다. 하류 소비자는 상류의 위치만 아는 것으로는 부족하고, 상류가 무엇을 제공할 수 있는지도 분명히 알아야 한다. 이 내용은 4장에서 다시 만난다.

## 2. 500줄 규칙

Claude Code는 SKILL.md의 길이를 500줄 이내로 유지하라고 권고한다. 샤오빙이 왜 500줄이냐고 묻자 카게는 500줄이 대략 2,000~3,000토큰이며, 스킬 하나를 활성화하는 데 합리적인 컨텍스트 비용이기 때문이라고 답한다. 시스템 프롬프트와 현재 대화 이력과 합쳐도 총 토큰이 관리 가능한 범위에 머문다는 것이다.

500줄을 넘는다면 "참조 자료"와 "라우팅 지침"을 혼동하고 있다는 신호다. 해법은 내용을 더 늘리는 것이 아니라 즉시 리팩터링하는 것이다.

| 리팩터링 신호 | 대응 |
|---|---|
| 공식이나 표준 설명이 큰 덩어리로 있음 | reference/ 디렉터리로 옮긴다 |
| 완전한 예시가 여러 개(하나가 30줄 초과) | examples/ 디렉터리로 옮긴다 |
| 출력 템플릿이 여러 개 | templates/ 디렉터리로 옮긴다 |
| 독립적으로 실행 가능한 로직 | scripts/ 스크립트로 캡슐화한다 |
| 병렬적인 기능 모듈이 여러 개 | 독립된 여러 스킬로 분리를 고려한다 |

## 3. allowed-tools: 지식이 행동을 제약한다

책은 allowed-tools를 스킬 보안 아키텍처의 핵심 필드라고 부르며, 단순한 권한 목록이 아니라 "지식이 행동을 제약해야 한다"는 설계 원칙을 담고 있다고 말한다. 구체적 권한은 스킬이 이해한 업무 논리에 따라 정한다.

- 코드 리뷰 스킬: 코드를 읽기만 하면 되고 수정은 엄격히 금지되므로 읽기 전용 도구만 준다.
- 문서 생성 스킬: 새 파일은 만들어야 하지만 기존 파일은 바꾸면 안 되므로 쓰기 권한만 주고 편집 권한은 명시적으로 금지한다.
- 테스트 실행 스킬: 특정 테스트 명령만 돌리면 되므로 Bash 명령을 정밀하게 제한해 임의 명령 주입을 막는다.

참고(노트 작성자): 앞서 frontmatter 문서에서 본 것처럼 같은 장은 allowed-tools가 도구를 "허용하고 자동 승인하는" 필드이며 제한은 disallowed-tools와 권한 설정이 맡는다고 경고한다. 이 절의 "제약" 서술은 설계 의도를 말하는 것으로 읽고, 실제 차단은 별도 설정으로 보강해야 한다.

### 3-1. 권한 설계 템플릿

책은 스킬 유형별로 최소 권한 원칙을 구현한 설정을 제시한다.

| 스킬 유형 | allowed-tools | 성격 |
|---|---|---|
| 감사형 | Read, Grep, Glob | 엄격한 읽기 전용 |
| 생성형 | Read, Grep, Glob, Write | 쓸 수는 있지만 편집은 불가 |
| 분석형 | Read, Grep, Glob, Bash(python:*) | 읽기 전용에 특정 스크립트 실행 추가 |
| 실행형 | Read, Bash(git status:*), Bash(git add:*), Bash(git commit:*), Bash(npm test:*) | 통제된 명령 화이트리스트 |

### 3-2. Bash의 세밀한 제어 문법

Bash 도구는 접두어 일치 방식으로 실행 가능한 명령을 세밀하게 통제한다. 문법은 `Bash(prefix:*)`이며, prefix는 허용할 명령 접두어, `*`는 뒤따르는 인자의 와일드카드다.

```
Bash(git:*)          # git으로 시작하는 모든 하위 명령 허용
Bash(git log:*)      # git log와 그 인자만 허용, git push 같은 위험 작업은 금지
Bash(npm test:*)     # 테스트 실행만 허용, npm install이나 npm publish 방지
Bash(python:*)       # 모든 Python 스크립트 실행 허용
Bash(./scripts/*:*)  # scripts/ 안의 특정 스크립트 실행 허용
```

Claude가 Bash 명령을 실행하려 하면 시스템은 실행 전 검사를 한다.

1. 접두어 추출: 요청된 전체 명령 문자열을 얻는다.
2. 규칙 매칭: 명령이 설정된 접두어로 시작하는지 본다.
3. 실행 결정: 일치하면 허용하고, 아니면 곧바로 거부하며 권한 오류를 돌려준다.

### 3-3. 정밀 권한 대 과잉 권한

커밋 스킬에는 status, add, commit 세 하위 명령만 열어 주는 것이 정밀 권한이다. 반대로 `Bash(*)`는 전역 와일드카드이며 모든 방어를 포기하는 것과 같다. 책은 보안 측면에서 Bash(*)가 allowed-tools를 아예 설정하지 않은 것과 거의 같고, Claude Code가 호스트 머신의 전체 셸 접근을 얻는 셈이라고 경고한다. `/deploy` 같은 고위험 작업 스킬에서는 치명적이다. 모델이 프롬프트 주입(prompt injection, 외부 입력에 숨은 지시로 모델을 조종하는 공격) 공격을 받으면 공격자가 이 권한으로 키를 훔치거나 운영 데이터를 삭제하거나 백도어를 심을 수 있기 때문이다.

## 4. 핵심 정리

- SKILL.md는 핵심 절차와 라우팅 표만 담고, 상세 지식은 reference/, templates/, scripts/로 분산한다.
- 참조는 "언제, 어디, 무엇"을 밝히는 계약형으로 쓴다.
- 500줄(약 2,000~3,000토큰)을 넘기면 내용을 늘리지 말고 분리한다.
- allowed-tools는 스킬 유형별 최소 권한으로 설계하고, Bash는 `Bash(prefix:*)`로 접두어까지 좁힌다.
- `Bash(*)`는 방어를 포기하는 설정이다.

<br>
<br>
<br>

[The Claude Code Operating Model](../)
