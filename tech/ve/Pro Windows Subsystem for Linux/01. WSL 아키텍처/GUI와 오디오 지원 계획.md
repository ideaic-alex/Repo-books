# GUI와 오디오 지원 계획

Build 2020에서 Microsoft는 WSL 2에 공식 GUI 지원을 도입하겠다고 발표했다. 이 문서는 책이 서술하는 계획된 구조, 즉 Wayland 컴포지터, RDP 전송, 오디오 방식을 정리한다. 집필 당시에는 상세 내용이 2021년에 공개될 예정이었다.

---

## 1. 현재의 GUI 실행 방법

- 공식 지원 이전에도 WSL 1과 2에서 Windows용 X 서버(VcXsrv, X410 등)로 GUI 앱을 실행할 수 있다.
- 설정 방법은 책의 7장 "Customizing WSL"에서 다룬다.

---

## 2. 예정된 구조

- **Wayland 컴포지터(compositor)**: Weston 기반이며, 화면 구성 요소를 RDP로 Windows에 넘긴다.
- **렌더링 위치**: 실제 그리기는 Windows에서, 컴퓨터의 GPU로 이뤄진다. 앱 창을 포함한 리눅스 GUI 요소를 Windows가 그리고, 키보드와 마우스 입력은 Windows가 받아 리눅스로 되돌려 보낸다.
- **Xwayland**: Xorg 라이브러리 기반의 기존 리눅스 GUI 앱을 위한 호환 계층. Wayland 입력 장치를 쓰고 출력은 Wayland 표면으로 전달하는 X 서버를 포함한다.
- 이 컴포지터는 Windows에 내장된 RDP 클라이언트와 연결된다.

---

## 3. RDP의 RAIL과 VAIL

- **RAIL(Remote Application Integrated Locally)**: 집필 시점에 리눅스의 그래픽 데이터를 Windows로 보내는 데 쓰는 RDP 채널.
- **VAIL(Virtual Application Integrated Locally)**: Microsoft가 제안한 RDP 확장. 당시에는 Windows 클라이언트 사이에서만 쓰였다.
- VAIL이 RDP 표준에 들어가면 RAIL 채널 대신 비디오 프레임버퍼를 리눅스에서 Windows로 직접 복사할 수 있어 GUI 성능이 크게 좋아진다. Intel GVT-g 기술과 비슷하며 원격·가상 데스크톱 연동에도 응용될 수 있다.
- Microsoft는 Wayland 컴포지터, FreeRDP 기여분, RDP 확장을 모두 오픈소스로 공개하겠다고 했다.

---

## 4. 오디오

- GUI와 함께 오디오도 지원된다.
- 최소한의 **PulseAudio** 계층이 별도의 사이드카 컨테이너(sidecar container)에서 돌아가고, 통신에 쓰는 유닉스 도메인 소켓이 WSL 2 배포판에 마운트된다.

---

## 5. 이 장의 맺음

- 실제 오픈소스 리눅스 커널과 업스트림으로 올리는 개방형 프로토콜을 중심에 두는 방향은 Microsoft의 큰 전환으로 평가된다.
- 이런 구조 이해를 바탕으로 이후 장에서 각 구성 요소를 활용하는 법을 다룬다.

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
