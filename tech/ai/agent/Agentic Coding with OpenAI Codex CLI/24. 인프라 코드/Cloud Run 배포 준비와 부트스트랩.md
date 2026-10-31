# Cloud Run 배포 준비와 부트스트랩

Run or Relax의 배포는 앞의 세 장이 만나는 지점이다. API는 컨테이너이고, Cloud Run은 컨테이너를 돌리다가 아무도 07:02 열차를 묻지 않으면 0개로 줄여 준다. 보드는 정적 파일이라서 Cloud Storage 버킷이 실행 중인 서버보다 훨씬 싼 값에 서빙한다. 둘 다 테라폼이 만들고, 테라폼은 Codex CLI가 쓴다. 이 문서는 첫 배포가 막히기 쉬운 준비 단계, 곧 사전 확인, 컨테이너 시작 명령, 인증과 원격 상태 버킷, 부트스트랩 모듈, 이미지 빌드까지를 다룬다.

---

## 1. 배포 전에 확인할 네 가지 접점

앞선 장들이 남긴 것 중 배포가 곧바로 의존하는 네 가지를 먼저 못 박는다.

1. FastAPI 앱이 `departures.app:app`으로 임포트된다. 컨테이너 시작 명령이 필요로 하는 경로다.
2. Cloud Run은 `$PORT`(기본 8080)에 적힌 포트로 트래픽을 보낸다. 서버는 개발용 기본값이 아니라 `0.0.0.0:$PORT`에 바인딩해야 한다.
3. 보드는 정적 `out/` 디렉터리로 빌드된다(23장의 `output: "export"`). 이 디렉터리가 버킷에 올라간다.
4. 보드는 API 주소를 `NEXT_PUBLIC_DEPARTURES_API_URL`에서 읽는데, 이 값은 빌드할 때 박힌다. API는 `RUN_OR_RELAX_CORS_ORIGIN`으로 보드를 통과시킨다. 이 두 값이 두 서비스의 이음매다. 틀리면 테스트는 전부 초록인데 배포된 보드에는 아무것도 그려지지 않는다.

## 2. 컨테이너 진입점: Procfile

빌드팩(buildpack)은 파이썬 프로젝트를 감지해 Dockerfile 없이 이미지를 만들지만, Cloud Run의 포트에서 웹 서버를 어떻게 띄울지는 짐작하지 못한다. 한 줄짜리 Procfile이 모호함을 없앤다.

```text
# Procfile
web: uvicorn departures.app:app --host 0.0.0.0 --port ${PORT:-8080}
```

`${PORT:-8080}`은 운영에서는 Cloud Run이 주입한 `$PORT`를 쓰고 로컬에서는 8080으로 되돌아간다. 이 줄을 빼먹으면 이미지는 빌드되고 배포도 성공하지만, 컨테이너가 응답하지 않아 Cloud Run이 헬스 체크에서 컨테이너를 죽인다. 인프라 문제처럼 보이지만 실제로는 시작 명령이 없는 것이다.

데이터는 어디서 오는가 하는 질문이 하나 남는다. 실제 Run or Relax라면 열차 시각 API에서 실시간 출발과 지연을 읽겠지만, `timetable.json`과 `delays.json`은 이 장에서 배포할 거리를 만들기 위한 대역(stand-in)일 뿐이다. 버리는 예제 데이터이므로 프로비저닝 없이 이미지 안에 실려 간다. 운영 시스템이라면 서비스가 실제 API를 가리키게 하고, 기본 URL은 설정으로, 키는 Secret Manager에 둔다. 다만 그건 이 장이 맡기엔 큰 일이고 뒤따르는 Codex 작업 방식을 바꾸지도 않는다.

## 3. 인증과 원격 상태 부트스트랩

