# 방화벽과 GUI 문제 해결

WSL 2는 별도 가상 네트워크를 쓰기 때문에 Windows 쪽 X 서버가 WSL의 접속을 받을 수 있도록 방화벽을 열어야 한다. 이 문서는 서버별 허용 방법, 노출 범위를 줄이는 규칙, 그리고 GUI가 뜨지 않을 때의 점검 항목을 정리한다.

---

## 1. WSL 2에서 방화벽 허용

- **X410**: 트레이 아이콘 우클릭 후 "Allow Public Access"를 선택하고, Windows 방화벽 창에서 "Public networks"를 체크한 다음 X410을 재시작한다.
- **VcXsrv**: XLaunch 설정에서 "Disable access control"을 체크하고, 마찬가지로 방화벽 창에서 "Public networks"를 체크한다.

---

## 2. 공개 네트워크 노출 위험과 대응

- 공용 네트워크에서 서비스를 여는 것은 분명한 보안 위험이다.
- **대응 1**: 카페나 기내 같은 공용 네트워크에서는 GUI 앱을 쓰지 않는다.
- **대응 2**: 허용 범위를 WSL 가상 서브넷으로만 제한하는 방화벽 규칙을 만든다.

제한 규칙을 만드는 절차는 다음과 같다.

1. WSL에서 `cmd.exe /C wf.msc`로 고급 방화벽 설정을 연다.
2. "Inbound Rules"에서 사용 중인 X 서버를 찾는다. 공용/개인 네트워크와 TCP/UDP별로 규칙이 있으며 편집 대상은 공용 TCP 규칙이다.
3. 속성의 General에서 "Allow the connection"을 선택한다.
4. "Protocols and Ports"에서 프로토콜을 TCP, 로컬 포트를 특정 포트 6000으로 지정한다.
5. "Scope"에서 원격 IP 범위로 `172.16.0.0/12`(WSL 가상 서브넷 범위)를 추가한다.
6. 공용 UDP 규칙은 차단 상태로 둔다. X 프로토콜은 보통 UDP를 쓰지 않는다.

---

## 3. 실행 오류 점검

- **대표 증상(cannot open display)**: "cannot open display"나 "Connection refused" 계열 오류는 배포판이 Windows의 X 서버에 연결하지 못했다는 뜻이다.
- **체크리스트**: X 서버가 설치되어 있는지, 실행 중인지(트레이 확인), `DISPLAY`가 WSL 버전에 맞게 설정됐는지 순서대로 본다.

---

## 4. dbus 문제

- **dbus**: 리눅스 데스크톱의 장치 메시징 서비스다. X는 정상인데 특정 앱만 실패하고 오류 메시지에 dbus가 나올 때 시도해 볼 만하다.
- 설치와 장치 ID 생성(배포판 설치당 한 번), 그리고 GUI 앱 실행 전 `dbus-launch` 실행 순서로 진행한다.

```bash
sudo apt install dbus-x11
sudo dbus-uuidgen --ensure
dbus-launch --exit-with-x11
```

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
