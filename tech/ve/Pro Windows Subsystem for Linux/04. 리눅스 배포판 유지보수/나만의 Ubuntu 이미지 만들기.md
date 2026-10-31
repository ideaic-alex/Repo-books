# 나만의 Ubuntu 이미지 만들기

Canonical이 제공하는 표준 이미지 대신, 원하는 패키지가 미리 들어 있는 Ubuntu WSL 이미지를 직접 만드는 전체 과정이다. 이 문서는 전체 개요와 기본 이미지를 부트스트랩하는 단계까지 다룬다. 이미지를 커스터마이징하고 가져오는 단계는 다음 문서에서 다룬다.

---

## 1. 왜 직접 만드는가

- **표준 이미지**: Canonical은 Microsoft Store, 클라우드 이미지 사이트, `wsl.exe --install`로 표준 Ubuntu 이미지를 제공한다. 이 이미지는 클라우드 서버의 기본 패키지 구성에 가깝다. 내부 QA를 거쳤고 기업용 유료 지원도 있다.
- **직접 만드는 경우**: 특정 패키지 구성이 필요할 때다. 책의 예시는 GIS(지리정보시스템) 실습실을 운영하는 대학 관리자가, GIS 패키지가 미리 설치된 이미지를 만들어 학생이나 실습실 PC 전체에 배포하는 상황이다.

---

## 2. 전체 흐름

1. 이미지 부트스트랩 도구를 설치한다.
2. 이미지를 만들 임시 폴더를 만든다.
3. 그 폴더에 최소한의 패키지만으로 기본 Ubuntu 이미지를 부트스트랩한다.
4. `chroot`로 이미지 안에서 명령을 실행해 패키지를 설치하고 옵션을 설정한다.
5. 폴더를 tarball로 묶어 Windows 파일 시스템으로 옮긴다.
6. 그 tarball을 직접 만든 WSL 이미지로 가져온다.

---

## 3. 부트스트랩 도구와 작업 폴더

- **debootstrap**: Ubuntu 아카이브의 패키지로 기본 이미지를 만들어 주는 도구다.
- **작업 폴더**: 이미지의 전체 파일 시스템이 이 폴더 안에 만들어진다. 책은 `/tmp/wslchroot`를 쓴다.

```bash
sudo apt -y install debootstrap
mkdir /tmp/wslchroot
```

---

## 4. 기본 이미지 만들기 (debootstrap 실행)

- **`--arch`**: 시스템 아키텍처(예: `amd64`).
- **`--include`**: 기본 이미지에 함께 넣을 패키지. 책의 설명에는 sudo와 python3가 나오지만, 실제 예시 명령에는 `sudo`만 들어 있다.
- **나머지 인자**: 릴리스 코드명(`focal`은 Ubuntu 20.04 LTS), 대상 폴더, 아카이브 저장소 URL.
- **변형**: arm64로 빌드할 수 있다(다른 아키텍처 사이의 교차 빌드는 더 복잡하다). 다른 릴리스(예: Ubuntu 21.04의 hirsute)나 로컬 미러를 쓸 수도 있다.
- **도움말**: `man debootstrap`.

```bash
sudo debootstrap --arch "amd64" --include=sudo focal /tmp/wslchroot http://archive.ubuntu.com/ubuntu/
```

완료되면 해당 폴더에 최소한의 구성을 갖춘 Ubuntu가 설치된다.

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
