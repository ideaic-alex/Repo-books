# 그래픽 앱과 X 서버

WSL에서 리눅스 GUI 앱을 쓰는 공식 기능(WSLg)은 이 책을 쓸 때 Windows Insider Dev 채널의 프리뷰 단계였다. 정식 버전에서 지금 GUI 앱을 쓰려면 Windows에 X 서버를 따로 설치하고, 배포판이 그 서버로 화면을 보내도록 설정해야 한다.

---

## 1. 동작 원리

- **배포판 안의 X 서버(X server)**: GUI 앱을 설치하면 의존성 패키지로 함께 깔리지만, 실제로는 사용하지 않는다.
- **X 출력 전달(X forwarding)**: 앱이 그리는 화면을 로컬 포트로 내보내면, Windows에서 돌아가는 X 서버가 받아서 화면에 띄운다.

---

## 2. Windows용 X 서버 선택

- 선택지로는 VcXsrv, X410, Xmanager, Xming, Cygwin/X, MobaXterm이 있다.
- **VcXsrv**: 무료 오픈소스이고 upstream Xorg 코드를 기반으로 한다. 대신 제대로 실행되게 하려면 손이 더 간다.
- **X410**: 유료이며 Microsoft Store에서만 받을 수 있다. 완성도가 높고 직접 설정할 것이 적다.
- 커뮤니티에서는 이 두 가지를 가장 많이 쓴다.

---

## 3. DISPLAY 변수 설정

앱이 화면을 어디로 보낼지는 `DISPLAY` 환경 변수가 정한다. 이 값이 WSL 버전에 따라 달라진다.

- **WSL 1**: 네트워크 스택을 Windows와 함께 쓰므로, 로컬 주소를 그대로 지정하면 된다.
- **WSL 2**: 호스트 Windows의 IP로 보내야 한다. 이 IP는 WSL이 자동으로 만든 `/etc/resolv.conf`의 nameserver 값에서 얻는다.
- `wsl.conf`에서 `resolv.conf` 자동 생성을 꺼 두었다면 이 값이 맞지 않을 수 있다. 그럴 때는 `powershell.exe`로 Windows 쪽 IP를 직접 조회해서 쓴다.
- 자주 쓴다면 `.bashrc`에 넣어 두면 된다. Windows 10 빌드 21286 이상에서는 `/etc/wsl.conf`의 `[boot]` 명령으로 등록할 수도 있다.
- **libGL 가속(LIBGL_ALWAYS_INDIRECT)**: 앱이 libGL 가속을 지원하면 이 변수를 1로 지정한다. 그러면 렌더링을 Windows 쪽 X 서버에 맡긴다. OpenGL 1.4 이하에서 효과가 있다.

```bash
export DISPLAY=127.0.0.1:0.0                                          # WSL 1
export DISPLAY=$(awk '/nameserver/ {print $2}' /etc/resolv.conf):0    # WSL 2
export LIBGL_ALWAYS_INDIRECT=1
```

---

## 4. GUI 앱 설치와 실행

- X 서버 설치, 방화벽 설정, `DISPLAY` 지정까지 끝났으면 GUI 앱을 설치한다. Xorg 관련 의존성 패키지가 많이 함께 설치되지만, 배포판 안의 X 서버는 실행하지 않는다.
- 책에서는 간단한 GUI 패키지 관리자인 Synaptic을 예로 든다.

```bash
sudo apt -y install synaptic
sudo synaptic
```

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
