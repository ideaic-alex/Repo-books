# 2장. WSL 활성화 (Enabling WSL)

WSL은 기본으로 꺼져 있어서 GUI나 명령줄로 켜야 하며, 모든 Windows 에디션에서 가능하다. 이 장은 여러 활성화 방법과 배포판 설치 방법, 그리고 설치가 내부에서 어떻게 이뤄지는지를 다룬다.

---

## 1. 이 장의 핵심 요점

- **활성화 방법**: GUI, PowerShell, DISM, `wsl.exe --install` 중 환경에 맞게 선택한다. WSL 2는 Virtual Machine Platform도 필요하다.
- **기본 버전**: GUI나 명령으로 WSL 2를 켜도 `wsl.exe --set-default-version 2`로 기본값을 따로 지정해야 할 수 있다.
- **배포판 선택**: 패키지 관리자, 앱 지원, 상용 지원, WSL 전용 기능을 기준으로 고른다.
- **설치 경로**: 스토어(권장), `.appx` 사이드로드(개발자 모드와 보안 주의), `wsl.exe --import`로 rootfs 가져오기.
- **저장 위치**: WSL 1은 파일 시스템 폴더, WSL 2는 `ext4.vhdx`이며 직접 접근은 금지하고 `\\wsl$\`를 이용한다.
- **내부 구성**: `system32\lxss` 도구와 라이브러리, DistroLauncher가 호출하는 문서화되지 않은 WSL API.

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
