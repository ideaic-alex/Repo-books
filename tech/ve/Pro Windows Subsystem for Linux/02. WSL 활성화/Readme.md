# 2장. WSL 활성화 (Enabling WSL)

WSL은 기본으로 꺼져 있어서 GUI나 명령줄에서 직접 켜야 한다. 모든 Windows 에디션에서 켤 수 있다. 이 장은 WSL을 켜는 여러 방법과 배포판을 설치하는 방법을 설명하고, 설치할 때 내부에서 어떤 일이 일어나는지도 다룬다.

---

## 1. 이 장의 핵심 요점

- **활성화 방법**: GUI, PowerShell, DISM, `wsl.exe --install` 중 환경에 맞는 방법을 고른다. WSL 2를 쓰려면 Virtual Machine Platform도 켜야 한다.
- **기본 버전**: GUI나 명령으로 WSL 2를 켰더라도, `wsl.exe --set-default-version 2`로 기본 버전을 따로 지정해야 할 수 있다.
- **배포판 선택**: 패키지 관리자, 앱 지원 여부, 유료 지원, WSL 전용 기능을 기준으로 고른다.
- **설치 방법**: 스토어에서 설치하는 방법이 권장된다. 그 밖에 `.appx` 파일을 직접 설치(사이드로드)하는 방법이 있는데, 개발자 모드를 켜야 하고 보안에 주의해야 한다. `wsl.exe --import`로 rootfs를 가져와 설치하는 방법도 있다.
- **저장 위치**: WSL 1은 일반 폴더에 파일 시스템으로 저장하고, WSL 2는 `ext4.vhdx` 파일에 저장한다. 이 파일들에는 직접 접근하지 말고 `\\wsl$\` 경로로 접근한다.
- **내부 구성**: `system32\lxss` 폴더의 도구와 라이브러리, 그리고 DistroLauncher가 호출하는 비공개 WSL API(공식 문서가 없는 API)로 이루어진다.

---

## 2. 섹션 문서

- [WSL 활성화 방법](WSL%20활성화%20방법.md)
- [배포판 선택과 설치](배포판%20선택과%20설치.md)
- [rootfs 가져오기](rootfs%20가져오기.md)
- [설치 위치와 WSL 도구](설치%20위치와%20WSL%20도구.md)
- [WSL API와 DistroLauncher](WSL%20API와%20DistroLauncher.md)

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
