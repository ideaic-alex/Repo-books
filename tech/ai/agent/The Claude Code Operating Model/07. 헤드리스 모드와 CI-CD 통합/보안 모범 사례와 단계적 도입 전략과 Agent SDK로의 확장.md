# 보안 모범 사례, 단계적 도입 전략, Agent SDK로의 확장

CI/CD에서 AI 에이전트를 돌리는 것은 진지하게 다뤄야 할 보안 문제다. 이 문서는 잘못 설정한 헤드리스 작업이 부르는 네 가지 위험, 다섯 겹의 방어(최소 권한, 비밀 관리, 컨테이너 격리, 비용 보호, 감사 로그), 팀이 PR 리뷰를 단계적으로 도입하는 4단계 경로, 그리고 CLI에서 Agent SDK(프로그래밍 인터페이스)로 확장하는 방법을 정리한다. 케이지의 말처럼 이것은 과잉 반응이 아니다.

---

## 1. 잘못 설정한 작업이 부르는 위험

- **기밀 유출**: 에이전트가 .env, config.json, 하드코딩된 자격 증명 파일을 읽어 출력한다. 가정이 아니고 악의적 프롬프트도 필요 없다. "설정을 점검하라"는 요청을 받은 리뷰 에이전트는 기꺼이 그렇게 한다. 원서는 `--allowedTools "Read,Grep"`로 "설정의 문제점을 검토하라"고 시킨 결과 CI 로그에 운영 DB 접속 문자열(계정과 비밀번호 포함)과 결제 비밀 키가 그대로 찍힌 사례를 보여 준다. 이 노트에서는 비밀 값이 든 로그 본문은 싣지 않는다.
- **파괴적 작업**: 악의적인 셸 명령을 실행해 빌드 환경을 망가뜨리거나 코드를 덮어쓴다.
- **통제 불능 비용**: 무한 루프에 빠지거나 무의미한 대량 생성을 유도당해 API 호출 비용이 과다해진다.
- **콘텐츠 오염**: PR/MR 댓글에 환각 내용, 부적절한 발언, 심지어 주입된 공격 페이로드를 출력한다.

방어 전략은 여러 층의 심층 방어(defense-in-depth)로 세운다. 원서 본문은 "네 겹"이라고 소개하지만 이어지는 소제목과 케이지의 노트는 다섯 겹(최소 권한, 비밀 관리, 컨테이너 격리, 비용 보호, 감사 로그)을 말한다. 이 노트는 다섯 겹을 기준으로 한다.

## 2. 다섯 겹의 방어

| 층 | 막는 것 | 핵심 수단 |
|---|---|---|
| 최소 권한 | Claude가 해서는 안 될 일을 하는 것 | `--allowedTools`를 작업별로 최소화 |
| 비밀 관리 | 자격 증명 유출 | 저장소 시크릿 참조, 프롬프트로 비밀 접근 지시 금지 |
| 컨테이너 격리 | 탈출 위험 | `--read-only`, `--tmpfs /tmp`, `--network none` |
| 비용 보호 | 폭주하는 청구서 | 경로 필터링, 동시성 제한, 두 가지 한도 |
| 감사 로그 | 추적 불가 | json 출력을 `tee -a`로 영구 저장 |

### 2-1. 최소 권한 원칙

작업별로 허용 도구를 좁힌다.

- 코드 리뷰: 읽기 전용 `--allowedTools "Read,Grep,Glob"`
- 형식 수정: 읽기와 쓰기 `--allowedTools "Read,Grep,Glob,Edit,Write"`
- Git 작업: 세밀한 Bash 허용 목록 `--allowedTools "Read,Grep,Glob,Bash(git diff *),Bash(git log *)"`

Claude에게 제한 없는 Bash 실행 권한을 절대 주지 않는다. 셸 기능이 꼭 필요한 시나리오에서도 패턴 매칭으로 실행 가능한 명령 범위를 엄격히 제한해야 한다(패턴 속 공백의 의미는 1번 문서 참조).

### 2-2. 비밀 관리

잘못된 방법은 키를 워크플로에 직접 적는 것이다(`ANTHROPIC_API_KEY: "sk-ant-xxx"`). 키가 Actions 실행 로그에 평문으로 남는다. 올바른 방법은 저장소 시크릿을 참조하는 것이다(`${{ secrets.ANTHROPIC_API_KEY }}`). GitHub Actions는 시크릿으로 참조한 값을 로그에서 자동으로 가려 `***`로 보여 준다.

그러나 마스킹이 있어도 프롬프트에서 모델에게 "모든 환경 변수를 나열하라"거나 "설정 세부 정보를 출력하라"고 하면, 모델이 출력 텍스트에 키의 실제 값을 되풀이할 수 있다. 모델이 생성한 이 텍스트는 자동 마스킹으로 잡히지 않아 키가 샌다. 그러므로 프롬프트에서 모델에게 환경 변수나 키 값에 접근, 읽기, 출력을 지시하지 않는다.

### 2-3. 컨테이너 격리

