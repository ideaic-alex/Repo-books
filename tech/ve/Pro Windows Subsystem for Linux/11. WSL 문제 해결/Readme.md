# 11장. WSL 문제 해결 (Troubleshooting WSL)

WSL 설치는 대체로 순조롭지만, 몇 가지 상황에서는 문제가 생긴다. 이 장은 먼저 설치 단계에서 확인할 항목과 가상화 환경의 제약을 다룬다. 이어서 systemd, dbus, 커널 모듈처럼 리눅스 앱이 기대하는 구성요소가 WSL에서 어떻게 문제가 되는지 살펴본다. 마지막으로 strace로 앱이 실패한 원인을 추적하는 방법을 설명한다.

---

## 1. 핵심 요점

- 설치가 안 되면 먼저 Windows 선택 기능 두 개(Virtual Machine Platform, Windows Subsystem for Linux)가 켜져 있는지 확인한다.
- 서드파티 백신이 `lxcore`, `lxsys`를 막으면 WSL이 동작하지 않으므로, 백신의 허용 목록을 점검한다.
- 배포판 런처는 Microsoft Store에서 항상 최신 상태로 유지한다.
- 가상 머신 안의 Windows에서는 중첩 가상화가 노출되지 않으면 WSL 2를 쓸 수 없고 WSL 1만 쓸 수 있다.
- WSL에서는 systemd를 기본으로 쓸 수 없다. 그래서 systemctl, snap, dbus에서 문제가 생긴다.
- 앱에 커널 모듈이 필요하면, WSL 2에서 Microsoft가 제공하는 커널에 그 모듈이 들어 있는지 `dmesg` 등으로 확인한다.
- WSL 1에서 앱이 실패하면 `strace`로 구현되지 않은 시스템 콜을 찾아 본다.

---

## 2. 섹션 문서

- [설치와 가상화 점검](설치와%20가상화%20점검.md)
- [리눅스 구성요소 의존성](리눅스%20구성요소%20의존성.md)
- [strace로 애플리케이션 추적](strace로%20애플리케이션%20추적.md)

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
