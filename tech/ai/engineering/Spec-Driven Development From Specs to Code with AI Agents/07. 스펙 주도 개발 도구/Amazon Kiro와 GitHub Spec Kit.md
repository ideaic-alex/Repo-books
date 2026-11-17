# Amazon Kiro와 GitHub Spec Kit

스펙을 중심에 두는 두 대표 도구를 살핀다. 하나는 편집기 환경 자체를 제공하는 Amazon Kiro이고, 다른 하나는 편집기가 아니라 도구 모음과 절차인 GitHub Spec Kit다. 두 도구 모두 AI가 정해진 산출물의 사슬을 따라 일하게 만든다는 점에서 같은 방향을 향한다. 원서는 둘을 AIUP와 경쟁 관계가 아니라 보완 관계로 본다.

---

## 1. Amazon Kiro

Amazon Kiro는 스펙 주도 개발과 구현을 위한 구조적 안내를 강조하는 AI 코딩 환경이다. 스펙과 프로젝트 지침은 일반 Markdown에 둔다. 전형적인 Kiro 작업 흐름은 세 가지 산출물을 쓴다.

| 산출물 | 담는 내용 |
|---|---|
| Requirements.md | 의도와 인수 기준(acceptance criteria) |
| Design.md | 아키텍처 방향과 결정 |
| Tasks.md | 설계를 AI 에이전트가 실행할 단계로 옮긴 것 |

이 구조 덕분에 AI와의 상호작용이 예측 가능해진다. 에이전트에게 기능을 그냥 만들라고 시키는 것이 아니라, 정해진 산출물의 사슬을 따르게 한다. 요구사항에서 설계로, 설계에서 작업으로 이어진다.

### AIUP와의 관계

AIUP는 시스템 유스케이스를 실행 가능한 행동 계약의 중심에 둔다. Kiro는 요구사항, 설계, 작업의 워크플로를 중심에 둔다. 두 접근은 서로 호환되며 경쟁하지 않는다. 실무에서는 시스템 유스케이스가 더 넓은 Kiro식 흐름 안에서 행동의 정밀도를 제공할 수 있다.

## 2. GitHub Spec Kit

GitHub Spec Kit는 IDE가 아니다. 구조화된 스펙 주도 AI 개발을 위한 도구 모음이자 워크플로다. 구성 요소는 세 가지다.

- `specify` CLI 도구
- AI가 참고하는 프로젝트 기억 장소로 쓰는 `.specify` 디렉터리
- 작업 순서를 강제하는 슬래시 명령

생애 주기는 명시적이며 다섯 단계로 이뤄진다.

1. Constitution(헌장, 프로젝트가 지킬 원칙)
2. Specification(스펙)
3. Planning(계획)
4. Tasks(작업)
5. Implementation(구현)

참고(노트 작성자): 원서는 Constitution을 따로 풀이하지 않는다. 위 괄호 설명은 단어의 일반적인 뜻으로 보충한 것이다.

각 단계는 버전 관리되는 Markdown 산출물을 만든다. Spec Kit의 강점은 워크플로를 강제한다는 것이다. 프롬프트의 혼란을 줄이고, 이름 붙은 산출물과 정해진 순서를 중심으로 한 예측 가능한 AI 상호작용으로 바꾼다. 이 순서 덕분에 팀의 방향이 맞춰지고, 코드 생성 전에 해야 할 사고를 건너뛰기 어려워진다.

### AIUP와의 관계

AIUP가 행동의 정밀도와 추적성에 초점을 둔다면, Spec Kit은 정의된 생애 주기를 둘러싼 규율 있는 지휘(orchestration)에 초점을 둔다.

## 3. 두 도구의 차이 한눈에

| 비교 | Amazon Kiro | GitHub Spec Kit |
|---|---|---|
| 정체 | AI 코딩 환경(IDE) | 도구 모음과 워크플로 |
| 중심 흐름 | 요구사항, 설계, 작업 | 헌장, 스펙, 계획, 작업, 구현 |
| 산출물 | 일반 Markdown 3종 | 버전 관리되는 Markdown |
| 강점 | 예측 가능한 산출물 사슬 | 순서 강제 |

참고(노트 작성자): 위 표는 원서의 서술을 비교하기 쉽게 다시 정리한 것이다. 원서에 이 표 자체는 없다.

---

## 4. 핵심 정리

- Kiro는 Requirements.md, Design.md, Tasks.md의 세 산출물로 AI를 정해진 사슬에 따라 움직이게 한다.
- Spec Kit은 specify CLI, .specify 디렉터리, 슬래시 명령으로 헌장, 스펙, 계획, 작업, 구현의 순서를 강제한다.
- AIUP는 행동의 정밀도와 추적성에 집중하고 Kiro와 Spec Kit은 흐름의 규율에 집중하므로 서로 보완한다.

<br>
<br>
<br>

[Spec-Driven Development From Specs to Code with AI Agents](../)
