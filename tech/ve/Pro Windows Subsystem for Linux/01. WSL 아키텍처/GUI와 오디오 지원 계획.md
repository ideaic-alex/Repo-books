# GUI와 오디오 지원 계획

Build 2020에서 Microsoft는 WSL 2에 공식 GUI 지원을 넣겠다고 발표했다. 이 문서는 책이 설명하는 계획된 구조, 즉 Wayland 컴포지터, RDP 전송, 오디오 방식을 정리한다. 책을 쓸 당시에는 자세한 내용이 2021년에 공개될 예정이었다.

---

## 1. 현재의 GUI 실행 방법

- 공식 지원이 나오기 전에도 WSL 1과 2에서 Windows용 X 서버(VcXsrv, X410 등)로 GUI 앱을 실행할 수 있다.
- 설정 방법은 책의 7장 "Customizing WSL"에서 다룬다.

---

## 2. 예정된 구조

- **Wayland 컴포지터(compositor)**: Weston을 기반으로 하며, 화면 구성 요소를 RDP로 Windows에 넘긴다.
- **렌더링 위치**: 실제 그리기는 Windows에서 컴퓨터의 GPU로 처리한다. 앱 창을 비롯한 리눅스 GUI 요소를 Windows가 그리고, 키보드와 마우스 입력도 Windows가 받아서 리눅스로 돌려보낸다.
- **Xwayland**: Xorg 라이브러리를 쓰는 기존 리눅스 GUI 앱을 위한 호환 계층이다. Wayland 입력 장치를 사용하고 출력은 Wayland 표면으로 넘기는 X 서버가 들어 있다.
- 이 컴포지터는 Windows에 내장된 RDP 클라이언트와 연결된다.

---

## 3. RDP의 RAIL과 VAIL

- **RAIL(Remote Application Integrated Locally)**: 책을 쓸 당시 리눅스의 그래픽 데이터를 Windows로 보낼 때 쓰던 RDP 채널이다.
- **VAIL(Virtual Application Integrated Locally)**: Microsoft가 제안한 RDP 확장이다. 당시에는 Windows 클라이언트끼리만 쓸 수 있었다.
- VAIL이 RDP 표준에 들어가면 RAIL 채널을 거치지 않고, 비디오 프레임버퍼를 리눅스에서 Windows로 바로 복사할 수 있다. 그러면 GUI 성능이 크게 좋아진다. 이 방식은 Intel GVT-g 기술과 비슷하며, 원격·가상 데스크톱과 연동하는 데도 쓸 수 있다.
- Microsoft는 Wayland 컴포지터, FreeRDP에 기여한 코드, RDP 확장을 모두 오픈소스로 공개하겠다고 밝혔다.

---

## 4. 오디오

- GUI와 함께 오디오도 지원한다.
- 최소한의 **PulseAudio** 계층이 별도의 사이드카 컨테이너(sidecar container)에서 실행된다. 통신에 쓰는 유닉스 도메인 소켓은 WSL 2 배포판에 마운트된다.

---

## 5. 이 장의 맺음

- 실제 오픈소스 리눅스 커널과, 업스트림에 올리는 개방형 프로토콜을 중심에 두는 방향은 Microsoft의 큰 전환으로 평가된다.
- 이런 구조를 이해해 두면 이후 장에서 각 구성 요소를 활용하는 방법을 더 쉽게 따라갈 수 있다.

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
