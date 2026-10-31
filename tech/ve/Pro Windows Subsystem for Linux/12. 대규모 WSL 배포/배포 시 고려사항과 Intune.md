# 배포 시 고려사항과 Intune

WSL을 조직 단위로 배포할 때 미리 알아 둘 점을 정리한다. 파일 시스템 저장 위치, 사용자 권한, 배포판 현황 관리, 보안 소프트웨어와의 충돌이 여기에 해당한다. 마지막에는 Microsoft Intune으로 배포판을 설치하는 방법도 다룬다.

---

## 1. 배포 전 고려사항

- **저장 위치 보존**: WSL 파일 시스템은 사용자 계정의 `%APPDATA%\local` 디렉터리 안에 저장된다. 재시작할 때 이 디렉터리가 지워지면 로그인할 때마다 배포판을 다시 설치해야 한다.
- **대안**: 자동화 도구가 사용자 대신 `wsl.exe --import`를 실행하게 하면 파일 시스템을 저장할 위치를 직접 정할 수 있다. 재시작해도 지워지지 않는 경로를 고르면 된다.

```powershell
wsl.exe --import <배포판이름> <설치경로> <rootfs.tar>
```

- **권한 범위**: PC 사용자는 WSL 배포판 안에서 root 권한을 가진다. 리눅스의 root는 Windows의 Administrator 계정처럼 해당 배포판 안에서 모든 권한을 가진 계정이다. 하지만 Windows 자원에는 Windows 보안 정책이 그대로 적용된다. 그래서 사용자는 배포판 안에서 root여도 자기 Windows 계정이 허용하는 만큼만 Windows 자원에 접근할 수 있다.
- **현황 파악**: PC와 사용자가 늘어날수록 WSL 설치 현황을 관리하기가 어려워진다. 배포한 배포판 전체를 파악할 수 있도록 Ansible이나 Landscape 같은 관리 시스템을 쓰기를 권한다.
- **보안 제품**: 서드파티 보안 시스템이 WSL 드라이버를 불러오지 못하게 막을 수 있다. 예상하지 못한 문제를 피하려면 사용자에게 배포하기 전에 반드시 테스트한다.

---

## 2. Intune으로 Ubuntu on WSL 배포

- **MDM 개념(Mobile Device Management)**: 기업이 모든 PC와 모바일 기기에 표준 앱과 설정을 똑같이 적용하도록 관리하는 방식이다.
- **Intune(Microsoft)**: Microsoft의 MDM 제품이다. Windows Store에 있는 WSL 배포판을 사용자 PC에 미리 설치해 둘 수 있다.
- **효과**: 사용자는 회사 기기에 로그인하자마자 WSL을 바로 쓸 수 있다.

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
