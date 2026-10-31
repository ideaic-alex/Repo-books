# systemd 실행하기

systemd는 커널과 애플리케이션 사이에서 여러 관리 작업을 맡는 도구 모음이다. 가장 잘 알려진 부분은 백그라운드 서비스를 시작하고 멈추는 init 시스템이다. WSL은 systemd를 기본으로 지원하지 않으므로, systemd에 의존하는 앱을 쓰려면 직접 실행해야 한다.

---

## 1. systemd 배경

- **init 시스템**: Upstart, SysVinit 같은 예전 init을 대체한다. 부팅할 때 어떤 서비스를 어떤 순서로 시작할지 정한다.
- **모듈 구조**: 배포판마다 사용하는 구성 요소가 다르다. 저자가 좋아하는 `systemd-nspawn`은 chroot의 대안으로, 여러 플랫폼에서 컨테이너를 쓸 때 유용하다고 한다.
- **systemd 없는 환경**: Devuan(SysVinit 사용)이나 OpenRC처럼 systemd를 쓰지 않는 배포판도 있고, 많은 앱은 systemd 없이도 동작한다.
- **확산 과정**: Ubuntu는 2015년에 systemd를 표준으로 채택했다. 이후 널리 퍼지면서 일부 고급 앱은 systemd가 있어야만 동작하게 되었다. 저자는 당분간 주류 리눅스가 systemd 기반일 것으로 본다.

---

## 2. WSL에서의 제약

- WSL은 자체 단순 init을 쓴다. 이 init이 환경 변수 상호운용, `/mnt/c`로 Windows 드라이브 마운트, 파일 공유 같은 기본 환경 설정을 맡는다.
- **PID 1 문제**: WSL의 init이 이미 PID 1을 차지하고 있어서 systemd를 PID 1로 실행할 수 없다. 그런데 많은 앱은 systemd가 PID 1이라고 가정하고 동작한다.
- 해법은 systemd를 직접 시작하되, 별도의 새 환경 안에서 PID 1로 동작하게 하는 것이다.

---

## 3. 기존 프로젝트

이 작업을 대신 처리해 주는 프로젝트로 다음 세 가지가 소개된다.

- **one-script-wsl2-systemd**
- **Genie**
- **Subsystemctl**

---

## 4. 직접 하는 간단한 방법

프로세스 네임스페이스를 새로 만들고, 그 안에서 systemd를 PID 1로 실행한 뒤, 현재 터미널 세션을 그 안으로 옮기는 방법이다.

1. `daemonize` 유틸리티를 설치한다.
2. `daemonize`와 `unshare`로 새 PID 네임스페이스를 만들고, 그 안에서 systemd를 실행한다.
3. 네임스페이스 바깥에서 systemd 프로세스의 PID를 구한다.
4. `nsenter`로 사용자 세션을 그 네임스페이스 안으로 들여보낸다. 이후에는 systemd가 PID 1로 보인다.

```bash
sudo apt -y install daemonize
sudo daemonize unshare --fork --pid --mount-proc /lib/systemd/systemd &
SYSTEMD_PID="$(ps -eo pid=,args= | awk '$2=="/lib/systemd/systemd" {print $1}')"
sudo /usr/bin/nsenter --all --target "$SYSTEMD_PID" -- su - "$USER"
```

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
