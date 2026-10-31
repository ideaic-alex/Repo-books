# 머리말과 이 책에 대하여

이 문서는 Hayden Barnes의 『Pro Windows Subsystem for Linux (WSL)』(Apress, 2021, 1판)의 머리말(Introduction)과 저자 소개를 정리한 노트다. 이 책이 무엇을 다루는지, 누구를 위한 책인지, WSL이 어떤 과정을 거쳐 지금의 모습이 되었는지를 먼저 훑어 두면 본문을 읽기가 한결 쉽다.

---

## 1. 저자와 책 소개

- **저자(Author)**: Hayden Barnes. SUSE에서 Windows Containers 엔지니어링 매니저로 일하고 있고, Microsoft MVP로 선정되었다. 이전에는 Canonical에서 Ubuntu on WSL 팀을 이끌었다. WSL 전문 커뮤니티 컨퍼런스인 WSLConf를 만들었고, WSL 전용 리눅스 배포판을 처음 만든 회사 Whitewater Foundry를 창업했다.
- **기술 감수(Technical Reviewer)**: Nuno Do Carmo. Windows, Unix, Linux 관리 경력이 오래된 Microsoft MVP다. WSL에 클라우드 네이티브 기술을 접목하는 데 관심이 많다.
- **책의 성격(Scope)**: IT 관리부터 개발 업무까지, WSL을 쓰며 만나는 다양한 과제를 폭넓게 다루는 실무서다.
- **헌정(Dedication)**: 저자는 이 책을 WSL 커뮤니티에 바친다고 밝힌다.

---

## 2. 대상 독자와 다루는 범위

- **대상 독자(Audience)**: WSL을 개발 환경으로 쓰려는 개발자와, WSL을 조직에 도입해서 관리해야 하는 IT 관리자를 모두 염두에 두고 썼다.
- **실습 주제(Hands-on topics)**: 널리 쓰이는 통합 개발 환경(IDE)을 WSL에 연결하기, WSL 2용 커스텀 리눅스 커널 빌드하기, 자체 패키지를 담은 파생 리눅스 배포판 만들기, WSL의 bash 스크립트로 Outlook 메일 자동화하기를 직접 해 본다.
- **설정과 최적화(Tuning)**: 명령줄부터 레지스트리까지 WSL 1과 WSL 2의 고급 설정을 다룬다. `wsl.conf`와 `.wslconfig`의 모든 옵션, 그리고 성능을 높이는 권장 사항도 함께 설명한다.

---

## 3. WSL의 역사 요약

머리말은 본격적인 내용에 들어가기 전에 WSL이 어떻게 태어났는지부터 정리한다.

1. **Project Astoria(2015~2017)**: Windows Phone에서 안드로이드 앱을 실행하려던 Microsoft 내부 프로젝트다(공개 명칭은 Windows Bridge for Android). 2015년 Build에서 발표되었지만 정식으로 출시되지 못하고, 2017년 Windows Phone과 함께 종료되었다. 기반 기술은 Microsoft Research의 Project Drawbridge에서 나왔다. Drawbridge는 pico process를 이용해 애플리케이션을 샌드박스에 가두는 연구였다.
2. **Bash on Ubuntu on Windows(2016)**: Astoria의 기반 기술을 개발자용 Bash 터미널로 다시 활용했다. 핵심은 바이너리 변환 계층이다. 이 계층이 NT 커널 위의 pico process에서 리눅스 바이너리를 실행한다. Canonical과 협력해 Windows 10 1607에 포함되었다.
3. **Windows Subsystem for Linux(2017)**: Windows 10 1709부터 이름이 WSL로 바뀌었고, Microsoft Store에서 여러 배포판을 설치할 수 있게 되었다. 이 변환 계층 방식은 2019년에 WSL 2가 발표된 뒤로 **WSL 1**이라고 부른다.
4. **WSL 2(2019년 발표, Windows 10 2004에서 정식 출시)**: 변환 계층 대신 경량 Hyper-V 컨테이너 안에서 실제 리눅스 커널을 실행한다. Windows 10 Home을 포함한 모든 에디션에서 쓸 수 있다. 호환성과 성능이 크게 좋아졌고, GPU 가속, 공식 GUI 지원, KVM 게스트를 위한 중첩 가상화도 가능해졌다.

- **이름의 유래(Naming)**: 이름은 이전 POSIX 호환 계층인 Windows Services for UNIX의 작명 방식을 따랐다고 한다. 상표 문제 때문에 이름을 Linux로 시작할 수 없었다는 사정도 있다. 당시에는 리눅스 커널이 들어 있지도 않았다. "리눅스를 실행하는 Windows의 하위 시스템"이라고 이해하면 된다.

---

## 4. 책의 구성과 읽는 법

- **1~2장**: WSL 아키텍처(WSL 1과 WSL 2의 차이, GPU와 GUI의 앞으로의 방향), WSL 활성화, 배포판 설치.
- **3~4장**: 배포판 관리(목록 확인, 실행, 백업과 복원, 커널 관리), 리눅스 배포판 유지보수(패키지, 직접 만드는 Ubuntu 이미지).
- **5~6장**: 배포판별 설정(`wsl.conf`), WSL 2 전역 설정(`.wslconfig`, 레지스트리).
- **7~8장**: X 서버와 GUI 앱, 자체 init 설정, systemd 실행, 커널 직접 빌드, KVM, 고급 네트워킹.
- **9~10장**: Windows와의 상호운용성, 엔터프라이즈 개발(Microk8s, Docker Desktop, IDE 연결, GPU 연산).
- **11~12장**: 문제 해결, 대규모 배포.

읽는 요령은 읽는 사람의 상황에 따라 다르다.

- **처음 입문하는 경우**: 1~3장에서 개념과 기본 조작을 익힌 뒤, 필요한 장으로 넘어간다.
- **설정이 주 관심사인 경우**: 5~6장을 참고 자료로 두고, 필요할 때 찾아본다.
- **관리자인 경우**: 11~12장을 먼저 읽고, 필요하면 앞 장으로 돌아간다.

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
