# 인프라 코드

앞선 두 장에서 만든 Run or Relax의 백엔드와 프런트엔드는 노트북에서만 돈다. 이 장은 그 스택을 Google Cloud Run과 Cloud Storage에 올리는 과정을 Codex CLI와 함께 따라가면서, 인프라 코드를 에이전트와 다룰 때 무엇이 달라지는지 설명한다. 인프라는 잘못된 한 줄이 운영 환경을 내리거나 삭제할 수 있어서, 에이전트는 계획하고 제안하고 사람이 검토해서 적용하는 구조가 기본이다.

장 전체는 에이전트를 제안하는 쪽에 붙잡아 두는 방법을 다룬다. AGENTS.md, 훅, 샌드박스, CI/CD, GitOps가 그 경계를 어떻게 겹겹이 지키는지, 그리고 환각과 낡은 프로바이더 지식을 결정적 도구와 MCP 서버로 어떻게 줄이는지 살펴본다.

---

## 1. 핵심 요점

- 인프라는 폭발 반경이 크므로 에이전트는 계획, 초안, 제안까지만 하고 `terraform apply`는 사람이 실행한다.
- 인프라용 AGENTS.md는 `infra/` 같은 하위 디렉터리에 두고, 테라폼과 스캐너 명령, 그리고 apply 금지만 적는다.
- 문서의 금지는 권고일 뿐이므로 `PreToolUse` 훅으로 `terraform apply`, `terraform destroy`, `gcloud run deploy`를 구속력 있게 막는다.
- tflint와 checkov를 세션 안에서 돌려 깨끗하게 종료될 때까지 반복시키고, 이를 `/goal`로 감싼다. 의도된 공개는 인라인 예외로 남긴다.
- 계획 검토(`codex exec -a untrusted -s read-only`)가 가장 가치 큰 패턴이고, 리팩터링은 변경 없는 계획을 목표로 한다.
- 첫 배포에는 인증, 상태 버킷, Procfile, 부트스트랩 선행 적용 같은 사람 몫의 전제 조건이 있다.
- Terraform MCP 서버는 읽기 도구만 노출해 환각을 줄이고, GitOps는 경계를 구조로 만든다.
- 드리프트 감지 등 2일차 운영은 읽기 전용 `codex exec` 파이프라인으로 돌리고 수정은 사람이 승인한다.

---

## 2. 문서 목록

- [인프라 코드가 에이전트에게 어려운 이유](%EC%9D%B8%ED%94%84%EB%9D%BC%20%EC%BD%94%EB%93%9C%EA%B0%80%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%EC%97%90%EA%B2%8C%20%EC%96%B4%EB%A0%A4%EC%9A%B4%20%EC%9D%B4%EC%9C%A0.md): 폭발 반경, 환각, 학습 목표, 세 단계 대응 전략
- [인프라용 AGENTS.md와 apply 차단 훅](%EC%9D%B8%ED%94%84%EB%9D%BC%EC%9A%A9%20AGENTS.md%EC%99%80%20apply%20%EC%B0%A8%EB%8B%A8%20%ED%9B%85.md): 인프라 AGENTS.md 내용, PreToolUse 훅, 샌드박스, 파일 배치
- [결정적 도구로 루프 닫기](%EA%B2%B0%EC%A0%95%EC%A0%81%20%EB%8F%84%EA%B5%AC%EB%A1%9C%20%EB%A3%A8%ED%94%84%20%EB%8B%AB%EA%B8%B0.md): tflint와 checkov 루프, /goal, CI 게이트, 도구의 한계
- [테라폼 작업 흐름](%ED%85%8C%EB%9D%BC%ED%8F%BC%20%EC%9E%91%EC%97%85%20%ED%9D%90%EB%A6%84.md): 모듈 생성, 계획 검토, 변경 없는 리팩터링
- [Cloud Run 배포 준비와 부트스트랩](Cloud%20Run%20%EB%B0%B0%ED%8F%AC%20%EC%A4%80%EB%B9%84%EC%99%80%20%EB%B6%80%ED%8A%B8%EC%8A%A4%ED%8A%B8%EB%9E%A9.md): Procfile, 인증과 상태 버킷, 부트스트랩 모듈, 이미지 빌드, 배포 순서 그림
- [Cloud Run 서비스와 checkov 예외](Cloud%20Run%20%EC%84%9C%EB%B9%84%EC%8A%A4%EC%99%80%20checkov%20%EC%98%88%EC%99%B8.md): 서비스 모듈, 서비스 간 연결, apply와 업로드, 예상 checkov 지적, GKE
- [Terraform MCP 서버와 GitOps](Terraform%20MCP%20%EC%84%9C%EB%B2%84%EC%99%80%20GitOps.md): enabled_tools로 범위 제한, GitOps와 출력 스키마
- [안전장치와 CI-CD와 운영](%EC%95%88%EC%A0%84%EC%9E%A5%EC%B9%98%EC%99%80%20CI-CD%EC%99%80%20%EC%9A%B4%EC%98%81.md): 프로필, PR 계획 검토, 네 겹의 경계, 드리프트 감지, 다른 도구, README
- [요약](%EC%9A%94%EC%95%BD.md): 장의 열세 가지 요점 정리
- [연습 문제](%EC%97%B0%EC%8A%B5%20%EB%AC%B8%EC%A0%9C.md): 다섯 개 문제와 풀이 방향

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