코드 리뷰 작업을 돌릴 고도로 안전한 "샌드박스"를 만드는 GitHub Actions 조각은 `container`에 `image: node:20`과 `options: --read-only --tmpfs /tmp --network none`을 주는 것이다.

- `--read-only`: 파일 시스템을 읽기 전용으로 만들어 쓰기를 막는다. 임시 파일용 쓰기 공간은 `--tmpfs /tmp`로 제공한다.
- `--network none`: 외부 접근이 필요 없는 리뷰 작업에서 네트워크를 완전히 끊는다. Claude는 저장소 안의 파일만 읽을 수 있고 외부와 통신하지 못한다.

참고(노트 작성자): 네트워크를 끊으면 Anthropic API에도 닿지 못하므로, 이 설정이 모델 호출이 필요한 작업과 어떻게 양립하는지는 원서가 설명하지 않는다. 적용 전에 구성 방식(예: 모델 호출을 컨테이너 밖에서 처리)을 따로 검토해야 한다.

### 2-4. 비용 보호

리소스를 아끼는 설정이다. 경로 필터링으로 src 디렉터리의 파일이 바뀔 때만 트리거하고(`paths`에 `'src/**'`, 테스트 파일은 `'!src/**/*.test.*'`로 제외), 동시성 제한으로 같은 PR에는 최신 실행만 남기고 중간 버전은 자동 취소한다(`concurrency.group: claude-${{ github.event.pull_request.number }}`, `cancel-in-progress: true`).

```yaml
on:
  pull_request:
    paths:
      - 'src/**'
      - '!src/**/*.test.*'
concurrency:
  group: claude-${{ github.event.pull_request.number }}
  cancel-in-progress: true
```

경로 필터링과 동시성 제어가 비용 최적화의 1차 방어선이다. 실행 한 번의 자원 소비를 제한하는 것보다 불필요한 트리거를 근원에서 막는 편이 총비용을 줄이는 데 더 효과적이다.

### 2-5. 감사 로그

`claude -p "task" --output-format json | tee -a /var/log/claude-audit.jsonl`처럼 JSON 출력을 파일에 덧붙여 저장한다. JSON 출력에는 session_id, total_cost_usd, num_turns, usage 같은 핵심 감사 필드가 자동으로 들어 있다. 규제가 엄격한 환경이라면 이 로그를 ELK나 Datadog 같은 중앙 로그 시스템에 실시간으로 보내 장기 보관과 심층 분석을 하길 권한다.

### 2-6. 케이지의 노트

다섯 겹의 방어는 "선택 문제"가 아니라 프로덕션의 "필수 문제"다. 최소 권한은 Claude가 해서는 안 될 일을 하지 못하게 하고, 비밀 관리는 자격 증명 유출을 엄격히 막고, 컨테이너 격리는 탈출 위험을 막고, 비용 보호는 폭주하는 청구서를 막고, 감사 로그는 완전한 추적을 보장한다. 한 겹이라도 빠지면 보안 방어에 치명적인 틈이 생긴다.

## 3. 단계적 도입 전략: 4단계

"이 모든 기술적 세부 뒤에, 우리 팀이 PR 리뷰에 헤드리스 모드를 도입하려면 단계별로 어떻게 하나?"라는 물음에 케이지는 4단계 점진 경로를 제안한다.

| 단계 | 이름 | 동작 | 핵심 목표 |
|---|---|---|---|
| 1 | 관찰자 모드(Observer Mode) | Claude는 읽기 전용 분석만 하고 보고서를 내되 어떤 프로세스도 막지 않는다. 보고서는 PR 댓글로 달려 팀원이 참고하거나 무시한다 | 신뢰 구축. 리뷰 품질을 직접 체감하고 한계(오탐이 잦은 상황 등)를 찾아 프롬프트와 매개변수를 개선 |
| 2 | 조언자 모드(Advisor Mode) | 충분한 긍정 피드백이 쌓이면 리뷰 결과를 CI 상태 모니터링에 포함한다. 심각한 문제가 감지되면 CI 상태를 "경고"(노란색)로 표시하되 병합은 막지 않는다. 사람 리뷰어가 보고서를 보고 최종 판단 | 사람과 AI의 협업 |
| 3 | 관문 모드(Gatekeeper Mode) | Claude 리뷰가 코드 병합의 필수 조건 중 하나가 된다. 심각한 보안 문제가 감지되면 CI 상태가 즉시 빨간색이 되어 병합을 막는다. 단, 특정 권한자가 Claude의 차단을 수동으로 넘길 수 있는 "탈출구"를 반드시 둔다(불안정한 테스트 케이스를 건너뛰는 것과 비슷) | 강제 품질 관문 |
| 4 | 능동 수리 모드(Proactive Repair Mode) | Claude가 문제를 찾는 데서 나아가 서식 오류 자동 수정, 빠진 예외 처리 보충, 단위 테스트 생성을 한다. Write 도구 권한을 켜야 하지만 모든 수정은 새 커밋으로 제출해야 하고 PR 작성자의 원래 코드를 직접 수정하는 것은 엄격히 금지 | 자동 수리 |

