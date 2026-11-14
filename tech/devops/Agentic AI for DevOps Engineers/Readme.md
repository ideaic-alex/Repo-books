# **Agentic AI for DevOps Engineers 학습 노트**
(Agentic AI for DevOps Engineers: Building autonomous CI/CD, infrastructure, and operations workflows, 장별 정리 노트)
<br>

이 문서는 Trevoir Williams의 『Agentic AI for DevOps Engineers』(Packt)를 장별로 정리한 한국어 학습 노트입니다. 원문을 번역한 것이 아니라 내용을 우리말로 풀어서 다시 설명했고, 처음 나오는 용어에는 쉬운 풀이를 붙였습니다. 책은 생성형 AI의 기본 개념에서 시작해 AI 지원 IaC·CI 파이프라인·PR 검증 실습, 거버넌스와 도입 계획, Azure OpenAI를 파이프라인에 통합하는 방법을 다룹니다. 이어서 CI/CD 실패를 분류하고 PR 품질을 평가하는 에이전트, 메모리와 MCP(Model Context Protocol), 멀티 에이전트 인시던트 대응과 관측성, 운영 준비 체크리스트까지 8개 장으로 단계별로 안내합니다. 이 노트는 책의 장 구성을 그대로 따라 장마다 폴더 하나로 정리했습니다.

> **이 노트를 읽을 때 유의할 점**
> - 이 노트는 원서의 **요약·해설본**이며 원서를 대신하지 않습니다. 코드, 설정 값, 프롬프트, 명령 옵션처럼 정확성이 필요한 내용은 반드시 원서와 공식 문서에서 확인하세요.
> - 원서의 코드는 핵심 줄만 옮겼습니다. PDF 추출 과정에서 코드의 들여쓰기와 줄바꿈이 깨진 곳은 문맥으로 복원했고, 해당 문서에 그 사실을 적었습니다.
> - 책에 없는 보충 설명은 `참고(노트 작성자)`로 따로 표시했습니다.
> - 원서의 스크린샷과 그림은 싣지 않았고 글과 표로 풀어 설명했습니다.
> - 책이 소개하는 도구, 화면, 서비스는 책이 쓰인 시점 기준입니다. 최신 버전과 이름이나 동작이 다를 수 있습니다.
> - 비밀번호, 토큰, 키, 구독 ID 같은 값은 자리표시자로 바꿨습니다. 실습할 때는 자신의 값을 쓰고 비밀 값을 저장소에 올리지 마세요.
<br>

---

## 목차

- [머리말과 이 책에 대하여](00.%20%EB%A8%B8%EB%A6%AC%EB%A7%90%EA%B3%BC%20%EC%9D%B4%20%EC%B1%85%EC%97%90%20%EB%8C%80%ED%95%98%EC%97%AC/Readme.md) — 책의 목적, 저자, 구성, 읽는 순서, 준비물
- [DevOps를 위한 생성형 AI 개념](01.%20DevOps%EB%A5%BC%20%EC%9C%84%ED%95%9C%20%EC%83%9D%EC%84%B1%ED%98%95%20AI%20%EA%B0%9C%EB%85%90/Readme.md) — 생성형 AI와 LLM, DevOps 업무와의 대응, AI 지원과 AI 자율, 위험
  - [AI 지원 DevOps와 AI 자율 DevOps 그리고 위험](01.%20DevOps%EB%A5%BC%20%EC%9C%84%ED%95%9C%20%EC%83%9D%EC%84%B1%ED%98%95%20AI%20%EA%B0%9C%EB%85%90/AI%20%EC%A7%80%EC%9B%90%20DevOps%EC%99%80%20AI%20%EC%9E%90%EC%9C%A8%20DevOps%20%EA%B7%B8%EB%A6%AC%EA%B3%A0%20%EC%9C%84%ED%97%98.md)
  - [DevOps 수명주기에 AI 대응시키기](01.%20DevOps%EB%A5%BC%20%EC%9C%84%ED%95%9C%20%EC%83%9D%EC%84%B1%ED%98%95%20AI%20%EA%B0%9C%EB%85%90/DevOps%20%EC%88%98%EB%AA%85%EC%A3%BC%EA%B8%B0%EC%97%90%20AI%20%EB%8C%80%EC%9D%91%EC%8B%9C%ED%82%A4%EA%B8%B0.md)
  - [생성형 AI와 LLM 이해하기](01.%20DevOps%EB%A5%BC%20%EC%9C%84%ED%95%9C%20%EC%83%9D%EC%84%B1%ED%98%95%20AI%20%EA%B0%9C%EB%85%90/%EC%83%9D%EC%84%B1%ED%98%95%20AI%EC%99%80%20LLM%20%EC%9D%B4%ED%95%B4%ED%95%98%EA%B8%B0.md)
  - [요약과 핵심 개념](01.%20DevOps%EB%A5%BC%20%EC%9C%84%ED%95%9C%20%EC%83%9D%EC%84%B1%ED%98%95%20AI%20%EA%B0%9C%EB%85%90/%EC%9A%94%EC%95%BD%EA%B3%BC%20%ED%95%B5%EC%8B%AC%20%EA%B0%9C%EB%85%90.md)
