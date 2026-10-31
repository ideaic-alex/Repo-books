# Cloud Run 서비스와 checkov 예외

부트스트랩과 이미지 푸시가 끝나면 실제 서비스를 올릴 차례다. 이 단계는 운영 중인 인프라를 바꾸므로 테라폼의 일이고, 에이전트의 일은 그 테라폼을 쓰는 것이다. 이 문서는 Cloud Run 서비스 모듈의 프롬프트, 두 서비스를 잇는 값, 계획 검토와 apply 이후 보드 업로드, 남겨 두는 checkov 지적 목록, 예외 주석의 위치 규칙, 그리고 Cloud Run이 부족할 때의 GKE 선택지를 다룬다.

---

## 1. Cloud Run 서비스 모듈 프롬프트

```text
Create a Terraform module that deploys the Run or Relax API to Cloud Run,
with:
- A google_cloud_run_v2_service running the image
  REGION-docker.pkg.dev/PROJECT/run-or-relax/api at a variable image_tag
- The container listening on port 8080
- A dedicated service account (least privilege), not the default Compute SA
- Scaling from 0 to a max of 4 instances
- The RUN_OR_RELAX_CORS_ORIGIN env var set to the board's origin (scheme and
  host only, e.g. https://BUCKET.storage.googleapis.com, no path)
- A public invoker binding (roles/run.invoker for allUsers): the board calls
  the API directly from the browser, so the service is intentionally public
- Variables for project, region, image_tag, and cors_origin
- An output for the service URL
```

이 프롬프트의 두 줄이 장 사이의 연결을 맡고 있고, 배포가 보통 여기서 깨진다.

- **`RUN_OR_RELAX_CORS_ORIGIN`**은 FastAPI 서비스가 CORS 미들웨어를 위해 읽는 환경 변수다(22장). 사람이 방문하는 `index.html` URL이 아니라 경로 없는 origin(스킴과 호스트, `https://BUCKET.storage.googleapis.com`)을 원한다. 보드 버킷의 origin을 넣으면 브라우저의 교차 출처 요청이 허용된다. 비워 두거나 전체 페이지 URL을 넣으면 배포된 보드의 모든 요청이 차단되는데, 백엔드 테스트는 전부 통과한다. 그래서 보드 버킷 모듈은 사람용 `site_url`과 API용 origin, 두 값을 출력한다.
- 이 모듈이 출력하는 **Cloud Run 서비스 URL**은 보드를 빌드할 때 `NEXT_PUBLIC_DEPARTURES_API_URL`로 쓴 값이다(23장).

두 서비스는 하드코딩한 문자열이 아니라 테라폼의 출력과 변수를 통해 서로를 찾는다. 그 덕에 같은 구성으로 개발과 운영 복사본을 `.tfvars`만 다르게 해서 세울 수 있다.

공개 invoker 바인딩은 일부러 남겨 두는 checkov 지적 중 하나다. `allUsers`에게 열린 Cloud Run 서비스는 보통 위험 신호지만, 이 서비스는 읽기 전용 출발 전광판이라서 예외 처리가 정직하고 검토자도 이유를 볼 수 있다. 버킷 때와 마찬가지로 도구는 목록화할 수 있는 것을 잡고, 의도는 사람이 채운다.

## 2. 계획 전에 검증한다

`infra/`에 결정적 도구를 먼저 돌린다. Google 룰셋은 순서가 있어서 `tflint --init`이 플러그인을 설치해야 `tflint`를 쓸 수 있다.

```bash
terraform fmt -recursive infra
terraform -chdir=infra init -backend=false
terraform -chdir=infra validate
tflint --chdir=infra --init
tflint --chdir=infra
checkov -d infra --compact
```

여기서 `init -backend=false`는 오프라인 경로다. 자격 증명도 상태 백엔드도 없이 문법과 프로바이더 스키마를 검증하며, 에이전트의 루프에 필요한 바로 그것이다. 실제 배포에는 부트스트랩 단계의 백엔드가 설정된 `init`을 쓴다. 어느 쪽이든 `terraform init`은 프로바이더 플러그인을 내려받고 `.terraform.lock.hcl`을 쓴다. 이 락 파일을 커밋해야 모든 머신과 CI가 같은 프로바이더 버전을 쓴다.

샌드박스가 걸린 에이전트 환경은 프로바이더 다운로드와 플러그인 설치를 막는 경우가 있다. 이때 `terraform init`, `terraform validate`, `tflint --init`, checkov의 메타데이터 조회가 멈추거나 실패할 수 있다. 그러면 네트워크 접근을 승인하거나 일반 터미널에서 검증 단계를 돌린다. 설정이 틀린 것이 아니라 도구가 레지스트리에 닿지 못한 것이다.

## 3. 계획, 검토, 적용, 업로드

배포 전에 계획을 만들고 검토한다. 앞에서 본 경계의 안전한 쪽 루프와 같다.

```bash
terraform -chdir=infra plan -out=tfplan -no-color > plan-output.txt
codex exec -a untrusted -s read-only "Review plan-output.txt. Confirm
the Cloud Run service, its service account, the IAM invoker binding, the
Artifact Registry repository, and the static-site bucket are created as
expected, and flag anything else."
```