에이전트는 테라폼을 쓸 뿐 클라우드 자격 증명을 갖지 않으며, 자기 상태가 저장될 버킷도 스스로 만들 수 없다. 둘 다 어떤 모듈이든 적용하기 전에 사람이 한 번 해 두는 설정이다. 이를 건너뛰는 것이 첫 배포가 `terraform init`에서 죽는 가장 흔한 이유다. 먼저 ADC(Application Default Credentials)가 프로젝트를 가리키도록 인증한다.

```bash
gcloud auth login
gcloud auth application-default login
gcloud config set project "$PROJECT_ID"
gcloud auth application-default set-quota-project "$PROJECT_ID"
```

그다음 상태 버킷을 테라폼 밖에서 만든다. 백엔드가 있어야 테라폼이 거기에 상태를 저장할 수 있으므로, 어떤 `terraform apply`로도 풀 수 없는 닭과 달걀 문제다.

```bash
gcloud storage buckets create "gs://${PROJECT_ID}-terraform-state" \
  --project="$PROJECT_ID" --location="$REGION" --uniform-bucket-level-access
gcloud storage buckets update "gs://${PROJECT_ID}-terraform-state" --versioning
```

저장소에는 자리표시자 버킷 이름이 든 `backend.hcl.example`이 들어 있고, 그대로는 쓸 수 없다. 이것을 `backend.hcl`로 복사해 실제로 유일한 버킷 이름을 넣는다. 상태 버킷 이름은 Google Cloud 전체에서 충돌하므로 `PROJECT-terraform-state`를 프로젝트에 맞는 이름으로 바꿔야 한다.

```hcl
# infra/backend.hcl
bucket = "your-project-id-terraform-state"
prefix = "run-or-relax/dev"
```

이제 백엔드를 초기화한다. `backend.hcl`이 바뀔 때마다 `-reconfigure`로 다시 돌린다.

```bash
terraform -chdir=infra init -reconfigure -backend-config=backend.hcl
```

주의할 점이 있다. `terraform validate`는 `terraform init`이 백엔드에서 실패했어도 `Success! The configuration is valid.`를 출력할 수 있다. 로컬 파일의 문법과 프로바이더 스키마만 보기 때문이다. validate가 초록이어도 백엔드가 초기화됐다, 상태 버킷이 존재한다, 자격 증명이 건강하다는 증거는 아니다. 배포 준비 상태는 validate가 아니라 init 결과를 읽고 판단한다.

`init`이 `auth: "invalid_grant"`로 실패하면 HCL이 아니라 인증 문제다. 자격 증명이 오래됐거나, 다른 계정의 것이거나, 환경 변수로 강제된 서비스 계정 키에 가려진 경우다. 앞의 ADC 로그인을 다시 하고, 키가 강제되고 있다면 지운다.

```bash
gcloud auth list                          # 어느 계정이 활성인가
echo "$GOOGLE_APPLICATION_CREDENTIALS"    # 키가 강제되고 있는가
unset GOOGLE_APPLICATION_CREDENTIALS
terraform -chdir=infra init -reconfigure -backend-config=backend.hcl
```

이 소절은 장의 주제를 사람 쪽에서 본 모습이다. 에이전트는 제안하는 쪽에 있고, 실제로 계정을 건드릴 수 있는 유일한 것들인 자격 증명과 상태 버킷은 사람이 준비한다.

## 4. 부트스트랩: API와 이미지 저장소

첫 이미지를 푸시하려면 두 가지가 먼저 있어야 하고, 둘 다 테라폼이 한 번 만든다. 스택이 쓰는 Google API 활성화, 그리고 이미지가 올라갈 Artifact Registry 저장소다. 이를 부트스트랩 모듈로 생성하게 한다.

```text
Create a Terraform bootstrap module that:
- Enables the required Google APIs with google_project_service: Cloud Run,
  Cloud Build, Artifact Registry, IAM, and Cloud Storage
- Creates a google_artifact_registry_repository named run-or-relax (Docker
  format) in the target region. Google-managed encryption is fine for a
  teaching repo, so add an inline checkov suppression for the
  customer-managed-key finding
- Variables for project and region; output the repository path
```