- [DevOps에서 생성형 AI의 실무 활용](02.%20DevOps%EC%97%90%EC%84%9C%20%EC%83%9D%EC%84%B1%ED%98%95%20AI%EC%9D%98%20%EC%8B%A4%EB%AC%B4%20%ED%99%9C%EC%9A%A9/Readme.md) — AI 지원 IaC, CI 파이프라인 작성, PR 검증, 릴리스 노트, 인시던트 분류 실습
  - [AI 지원 CI 파이프라인 작성](02.%20DevOps%EC%97%90%EC%84%9C%20%EC%83%9D%EC%84%B1%ED%98%95%20AI%EC%9D%98%20%EC%8B%A4%EB%AC%B4%20%ED%99%9C%EC%9A%A9/AI%20%EC%A7%80%EC%9B%90%20CI%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%20%EC%9E%91%EC%84%B1.md)
  - [AI 지원 IaC 실습](02.%20DevOps%EC%97%90%EC%84%9C%20%EC%83%9D%EC%84%B1%ED%98%95%20AI%EC%9D%98%20%EC%8B%A4%EB%AC%B4%20%ED%99%9C%EC%9A%A9/AI%20%EC%A7%80%EC%9B%90%20IaC%20%EC%8B%A4%EC%8A%B5.md)
  - [AI 지원 PR 검증](02.%20DevOps%EC%97%90%EC%84%9C%20%EC%83%9D%EC%84%B1%ED%98%95%20AI%EC%9D%98%20%EC%8B%A4%EB%AC%B4%20%ED%99%9C%EC%9A%A9/AI%20%EC%A7%80%EC%9B%90%20PR%20%EA%B2%80%EC%A6%9D.md)
  - [AI 지원 릴리스 노트 생성](02.%20DevOps%EC%97%90%EC%84%9C%20%EC%83%9D%EC%84%B1%ED%98%95%20AI%EC%9D%98%20%EC%8B%A4%EB%AC%B4%20%ED%99%9C%EC%9A%A9/AI%20%EC%A7%80%EC%9B%90%20%EB%A6%B4%EB%A6%AC%EC%8A%A4%20%EB%85%B8%ED%8A%B8%20%EC%83%9D%EC%84%B1.md)
  - [AI 지원 인시던트 분류](02.%20DevOps%EC%97%90%EC%84%9C%20%EC%83%9D%EC%84%B1%ED%98%95%20AI%EC%9D%98%20%EC%8B%A4%EB%AC%B4%20%ED%99%9C%EC%9A%A9/AI%20%EC%A7%80%EC%9B%90%20%EC%9D%B8%EC%8B%9C%EB%8D%98%ED%8A%B8%20%EB%B6%84%EB%A5%98.md)
  - [요약과 핵심 개념](02.%20DevOps%EC%97%90%EC%84%9C%20%EC%83%9D%EC%84%B1%ED%98%95%20AI%EC%9D%98%20%EC%8B%A4%EB%AC%B4%20%ED%99%9C%EC%9A%A9/%EC%9A%94%EC%95%BD%EA%B3%BC%20%ED%95%B5%EC%8B%AC%20%EA%B0%9C%EB%85%90.md)
