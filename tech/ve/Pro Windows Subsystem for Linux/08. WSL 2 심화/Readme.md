# 8장. WSL 2 심화 (Going Further with WSL 2)

GUI 앱과 자동 시작 서비스를 갖췄다면 WSL 2로 더 깊은 작업을 할 수 있다. 이 장은 systemd 실행, 커널 직접 빌드, 중첩 가상화(KVM)와 QEMU 게스트 OS, 그리고 WSL 2 고급 네트워킹을 다룬다. 어느 정도 리눅스 지식이 있으면 따라가기 수월하다.

---

## 1. 핵심 요점

- WSL은 systemd를 지원하지 않으며 systemd는 PID 1이어야 하므로 별도 프로세스 네임스페이스를 만들어 우회한다.
- Microsoft의 WSL 2 커널 소스를 받아 설정을 바꾸고 다시 빌드한 뒤 `.wslconfig`로 지정하면 커스텀 커널을 쓸 수 있다.
- KVM을 커널 모듈로 빌드하면 중첩 가상화가 가능하고, 이를 바탕으로 minikube나 QEMU 게스트 OS를 돌릴 수 있다.
- WSL 2는 자체 NAT 서브넷의 IP를 가지므로 외부(LAN) 접근에는 포트 프록시와 방화벽 규칙이 필요하다.
- WSL 2의 IP는 실행할 때마다 바뀌므로 포트 포워딩은 자동화해야 한다.

---

## 2. 섹션 문서

- [systemd 실행하기](systemd%20실행하기.md)
- [WSL 2 커널 직접 빌드](WSL%202%20커널%20직접%20빌드.md)
- [중첩 KVM과 게스트 운영체제](중첩%20KVM과%20게스트%20운영체제.md)
- [WSL 2 고급 네트워킹](WSL%202%20고급%20네트워킹.md)

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