이 모듈은 나머지보다 먼저 적용해야 하고, 이유는 첫 배포에서 실제로 걸리는 순서 함정이다. 스택 전체를 한 번의 `terraform apply`로 적용하면 Cloud Run 서비스와 Artifact Registry 저장소를 함께 계획한다. 그런데 서비스는 저장소가 생기기 전에는 존재할 수 없는 이미지를 참조하므로 apply가 실패한다. 그래서 부트스트랩을 따로 먼저 적용하고(장기적으로는 별도 상태를 가진 별도 테라폼 루트로 두는 편이 깔끔하다), 이미지를 빌드한 다음 나머지를 적용한다.

> 원서 그림 설명(약 506쪽, 글로 풀어 씀): 그림 24-1. Cloud Run 배포 순서. 위에서 아래로 gcloud 로그인과 ADC 인증, 테라폼 밖에서 상태 버킷 만들기(백엔드가 먼저 있어야 한다), terraform init -reconfigure, 1단계 apply -target=module.bootstrap(API와 Artifact Registry 활성화), gcloud builds submit으로 빌드와 푸시(태그가 image_tag와 일치해야 한다), terraform plan -out=tfplan, codex exec로 plan-output.txt 검토, 2단계 terraform apply(버킷은 만들지만 채우지는 않는다), gcloud storage cp로 보드 업로드가 이어진다. 점선 화살표 둘은 1단계 apply에서 빌드로 가는 "저장소가 이미지보다 먼저 있어야 한다"와 빌드에서 2단계 apply로 가는 "이미지가 두 번째 apply보다 먼저 있어야 한다"를 뜻한다.

그림은 배포가 정해진 순서로 이어지는 과정임을 보여 준다. 사람이 인증하고 테라폼 밖에서 상태 버킷을 만든 뒤 `init`, 부트스트랩 모듈의 1단계 apply, 이미지 빌드와 푸시, plan, 에이전트의 계획 검토, 2단계 apply, 보드 업로드 순으로 간다. 점선은 닭과 달걀 의존성이다. 저장소가 있어야 이미지를 만들 수 있고, 이미지가 있어야 두 번째 apply가 가능하다.

```bash
# phase 1: APIs and the registry only
terraform -chdir=infra apply -target=module.bootstrap
```

## 5. .gcloudignore와 이미지 빌드

빌드 전에 `.gcloudignore`를 추가한다. 그래야 Cloud Build가 가상 환경, node 모듈, 캐시, 로컬 테라폼 상태가 아니라 소스만 올린다. 이 차이가 파일 수백 개와 1GB의 차이다.

```text
# .gcloudignore (핵심 줄만)
.git
.venv/
.uv-cache/
**/__pycache__/
frontend/node_modules/
frontend/.next/
frontend/out/
infra/.terraform/
infra/backend.hcl
```

원서의 목록에는 이 밖에도 `.mypy_cache/`, `.pytest_cache/`, `.ruff_cache/`, `infra/*.tfvars`, `infra/tfplan`, `infra/plan-output.txt`가 한 줄씩 들어 있다. 가상 환경과 각종 캐시, 프런트엔드 빌드 산출물, 그리고 상태·계획·변수 파일처럼 올릴 필요가 없거나 올리면 안 되는 것을 모두 제외하는 목록이다.

이제 빌드하고 푸시한다. 태그는 장식이 아니다. Cloud Run 모듈이 읽는 `image_tag` 변수와 일치해야 하고, 틀리면 테라폼이 존재하지 않는 태그를 배포한다.

```bash
gcloud builds submit --pack image=REGION-docker.pkg.dev/PROJECT/run-or-relax/api:v1 .
```

기본 빌드팩은 22장에서 정한 프로젝트의 파이썬 3.14 고정을 읽어 별도 설정 없이 빌드한다. 런타임을 최신으로 유지해야 이 단계가 지루하게 넘어간다.

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