- [DevOps AI 도구와 거버넌스, 엔터프라이즈 준비](03.%20DevOps%20AI%20%EB%8F%84%EA%B5%AC%EC%99%80%20%EA%B1%B0%EB%B2%84%EB%84%8C%EC%8A%A4%2C%20%EC%97%94%ED%84%B0%ED%94%84%EB%9D%BC%EC%9D%B4%EC%A6%88%20%EC%A4%80%EB%B9%84/Readme.md) — AI 도구 지형, 계층별 점검, 가드레일과 감사, 도입 플레이북과 ROI
  - [AI 가드레일과 감사, 책임](03.%20DevOps%20AI%20%EB%8F%84%EA%B5%AC%EC%99%80%20%EA%B1%B0%EB%B2%84%EB%84%8C%EC%8A%A4%2C%20%EC%97%94%ED%84%B0%ED%94%84%EB%9D%BC%EC%9D%B4%EC%A6%88%20%EC%A4%80%EB%B9%84/AI%20%EA%B0%80%EB%93%9C%EB%A0%88%EC%9D%BC%EA%B3%BC%20%EA%B0%90%EC%82%AC%2C%20%EC%B1%85%EC%9E%84.md)
  - [AI 도입 플레이북과 ROI 측정](03.%20DevOps%20AI%20%EB%8F%84%EA%B5%AC%EC%99%80%20%EA%B1%B0%EB%B2%84%EB%84%8C%EC%8A%A4%2C%20%EC%97%94%ED%84%B0%ED%94%84%EB%9D%BC%EC%9D%B4%EC%A6%88%20%EC%A4%80%EB%B9%84/AI%20%EB%8F%84%EC%9E%85%20%ED%94%8C%EB%A0%88%EC%9D%B4%EB%B6%81%EA%B3%BC%20ROI%20%EC%B8%A1%EC%A0%95.md)
  - [DevOps AI 도구 지형과 위험 매트릭스](03.%20DevOps%20AI%20%EB%8F%84%EA%B5%AC%EC%99%80%20%EA%B1%B0%EB%B2%84%EB%84%8C%EC%8A%A4%2C%20%EC%97%94%ED%84%B0%ED%94%84%EB%9D%BC%EC%9D%B4%EC%A6%88%20%EC%A4%80%EB%B9%84/DevOps%20AI%20%EB%8F%84%EA%B5%AC%20%EC%A7%80%ED%98%95%EA%B3%BC%20%EC%9C%84%ED%97%98%20%EB%A7%A4%ED%8A%B8%EB%A6%AD%EC%8A%A4.md)
  - [기존 스택의 AI 계층별 점검](03.%20DevOps%20AI%20%EB%8F%84%EA%B5%AC%EC%99%80%20%EA%B1%B0%EB%B2%84%EB%84%8C%EC%8A%A4%2C%20%EC%97%94%ED%84%B0%ED%94%84%EB%9D%BC%EC%9D%B4%EC%A6%88%20%EC%A4%80%EB%B9%84/%EA%B8%B0%EC%A1%B4%20%EC%8A%A4%ED%83%9D%EC%9D%98%20AI%20%EA%B3%84%EC%B8%B5%EB%B3%84%20%EC%A0%90%EA%B2%80.md)
  - [요약과 핵심 개념](03.%20DevOps%20AI%20%EB%8F%84%EA%B5%AC%EC%99%80%20%EA%B1%B0%EB%B2%84%EB%84%8C%EC%8A%A4%2C%20%EC%97%94%ED%84%B0%ED%94%84%EB%9D%BC%EC%9D%B4%EC%A6%88%20%EC%A4%80%EB%B9%84/%EC%9A%94%EC%95%BD%EA%B3%BC%20%ED%95%B5%EC%8B%AC%20%EA%B0%9C%EB%85%90.md)
- [생성형 AI를 DevOps 파이프라인에 통합하기](04.%20%EC%83%9D%EC%84%B1%ED%98%95%20AI%EB%A5%BC%20DevOps%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%EC%97%90%20%ED%86%B5%ED%95%A9%ED%95%98%EA%B8%B0/Readme.md) — Azure OpenAI 연동, 결정적 워크플로, 컴포지트 액션, 비용·관측성·보안, ChatOps
  - [AI 비용과 성능 관리](04.%20%EC%83%9D%EC%84%B1%ED%98%95%20AI%EB%A5%BC%20DevOps%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%EC%97%90%20%ED%86%B5%ED%95%A9%ED%95%98%EA%B8%B0/AI%20%EB%B9%84%EC%9A%A9%EA%B3%BC%20%EC%84%B1%EB%8A%A5%20%EA%B4%80%EB%A6%AC.md)
  - [AI 엔진 준비와 Azure OpenAI 프로비저닝](04.%20%EC%83%9D%EC%84%B1%ED%98%95%20AI%EB%A5%BC%20DevOps%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%EC%97%90%20%ED%86%B5%ED%95%A9%ED%95%98%EA%B8%B0/AI%20%EC%97%94%EC%A7%84%20%EC%A4%80%EB%B9%84%EC%99%80%20Azure%20OpenAI%20%ED%94%84%EB%A1%9C%EB%B9%84%EC%A0%80%EB%8B%9D.md)
  - [AI 증강 ChatOps](04.%20%EC%83%9D%EC%84%B1%ED%98%95%20AI%EB%A5%BC%20DevOps%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%EC%97%90%20%ED%86%B5%ED%95%A9%ED%95%98%EA%B8%B0/AI%20%EC%A6%9D%EA%B0%95%20ChatOps.md)
  - [AI 호출의 관측성과 피드백](04.%20%EC%83%9D%EC%84%B1%ED%98%95%20AI%EB%A5%BC%20DevOps%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%EC%97%90%20%ED%86%B5%ED%95%A9%ED%95%98%EA%B8%B0/AI%20%ED%98%B8%EC%B6%9C%EC%9D%98%20%EA%B4%80%EC%B8%A1%EC%84%B1%EA%B3%BC%20%ED%94%BC%EB%93%9C%EB%B0%B1.md)
  - [CI-CD의 안전한 AI 통합 패턴](04.%20%EC%83%9D%EC%84%B1%ED%98%95%20AI%EB%A5%BC%20DevOps%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%EC%97%90%20%ED%86%B5%ED%95%A9%ED%95%98%EA%B8%B0/CI-CD%EC%9D%98%20%EC%95%88%EC%A0%84%ED%95%9C%20AI%20%ED%86%B5%ED%95%A9%20%ED%8C%A8%ED%84%B4.md)
  - [결정적 AI 워크플로 단계 설계](04.%20%EC%83%9D%EC%84%B1%ED%98%95%20AI%EB%A5%BC%20DevOps%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%EC%97%90%20%ED%86%B5%ED%95%A9%ED%95%98%EA%B8%B0/%EA%B2%B0%EC%A0%95%EC%A0%81%20AI%20%EC%9B%8C%ED%81%AC%ED%94%8C%EB%A1%9C%20%EB%8B%A8%EA%B3%84%20%EC%84%A4%EA%B3%84.md)
  - [요약과 핵심 개념](04.%20%EC%83%9D%EC%84%B1%ED%98%95%20AI%EB%A5%BC%20DevOps%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%EC%97%90%20%ED%86%B5%ED%95%A9%ED%95%98%EA%B8%B0/%EC%9A%94%EC%95%BD%EA%B3%BC%20%ED%95%B5%EC%8B%AC%20%EA%B0%9C%EB%85%90.md)
  - [재사용 가능한 Azure OpenAI 컴포지트 액션](04.%20%EC%83%9D%EC%84%B1%ED%98%95%20AI%EB%A5%BC%20DevOps%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%EC%97%90%20%ED%86%B5%ED%95%A9%ED%95%98%EA%B8%B0/%EC%9E%AC%EC%82%AC%EC%9A%A9%20%EA%B0%80%EB%8A%A5%ED%95%9C%20Azure%20OpenAI%20%EC%BB%B4%ED%8F%AC%EC%A7%80%ED%8A%B8%20%EC%95%A1%EC%85%98.md)
  - [프롬프트와 입력 복잡도 줄이기](04.%20%EC%83%9D%EC%84%B1%ED%98%95%20AI%EB%A5%BC%20DevOps%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%EC%97%90%20%ED%86%B5%ED%95%A9%ED%95%98%EA%B8%B0/%ED%94%84%EB%A1%AC%ED%94%84%ED%8A%B8%EC%99%80%20%EC%9E%85%EB%A0%A5%20%EB%B3%B5%EC%9E%A1%EB%8F%84%20%EC%A4%84%EC%9D%B4%EA%B8%B0.md)
