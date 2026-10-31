# rootfs 가져오기

배포판은 루트 파일 시스템(rootfs) 아카이브에서 직접 설치할 수도 있다. 이 문서는 rootfs 구하는 법, `wsl.exe --import` 사용법, 가져온 뒤 사용자 설정까지 정리한다.

---

## 1. rootfs란

- **rootfs**: 동작하는 리눅스 설치본의 스냅샷을 tar로 묶고 gzip으로 압축한 파일(`.tar.gz`).
- 일부 배포판이 직접 제공하며, GitHub에는 서드파티 빌드도 있다.
- Ubuntu는 스토어에 올라간 LTS 버전(18.04, 20.04 등)의 야간 빌드를 제공한다. 6개월마다 나오는 중간 버전의 야간 빌드도 있어 최신 패키지를 쓸 수 있다.
- 이들은 클라우드 이미지 서버에서 릴리스 코드명별로 정리돼 있고, 코드명과 버전 번호의 대응은 Ubuntu 릴리스 목록에서 확인한다.

---

## 2. 올바른 파일 고르기

- 예시는 20.10 중간 릴리스인 groovy를 쓴다. 서버의 해당 코드명 아래 `current` 페이지에서 플랫폼별 빌드를 본다.
- WSL용 빌드는 파일명이 `-<플랫폼>-wsl.rootfs.tar.gz`로 끝난다.
- 인텔·AMD는 `amd64`, Surface Pro X 같은 ARM 기기는 `arm64`를 받는다.
- 파일명에 `server`가 들어가는 것은 Ubuntu 서버와 같은 기반으로 만들었기 때문이다.

---

## 3. wsl.exe --import

- 형식: 배포판 이름, 압축을 풀 위치, rootfs 파일 경로, 선택적으로 `--version`.
- 같은 rootfs를 다른 이름으로 여러 번 설치해 용도별 배포판(예: GPU 작업용)을 만들 수 있다. 복제는 3장에서 다룬다.

```powershell
wsl.exe --import UbuntuGroovy-2 C:\WSL\Ubuntu-Groovy-2 $HOME\Downloads\groovy-server-cloudimg-amd64-wsl.rootfs.tar.gz --version 2
wsl.exe -d UbuntuGroovy-2
```

- 가져온 배포판은 시작 메뉴 아이콘이 생기지 않으므로 PowerShell에서 `wsl.exe -d <이름>`으로 시작한다.
- 새 **Windows Terminal**은 가져온 배포판을 자동으로 목록에 추가한다. 스토어와 GitHub에서 받을 수 있고, 기존 콘솔보다 크게 개선돼 WSL과 PowerShell에 강력히 권장된다.

---

## 4. 기본 사용자 만들기

- import로 설치하면 비특권 기본 사용자가 없고 루트로 시작된다.
- Ubuntu에서는 사용자를 만들고 sudo 그룹에 넣은 뒤 전환한다.

```bash
adduser hayden
usermod -aG sudo hayden
su hayden
```

- 특정 사용자로 시작하려면 PowerShell에서 `-u` 옵션을 쓴다.

```powershell
wsl.exe -d Ubuntu-Groovy -u hayden
```

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
