# 사용자 관리

이 장은 여러 사람이 함께 쓰는 Jenkins에서 사용자를 만들고 권한을 나눠 주는 방법을 다룬다. 일부 팀원은 시스템 전체를 관리하는 관리자이고, 나머지는 잡을 보고 실행하는 정도의 최소 권한만 가진다. 이 노트는 사용자 계정 만들기부터 역할 기반 접근 제어, 매트릭스 방식 보안까지 순서대로 정리한다.

핵심 흐름은 계정을 만들고, 권한을 줄 방식을 고르고, 사용자 계정으로 직접 로그인해 결과를 확인하는 것이다. 이 노트는 책의 화면 기준으로 작성했으므로 이후 Jenkins 버전에서는 메뉴 이름이나 위치가 달라졌을 수 있다.

---

## 1. 핵심 요점

- 사용자는 Manage Jenkins → Manage Users → Create User에서 만든다. Username, Password, Confirm Password, Full Name, E-mail Address를 입력한다.
- 역할을 쓰려면 Role-Based Authorization Strategy 플러그인을 설치하고, Configure Global Security의 Authorization에서 Role-Based Strategy를 선택해야 한다.
- 역할을 만든 뒤 사용자에게 붙이는 두 단계로 나뉜다. 만드는 곳은 Manage Roles, 붙이는 곳은 Assign Roles다.
- 전역 역할은 Jenkins 전체에, 프로젝트 기반 역할은 이름 패턴(예: .*Testing)에 맞는 잡에만 적용된다.
- 프로젝트 역할만으로는 부족하다. Overall 권한이 있는 전역 역할이 없으면 사용자는 대시보드에서 아무것도 볼 수 없다.
- 매트릭스 기반 보안은 표에서 사용자별 권한을 직접 체크하며, Anonymous Users와 Authenticated Users 그룹이 기본으로 있다.
- 프로젝트 기반 매트릭스 권한 전략은 잡마다 별도 표를 두고 Inheritance Strategy로 상속 여부를 정한다.
- 권한이 없는 메뉴(Configure, Delete Project 등)는 사용자 화면에서 보이지 않으므로, 설정 후 해당 계정으로 로그인해 확인한다.

---

## 2. 문서 목록

- [사용자 만들기와 플러그인 준비](사용자 만들기와 플러그인 준비.md): 사용자 생성 절차, 역할 방식의 필요성, 플러그인 설치와 전략 켜기
- [전역 역할과 프로젝트 역할](전역 역할과 프로젝트 역할.md): 역할 만들기와 붙이기, 이름 패턴으로 잡 범위 제한, 로그인 확인
- [매트릭스 기반 보안](매트릭스 기반 보안.md): 매트릭스 보안과 프로젝트 기반 매트릭스 설정, 상속 전략, 세 방식 비교
- [요약과 핵심 개념](요약과 핵심 개념.md): 장 전체 흐름, 핵심 개념, 용어, 놓치기 쉬운 점

<br>
<br>
<br>

[CICD Pipeline Using Jenkins Unleashed](../)