단계를 나누는 이유는 인내심에 관한 격언이 아니다. 각 단계가 다음 단계에 필요한 증거를 만들어 내기 때문이다. 몇 주치 리뷰 결과가 없으면 진짜 발견과 오탐을 구분할 수 없고, 에이전트가 무엇을 막도록 허용할지 정할 근거가 없다. 각 단계를 증거가 쌓일 만큼(보통 몇 주) 돌리고, 달력이 아니라 기각률(dismissal rate, 개발자가 AI 지적을 무시·기각하는 비율)이 다음 단계로 넘어갈 때를 정하게 하라고 원서는 말한다.

## 4. CLI에서 Agent SDK로

앞 예시는 모두 CLI로 Claude Code를 호출했다. 실제 엔지니어링에서는 Agent SDK(TypeScript, Python 지원)도 있어서, 명령줄 매개변수 대신 프로그래밍 언어로 헤드리스 실행 흐름을 직접 제어할 수 있다. 원서는 TypeScript와 Python 예시를 보여 준다.

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";
for await (const message of query({
  prompt: `Review the code changes in the following files: ${changedFiles.join(", ")}`,
  options: { allowedTools: ["Read", "Grep", "Glob"], maxTurns: 10, maxBudgetUsd: 0.50,
             model: "claude-sonnet-4-6", outputFormat: { type: "json_schema", schema: reviewSchema } },
})) {
  if (message.type === "system" && message.subtype === "init") sessionId = message.session_id;
  if (message.type === "result" && message.structured_output) result = message.structured_output;
}
```

Python 예시는 `from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage`로 가져와 `ClaudeAgentOptions(allowed_tools=["Read","Grep","Glob"], max_turns=10, max_budget_usd=0.50, model="claude-sonnet-4-6")`를 만들고, `async for message in query(prompt=..., options=options)`에서 `ResultMessage`를 만나면 `message.result`를 돌려준다.

CLI 옵션과 SDK 옵션은 대응된다. 이 표는 원서의 두 예시를 나란히 놓고 노트 작성자가 정리한 것이다.

| CLI 옵션 | TypeScript | Python |
|---|---|---|
| `--allowedTools` | allowedTools | allowed_tools |
| `--max-turns` | maxTurns | max_turns |
| `--max-budget-usd` | maxBudgetUsd | max_budget_usd |
| `--model` | model | model |
| `--json-schema` | outputFormat: { type: "json_schema", schema } | (예시에 없음) |

원서 설명은 TypeScript 예시가 "프로세스 내 MCP 서버를 만들어 DB 조회와 알림 전송을 도구로 감싸는" 코드라고 소개하지만 실제 코드는 PR 리뷰 호출이다. 소개 문장과 코드가 맞지 않아 보이며, 이 노트는 실제 코드 내용을 기준으로 정리했다. 코드 사이에 "Kage's notes"(다섯 겹 방어)가 끼어든 조판 때문에 TypeScript 코드가 쪽을 넘어 끊겨 있었고, 앞뒤를 이어 복원했다.

CLI와 Agent SDK의 관계는 curl과 HTTP 클라이언트 라이브러리의 관계와 같다. CLI는 가볍고 편해서 간단한 자동화 스크립트와 CI/CD 파이프라인에 알맞고, Agent SDK는 복잡한 논리가 필요한 상황을 위한 것이다. 이전 리뷰 결과에 따라 다음 프롬프트를 동적으로 바꾸거나, 여러 Claude 호출에 걸친 복잡한 워크플로를 조율하거나, 대규모 애플리케이션에 Claude를 깊이 통합할 때 Agent SDK가 프로그래밍 유연성을 준다. 구체적 사용법은 8장에서 다룬다.

---

## 5. 핵심 정리

- 위험은 기밀 유출, 파괴적 작업, 통제 불능 비용, 콘텐츠 오염이다. 방어는 최소 권한, 비밀 관리, 컨테이너 격리, 비용 보호, 감사 로그의 다섯 겹이다.
- 리뷰는 읽기 전용(`Read,Grep,Glob`), 형식 수정은 `Edit,Write` 추가, Git은 `Bash(git diff *)`, `Bash(git log *)`로 좁힌다. 제한 없는 Bash는 절대 금지다.
- 시크릿은 `${{ secrets.… }}`로 참조하되, 프롬프트에서 모델에게 환경 변수 출력을 시키지 않는다. 자동 마스킹은 모델이 쓴 텍스트를 못 잡는다.
- 컨테이너는 `--read-only --tmpfs /tmp --network none`, 비용은 `paths`와 `concurrency`로 근원에서 줄이고, 감사는 `tee -a /var/log/claude-audit.jsonl`로 남긴다.
- 도입은 관찰자, 조언자, 관문(탈출구 필수), 능동 수리(새 커밋으로만) 순이며, 기각률이 다음 단계를 정한다.
- CLI는 간단한 파이프라인용, Agent SDK(TypeScript, Python)는 복잡한 논리용이다.

<br>
<br>
<br>

[The Claude Code Operating Model](../)
