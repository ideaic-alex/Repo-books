# AI 엔진 준비와 Azure OpenAI 프로비저닝

3장이 조직 차원의 거버넌스를 다뤘다면, 4장은 구현으로 들어간다. 목표는 AI를 그냥 보조 도구로 쓰는 데서 그치지 않고 전달 시스템에 의도적이고 전문적으로 통합하는 것이다. 이 장이 끝나면 프로젝트는 AI를 통제된 파이프라인의 일부로 갖게 된다.

이 문서는 장 전체의 준비 단계를 다룬다. 실습에 필요한 환경, 어떤 AI 엔진을 쓸지 고르는 기준, Azure OpenAI 리소스를 만들고 모델을 배포하는 절차, 그리고 접속 정보를 GitHub 환경 시크릿에 넣는 방법이다.

---

## 1. 장의 구성과 기술 요구 사항

이 장은 다음 순서로 진행된다. AI 엔진 준비, 결정적 AI 워크플로 단계 설계, 재사용 가능한 컴포지트 액션 만들기, 프롬프트와 입력 복잡도 줄이기, AI 비용과 성능 관리, 관측성과 피드백, 안전한 통합 패턴, AI 증강 ChatOps다. 8개 주제는 이 노트의 문서 8개와 그대로 대응한다.

특별한 로컬 하드웨어는 필요 없다. AI 호출은 Azure OpenAI가 처리하고 자동화는 GitHub 호스트 러너(GitHub가 제공하는 실행 서버)에서 돈다. 필요한 것은 다음과 같다.

- Git, 코드 편집기(Visual Studio Code, Visual Studio, Rider 등), 브라우저가 있는 컴퓨터와 GitHub, Azure 포털, Microsoft Foundry에 닿는 인터넷
- YAML, GitHub Actions, 풀 리퀘스트(PR) 워크플로에 대한 기본 지식
- GitHub Actions가 켜진 저장소, `.github/workflows` 아래 워크플로 파일을 만들거나 고칠 권한, 저장소 환경과 시크릿을 설정할 권한
- Microsoft Foundry와 Azure OpenAI 모델에 접근 가능한 Azure 구독

예제 코드는 Packt의 GitHub 저장소 `Agentic-AI-for-DevOps-Engineers`에 있고 완성본은 `finish` 디렉터리다. 핵심 작업 파일은 다섯 개다.

| 파일(finish 기준) | 역할 |
|---|---|
| .github/workflows/release-ai.yml | 릴리스 노트 워크플로 |
| .github/azure-openai-chat/action.yml | 재사용 Azure OpenAI 컴포지트 액션 |
| ai/prompts/release-notes.prompt.md | 결정적 프롬프트 |
| .github/workflows/chatops-ai.yml | ChatOps 워크플로 |
| ai/prompts/chatops.prompt.md | ChatOps 프롬프트 |

릴리스 노트 워크플로는 Azure OpenAI 시크릿으로 릴리스 노트를 만든다. ChatOps 워크플로는 같은 Azure OpenAI 시크릿에 GitHub 토큰을 더해 AI 응답을 PR에 게시한다.

참고(노트 작성자): 원서의 파일명에는 하이픈 대신 비분리 하이픈 문자가 섞여 인쇄되어 있다. 노트에서는 실제 사용되는 일반 하이픈으로 통일했다. 또 원서가 릴리스 노트 워크플로가 시크릿으로 "AI 응답을 PR에 게시한다"고도 적은 문장은 ChatOps 설명이 겹쳐 들어간 것으로 보여, 릴리스 노트는 초안 릴리스를 만드는 것으로 이해했다.

## 2. 환경 시크릿 준비

GitHub에 `devops-dev`라는 환경(environment)을 만들고 아래 네 개를 환경 시크릿으로 둔다.

| 시크릿 이름 | 용도 |
|---|---|
| AZURE_OPENAI_ENDPOINT | Azure OpenAI 엔드포인트 URL |
| AZURE_OPENAI_API_KEY | Azure OpenAI API 키 |
| AZURE_OPENAI_DEPLOYMENT | Azure OpenAI 배포 이름 |
| GH_CHATOPS_TOKEN | ChatOps 워크플로가 PR에 응답을 게시할 때 쓰는 토큰 |

## 3. AI 엔진 고르기

Microsoft Foundry와 Azure OpenAI 모델이 유일한 선택지는 아니다. 원서는 대안을 이렇게 비교한다.

