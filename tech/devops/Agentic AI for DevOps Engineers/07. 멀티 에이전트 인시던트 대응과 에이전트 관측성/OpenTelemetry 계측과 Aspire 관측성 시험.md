# OpenTelemetry 계측과 Aspire 관측성 시험

이번 실습은 두 부분이다. 먼저 앞서 만든 멀티 에이전트 워크플로 파일을 확장해 로그, 트레이스, 지표를 남기고, 출력을 결정론적으로 평가하는 코드를 넣는다. 이어서 Docker로 독립 실행형 Aspire Dashboard를 띄우고, 계측된 워크플로를 실행해 텔레메트리가 화면에 쌓이는 모습을 확인한다. 계측된 워크플로는 OTLP(OpenTelemetry Protocol, 텔레메트리 전송 규약)로 데이터를 내보낸다. 모든 입력은 저장소의 합성 샘플이다.

완성된 검증본은 원서가 안내하는 Packt 저장소의 `finish/ai/agents/MultiAgentIncidentResponseWorkflowWithObservability.cs`에 고정되어 있다. 새 파일 `MultiAgentIncidentResponseWorkflowWithObservability.cs`를 만들어 앞 버전 위에 쌓는다. 이 문서의 코드는 핵심 줄만 싣는다.

---

## 1. 계측 코드 추가하기 (단계 1~25)

### 1-1. 패키지와 네임스페이스 (단계 1~2)

추가 패키지는 Microsoft.Extensions.Logging 10.0.0, OpenTelemetry 1.15.0, OpenTelemetry.Exporter.OpenTelemetryProtocol 1.15.0, OpenTelemetry.Instrumentation.Http 1.15.0이다. 이 버전들은 고정 커밋의 검증본과 맞춘 것이므로 한 묶음으로 취급하라고 원서가 강조한다. 하나만 올리면 API가 바뀌어 전체를 다시 시험해야 할 수 있다. 네임스페이스는 활동, 시간 측정, 미터용 System.Diagnostics 계열, 그리고 로깅과 OpenTelemetry의 Logs, Metrics, Resources, Trace 계열을 추가한다.

### 1-2. 시작 설정 (단계 3~6)

3. 시작 시 로컬 gRPC 출력을 위해 암호화되지 않은 HTTP/2를 켠다(`Http2UnencryptedSupport` 스위치).
4. 서비스 이름 `genai-incident-workflow`, 소스 이름과 미터 이름 `GenAIDevOps.Observability`를 상수로 정한다.
5. OTLP 엔드포인트를 `OTEL_EXPORTER_OTLP_ENDPOINT`에서 읽고 기본값은 `http://localhost:4317`이다. 프로토콜은 `OTEL_EXPORTER_OTLP_PROTOCOL`이 다른 값을 요구하지 않으면 gRPC다.
6. 공통, 로그, 트레이스, 지표용 OTLP 헤더를 정규화한다. 참조 코드의 `NormalizeOtlpHeaders`는 쉼표나 세미콜론으로 구분된 키/값을 받고, 잘못된 항목은 거부하며, 값을 버리면 경고를 낸다.

### 1-3. 리소스, 소스, 미터 (단계 7~8)

공유 리소스 메타데이터, `ActivitySource`, `Meter`를 만든다. 서비스 이름이 백엔드에 표시되는 리소스 정체성이 된다.

### 1-4. 지표 정의 (단계 9)

미터 카운터와 히스토그램을 초기화한다. 이름은 다음과 같다.

| 이름 | 종류 | 의미 |
|---|---|---|
| ai.workflow.runs | 카운터 | 워크플로 실행 횟수 |
| ai.workflow.failures | 카운터 | 워크플로 실패 횟수 |
| ai.agent.responses | 카운터 | 에이전트 응답 수 |
| ai.evaluation.score | 히스토그램 | 평가 점수 분포 |
| ai.workflow.duration.ms | 히스토그램 | 워크플로 소요 시간(밀리초) |

### 1-5. 로그, 트레이스, 지표 제공자 (단계 10~12)

- 로거 팩토리는 서식이 적용된 메시지와 스코프를 포함하고 구조화된 로그를 OTLP로 내보낸다. 최소 로그 수준은 Information이다.
- 트레이서 제공자는 항상 켜짐 샘플러(`AlwaysOnSampler`)를 쓰고, 애플리케이션 소스와 AI 소스(`Microsoft.Extensions.AI`, `Microsoft.Agents.AI`), HTTP 클라이언트 계측, OTLP 내보내기를 구성한다.
- 미터 제공자는 애플리케이션 미터와 같은 두 AI 미터를 등록하고 같은 OTLP 엔드포인트로 내보낸다.