- [CI-CD 실패 분류와 PR 품질 평가를 위한 에이전틱 AI](05.%20CI-CD%20%EC%8B%A4%ED%8C%A8%20%EB%B6%84%EB%A5%98%EC%99%80%20PR%20%ED%92%88%EC%A7%88%20%ED%8F%89%EA%B0%80%EB%A5%BC%20%EC%9C%84%ED%95%9C%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8B%B1%20AI/Readme.md) — AI 에이전트 구성, 안전한 사용, 실패 분류 에이전트, 점진적 자율성, PR 품질 평가
  - [AI 에이전트의 정의와 구성 요소](05.%20CI-CD%20%EC%8B%A4%ED%8C%A8%20%EB%B6%84%EB%A5%98%EC%99%80%20PR%20%ED%92%88%EC%A7%88%20%ED%8F%89%EA%B0%80%EB%A5%BC%20%EC%9C%84%ED%95%9C%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8B%B1%20AI/AI%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%EC%9D%98%20%EC%A0%95%EC%9D%98%EC%99%80%20%EA%B5%AC%EC%84%B1%20%EC%9A%94%EC%86%8C.md)
  - [CI-CD에서 에이전트를 안전하게 쓰기와 가드레일](05.%20CI-CD%20%EC%8B%A4%ED%8C%A8%20%EB%B6%84%EB%A5%98%EC%99%80%20PR%20%ED%92%88%EC%A7%88%20%ED%8F%89%EA%B0%80%EB%A5%BC%20%EC%9C%84%ED%95%9C%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8B%B1%20AI/CI-CD%EC%97%90%EC%84%9C%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%EB%A5%BC%20%EC%95%88%EC%A0%84%ED%95%98%EA%B2%8C%20%EC%93%B0%EA%B8%B0%EC%99%80%20%EA%B0%80%EB%93%9C%EB%A0%88%EC%9D%BC.md)
  - [PR 분석 워크플로에 에이전트 통합](05.%20CI-CD%20%EC%8B%A4%ED%8C%A8%20%EB%B6%84%EB%A5%98%EC%99%80%20PR%20%ED%92%88%EC%A7%88%20%ED%8F%89%EA%B0%80%EB%A5%BC%20%EC%9C%84%ED%95%9C%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8B%B1%20AI/PR%20%EB%B6%84%EC%84%9D%20%EC%9B%8C%ED%81%AC%ED%94%8C%EB%A1%9C%EC%97%90%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%ED%86%B5%ED%95%A9.md)
  - [실패 분류 에이전트 구현 실습](05.%20CI-CD%20%EC%8B%A4%ED%8C%A8%20%EB%B6%84%EB%A5%98%EC%99%80%20PR%20%ED%92%88%EC%A7%88%20%ED%8F%89%EA%B0%80%EB%A5%BC%20%EC%9C%84%ED%95%9C%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8B%B1%20AI/%EC%8B%A4%ED%8C%A8%20%EB%B6%84%EB%A5%98%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EA%B5%AC%ED%98%84%20%EC%8B%A4%EC%8A%B5.md)
  - [에이전트 패턴과 PR 품질 평가 에이전트](05.%20CI-CD%20%EC%8B%A4%ED%8C%A8%20%EB%B6%84%EB%A5%98%EC%99%80%20PR%20%ED%92%88%EC%A7%88%20%ED%8F%89%EA%B0%80%EB%A5%BC%20%EC%9C%84%ED%95%9C%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8B%B1%20AI/%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%ED%8C%A8%ED%84%B4%EA%B3%BC%20PR%20%ED%92%88%EC%A7%88%20%ED%8F%89%EA%B0%80%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8.md)
  - [에이전트가 운영에서 실패하는 이유와 점진적 자율성](05.%20CI-CD%20%EC%8B%A4%ED%8C%A8%20%EB%B6%84%EB%A5%98%EC%99%80%20PR%20%ED%92%88%EC%A7%88%20%ED%8F%89%EA%B0%80%EB%A5%BC%20%EC%9C%84%ED%95%9C%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8B%B1%20AI/%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%EA%B0%80%20%EC%9A%B4%EC%98%81%EC%97%90%EC%84%9C%20%EC%8B%A4%ED%8C%A8%ED%95%98%EB%8A%94%20%EC%9D%B4%EC%9C%A0%EC%99%80%20%EC%A0%90%EC%A7%84%EC%A0%81%20%EC%9E%90%EC%9C%A8%EC%84%B1.md)
  - [요약과 핵심 개념](05.%20CI-CD%20%EC%8B%A4%ED%8C%A8%20%EB%B6%84%EB%A5%98%EC%99%80%20PR%20%ED%92%88%EC%A7%88%20%ED%8F%89%EA%B0%80%EB%A5%BC%20%EC%9C%84%ED%95%9C%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8B%B1%20AI/%EC%9A%94%EC%95%BD%EA%B3%BC%20%ED%95%B5%EC%8B%AC%20%EA%B0%9C%EB%85%90.md)
