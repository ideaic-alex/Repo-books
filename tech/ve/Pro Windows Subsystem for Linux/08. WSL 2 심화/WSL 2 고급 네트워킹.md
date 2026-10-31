# WSL 2 고급 네트워킹

WSL 1은 시스템 콜 변환 계층이라 Windows와 네트워크 스택을 공유했고 localhost가 곧 localhost였다. WSL 2는 DHCP NAT 서브넷의 자체 IP를 가지므로 더 복잡하다. 첫 번째 문제는 X 서버 연결(7장)이고, 두 번째는 WSL 2 서비스를 장치 밖(LAN)에서 접근하는 일이다.

---

## 1. LAN 노출이 필요한 이유

- localhost에서는 WSL 안의 서비스가 보이지만 다른 장치에서는 접근할 수 없다.
- 외부 접근에는 Windows 방화벽의 포트 개방과, 그 포트를 WSL 2 환경 IP로 포워딩하는 설정이 모두 필요하다.
- 예시는 Apache 웹 서버(`sudo service apache2 start`)이며, `wslview http://localhost`(wslutilities 도구)로 기본 페이지를 연다.

---

## 2. IP 주소 확인

- **Windows IP**: PowerShell의 `Get-NetIPAddress`로 이더넷이나 Wi-Fi 주소를 확인한다. 이 주소는 LAN의 다른 장치에서 접근할 수 있다.
- **WSL IP**: `ip a`에서 `eth0` 장치를 보거나 `ip addr show eth0`를 awk로 파싱한다. 이 주소는 기본적으로 LAN에서 접근할 수 없다.
- 포워딩과 방화벽 설정 전에 다른 장치에서 접속하면 시간 초과가 난다.

---

## 3. 포트 프록시와 방화벽 규칙

관리자 권한 PowerShell에서 진행한다.

- **포트 프록시(portproxy)**: `netsh interface portproxy`로 Windows IP의 포트를 WSL IP의 같은 포트로 연결한다.
- **방화벽 규칙**: `netsh advfirewall`로 해당 포트의 인바운드 TCP를 허용한다.
- **대안(주의)**: `New-NetFirewallRule`로 WSL 가상 어댑터(`vEthernet (WSL)`)로 오는 모든 트래픽을 허용할 수 있다. 하지만 Windows 방화벽의 보호 없이 WSL을 네트워크에 완전히 개방하므로 주의해야 한다.

```
netsh interface portproxy add v4tov4 listenaddress=<Windows IP> listenport=80 connectaddress=<WSL IP> connectport=80
netsh advfirewall firewall add rule name="Open Port 80 for WSL2" dir=in action=allow protocol=TCP localport=80
```

---

## 4. WSL IP가 바뀌는 문제와 자동화

- WSL 2의 IP는 실행할 때마다 바뀌므로 재부팅 후 포트 포워딩을 매번 다시 설정해야 한다.
- PowerShell이나 bash 명령을 `.bashrc`에 넣거나 빌드 21286 이상의 `[boot] command=` 옵션으로 자동화한다.
- 책의 스크립트는 다음 순서로 동작한다.
  1. `Get-NetIPAddress -AddressFamily IPv4`로 네트워크 어댑터의 InterfaceIndex를 미리 알아 둔다.
  2. 스크립트 안에서 `eth0`의 현재 WSL IP를 구한다.
  3. `powershell.exe`로 InterfaceIndex에 해당하는 Windows IP를 조회한다.
  4. `Start-Process -Verb RunAs`로 `netsh`를 호출해 portproxy를 다시 등록한다.
- 스크립트 상단에서 InterfaceIndex와 포트 번호만 설정값으로 바꿔 쓰면 된다.

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