- OpenAI 공개 API: OpenAI 모델에 직접 접근한다. Azure OpenAI 모델 대부분을 직접 쓸 수 있고, Azure 구독이 필요 없으며 SDK 지원이 넓다. 하지만 이 프로젝트는 기업이 통제하는 CI/CD 시스템과 Azure 우선 조직을 모델링하므로 덜 이상적이다. 개인 엔지니어, 작은 스타트업, 개념 증명(PoC)에는 공개 API도 여전히 훌륭한 선택이라고 원서는 덧붙인다.
- Anthropic Claude: 공개 API나 Amazon Bedrock으로 접근한다. 추론 능력과 안전 통제가 강하고 토큰 한도가 높기로 알려져 있다. 그러나 AWS나 Anthropic 의존성이 생기고 Microsoft 생태계와는 덜 맞는다.
- AWS Bedrock: Claude, Llama 등 여러 모델 계열에 접근한다. AWS 중심 환경에 잘 맞고 이 장의 개념 대부분을 AWS 스택에 옮길 수 있다. Azure 중심 프로젝트에서는 구조상 어색하다.
- LLM 자체 호스팅: Llama 같은 모델을 가상 머신, 쿠버네티스 클러스터, 온프레미스 장비에서 돌린다. 완전한 통제가 가능하고 데이터가 환경 밖으로 나가지 않아 엄격한 데이터 거주 요건에 중요하다. 그러나 GPU 인프라 비용, 확장 복잡성, 운영 부담이 모두 DevOps의 몫이라 일반적으로 DevOps 실무자보다 ML 팀에 어울린다.

결론은 엔터프라이즈 통제 모델과 Azure 우선 환경에 맞는 Azure OpenAI다.

## 4. Azure OpenAI 프로비저닝 절차

Azure 계정과 리소스를 만들 권한이 이미 있다고 가정한다.

1. Azure 포털에서 OpenAI를 검색해 새 리소스를 만든다. 포털 흐름에서 권장하는 Foundry를 쓴다.
2. 양식을 채운다. 리소스 그룹은 프로젝트 앞부분에서 쓴 것과 같게 하고, 예제의 리소스 이름은 `genai-devops-openai`, 리전은 가용성에 따라 고르며, 기본 프로젝트 이름은 리소스 이름과 맞춘다. 검토 후 만들고 배포를 확인한다.
3. 리소스가 만들어지면 열어서 Foundry 포털로 간다. 화면이 기대와 다르면 상단의 New Foundry 스위치로 화면을 전환한다.
4. Foundry 포털에서 `gpt-4o-mini`를 검색해 기본 설정으로 배포한다. 추론, 수학, 멀티모달 추론을 지원해 실습에 충분하다. 본인 상황에 가장 적절하고 쓸 수 있는 버전을 쓰라는 원서의 메모가 있다.
5. 배포 후 세 값을 모은다. 배포 이름은 Foundry에서 보이며 예제에서는 `gpt-4o-mini`다. URL과 키는 Azure 포털의 Foundry 리소스에서 Resource Management, Keys and Endpoint로 들어가면 있다.

## 5. GitHub에 값 저장

1. 저장소 설정의 Secrets and variables로 간다.
2. 시크릿을 넣기 전에 환경(예제는 `devops-dev`)을 만든다.
3. 환경 시크릿으로 `AZURE_OPENAI_ENDPOINT`(포털의 엔드포인트 값), `AZURE_OPENAI_API_KEY`(키), `AZURE_OPENAI_DEPLOYMENT`(Foundry의 배포 이름)를 추가한다.

이렇게 하면 워크플로가 YAML이나 저장소에 비밀 값을 하드코딩할 필요가 없다. 원서는 이것이 표준 DevOps 위생이라고 말한다. 값은 자리표시자로만 다루고, 실제 엔드포인트와 키는 어디에도 적지 않는다.

## 6. 핵심 정리

- 실습은 Azure OpenAI와 GitHub 호스트 러너로 돌아가 특별한 로컬 사양이 필요 없다.
- 엔진 후보는 공개 OpenAI API, Claude, Bedrock, 자체 호스팅이며 이 프로젝트는 엔터프라이즈 통제와 Azure 우선 때문에 Azure OpenAI를 쓴다.
- 배포 모델은 gpt-4o-mini이고 배포 이름, URL, 키 세 값을 모은다.
- 세 값과 ChatOps 토큰은 devops-dev 환경 시크릿으로 두어 하드코딩을 피한다.

<br>
<br>
<br>

[Agentic AI for DevOps Engineers](../)