```csharp
using var tracerProvider = Sdk.CreateTracerProviderBuilder()
    .SetResourceBuilder(resourceBuilder)
    .SetSampler(new AlwaysOnSampler())
    .AddSource(SourceName).AddSource("Microsoft.Agents.AI")
    .AddHttpClientInstrumentation().AddOtlpExporter(/* endpoint, protocol */)
    .Build();
```

### 1-6. 실행 흐름 계측 (단계 13~20)

13. 워크플로 실행 횟수를 1 올리고 "인시던트 워크플로 데모 시작" 로그를 처음 남긴다. 참조 파일에는 주석 처리된 선택 블록 `OTEL_ONLY_TEST`(맥박 확인용)가 있다. 모델 호출 없이 기본 텔레메트리가 백엔드에 닿는지만 보고 싶을 때 임시로 켜고, 전체 실습에서는 꺼 둔다.
14. LLM 연결용 환경 변수를 초기화하고 나머지 로직을 try 블록으로 감싼다.
15. try 안에서 루트 활동을 시작하고 이름과 배포를 식별하는 태그를 달며 워크플로 시작을 로그로 남긴다.
16. 계측된 채팅 클라이언트를 만든다. OpenTelemetry 미들웨어가 사용자 정의 워크플로 스팬에 더해 모델 클라이언트 활동도 기록한다. 핵심은 `.UseOpenTelemetry(... cfg.EnableSensitiveData = true)`를 클라이언트 체인에 끼우는 것이다.
17. 입력 로딩을 `incident.workflow.load-input` 활동으로 감싸 파일 로딩 지연과 실패가 트레이스에 나타나게 한다. 자르기와 프롬프트 로딩은 이전 버전과 같다.
18. 전문가 에이전트 실행을 또 다른 활동으로 감싸 에이전트 수(3)를 태그로 달고 이전처럼 워크플로를 돌린다. 끝에는 완료 로그와 생성된 메시지 수를 남긴다.
19. 결정론적 검증 후 지휘관 결과를 평가한다.
20. 평가 결과를 루트 활동에 `ai.eval.score`, `ai.eval.passed` 태그로 기록한다.

`EnableSensitiveData` 설정은 메시지 내용과 함수 인자 등을 텔레메트리에 노출한다. 합성 교육 데이터를 들여다보려고만 켠 것이다. 실제 운영 워크로드에서는 승인된 데이터 거버넌스 정책이 내용 수집을 명시적으로 허용하지 않는 한 false로 둬야 한다.

### 1-7. 평가 함수 (단계 21~22)

참조 코드는 여덟 개 검사에 정수 가중치를 매겨 총점이 80점 이상이면 통과로 본다. 검사 항목은 아래와 같다.

| 검사 | 가중치 |
|---|---|
| 인시던트 ID 있음 | 10 |
| 경영진 요약 있음 | 15 |
| 유력 원인 있음 | 15 |
| 즉시 조치 있음 | 15 |
| 롤백 권고 있음 | 15 |
| 검증 계획 있음 | 15 |
| 이해관계자 메시지 있음 | 10 |
| 검증 계획이 엔드포인트나 지표 확인을 언급함(`/orders`, error, latency 중 하나 포함) | 5 |

합계는 100점이고 80점 기준이므로, 예를 들어 15점짜리 항목 하나가 비어도 85점으로 통과하지만 두 개가 비면 70점으로 탈락한다. 반환 타입은 `EvaluationCheck`와 `EvaluationSummary`라는 레코드다.

원서는 이 평가가 결정론적인 구조 점검이지 사실 정확성이나 복구 안전성에 대한 완전한 판단이 아니라고 분명히 한다. 운영 평가는 근거 정합성(grounding), 근거 없는 권고, 프롬프트 주입 저항성, 정책 준수, 엄선된 인시던트 데이터셋 대비 회귀 동작까지 시험해야 한다.

### 1-8. 산출물과 마무리 (단계 22~25)

점수 지표를 기록하고 평가 요약을 들여쓴 JSON으로 출력한다. artifacts 디렉터리를 만들어 `incident-response.json`과 `evaluation-summary.json`을 써서, 생성된 응답과 평가가 실행 뒤에도 남게 한다. try 끝에서 성공 완료 로그를 남긴다. catch에서는 실패 카운트 1을 기록하고 실패한 활동을 로그에 남긴 뒤 예외를 다시 던져 프로그램을 끝낸다. finally에서는 스톱워치를 멈추고 소요 시간을 기록하며 트레이스와 미터 제공자를 비우고(flush) 약 2초 기다린 뒤 닫아, 텔레메트리가 모두 내보내지게 한다.