- [고급 시나리오 메모리와 MCP](06.%20%EA%B3%A0%EA%B8%89%20%EC%8B%9C%EB%82%98%EB%A6%AC%EC%98%A4%20%EB%A9%94%EB%AA%A8%EB%A6%AC%EC%99%80%20MCP/Readme.md) — 에이전트 메모리, MCP 서버 구축과 시험, MCP 에이전트의 PR 분석 연결
  - [DevOps 에이전트의 메모리](06.%20%EA%B3%A0%EA%B8%89%20%EC%8B%9C%EB%82%98%EB%A6%AC%EC%98%A4%20%EB%A9%94%EB%AA%A8%EB%A6%AC%EC%99%80%20MCP/DevOps%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%EC%9D%98%20%EB%A9%94%EB%AA%A8%EB%A6%AC.md)
  - [GitHub용 MCP 서버 구축](06.%20%EA%B3%A0%EA%B8%89%20%EC%8B%9C%EB%82%98%EB%A6%AC%EC%98%A4%20%EB%A9%94%EB%AA%A8%EB%A6%AC%EC%99%80%20MCP/GitHub%EC%9A%A9%20MCP%20%EC%84%9C%EB%B2%84%20%EA%B5%AC%EC%B6%95.md)
  - [MCP 에이전트를 PR 분석 워크플로에 연결해 검증](06.%20%EA%B3%A0%EA%B8%89%20%EC%8B%9C%EB%82%98%EB%A6%AC%EC%98%A4%20%EB%A9%94%EB%AA%A8%EB%A6%AC%EC%99%80%20MCP/MCP%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%EB%A5%BC%20PR%20%EB%B6%84%EC%84%9D%20%EC%9B%8C%ED%81%AC%ED%94%8C%EB%A1%9C%EC%97%90%20%EC%97%B0%EA%B2%B0%ED%95%B4%20%EA%B2%80%EC%A6%9D.md)
  - [PR 품질 에이전트에 MCP 도구 연결](06.%20%EA%B3%A0%EA%B8%89%20%EC%8B%9C%EB%82%98%EB%A6%AC%EC%98%A4%20%EB%A9%94%EB%AA%A8%EB%A6%AC%EC%99%80%20MCP/PR%20%ED%92%88%EC%A7%88%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%EC%97%90%20MCP%20%EB%8F%84%EA%B5%AC%20%EC%97%B0%EA%B2%B0.md)
  - [Postman으로 MCP 서버 시험](06.%20%EA%B3%A0%EA%B8%89%20%EC%8B%9C%EB%82%98%EB%A6%AC%EC%98%A4%20%EB%A9%94%EB%AA%A8%EB%A6%AC%EC%99%80%20MCP/Postman%EC%9C%BC%EB%A1%9C%20MCP%20%EC%84%9C%EB%B2%84%20%EC%8B%9C%ED%97%98.md)
  - [도구와 MCP](06.%20%EA%B3%A0%EA%B8%89%20%EC%8B%9C%EB%82%98%EB%A6%AC%EC%98%A4%20%EB%A9%94%EB%AA%A8%EB%A6%AC%EC%99%80%20MCP/%EB%8F%84%EA%B5%AC%EC%99%80%20MCP.md)
  - [요약과 핵심 개념](06.%20%EA%B3%A0%EA%B8%89%20%EC%8B%9C%EB%82%98%EB%A6%AC%EC%98%A4%20%EB%A9%94%EB%AA%A8%EB%A6%AC%EC%99%80%20MCP/%EC%9A%94%EC%95%BD%EA%B3%BC%20%ED%95%B5%EC%8B%AC%20%EA%B0%9C%EB%85%90.md)
  - [워크플로 수준 메모리 실습](06.%20%EA%B3%A0%EA%B8%89%20%EC%8B%9C%EB%82%98%EB%A6%AC%EC%98%A4%20%EB%A9%94%EB%AA%A8%EB%A6%AC%EC%99%80%20MCP/%EC%9B%8C%ED%81%AC%ED%94%8C%EB%A1%9C%20%EC%88%98%EC%A4%80%20%EB%A9%94%EB%AA%A8%EB%A6%AC%20%EC%8B%A4%EC%8A%B5.md)
