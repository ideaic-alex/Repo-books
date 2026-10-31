# Ansible로 Ubuntu on WSL 관리

Ansible은 대표적인 오픈소스 구성 관리 자동화 플랫폼이다. Red Hat이 개발했고 GitHub와 Ubuntu APT 저장소에서 받을 수 있으며 유료 지원 플랜도 있다. 이 문서는 WSL 배포판을 Ansible로 관리하기 위한 서버 조건, sshd 구성, 포트 설계, 인벤토리와 키 인증을 정리한다.

---

## 1. 사전 조건

- **서버 측(Control node)**: Ansible 서버는 Linux 또는 macOS 시스템이 필요하다. Windows는 서버로 지원되지 않는다.
- **관리 대상(Managed node)**: 관리할 시스템은 OpenSSH 같은 SSH 서버를 실행해야 한다. Ubuntu WSL에서는 APT로 설치한다.

```bash
sudo apt install openssh-server
```

- **서비스 기동**: WSL은 서비스를 자동으로 시작하지 않으므로 앞서 다룬 systemd 환경을 구성하거나, systemd를 쓰지 않을 경우 다른 방법으로 `sshd`를 기동해야 한다.
- **Task Scheduler 방식**: Windows 로그인 시 실행되는 작업 스케줄러 작업이 `wsl.exe`로 배포판과 그 안의 sshd를 시작하게 한다.

---

## 2. 포트 설계

- **기본값(Default)**: sshd는 22번 포트를 사용한다.
- **한 PC에 여러 배포판**: 같은 포트를 여러 서비스가 동시에 듣지 못하므로 배포판마다 sshd 포트를 다르게 설정한다. 원격 서버에서 관리할 때는 Windows PC의 호스트 이름이나 IP로 접속하고, 각 WSL 인스턴스에서 Windows로 프록시된 포트를 대상으로 한다.
- **같은 PC 안의 예외**: 서버와 관리 대상이 모두 같은 PC의 WSL 2 배포판이면 포트를 바꾸지 않고 내부 주소로 각각 지정할 수 있다. 내부 주소는 WSL 2에서만 PC의 실제 네트워크와 분리되어 존재하므로 서버와 클라이언트 모두 WSL 2여야 한다.

---

## 3. 인벤토리와 키 인증

- **호스트 인벤토리(Inventory)**: 관리 서버의 `/etc/ansible/hosts`에 호스트 이름 또는 IP를 적고, 22번이 아니면 `이름:포트` 형태로 포트를 붙인다.
- **SSH 키 쌍**: 서버에서 `ssh-keygen`으로 키를 만들고 공개키를 각 클라이언트에서 접속 사용자의 `$HOME/.ssh/authorized_keys`에 넣는다. Ubuntu는 기본적으로 공개키 인증을 지원한다.
- **키 배포 요령**: 공개키와 개인키가 모두 있는 시스템에서 `ssh-copy-id`를 쓰면 편하다. 이때 클라이언트 sshd가 비밀번호 인증을 허용하도록 잠시 바꿔야 할 수 있다.

```text
192.0.2.50
windows-pc.example.org
windows-pc.example.org:8022
```

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
