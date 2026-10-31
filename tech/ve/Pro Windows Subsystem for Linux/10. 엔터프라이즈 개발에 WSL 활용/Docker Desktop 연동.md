# Docker Desktop 연동

Docker Desktop을 WSL 2 기반 엔진으로 설정하면 Windows와 각 WSL 배포판이 같은 Docker 엔진을 공유한다. WSL 안에서도 PowerShell이나 cmd에서와 똑같이 Docker 명령을 쓸 수 있다.

---

## 1. WSL 지원 설정

- Windows에 Docker Desktop을 설치한 뒤, 시스템 트레이의 Docker 아이콘을 열고 설정(톱니바퀴)으로 들어간다.
- **WSL 2 기반 엔진(WSL 2-based engine)**: 이 옵션을 켜면 기존 Docker Desktop 가상 머신 대신 WSL 2 인프라를 이용한 경량 환경이 쓰인다.
- **WSL 통합(WSL Integration)**: Resources 아래의 이 메뉴에서 배포판별로 통합을 켜고 끈다. 켠 배포판과 Windows가 같은 Docker 엔진을 쓴다.

---

## 2. WSL에서 컨테이너 빌드

- 통합을 켠 배포판 안에서 Docker 명령을 그대로 쓸 수 있다.
- 책은 Docker의 `getting-started` 예제 앱을 사용한다. `git clone`으로 받고 해당 디렉터리에서 이미지를 빌드하면 이미지 ID가 나오고, 이를 이용해 컨테이너를 실행한다.
- 실행한 컨테이너가 제공하는 웹 페이지는 Windows의 브라우저에서 `127.0.0.1`로 열어 확인한다.

```bash
git clone https://github.com/docker/getting-started
cd getting-started
docker build .
```

---

## 3. 참고

- GPU 연산이 필요한 경우에는 Docker Desktop 대신 WSL 안에 Docker를 직접 설치하는 방식이 쓰인다. 이는 GPU 연산 문서에서 다룬다. 책에서는 Docker Desktop의 GPU 지원이 계획 중이라고 언급한다.

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