- [멀티 에이전트 인시던트 대응과 에이전트 관측성](07.%20%EB%A9%80%ED%8B%B0%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EC%9D%B8%EC%8B%9C%EB%8D%98%ED%8A%B8%20%EB%8C%80%EC%9D%91%EA%B3%BC%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EA%B4%80%EC%B8%A1%EC%84%B1/Readme.md) — 멀티 에이전트 인시던트 대응, 관측성과 평가, OpenTelemetry와 Aspire
  - [OpenTelemetry 계측과 Aspire 관측성 시험](07.%20%EB%A9%80%ED%8B%B0%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EC%9D%B8%EC%8B%9C%EB%8D%98%ED%8A%B8%20%EB%8C%80%EC%9D%91%EA%B3%BC%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EA%B4%80%EC%B8%A1%EC%84%B1/OpenTelemetry%20%EA%B3%84%EC%B8%A1%EA%B3%BC%20Aspire%20%EA%B4%80%EC%B8%A1%EC%84%B1%20%EC%8B%9C%ED%97%98.md)
  - [멀티 에이전트를 쓰는 이유와 오케스트레이션 패턴 및 안전 경계](07.%20%EB%A9%80%ED%8B%B0%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EC%9D%B8%EC%8B%9C%EB%8D%98%ED%8A%B8%20%EB%8C%80%EC%9D%91%EA%B3%BC%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EA%B4%80%EC%B8%A1%EC%84%B1/%EB%A9%80%ED%8B%B0%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%EB%A5%BC%20%EC%93%B0%EB%8A%94%20%EC%9D%B4%EC%9C%A0%EC%99%80%20%EC%98%A4%EC%BC%80%EC%8A%A4%ED%8A%B8%EB%A0%88%EC%9D%B4%EC%85%98%20%ED%8C%A8%ED%84%B4%20%EB%B0%8F%20%EC%95%88%EC%A0%84%20%EA%B2%BD%EA%B3%84.md)
  - [샘플 인시던트 데이터와 전문 에이전트 프롬프트](07.%20%EB%A9%80%ED%8B%B0%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EC%9D%B8%EC%8B%9C%EB%8D%98%ED%8A%B8%20%EB%8C%80%EC%9D%91%EA%B3%BC%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EA%B4%80%EC%B8%A1%EC%84%B1/%EC%83%98%ED%94%8C%20%EC%9D%B8%EC%8B%9C%EB%8D%98%ED%8A%B8%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%99%80%20%EC%A0%84%EB%AC%B8%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%ED%94%84%EB%A1%AC%ED%94%84%ED%8A%B8.md)
  - [에이전트 관측성과 평가](07.%20%EB%A9%80%ED%8B%B0%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EC%9D%B8%EC%8B%9C%EB%8D%98%ED%8A%B8%20%EB%8C%80%EC%9D%91%EA%B3%BC%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EA%B4%80%EC%B8%A1%EC%84%B1/%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EA%B4%80%EC%B8%A1%EC%84%B1%EA%B3%BC%20%ED%8F%89%EA%B0%80.md)
  - [오케스트레이션 워크플로 구현](07.%20%EB%A9%80%ED%8B%B0%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EC%9D%B8%EC%8B%9C%EB%8D%98%ED%8A%B8%20%EB%8C%80%EC%9D%91%EA%B3%BC%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EA%B4%80%EC%B8%A1%EC%84%B1/%EC%98%A4%EC%BC%80%EC%8A%A4%ED%8A%B8%EB%A0%88%EC%9D%B4%EC%85%98%20%EC%9B%8C%ED%81%AC%ED%94%8C%EB%A1%9C%20%EA%B5%AC%ED%98%84.md)
  - [요약과 핵심 개념](07.%20%EB%A9%80%ED%8B%B0%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EC%9D%B8%EC%8B%9C%EB%8D%98%ED%8A%B8%20%EB%8C%80%EC%9D%91%EA%B3%BC%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EA%B4%80%EC%B8%A1%EC%84%B1/%EC%9A%94%EC%95%BD%EA%B3%BC%20%ED%95%B5%EC%8B%AC%20%EA%B0%9C%EB%85%90.md)
  - [워크플로 실행과 자격 증명 설정](07.%20%EB%A9%80%ED%8B%B0%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EC%9D%B8%EC%8B%9C%EB%8D%98%ED%8A%B8%20%EB%8C%80%EC%9D%91%EA%B3%BC%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EA%B4%80%EC%B8%A1%EC%84%B1/%EC%9B%8C%ED%81%AC%ED%94%8C%EB%A1%9C%20%EC%8B%A4%ED%96%89%EA%B3%BC%20%EC%9E%90%EA%B2%A9%20%EC%A6%9D%EB%AA%85%20%EC%84%A4%EC%A0%95.md)