## 2. Aspire Dashboard 띄우고 시험하기

독립 실행형 Aspire Dashboard는 개발과 단기 진단용이다. 텔레메트리를 메모리에 저장하므로 내구성 있는 운영 관측성 플랫폼으로 취급하면 안 된다. 최신 안내는 aspire.dev의 standalone dashboard 문서에 있다.

1. Docker Desktop 또는 호환 컨테이너 런타임을 설치하고 실행 중인지 확인한다.
2. 아래 명령으로 대시보드 컨테이너를 실행한다.

```
docker run --rm -it -p 18888:18888 -p 4317:18889 -p 4318:18890 -d --name aspire-dashboard mcr.microsoft.com/dotnet/aspire-dashboard:latest
```

옵션의 뜻은 다음과 같다. `--rm`은 컨테이너가 멈추면 자동 삭제해 찌꺼기를 남기지 않는다(남겨도 상관없다면 생략 가능). `-it`는 대화형 실행으로 `-i`는 표준 입력 유지, `-t`는 터미널 할당이다. `-d`는 분리 모드로 백그라운드 실행이다. `-p`는 포트 매핑이다. 호스트 18888은 대시보드 화면, 호스트 4317은 컨테이너의 OTLP/gRPC 수신기(18889)로, 참조 에이전트의 기본값 `http://localhost:4317`과 gRPC에 맞는다. 호스트 4318은 OTLP/HTTP 수신기(18890)로, 두 환경 변수로 에이전트를 OTLP/HTTP로 바꿀 때 쓴다. `--name`은 컨테이너 이름이고 마지막 인자는 이미지다. 이미지를 처음 내려받으므로 시간이 걸릴 수 있다.

참고(노트 작성자): 원서 문장에는 "첫 번째 매핑이 호스트 18888을 컨테이너 18888에 연결한다"라고 되어 있다. 명령줄의 `-p 18888:18888`과 일치하므로 그대로 옮겼다.

3. `docker ps`로 컨테이너 ID, 이미지, 실행 시간, 포트를 확인한다.
4. `docker logs aspire-dashboard`로 대시보드 로그인 URL을 얻는다.
5. 로그에 나온 URL을 브라우저에서 연다. 처음에는 비어 있으므로 남아 있는 지표와 트레이스를 지워 깨끗한 상태에서 시작한다(그림 7.5, 빈 대시보드).
6. finish 디렉터리에서 계측된 앱을 실행한다.

```
dotnet run --file ai/agents/MultiAgentIncidentResponseWorkflowWithObservability.cs -- ai/samples/incidents/orderservice-sev2
```

7. 콘솔에는 이전처럼 로그와 최종 인시던트 응답이 나오고 평가 요약도 함께 출력된다. 평가 요약은 artifacts 폴더에도 파일로 저장된다(그림 7.6).
8. 대시보드로 돌아가 Structured logs 화면에서 인시던트 워크플로 시작과 각 전문가의 업데이트 같은 로그된 활동을 본다(그림 7.7, 상관된 워크플로 활동과 스트리밍 업데이트).
9. Traces 화면에서 전문가들, 오케스트레이션, 지휘관이 각각 어디서 시작했는지 앞서 코드에 단 태그로 식별한다. 입력 로딩, 병렬 전문가 실행, 지휘관 종합, 모델 클라이언트 활동이 폭포 모양으로 나열된다(그림 7.8).
10. 관련 스팬의 입력과 출력 메시지를 본다. 메시지 내용이 보이는 것은 이 합성 데모에서 민감 텔레메트리를 켰기 때문이다.

## 3. 운영으로 가기 전에

내구성 있는 운영 모니터링은 독립 대시보드에 의존하지 말고 OpenTelemetry를 Azure Monitor/Application Insights나 Grafana 같은 지원되는 백엔드로 내보내야 한다. .NET OpenTelemetry를 Azure Monitor로 보내는 방법은 Microsoft Learn 문서에 안내되어 있다.

참고(노트 작성자): 원서가 단계 23과 24, 25에 걸쳐 쓴 세부 항목을 위 1-8절에서 하나로 묶었다. 단계 번호는 원서의 번호 체계를 따르되 일부는 한 소절에 합쳤다. 코드 속 줄바꿈이 깨진 부분(예: `!` 뒤에서 끊긴 `string.IsNullOrWhiteSpace`)은 문맥으로 복원해 이해했다.
