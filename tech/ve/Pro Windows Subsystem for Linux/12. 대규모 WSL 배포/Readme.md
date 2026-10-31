# 12장. 대규모 WSL 배포 (Deploying WSL at Scale)

WSL을 여러 PC와 사용자에게 배포하려면 배포 전에 알아 둘 점이 있고, 배포한 뒤에는 배포판 현황을 파악하고 관리할 도구가 필요하다. 이 장은 배포할 때 고려할 점과 Intune으로 배포하는 방법을 다룬다. 이어서 Canonical Landscape와 Ansible로 Ubuntu on WSL을 관리하는 방법을 설명한다.

---

## 1. 핵심 요점

- WSL 파일 시스템은 사용자 계정의 `%APPDATA%\local` 아래에 저장되므로, PC를 재시작해도 이 디렉터리가 지워지지 않아야 한다.
- 자동화로 설치할 때는 `wsl.exe --import`로 지워지지 않는 위치를 직접 지정할 수 있다.
- 사용자는 WSL 배포판 안에서 root 권한을 갖지만, Windows 자원에는 자기 Windows 계정에 허용된 만큼만 접근한다.
- 서드파티 보안 제품이 WSL 드라이버를 막을 수 있으므로, 전체 사용자에게 배포하기 전에 테스트한다.
- Intune으로 Store의 WSL 배포판을 미리 설치해 두고, 배포한 뒤에는 Landscape나 Ansible로 관리한다.
- Landscape와 Ansible 모두 systemd 환경이 필요하다. systemd를 쓰지 않는다면 sshd를 다른 방법으로 직접 실행해야 한다.

---

## 2. 섹션 문서

- [배포 시 고려사항과 Intune](배포%20시%20고려사항과%20Intune.md)
- [Landscape로 Ubuntu on WSL 관리](Landscape로%20Ubuntu%20on%20WSL%20관리.md)
- [Ansible로 Ubuntu on WSL 관리](Ansible로%20Ubuntu%20on%20WSL%20관리.md)

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