- [맺음말과 다음 단계](08.%20%EB%A7%BA%EC%9D%8C%EB%A7%90%EA%B3%BC%20%EB%8B%A4%EC%9D%8C%20%EB%8B%A8%EA%B3%84/Readme.md) — 원칙, 운영 준비 체크리스트, 점진적 자율성 도입, 다음 단계
  - [성과 측정, 다음 단계, 학습 이어가기와 최종 요점](08.%20%EB%A7%BA%EC%9D%8C%EB%A7%90%EA%B3%BC%20%EB%8B%A4%EC%9D%8C%20%EB%8B%A8%EA%B3%84/%EC%84%B1%EA%B3%BC%20%EC%B8%A1%EC%A0%95%2C%20%EB%8B%A4%EC%9D%8C%20%EB%8B%A8%EA%B3%84%2C%20%ED%95%99%EC%8A%B5%20%EC%9D%B4%EC%96%B4%EA%B0%80%EA%B8%B0%EC%99%80%20%EC%B5%9C%EC%A2%85%20%EC%9A%94%EC%A0%90.md)
  - [요약과 핵심 개념](08.%20%EB%A7%BA%EC%9D%8C%EB%A7%90%EA%B3%BC%20%EB%8B%A4%EC%9D%8C%20%EB%8B%A8%EA%B3%84/%EC%9A%94%EC%95%BD%EA%B3%BC%20%ED%95%B5%EC%8B%AC%20%EA%B0%9C%EB%85%90.md)
  - [운영 준비 체크리스트와 점진적 자율성 도입](08.%20%EB%A7%BA%EC%9D%8C%EB%A7%90%EA%B3%BC%20%EB%8B%A4%EC%9D%8C%20%EB%8B%A8%EA%B3%84/%EC%9A%B4%EC%98%81%20%EC%A4%80%EB%B9%84%20%EC%B2%B4%ED%81%AC%EB%A6%AC%EC%8A%A4%ED%8A%B8%EC%99%80%20%EC%A0%90%EC%A7%84%EC%A0%81%20%EC%9E%90%EC%9C%A8%EC%84%B1%20%EB%8F%84%EC%9E%85.md)
  - [이 책이 다진 것과 변하지 않는 원칙](08.%20%EB%A7%BA%EC%9D%8C%EB%A7%90%EA%B3%BC%20%EB%8B%A4%EC%9D%8C%20%EB%8B%A8%EA%B3%84/%EC%9D%B4%20%EC%B1%85%EC%9D%B4%20%EB%8B%A4%EC%A7%84%20%EA%B2%83%EA%B3%BC%20%EB%B3%80%ED%95%98%EC%A7%80%20%EC%95%8A%EB%8A%94%20%EC%9B%90%EC%B9%99.md)

---

## 읽는 순서 제안

| 목적 | 추천 경로 |
|------|-----------|
| 생성형 AI와 DevOps의 접점을 먼저 잡고 싶다 | 1장 → 2장 |
| 조직에 AI를 도입하기 전에 통제 방안을 알고 싶다 | 3장 → 8장 |
| AI를 CI/CD 파이프라인에 직접 붙이고 싶다 | 2장 → 4장 |
| 에이전트를 만들고 안전하게 운영하고 싶다 | 5장 → 6장 → 7장 |
| 전체를 빠르게 복습하고 싶다 | 각 장의 Readme와 요약과 핵심 개념 |

## 용어 몇 가지

| 용어 | 쉬운 설명 |
|------|-----------|
| 생성형 AI / LLM | 글, 코드 같은 결과물을 만들어 내는 AI / 그 바탕이 되는 대규모 언어 모델. |
| 에이전트 | 목표를 받아 스스로 도구를 골라 쓰며 여러 단계를 수행하는 AI 프로그램. |
| 가드레일 | AI가 허용된 범위를 벗어나지 않도록 거는 제한과 검사. |
| 점진적 자율성 | 에이전트에 주는 권한을 작은 단계부터 검증하며 차츰 넓히는 방식. |
| MCP | 에이전트가 외부 도구와 데이터를 같은 방식으로 쓰게 하는 표준 규약. |
| 컴포지트 액션 | 여러 워크플로 단계를 묶어 재사용하게 만든 GitHub Actions 단위. |
| 관측성 | 지표, 로그, 트레이스로 시스템 내부 상태를 들여다볼 수 있는 정도. |
| 인시던트 | 서비스에 영향을 주는 장애나 사고. |

