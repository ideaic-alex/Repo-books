# Terraform MCP 서버와 GitOps

스택이 서고 나면 두 가지 보강이 남는다. 하나는 낡은 프로바이더 지식으로 인한 환각을 사전에 막는 Terraform MCP 서버이고, 다른 하나는 적용 경계를 정책이 아니라 구조로 만드는 GitOps다. 이 문서는 두 보강의 설정과 쓰는 방식, 그리고 둘이 공유하는 원칙인 "읽기는 열고 적용은 막는다"를 설명한다.

---

## 1. 낡은 프로바이더 지식을 막는 MCP 서버

지금까지 한 가지 실패 유형은 사후에 잡았을 뿐 예방하지는 못했다. 바로 낡은 프로바이더 지식이다. AGENTS.md는 규칙을 담고 스캐너는 안전하지 않은 출력을 잡지만, 에이전트가 더는 존재하지 않는 리소스 인자를 지어내는 것은 둘 다 막지 못한다. 동작하는 경로가 갖춰진 뒤에 이를 단단하게 만드는 보강이 HashiCorp의 공식 Terraform MCP 서버다. 이 서버는 Codex CLI를 포함한 모든 MCP(Model Context Protocol) 클라이언트에게 모델의 학습 시점 스냅숏이 아니라 Terraform Registry에 대한 실시간 접근을 준다. MCP 설정 자체는 8장에서 다뤘고, 인프라에서 내려야 할 결정은 어떤 도구를 노출할지다.

Google 프로바이더는 변동이 크기 때문에 실시간 조회의 효과가 가장 크다. 에이전트가 장 앞부분에서 걸려 넘어진, 이름이 바뀐 리소스를 짐작하지 않고 `google_cloud_run_v2_service`의 현재 인자를 확인한다. 서버를 프로젝트의 `.codex/config.toml`에 추가하고 `enabled_tools`로 범위를 좁혀서 에이전트에게 읽기 전용 레지스트리 조회만 보이게 한다.

```toml
[mcp_servers.terraform]
command = "docker"
args = ["run", "-i", "--rm", "hashicorp/terraform-mcp-server"]
enabled_tools = [
  "search_providers", "get_provider_details", "get_latest_provider_version",
  "search_modules", "get_module_details", "get_latest_module_version",
  "search_policies", "get_policy_details",
]
```

이 도구들은 환각을 낳는 질문에 답한다. 리소스가 실제로 받는 인자가 무엇인지, 프로바이더나 모듈의 최신 버전이 무엇인지, 모듈이 검증된 것인지, 어떤 정책이 적용되는지다. 에이전트는 추측하는 대신 조회한다.

## 2. 열어 두지 말아야 할 도구

이 서버에는 HCP Terraform과 Terraform Enterprise를 위한 워크스페이스 관리 도구도 들어 있고, 실행(run) 생성과 apply 또는 폐기 같은 동작이 포함된다. 이들은 적용 경계를 넘는다. 따라서 에이전트가 무인으로 도는 프로필의 `enabled_tools`에서는 빼야 한다. 이 장이 되풀이하는 패턴 그대로다. 읽기는 노출하고 적용은 보류한다. 레지스트리 조회는 자동화해도 안전하지만 실행을 일으키는 것은 그렇지 않다.

## 3. GitOps: 적용 경계를 구조로 만든다

지금까지는 모든 경계를 정책으로 강제했다. AGENTS.md의 금지, 샌드박스 모드, 사람이 거치는 파이프라인 단계다. GitOps는 이를 아키텍처로 강제하며, 에이전트가 지시를 지키느냐에 의존하지 않으므로 더 강하다.

GitOps에서는 Git이 단일 진실 공급원(single source of truth)이고, 조정(reconciliation) 컨트롤러가 커밋된 내용을 계속 적용한다. 에이전트는 클러스터나 프로젝트를 건드리지 않는다. 쓰는 것은 커밋이나 풀 리퀘스트뿐이고 적용은 컨트롤러가 한다. Google Cloud에서는 쿠버네티스 상태를 맞추는 Config Sync가 될 수도 있고, `main`에 머지되면 `terraform apply`를 돌리는 Cloud Build 트리거가 될 수도 있다. 어느 쪽이든 인프라를 바꾸는 것은 프롬프트를 입력하는 행위가 아니라 머지하는 행위다. 이 장이 설정으로 지키던 경계가 시스템의 속성이 된다. 자격 증명이 없고 출력이 커밋뿐인 에이전트는 어떤 프롬프트를 받아도 apply를 할 수 없다.

그래서 GitOps는 에이전트가 만드는 인프라에 특히 잘 맞는다. 에이전트가 만드는 결과물인 테라폼 변경, 쿠버네티스 오버레이, 환경 승격 수정은 반복적이고, 스키마가 정해져 있고, 머지되기 전에 검증할 수 있다.

## 4. 여러 환경을 한 번에 만들기: 출력 스키마

환경 여러 개를 한꺼번에 온보딩할 때는 출력 스키마를 가진 `codex exec`가 파이프라인이 파일로 나누고 커밋할 수 있는 구조화된 출력을 낸다.

```bash
codex exec \
  --sandbox workspace-write \
  --output-schema envs-schema.json \
  "Read environments.yaml, which lists each environment with its project id and \
   region. Generate the per-environment tfvars and backend config for the Run or \
   Relax stack, following the GitOps conventions in AGENTS.md."
```

에이전트가 작업 사본에 파일을 쓰면 CI가 검증하고 풀 리퀘스트를 연다. 사람이 머지하고, 그 뒤에야 컨트롤러 또는 머지로 트리거되는 `terraform apply`가 변경을 반영한다. 신경 써서 정해야 할 곳은 동기화 정책이다. 비운영 환경은 자가 치유(self-heal)와 정리(prune)를 자동으로 돌려도 되지만, 운영 리소스를 지울 수 있는 변경은 부수적인 수정이 아니라 그 자체로 검토받는 변경으로 다룬다.

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
