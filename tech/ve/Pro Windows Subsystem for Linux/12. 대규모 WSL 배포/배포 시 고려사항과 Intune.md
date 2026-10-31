# 배포 시 고려사항과 Intune

WSL을 조직 단위로 배포할 때 미리 알아 둘 저장 위치, 권한, 관리, 보안 소프트웨어 문제와 Microsoft Intune을 이용한 배포 방식을 정리한다.

---

## 1. 배포 전 고려사항

- **저장 위치 보존(Persistence)**: WSL 파일 시스템은 사용자 계정의 `%APPDATA%\local` 디렉터리 안에 저장된다. 재시작 때 이 디렉터리가 지워지면 로그인할 때마다 배포판을 다시 설치해야 한다.
- **대안(Alternative)**: 자동화로 사용자 대신 `wsl.exe --import`를 실행해 파일 시스템 저장 위치를 직접 지정하면 영속적인 경로를 고를 수 있다.

```powershell
wsl.exe --import <배포판이름> <설치경로> <rootfs.tar>
```

- **권한 범위(Privileges)**: PC 사용자는 WSL 배포판 안에서 root 권한을 가진다. root는 리눅스 안에서 Windows의 Administrator처럼 완전한 권한이다. 다만 Windows 보안 정책은 Windows 자원에 그대로 적용되어, 사용자는 자신의 Windows 계정이 허용하는 만큼만 접근한다.
- **가시성(Visibility)**: PC와 사용자가 늘수록 WSL 설치 현황 관리가 어려우므로 Ansible, Landscape 같은 관리 시스템으로 배포판 전체를 파악하도록 권한다.
- **보안 제품(Security software)**: 서드파티 보안 시스템이 WSL 드라이버 로드를 막을 수 있다. 사용자에게 배포하기 전에 반드시 테스트한다.

---

## 2. Intune으로 Ubuntu on WSL 배포

- **MDM 개념(Mobile Device Management)**: 기업의 모든 PC와 모바일 기기에 표준 앱과 설정을 맞추는 관리 방식이다.
- **Intune(Microsoft)**: Microsoft의 MDM 제품으로, Windows Store의 WSL 배포판을 사용자 시스템에 미리 설치해 둘 수 있다.
- **효과(Benefit)**: 사용자는 회사 기기에 로그인하자마자 바로 쓸 수 있는 WSL을 갖게 된다.

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