---

## 이 노트를 만든 방법과 사용한 프롬프트

이 노트는 AI 코딩 도구(Claude Code)에 원서 PDF와 기존 노트 형식을 주고 작성하게 한 결과물입니다. 작성에 쓴 지시문을 아래에 정리합니다. 원문 텍스트는 PDF에서 추출했고, 장 단위로 나눠 작성한 뒤 파일명과 링크, 코드 블록, 비밀 값 유무를 기계적으로 점검했습니다.

### 1. 최초 요청

> 'Agentic AI for DevOps Engineers' PDF를 'Repo-books' 저장소의 다른 작성된 폴더와 md 파일들을 참고해서 저장소의 'tech' 폴더에 문서를 작성합니다. 작성하는데 사용된 prompt는 'README.md' 파일에 정리해서 기록합니다.

### 2. 작업 방식

| 단계 | 내용 |
|---|---|
| 형식 조사 | 같은 저장소의 `tech/devops/CICD Pipeline Using Jenkins Unleashed-2`(머리말 폴더, 장 폴더, 장 Readme, 요약과 핵심 개념 구성)를 견본으로 삼았다. |
| 원문 추출 | PDF 272쪽의 텍스트와 목차(북마크)를 추출해 장별 쪽 범위를 정했다. |
| 장별 작성 | 장을 4개 묶음으로 나눠 각각 별도 작성자(에이전트)에게 아래 공통 프롬프트로 작성하게 했다. |
| 점검 | 문서 링크와 실제 파일명 일치, 금지 문자, 코드 블록 짝, 비밀 값과 추출 잡음 표식을 점검했다. |

| 담당 묶음 | 장 | PDF 쪽 범위 |
|---|---|---|
| 1 | 머리말, 1장, 2장 | 12~71쪽 |
| 2 | 3장, 4장 | 72~141쪽 |
| 3 | 5장, 6장 | 142~215쪽 |
| 4 | 7장, 8장 | 216~257쪽 |

### 3. 공통 작성 프롬프트(요지)

```text
역할: 영문 기술서 한 권을 한국어 학습 노트(마크다운 문서 묶음)로 정리하는 작성자다.
      담당 범위만 작성하고 저장소에는 올리지 않는다. 모든 문장은 한국어로 쓴다.
입력: 책 정보, PDF 추출 텍스트(쪽 구분자 포함), 담당 장과 쪽 범위, 출력 폴더명.
      원문은 구간별로 끝까지 읽는다.
형식: 견본 문서(장 Readme, 주제 문서, 요약과 핵심 개념)의 형식과 어조(평서문, 쉬운 설명)를 따른다.
      장 폴더 = Readme.md(소개, 핵심 요점, 문서 목록) + 주제 문서 + 요약과 핵심 개념.md.
      00 폴더 = Readme.md 한 개(목적, 저자, 구성, 읽는 순서, 준비물, 읽는 법).
내용 규칙:
  1. 번역이 아니라 이해한 뒤 우리말로 다시 설명한다. 원문 문장을 그대로 옮기지 않되
     절차, 설정 값, 단계, 주의점, 수치의 정보량은 줄이지 않는다.
  2. 실습(Demo, Step)은 단계별로 무엇을 만들고 어떤 결과가 나오는지 설명한다.
     코드는 핵심 줄만 짧게(문서당 약 30줄 이내) 싣는다.
  3. 영어 용어는 처음 나올 때 한국어 풀이를 붙이고, 제품명·명령·경로는 영어 그대로 둔다.
     용어는 전체에서 통일한다(에이전트, 가드레일, 컴포지트 액션 등).
  4. 원문에 없는 보충은 '참고(노트 작성자):'로 표시하고, 없는 사실을 지어내지 않는다.
     글자가 깨져 불확실한 곳은 그렇게 밝힌다.
  5. 비밀 값은 자리표시자로 쓰고, 스크린샷은 싣지 않는다.
  6. 문서는 도입 1~2문단, 구분선, 번호 붙인 절 순서. 표는 문서당 1~3개.
  7. 파일명에 / \ : * ? " < > | 를 쓰지 않는다.
보고: 작성 파일 목록과 글자 수, 복원한 부분, 다루지 못한 부분만 간결히 보고한다.
```

### 4. 이 프롬프트로 작성할 때의 한계

- 일부 문서는 원서 해당 절이 1~3쪽이라 3,000자에 못 미칩니다. 원문에 없는 내용을 채우지 않았습니다.
- PDF 텍스트 추출본은 코드 들여쓰기가 사라져 있어, 코드 구조를 문맥으로 복원한 부분이 있습니다.
- 정확한 코드와 설정은 원서와 원서의 예제 저장소에서 대조하세요.

---

## 이 노트에 대하여

- 각 장 폴더는 Readme.md, 주제별 문서, 요약과 핵심 개념으로 구성됩니다.
- 같은 저장소의 다른 학습 노트와 같은 형식을 따릅니다.
