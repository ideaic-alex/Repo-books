# 헤드리스 실행 codex exec

지금까지는 사람이 화면을 보면서 Codex CLI를 한 단계씩 확인하며 썼다. CI/CD 파이프라인(코드를 합치고 검증하고 배포하는 자동화 흐름)에서는 사람이 없다. 에이전트가 혼자 돌다가 끝나야 한다. 이렇게 화면 없이 도는 방식을 헤드리스(headless) 실행이라고 부른다.

이 장의 모든 패턴은 `codex exec` 명령 하나 위에 올라간다. GitHub Action이든 GitLab 파이프라인이든 셸 스크립트든, 속을 열어 보면 결국 `codex exec`를 부르고 있다. 이 문서는 그 명령의 CI용 옵션과 사용 요령을 정리한다.

---

## 1. codex exec가 하는 일

`codex exec`는 프롬프트 문자열 하나를 받아서 에이전트를 끝까지 돌리고, 종료 코드(exit code)로 결과를 알려 준다. 성공이면 0, 실패면 0이 아닌 값이다. 파이프라인 단계가 성공했는지는 이 종료 코드로 판단한다.

원서는 이 장 전체의 주제를 이렇게 정리한다. 에이전트가 파이프라인 안에서 도는 구조에서는 어떤 모델을 쓰느냐보다 파이프라인을 어떻게 설계했느냐가 더 중요하다. 그래서 이 장은 모델 얘기보다 권한, 격리, 출력 형식, 검증 같은 설계 얘기가 대부분이다.

## 2. CI에서 중요한 옵션

### 승인 정책과 샌드박스

승인 모드(`untrusted`, `on-request`, `never`)와 샌드박스 수준(`read-only`, `workspace-write`, `danger-full-access`)은 5장에서 자세히 다뤘다. CI에서는 TUI(터미널 화면) 메뉴 대신 명령줄에서 지정한다. 두 가지 조합이 기본이다.

| 목적 | 옵션 조합 |
| --- | --- |
| 자율 작업(파일 수정 포함) | `-c approval_policy=never` + `-s workspace-write` |
| 읽기만 하는 분석 | `-c approval_policy=untrusted` + `-s read-only` |

### 모델 고정

`--model`로 모델을 박아 두면 실행마다 같은 모델을 쓰므로 결과를 재현하기 쉽다. 기본값이 바뀌어도 파이프라인이 흔들리지 않는다.

### --json 이벤트 스트림

`--json`을 주면 출력이 JSONL(한 줄에 JSON 객체 하나)로 나온다. 실행은 `thread.started` 이벤트로 시작하는데, 여기에 스레드(대화 기록 한 묶음)의 `thread_id`가 들어 있다. 턴이 끝날 때마다 `turn.completed` 이벤트가 나오고, 여기에 토큰 사용량이 담긴다.

```json
{"type":"thread.started","thread_id":"019ec094-7865-7bf0-b1a4-7a12da9c0e40"}
{"type":"turn.completed","usage":{"input_tokens":4821,"cached_input_tokens":0,"output_tokens":612}}
```

각 줄이 그 자체로 완결된 객체이고 호출별 시간과 토큰 지표를 담고 있다. 그래서 뒤 단계가 출력 전체를 메모리에 모으지 않고도 이벤트를 하나씩 처리할 수 있다. 이것이 파이프라인 비용 감시의 기초다. 토큰 수를 관측 시스템에 보내고, 한 워크플로가 예산을 넘으면 알림을 걸면 된다. 자세한 활용은 `CI 에이전트 안전 전략과 관측.md`에서 다시 다룬다.

### --output-schema와 -o

`--output-schema`는 에이전트의 마지막 응답을 JSON Schema 모양으로 제한한다. `-o`(`--output-last-message`)와 같이 쓰면 결과가 파일로 떨어진다. 텍스트에서 JSON을 오려 내는 파싱 작업 없이, 검증된 JSON을 다음 단계가 바로 읽을 수 있다.

