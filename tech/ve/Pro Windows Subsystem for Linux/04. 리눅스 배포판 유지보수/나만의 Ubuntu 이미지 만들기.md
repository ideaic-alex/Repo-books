# 나만의 Ubuntu 이미지 만들기

Canonical이 제공하는 표준 이미지 대신, 원하는 패키지가 미리 들어간 Ubuntu WSL 이미지를 직접 만드는 전체 과정이다. 이 문서는 개요와 기본 이미지를 부트스트랩하는 단계까지, 다음 문서는 커스터마이징과 가져오기를 다룬다.

---

## 1. 왜 직접 만드는가

- **표준 이미지**: Canonical은 Microsoft Store, 클라우드 이미지 사이트, `wsl.exe --install`을 통해 표준 Ubuntu 이미지를 제공한다. 클라우드 서버 기본 패키지에 가깝고, 내부 QA를 거쳤으며 기업용 유료 지원도 있다.
- **직접 만드는 경우**: 특정 패키지 구성이 필요할 때. 책의 예시는 GIS(지리정보시스템) 실습실을 운영하는 대학 관리자가 GIS 패키지가 미리 설치된 이미지를 만들어 학생이나 실습실 PC 전체에 배포하는 상황이다.

---

## 2. 전체 흐름

1. 이미지 부트스트랩 도구를 설치한다.
2. 이미지를 만들 임시 폴더를 만든다.
3. 그 폴더에 최소 패키지만으로 기본 Ubuntu 이미지를 부트스트랩한다.
4. `chroot`로 이미지 안에서 명령을 실행해 패키지 설치와 옵션 설정을 한다.
5. 폴더를 tarball로 묶어 Windows 파일 시스템으로 옮긴다.
6. 그 tarball을 사용자 정의 WSL 이미지로 가져온다.

---

## 3. 부트스트랩 도구와 작업 폴더

- **debootstrap**: Ubuntu 아카이브의 패키지로 기본 이미지를 구성해 주는 도구다.
- **작업 폴더**: 이미지의 완전한 파일 시스템이 이 폴더 안에 만들어진다. 책은 `/tmp/wslchroot`를 사용한다.

```bash
sudo apt -y install debootstrap
mkdir /tmp/wslchroot
```

---

## 4. 기본 이미지 구성 (debootstrap 실행)

- **`--arch`**: 시스템 아키텍처(예: `amd64`).
- **`--include`**: 기본 이미지에 함께 넣을 패키지. 책의 설명은 sudo와 python3를 언급하지만 실제 예시 명령에는 `sudo`만 들어 있다.
- **나머지 인자**: 릴리스 코드명(`focal`은 Ubuntu 20.04 LTS), 대상 폴더, 아카이브 저장소 URL.
- **변형**: arm64로 빌드하거나(다른 아키텍처 간 교차 빌드는 더 복잡하다), 다른 릴리스(예: Ubuntu 21.04의 hirsute), 로컬 미러를 쓸 수 있다.
- **도움말**: `man debootstrap`.

```bash
sudo debootstrap --arch "amd64" --include=sudo focal /tmp/wslchroot http://archive.ubuntu.com/ubuntu/
```

완료되면 해당 폴더에 최소한의 완전한 Ubuntu 설치가 만들어진다.

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
