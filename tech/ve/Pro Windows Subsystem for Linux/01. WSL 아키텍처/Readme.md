# 1장. WSL 아키텍처 (WSL Architecture)

WSL을 제대로 활용하거나 기업 환경에 배포하려면 내부 구조와 역사를 알아야 한다. 이 장은 WSL 1과 WSL 2가 각각 어떤 방식으로 리눅스와 Windows의 상호 운용을 구현하는지 설명하고, 이후 추가될 GPU와 GUI 같은 최신 기능까지 살펴본다.

---

## 1. 이 장의 핵심 요점

- **WSL 1**: 피코 프로세스(pico process)와 `LxCore.sys`가 리눅스 시스템 콜을 NT 시스템 콜로 변환하는 방식이며, 호환성은 약 90%다.
- **WSL 2**: Hyper-V 기반 경량 가상화 위에서 실제 리눅스 커널이 돌아가므로 시스템 콜 호환성 문제가 해소된다.
- **가상 장치**: WSL 2의 파일과 네트워크는 Hyper-V 가상 블록 장치와 가상 어댑터를 통해 처리된다.
- **선택 기준**: WSL 1은 낮은 오버헤드와 단순한 네트워크, WSL 2는 성능과 Docker 등의 호환성, 커스텀 커널이 장점이다.
- **GPU 컴퓨트**: `/dev/dxgkrnl`을 통한 준가상화 GPU로 DirectML, Direct3D, CUDA 등을 지원한다.
- **GUI와 오디오**: Wayland 컴포지터, RDP, PulseAudio 기반의 공식 지원이 예고됐다.

---

## 2. 섹션 문서

- [WSL 1 구조와 시스템 콜 변환](WSL%201%20구조와%20시스템%20콜%20변환.md)
- [WSL 2 구조와 하이퍼바이저](WSL%202%20구조와%20하이퍼바이저.md)
- [WSL 1과 WSL 2 비교](WSL%201과%20WSL%202%20비교.md)
- [GPU 컴퓨트 지원](GPU%20컴퓨트%20지원.md)
- [GUI와 오디오 지원 계획](GUI와%20오디오%20지원%20계획.md)

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
