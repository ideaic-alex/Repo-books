# WSL 2 구조와 하이퍼바이저

WSL 2는 변환 계층을 확장하는 대신, 진짜 리눅스 커널을 Hyper-V 기반의 경량 가상화 환경에 올리는 방식을 택했다. 이 문서는 하이퍼바이저, 가상 머신 플랫폼, 가상 장치, WSL 2 커널을 정리한다.

---

## 1. Hyper-V와 하이퍼바이저 종류

- **Hyper-V**: Windows NT 커널에 내장된 네이티브 가상화 기술. 리눅스의 KVM, macOS의 Hypervisor.Framework에 해당한다.
- **타입 1 하이퍼바이저(Type 1)**: NT 커널 수준에서 동작하는 Hyper-V의 유형.
- **타입 2 하이퍼바이저(Type 2)**: VirtualBox, VMware 같은 서드파티 제품. 커널 드라이버를 올리긴 하지만 대부분 사용자 공간에서 구현된다.
- 두 종류는 충돌하므로, 당시에는 같은 Windows에서 VirtualBox와 WSL 2를 함께 쓸 수 없다.

---

## 2. 가상 머신 플랫폼과 Host Compute Service

- **가상 머신 플랫폼(Virtual Machine Platform)**: Windows 10에서 켜면 Hyper-V 기반 API가 노출된다.
- **Host Compute Service**: WSL 2가 이 API를 호출해 경량 리눅스 환경을 정의한다. 가상 파일 시스템과 가상 네트워크 어댑터를 붙이는 것도 이 호출로 한다.

---

## 3. 파일과 네트워크 처리 방식 차이

- WSL 1에서는 파일 열기나 포트 열기를 NT 커널이 직접 처리한다.
- WSL 2에서는 이런 요청을 리눅스 커널이 받고, 커널이 Hyper-V의 가상 장치와 상호작용한다.
- **가상 파일 시스템**: 디스크 이미지를 가상 블록 장치로 마운트하고 그 위에 파일 시스템을 둔다. IDE, SATA, NVMe 같은 물리 장치를 흉내 내는 것보다 성능이 좋고 부담이 적다.
- **가상 네트워크 어댑터**: Hyper-V가 에뮬레이션하며, 포트 요청은 리눅스 커널을 거쳐 이 어댑터로 간다.
- 이런 가상 장치는 `lshw`로 확인할 수 있다. 예를 들어 `eth0` 이더넷 인터페이스는 `hv_netvsc` 드라이버를 쓰고 10Gbit/s로 보인다.
- 해당 Hyper-V 장치 드라이버는 2009년부터 업스트림 리눅스 커널에 들어 있다.

---

## 4. WSL 2 커널

- 표준 리눅스 커널을 약간 수정해 WSL 2 환경에 맞게 최적화한 것이다.
- 소스는 GPL 2.0으로 공개돼 있다(`github.com/microsoft/WSL2-Linux-Kernel`).
- 커널 업데이트는 Windows Update로 배포된다.
- 이전 Windows 10 버전에서 올라온 일부 사용자는 설치 프로그램으로 직접 설치해야 한다(`aka.ms/wsl2kernel`). ARM64용 커널도 있다.
- 직접 커널을 빌드하는 방법은 책의 8장에서 다룬다.

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
