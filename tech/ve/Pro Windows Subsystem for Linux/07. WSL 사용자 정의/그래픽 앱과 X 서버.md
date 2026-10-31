# 그래픽 앱과 X 서버

WSL에서 리눅스 GUI 앱을 쓰는 공식 기능(WSLg)은 이 책 집필 시점에 Windows Insider Dev 채널 프리뷰였다. 정식 버전에서 지금 GUI 앱을 쓰려면 Windows에 X 서버를 따로 설치하고, 배포판이 그 서버로 화면을 보내도록 설정해야 한다.

---

## 1. 동작 원리

- **배포판 내부의 X 서버(X server)**: GUI 앱을 설치하면 의존성으로 함께 깔리지만 실제로는 사용하지 않는다.
- **X 출력 전달(X forwarding)**: 앱의 화면 출력을 로컬 포트를 통해 Windows에서 돌아가는 X 서버로 보낸다.

---

## 2. Windows용 X 서버 선택

- 후보로는 VcXsrv, X410, Xmanager, Xming, Cygwin/X, MobaXterm이 있다.
- **VcXsrv**: 무료 오픈소스이며 upstream Xorg 코드 기반이다. 대신 올바르게 띄우는 데 손이 더 간다.
- **X410**: 유료이며 Microsoft Store에서만 받을 수 있다. 완성도가 높고 수동 설정이 적다.
- 커뮤니티에서는 이 두 가지가 가장 흔하다.

---

## 3. DISPLAY 변수 설정

- **WSL 1**: 네트워크 스택이 Windows와 같으므로 로컬 주소를 그대로 가리키면 된다.
- **WSL 2**: 호스트 Windows의 IP로 보내야 한다. 이 IP는 WSL이 자동 생성한 `/etc/resolv.conf`의 nameserver 값에서 얻는다.
- `wsl.conf`로 `resolv.conf` 자동 생성을 껐다면 값이 맞지 않을 수 있다. 이때는 `powershell.exe`로 Windows 쪽 IP를 조회하는 방식으로 대체한다.
- 자주 쓴다면 `.bashrc`에 넣거나, Windows 10 빌드 21286 이상에서는 `/etc/wsl.conf`의 `[boot]` 명령으로 등록한다.
- **libGL 가속(LIBGL_ALWAYS_INDIRECT)**: 앱이 libGL 가속을 제공하면 이 변수를 1로 두어 렌더링을 Windows 쪽 X 서버에 넘긴다. OpenGL 1.4 이하에 효과가 있다.

```bash
export DISPLAY=127.0.0.1:0.0                                          # WSL 1
export DISPLAY=$(awk '/nameserver/ {print $2}' /etc/resolv.conf):0    # WSL 2
export LIBGL_ALWAYS_INDIRECT=1
```

---

## 4. GUI 앱 설치와 실행

- X 서버와 방화벽 설정, 리디렉션까지 끝나면 GUI 앱을 설치한다. Xorg 관련 의존성이 많이 딸려 오지만 배포판의 X 서버는 실행하지 않는다.
- 책의 예시는 간단한 GUI 패키지 관리자인 Synaptic이다.

```bash
sudo apt -y install synaptic
sudo synaptic
```

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