```bash
codex exec "Analyse src/ for security vulnerabilities" \
 --output-schema ./schemas/vuln-report.json \
 -o ./reports/vulnerabilities.json \
 -c approval_policy=untrusted
```

이 출력 계약(스키마)이 단계 사이를 잇는 접착제 역할을 한다.

## 3. 세션 이어서 하기 (codex exec resume)

`codex exec resume`은 이전 세션을 다시 연다. 파일을 읽은 기록, 도구 호출, 추론 내용까지 대화 맥락이 그대로 살아 있다. 그래서 앞 단계에서 확인된 작업 위에 다음 단계를 쌓는 다단계 CI를 만들 수 있다.

```bash
SESSION=$(codex exec --json "Migrate auth module to OAuth2" \
 -s workspace-write -c approval_policy=never \
 | jq -r 'select(.type=="thread.started") | .thread_id')
codex exec resume "$SESSION" "Run the test suite and fix any failures" \
 -s workspace-write -c approval_policy=never
```

1단계에서 마이그레이션을 만들고 `thread_id`를 뽑아 두었다가, 2단계에서 같은 스레드를 이어서 테스트를 돌리고 실패를 고치는 흐름이다.

- `--last`를 쓰면 세션 ID를 따로 기억하지 않아도 가장 최근 세션을 대상으로 삼는다.
- `codex exec resume`도 `--output-schema`를 받는다. 그래서 개발자 PC에서 대화형으로 탐색한 결과를 구조화된 출력으로 바로 파이프라인에 넘길 수 있다.
- 원격 실행기(remote executor)는 별도 레지스트리 자격 증명 없이 표준 Codex 인증으로 등록한다. 원격 실행을 쓰는 CI/CD 설정이 그만큼 단순해진다.

## 4. 표준 입력으로 맥락 넘기기

외부 데이터를 stdin(표준 입력)으로 에이전트에 바로 먹일 수 있다.

```bash
git diff origin/main...HEAD | codex exec "Review this diff for correctness and security issues" \
 -c approval_policy=untrusted --output-schema ./schemas/review.json
```

이것이 PR 리뷰 워크플로의 기본 모양이다. 세 요소가 각자 역할을 맡는다.

- diff가 범위가 좁은 맥락을 준다.
- `approval_policy=untrusted`가 파일 수정을 막는다.
- 구조화된 출력이 리뷰 결과를 기계가 읽을 수 있게 만든다.

큰 코드베이스는 모듈 하나당 세션 하나로 잘게 나눈다. 전체를 한 세션에 몰아넣지 않는 편이 낫다.

> 경고: 포크(fork)한 저장소에서 온 PR이 트리거하는 워크플로에서는 `--dangerously-bypass-approvals-and-sandbox`(별칭 `--yolo`)를 절대 쓰지 않는다. 외부인이 보낸 코드가 원격 코드 실행(RCE) 취약점으로 이어진다.

## 5. 비TTY 환경의 write_stdin 제한

CI 러너, Docker 컨테이너, 파이프 입력처럼 TTY(터미널 장치)가 없는 환경에서 `codex exec`를 돌리면 `write_stdin` 도구를 쓸 수 없다. 에이전트가 실행 중인 프로세스의 stdin에 글을 쓸 수 없다는 뜻이다. 키보드 입력을 기다리는 대화형 프로그램은 그 자리에서 멈춰 버린다.

피하는 방법은 세 가지다.

1. 대화형 입력 대신 `echo "input" | command`처럼 파이프로 입력을 준다.
2. 도구가 질문을 하지 않도록 인자나 환경 변수로 설정을 받게 한다.
3. 정말 대화형일 수밖에 없는 도구는 expect 방식의 래퍼(wrapper)로 감싼다.

가장 좋은 해법은 CI용 프롬프트를 처음부터 대화형 도구를 쓰지 않도록 설계하는 것이다.

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
