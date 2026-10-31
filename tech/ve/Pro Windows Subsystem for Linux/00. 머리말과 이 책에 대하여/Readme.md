# 머리말과 이 책에 대하여

이 문서는 Hayden Barnes의 『Pro Windows Subsystem for Linux (WSL)』(Apress, 2021, 1판)의 머리말(Introduction)과 저자 소개를 정리한 노트다. 책이 무엇을 다루는지, 누구를 위한 책인지, WSL이 어떤 역사를 거쳐 지금의 모습이 되었는지를 먼저 훑어 두면 본문을 읽기 쉽다.

---

## 1. 저자와 책 소개

- **저자(Author)**: Hayden Barnes. SUSE에서 Windows Containers 엔지니어링 매니저로 일하며 Microsoft MVP로 인정받았다. 이전에는 Canonical에서 Ubuntu on WSL 팀을 이끌었고, WSL 전문 커뮤니티 컨퍼런스 WSLConf를 만들었으며, WSL 전용 리눅스 배포판을 처음 만든 회사 Whitewater Foundry를 창업했다.
- **기술 감수(Technical Reviewer)**: Nuno Do Carmo. 오랜 Windows·Unix·Linux 관리 경력을 가진 Microsoft MVP로, WSL에 클라우드 네이티브 기술을 접목하는 데 관심이 크다.
- **책의 성격(Scope)**: IT 관리부터 개발 업무까지 WSL로 부딪히는 다양한 과제를 폭넓게 다루는 실무서다.
- **헌정(Dedication)**: WSL 커뮤니티에 바친다고 밝힌다.

---

## 2. 대상 독자와 다루는 범위

- **대상 독자(Audience)**: WSL을 개발 환경으로 쓰려는 개발자와 WSL을 조직에 도입하고 관리해야 하는 IT 관리자 모두를 염두에 둔다.
- **실습 주제(Hands-on topics)**: 인기 통합 개발 환경(IDE) 연결, WSL 2용 커스텀 리눅스 커널 빌드, 자체 패키지를 담은 파생 리눅스 배포판 제작, WSL의 bash 스크립트에서 Outlook 메일 자동화.
- **설정과 최적화(Tuning)**: 명령줄부터 레지스트리까지 WSL 1·2의 고급 설정, `wsl.conf`와 `.wslconfig`의 모든 옵션, 성능 권장 사항을 다룬다.

---

## 3. WSL의 역사 요약

머리말은 본격적인 내용에 앞서 WSL이 어떻게 태어났는지 정리한다.

1. **Project Astoria(2015~2017)**: Windows Phone에서 안드로이드 앱을 돌리려던 Microsoft 내부 프로젝트(공개 명칭 Windows Bridge for Android). 2015년 Build에서 발표되었고 정식 출시 없이 2017년 Windows Phone과 함께 종료되었다. 기반 기술은 Microsoft Research의 Project Drawbridge(pico process 기반 애플리케이션 샌드박싱)에서 나왔다.
2. **Bash on Ubuntu on Windows(2016)**: Astoria의 기반 기술을 개발자용 Bash 터미널로 재활용했다. NT 커널 위 pico process에서 리눅스 바이너리를 실행하는 바이너리 변환 계층이 핵심이며, Canonical과 협력해 Windows 10 1607에 포함되었다.
3. **Windows Subsystem for Linux(2017)**: Windows 10 1709부터 이름이 WSL로 바뀌고 Microsoft Store에서 여러 배포판을 설치할 수 있게 되었다. 이 변환 계층 방식이 2019년 WSL 2 발표 이후 **WSL 1**로 불린다.
4. **WSL 2(2019 발표, Windows 10 2004에서 정식)**: 변환 계층 대신 경량 Hyper-V 컨테이너 안에서 실제 리눅스 커널을 실행한다. Windows 10 Home을 포함한 모든 에디션에서 쓸 수 있고, 호환성과 성능이 크게 좋아졌으며 GPU 가속, 공식 GUI 지원, KVM 게스트용 중첩 가상화가 가능해졌다.

- **이름의 유래(Naming)**: 이전 POSIX 호환 계층인 Windows Services for UNIX의 명명 방식을 따랐고, 상표 문제로 이름을 Linux로 시작하지 못했다고 한다. 당시에는 리눅스 커널이 들어 있지도 않았다. "리눅스를 실행하는 Windows의 하위 시스템"으로 이해하면 된다.

---

## 4. 책의 구성과 읽는 법

- **1~2장**: WSL 아키텍처(WSL 1 대 WSL 2, GPU·GUI 미래 방향)와 WSL 활성화·배포판 설치.
- **3~4장**: 배포판 관리(목록, 실행, 백업·복원, 커널 관리)와 리눅스 배포판 유지보수(패키지, 직접 만드는 Ubuntu 이미지).
- **5~6장**: 배포판별 설정(`wsl.conf`)과 WSL 2 전역 설정(`.wslconfig`, 레지스트리).
- **7~8장**: X 서버와 GUI 앱, 자체 init 구성, systemd 실행, 커널 직접 빌드, KVM, 고급 네트워킹.
- **9~10장**: Windows와의 상호운용성, 엔터프라이즈 개발(Microk8s, Docker Desktop, IDE 연결, GPU 연산).
- **11~12장**: 문제 해결과 대규모 배포.

읽는 요령은 다음과 같다.

- **처음 입문**: 1~3장으로 개념과 기본 조작을 익힌 뒤 필요한 장으로 이동한다.
- **설정 위주**: 5~6장을 참조용으로 두고 필요할 때 찾아본다.
- **관리자 관점**: 11~12장을 먼저 보고 필요에 따라 앞 장으로 돌아간다.

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
