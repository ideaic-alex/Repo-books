# 5장. WSL 배포판 구성 (Configuring WSL Distros)

WSL 배포판을 설치한 뒤에는 일반 리눅스에는 없는 WSL 고유 설정들을 다루게 된다. 설정은 배포판마다 따로 적용하는 per-distro 설정과 기기의 모든 배포판에 영향을 주는 전역 설정으로 나뉘며, 이 장은 앞쪽인 `/etc/wsl.conf` 중심의 배포판별 설정을 다룬다. 마운트, 파일 권한, 대소문자 처리, 네트워크, 상호운용성, 기본 사용자와 부팅 명령까지 파일 하나에서 조절할 수 있다.

---

## 1. 핵심 요점

- `/etc/wsl.conf`는 배포판이 부팅될 때 읽히며, `[automount]`, `[network]`, `[interop]`, `[user]`, `[boot]` 섹션으로 구성된다.
- Windows 드라이브 자동 마운트의 위치, fstab 처리, 배포판 간 공유(`/mnt/wsl`), GPU용 라이브러리 경로를 조절할 수 있다.
- DrvFs의 `options`로 `metadata`, `uid`, `gid`, `umask`, `fmask`, `dmask` 등 권한 변환 방식을 정한다.
- 리눅스는 대소문자를 구분하고 Windows는 기본적으로 구분하지 않으며, 폴더 단위로 `fsutil.exe`나 `case` 옵션으로 조절한다.
- hosts, `resolv.conf`, 호스트 이름은 기본적으로 Windows에서 자동 생성되며 각각 끌 수 있다.
- interop과 `WSLENV`로 Windows와 리눅스의 프로그램 실행 및 환경 변수 공유를 제어한다.
- `[user]`로 기본 사용자를, `[boot]`로 시작 시 root 명령을 지정한다.

---

## 2. 섹션 문서

- [wsl.conf와 자동 마운트](wsl.conf%EC%99%80%20%EC%9E%90%EB%8F%99%20%EB%A7%88%EC%9A%B4%ED%8A%B8.md)
- [DrvFs 마운트 옵션과 파일 권한](DrvFs%20%EB%A7%88%EC%9A%B4%ED%8A%B8%20%EC%98%B5%EC%85%98%EA%B3%BC%20%ED%8C%8C%EC%9D%BC%20%EA%B6%8C%ED%95%9C.md)
- [대소문자 구분 처리](%EB%8C%80%EC%86%8C%EB%AC%B8%EC%9E%90%20%EA%B5%AC%EB%B6%84%20%EC%B2%98%EB%A6%AC.md)
- [네트워크와 호스트 이름 설정](%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%EC%99%80%20%ED%98%B8%EC%8A%A4%ED%8A%B8%20%EC%9D%B4%EB%A6%84%20%EC%84%A4%EC%A0%95.md)
- [상호운용성과 환경 변수 공유](%EC%83%81%ED%98%B8%EC%9A%B4%EC%9A%A9%EC%84%B1%EA%B3%BC%20%ED%99%98%EA%B2%BD%20%EB%B3%80%EC%88%98%20%EA%B3%B5%EC%9C%A0.md)
- [기본 사용자와 부팅 명령](%EA%B8%B0%EB%B3%B8%20%EC%82%AC%EC%9A%A9%EC%9E%90%EC%99%80%20%EB%B6%80%ED%8C%85%20%EB%AA%85%EB%A0%B9.md)

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
