# 12장. 대규모 WSL 배포 (Deploying WSL at Scale)

WSL을 여러 PC와 사용자에게 배포하려면 배포 전에 알아 둘 점이 있고, 배포 후에는 배포판 현황을 파악하고 관리할 도구가 필요하다. 이 장은 배포 시 고려사항과 Intune을 통한 배포, Canonical Landscape와 Ansible을 이용한 Ubuntu on WSL 관리를 다룬다.

---

## 1. 핵심 요점

- WSL 파일 시스템은 사용자 계정의 `%APPDATA%\local` 아래에 저장되므로 재시작 후에도 이 디렉터리가 보존되어야 한다.
- 자동화로 설치할 때는 `wsl.exe --import`로 영속적인 위치를 지정할 수 있다.
- 사용자는 WSL 배포판 안에서 root 권한을 갖지만 Windows 자원에는 Windows 계정 권한만큼만 접근한다.
- 서드파티 보안 제품이 WSL 드라이버를 막을 수 있으니 전면 배포 전에 테스트한다.
- Intune으로 Store의 WSL 배포판을 사전 배치하고, Landscape나 Ansible로 배포 후 관리한다.
- Landscape와 Ansible 모두 systemd 환경(또는 sshd를 다른 방법으로 기동)이 전제된다.

---

## 2. 섹션 문서

- [배포 시 고려사항과 Intune](배포%20시%20고려사항과%20Intune.md)
- [Landscape로 Ubuntu on WSL 관리](Landscape로%20Ubuntu%20on%20WSL%20관리.md)
- [Ansible로 Ubuntu on WSL 관리](Ansible로%20Ubuntu%20on%20WSL%20관리.md)

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
