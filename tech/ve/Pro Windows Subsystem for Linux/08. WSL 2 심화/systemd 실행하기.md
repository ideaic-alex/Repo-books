# systemd 실행하기

systemd는 커널과 애플리케이션 사이의 잡다한 일을 맡는 도구 모음이며, 가장 유명한 부분은 백그라운드 서비스를 시작하고 멈추는 init 시스템이다. WSL은 이를 기본 지원하지 않으므로 systemd에 의존하는 앱이 있다면 직접 띄워야 한다.

---

## 1. systemd 배경

- **init 시스템**: Upstart, SysVinit 같은 구형 init을 대체한다. 부팅 시 어떤 서비스를 어떤 순서로 시작할지 정한다.
- **모듈식 구성**: 배포판마다 쓰는 구성 요소가 다르다. 저자가 좋아하는 `systemd-nspawn`은 chroot의 대안이며 크로스 플랫폼 컨테이너에 유용하다고 한다.
- **비 systemd 환경**: Devuan(SysVinit 사용)이나 OpenRC처럼 systemd 없이 가는 배포판도 있고, 많은 앱은 systemd 없이도 동작한다.
- **채택 흐름**: Ubuntu에서는 2015년에 표준이 되었고 이후 널리 퍼져 일부 고급 앱의 의존성이 되었다. 저자는 당분간 주류 리눅스가 systemd 기반일 것으로 본다.

---

## 2. WSL에서의 제약

- WSL은 자체 단순 init을 쓴다. 환경 변수 상호운용, `/mnt/c`로의 Windows 드라이브 마운트, 파일 공유 등 기본 환경 정리를 맡는다.
- **PID 1 문제**: systemd는 WSL의 init이 이미 차지한 PID 1로 실행될 수 없다. 많은 앱은 systemd가 PID 1이라고 가정한다.
- 해법은 systemd를 수동으로 시작하되 별도의 새 환경 안에서 PID 1로 동작하게 하는 것이다.

---

## 3. 기존 프로젝트

이 방식을 대신 처리해 주는 프로젝트로 다음이 소개된다.

- **one-script-wsl2-systemd**
- **Genie**
- **Subsystemctl**

---

## 4. 직접 하는 간단한 방법

프로세스 네임스페이스를 새로 만들어 그 안에서 systemd를 PID 1로 돌리고, 현재 터미널 세션을 그 안으로 옮기는 절차다.

1. `daemonize` 유틸리티를 설치한다.
2. `daemonize`와 `unshare`로 새 PID 네임스페이스를 만들고 그 안에서 systemd를 실행한다.
3. 네임스페이스 바깥에서 systemd 프로세스의 PID를 구한다.
4. `nsenter`로 사용자 세션을 그 네임스페이스에 넣는다. 이후 systemd가 PID 1로 보인다.

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
