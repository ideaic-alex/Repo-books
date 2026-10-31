# CI 에이전트 안전 전략과 관측

자율성이 올라가면 잘못된 실행의 대가도 커진다. 그래서 CI에서 돌리는 에이전트의 안전장치는 선택이 아니다. 이 문서는 네 가지 안전 원칙, 비용과 감사를 위한 파이프라인 관측(토큰 사용량, 조향 메타데이터, 스레드 맥락), 긴 세션을 안정적으로 유지하는 WebSocket keepalive, 그리고 휴대폰으로 승인하는 원격 연결 패턴을 정리한다.

---

## 1. CI 에이전트를 위한 안전 전략

- 승인 모드를 알맞게 고른다. 읽기 전용 분석에는 `untrusted`, 파일을 쓰는 에이전트에는 `on-request`를 쓴다. `approval_policy=never`(`-c approval_policy=never`로 전달)는 러너가 완전히 격리(air-gapped)된 경우에만 쓴다. 모드, 샌드박스 수준, 이름 붙은 프로필은 5장에서 자세히 다뤘다.
- PR 내용은 신뢰할 수 없는 입력으로 취급한다. diff는 파일로 쓰고 프롬프트에서는 그 파일을 가리킨다. PR 제목이나 본문을 프롬프트에 그대로 끼워 넣지 않는다. 남이 쓴 글에 숨은 지시가 섞여 있으면 프롬프트 인젝션(prompt injection) 공격이 되기 때문이다.
- 시크릿을 관리한다. `OPENAI_API_KEY`는 암호화된 저장소 시크릿에 넣고, 필요한 단계에만 환경 변수로 내려 준다.
- 권한을 최소로 한다. `permissions` 블록으로 GitHub 토큰 범위를 필요한 만큼만 연다.

## 2. 파이프라인 관측

구조화된 출력은 기업용 CI/CD에 필요한 관측성을 준다. 비용 귀속(어느 잡이 얼마나 썼는가), 감사 기록, 청구 투명성이다.

### 토큰 사용량 추적

`codex exec`의 턴이 끝날 때마다 나오는 `turn.completed` 이벤트의 `usage` 객체에 토큰 수가 있다. 항목은 `input_tokens`, `cached_input_tokens`, `output_tokens`, `reasoning_output_tokens`다. 별도 계측 도구 없이 이 데이터만으로 잡별 비용을 나눌 수 있다.

### 조향(steering) 메타데이터

조향 메타데이터는 세션 동안 에이전트의 행동에 영향을 준 설정을 기록한다. 활성 모델, 추론 강도, 승인 모드, 어떤 AGENTS.md 파일이 읽혔는지가 들어 있다. CI/CD에서는 에이전트가 무엇을 했는가뿐 아니라 왜 그런 결정을 했는가에 대한 감사 기록이 된다.

### 스레드 맥락 비정규화

분석 페이로드는 스레드 맥락을 비정규화(denormalise)해서 담는다. 여러 데이터 소스를 조인하지 않고도 세션을 가로질러 조회할 수 있다는 뜻이다. 하루에 Codex CLI 잡을 수백 개 돌리는 조직이라면 다음 같은 집계 분석이 가능하다.

- 어느 저장소가 토큰을 가장 많이 쓰는가
- 어느 잡 종류가 출력 대비 추론 토큰 비율이 가장 높은가
- 모델을 낮췄을 때(`gpt-5.5`에서 `gpt-5.4-mini`로) 품질 손실 없이 가장 많이 절약되는 곳은 어디인가

### 리뷰 결과와 함께 분석 정보 보내기

20장의 구조화된 코드 리뷰 패턴에 관측을 더하면 전체 그림이 나온다. 아래는 이벤트를 파일에 모은 뒤 `jq`로 마지막 `turn.completed`의 `usage`를 뽑아 대시보드 엔드포인트로 보내는 구성의 핵심이다.

```yaml
- name: Run Codex review with analytics
  run: |
    codex exec --json -s read-only -c approval_policy=untrusted \
      "Review the PR diff for correctness and security." \
      | tee /tmp/review-events.jsonl
- name: Ship analytics to dashboard
  run: |
    jq -s '{repo: "${{ github.repository }}", job: "review",
      usage: ([.[] | select(.type == "turn.completed") | .usage] | last)}' \
      /tmp/review-events.jsonl
```

원서 예시에서는 `jq` 결과를 `curl -X POST -H "Content-Type: application/json" -d @-`로 `secrets.ANALYTICS_ENDPOINT`에 보낸다. `OPENAI_API_KEY`는 리뷰를 실행하는 단계의 `env`로 준다.

## 3. 장시간 세션의 안정성

긴 CI 세션의 안정성을 높이는 기능이 둘 있다.

### WebSocket keepalive ping

바깥으로 나가는 exec-server WebSocket 클라이언트가 주기적으로 keepalive ping을 보낸다. 프록시, 로드 밸런서, 방화벽이 유휴 연결을 말없이 끊는 것을 막아 준다. 이것이 없으면 여러 시간짜리 리팩터링, 전체 테스트 스위트 생성, 밤샘 의존성 감사 같은 긴 `codex exec`와 `codex remote-control` 세션이 유휴 시간이 프록시 타임아웃(기업 인프라에서 흔히 60~120초)을 넘는 순간 조용히 끊길 위험이 있다.

keepalive가 적용되는 연결은 세 종류다.

1. 직접 연결하는 exec-server 클라이언트
2. 랑데부(rendezvous) 방식의 하니스와 실행기(executor) 연결
3. 다중화된(multiplexed) 원격 실행기 스트림

들어오는(inbound) axum 연결은 수동 상태 그대로다. 결과적으로 기업 리버스 프록시나 클라우드 로드 밸런서 뒤에서 도는 CI 세션도 타임아웃 설정을 따로 고치지 않아도 된다.

### CI 트리거로서의 원격 연결

원격 연결을 쓰면 개발자가 파이프라인이 돌리는 에이전트 작업을 ChatGPT 모바일 앱에서 시작하고 지켜볼 수 있다. 이 패턴은 `codex remote-control`과 맞물리는데, 이 기능은 원서 집필 시점에 실험적(experimental)으로 표시되어 있었다. 흐름은 네 단계다.

1. CI 러너가 액세스 토큰으로 인증한 `codex remote-control`로 헤드리스 Codex CLI 세션을 시작한다.
2. 에이전트가 승인을 요구하면 개발자 휴대폰에 알림이 온다.
3. 개발자가 폰에서 대기 중인 동작을 살펴보고 승인하거나 거부한다.
4. 러너에서 에이전트가 실행을 이어 간다.

여기서 3단계 승인 체인이 나온다. 위험이 낮은 작업은 자동 승인하고, 중간 위험은 모바일로 올리고, 높은 위험은 데스크톱 리뷰에 맡긴다. CI가 던져 놓고 잊는 방식에서 개발자가 자리에 없어도 감독하는 방식으로 바뀐다. 기업용 액세스 토큰(17장 참고)과 합치면 모든 실행이 워크스페이스 신원에 묶여 거버넌스와 감사에 쓸 수 있다.

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