사람이 검토 결과를 읽고 `terraform apply`를 실행한다. 이것이 2단계 apply이며, 이제 Cloud Run 서비스가 참조하는 이미지가 존재한다. 이 apply는 버킷을 만들지만 채우지는 않는다. 빌드한 보드를 올리는 일은 프로비저닝과 일부러 분리된 별도의 콘텐츠 배포 단계이고, 23장의 정적 `out/` 디렉터리가 테라폼이 방금 만든 버킷과 만나는 유일한 지점이다.

```bash
gcloud storage cp -r frontend/out/* gs://$(terraform -chdir=infra output -raw board_bucket)/
```

이제 Run or Relax는 Cloud Run URL 뒤에서 `GET /departures`에 응답하고, 보드는 버킷에서 그것을 그린다. 순수한 판정 함수에서 시작한 이야기가 배포된 서비스로 끝났고, 그 과정에서 에이전트는 한 번도 적용 경계를 넘지 않았다.

## 4. 기대하는 checkov 지적

이 스택에서 checkov가 깨끗하다는 말은 지적이 0건이라는 뜻이 아니라 설명되지 않은 지적이 0건이라는 뜻이다. 몇 건은 매번 나오고, 작은 공개 교육용 배포에서는 그 대상이 의도된 것이므로 남겨 두는 것이 맞다. 원칙은 스캐너를 통째로 끄지 않고, 검토자가 읽을 수 있는 주석으로 하나씩 인라인 예외를 두는 것이다. 예상되는 목록이 표 24-1이다.

| 지적 | 대상 | 결정 |
| --- | --- | --- |
| 공개 읽기(`allUsers`에 `roles/storage.objectViewer`) | 보드 버킷 | 인라인으로 이유를 달아 예외. 의도된 공개 웹사이트다 |
| 공개 접근 차단 미적용 | 보드 버킷 | 인라인으로 이유를 달아 예외. 공개 사이트에는 이 예외가 필요하고, 로그 버킷은 차단을 유지한다 |
| 접근 로그 싱크 미설정 | 보드 버킷 | 교육용 배포에서는 예외. 운영에서는 버킷 로깅을 켠다 |
| 고객 관리 암호화 키 없음 | Artifact Registry 저장소 | 예외. 여기서는 Google 관리 암호화로 충분하며, 정책상 필요하면 CMEK를 쓴다 |
| 공개 invoker(`allUsers`에 `roles/run.invoker`) | Cloud Run 서비스 | 인라인으로 이유를 달아 예외. 보드가 쓰는 공개 읽기 전용 API다 |

이 표에 없는 지적은 알려진 예외가 아니라 진짜 고쳐야 할 문제다. 게이트가 주려는 신호가 바로 그것이다. 소음이 목록으로 정리돼 있으니 새로 생긴 실패가 눈에 띈다.

## 5. 예외 주석의 위치

주석 위치는 보기보다 중요하다. `#checkov:skip` 주석은 적용 대상 리소스 블록 안, 본문의 첫 줄에 있어야 한다. 리소스 선언 위쪽 줄에 두면 안 된다. 원서가 쓰는 Checkov 3.3.0은 블록 안에 있는 예외만 인식하고, 블록 위의 주석은 무시해서 지적이 그대로 나온다.

```hcl
resource "google_storage_bucket_iam_member" "board_public_read" {
  #checkov:skip=CKV_GCP_28:Intentional public website; the board is read-only static content
  bucket = google_storage_bucket.board.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"
}
```

체크 ID 뒤의 글이 사유이고, 검토자가 읽는 부분이다. 예외 하나에 리소스 하나, 승인할 수 있는 이유 하나라는 규율이 위 표의 목록을 정직하게 유지한다.

## 6. Cloud Run으로 부족할 때: GKE

Cloud Run은 Run or Relax에 딱 맞는다. 0까지 줄어드는 상태 없는 HTTP 서비스이기 때문이다. 서비스가 이를 넘어서면, 즉 꾸준한 트래픽 때문에 0으로 줄이는 이점이 사라지거나, 사이드카가 필요하거나, 세밀한 네트워킹이 필요하거나, 요청-응답이 아닌 워크로드를 돌릴 때는 목적지가 쿠버네티스가 되고, 산출물은 Cloud Run 리소스가 아니라 매니페스트가 된다. Codex를 쓰는 방식은 같고 검증 명령만 달라진다. AGENTS.md에 다음을 더한다.

```text
## Test commands (Kubernetes)
- `kubectl apply --dry-run=client -f .` for syntax validation
- `kubeconform -strict .` for schema validation
```

에이전트는 Cloud Run 모듈 때와 같은 요구 사항 프롬프트(레플리카 수, 리소스 한도, `/healthz` 프로브, ConfigMap 참조)로 Deployment, Service, HorizontalPodAutoscaler를 만들고, 커밋 전에 kubectl과 kubeconform 명령으로 검증한다. 이 탈출구는 실제로 있지만 거의 필요 없다. 습관이 아니라 Cloud Run의 한계가 이동을 강요할 때만 쓴다.

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
