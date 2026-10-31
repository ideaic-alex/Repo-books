# 방화벽과 GUI 문제 해결

WSL 2는 별도의 가상 네트워크를 쓰기 때문에, Windows 쪽 X 서버가 WSL의 접속을 받으려면 방화벽을 열어 줘야 한다. 이 문서는 X 서버별 허용 방법, 노출 범위를 줄이는 규칙, GUI가 뜨지 않을 때 확인할 항목을 정리한다.

---

## 1. WSL 2에서 방화벽 허용

- **X410**: 트레이 아이콘을 우클릭해 "Allow Public Access"를 선택한다. 이어서 Windows 방화벽 창에서 "Public networks"를 체크하고 X410을 다시 시작한다.
- **VcXsrv**: XLaunch 설정에서 "Disable access control"을 체크한다. 방화벽 창에서 "Public networks"를 체크하는 것은 X410과 같다.

---

## 2. 공용 네트워크 노출 위험과 대응

- 공용 네트워크에서 서비스를 여는 것은 분명한 보안 위험이다.
- **대응 1**: 카페나 기내 같은 공용 네트워크에서는 GUI 앱을 쓰지 않는다.
- **대응 2**: WSL 가상 서브넷에서 오는 접속만 허용하도록 방화벽 규칙을 만든다.

범위를 제한하는 규칙은 다음 순서로 만든다.

1. WSL에서 `cmd.exe /C wf.msc`를 실행해 고급 방화벽 설정을 연다.
2. "Inbound Rules"에서 사용 중인 X 서버를 찾는다. 공용/개인 네트워크와 TCP/UDP별로 규칙이 따로 있으며, 고칠 대상은 공용 TCP 규칙이다.
3. 속성의 General에서 "Allow the connection"을 선택한다.
4. "Protocols and Ports"에서 프로토콜은 TCP, 로컬 포트는 특정 포트 6000으로 지정한다.
5. "Scope"의 원격 IP 주소에 `172.16.0.0/12`(WSL 가상 서브넷 범위)를 추가한다.
6. 공용 UDP 규칙은 차단 상태로 둔다. X 프로토콜은 보통 UDP를 쓰지 않는다.

---

## 3. 실행 오류 점검

- **대표 증상(cannot open display)**: "cannot open display"나 "Connection refused" 같은 오류는 배포판이 Windows의 X 서버에 연결하지 못했다는 뜻이다.
- **점검 순서**: X 서버가 설치되어 있는지, 실행 중인지(트레이 아이콘으로 확인), `DISPLAY`가 WSL 버전에 맞게 설정되어 있는지를 차례로 확인한다.

---

## 4. dbus 문제

- **dbus**: 리눅스 데스크톱에서 프로그램끼리 메시지를 주고받게 해 주는 서비스다. X는 정상인데 특정 앱만 실패하고 오류 메시지에 dbus가 보일 때 시도해 볼 만하다.
- 먼저 패키지를 설치하고, 장치 ID를 만든다(배포판을 설치할 때 한 번만 하면 된다). 그다음 GUI 앱을 실행하기 전에 `dbus-launch`를 실행한다.

```bash
sudo apt install dbus-x11
sudo dbus-uuidgen --ensure
dbus-launch --exit-with-x11
```

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
