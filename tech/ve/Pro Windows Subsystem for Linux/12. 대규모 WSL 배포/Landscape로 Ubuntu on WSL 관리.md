# Landscape로 Ubuntu on WSL 관리

Canonical의 Landscape 서버는 기업 네트워크처럼 규모가 큰 Ubuntu on WSL 환경을 관리하는 공식적인 방법이다. 이 문서는 클라이언트를 서버에 등록하는 절차, 원격 스크립트 실행, 패키지 관리를 정리한다.

---

## 1. Landscape 개요와 전제

- **기능(Capability)**: Ubuntu 시스템 전체 또는 일부 집합을 모니터링하고, 스크립트 실행이나 패키지 설치로 능동적으로 유지보수한다.
- **전제(Prerequisite)**: Landscape 서버가 이미 설치되어 있어야 한다. 또 landscape-client는 systemd의 관리를 받는다고 가정하므로, 앞서 다룬 systemd 활성 환경 위에서 진행한다.

---

## 2. Landscape에 Ubuntu WSL 등록

1. 서버 관리 화면의 안내 링크에서 등록 URL과 ping URL을 확인한다. ping URL은 항상 HTTP이고 등록 URL은 대개 HTTPS다.
2. 저장소를 갱신하고 클라이언트를 설치한다.
3. 서버를 퀵스타트로 설치해 인증서가 공인 또는 사내 CA 서명이 아니라면, 서버의 `/etc/ssl/certs/landscape_server_ca.crt`를 각 클라이언트의 `/etc/landscape/server.pem`으로 복사하고 등록 시 `--ssl-public-key /etc/landscape/server.pem` 옵션을 덧붙인다.
4. `landscape-config`로 컴퓨터를 등록한다. 제목, 계정 이름, URL은 환경에 맞게 바꾼다.
5. 스크립트 실행을 허용할 사용자를 묻는 질문에는 사용자 이름이나 모든 사용자를 뜻하는 키워드 `ALL`을 입력한다.
6. 등록에 성공하면 서버의 보류 중 컴퓨터(Pending Computers) 페이지에서 해당 컴퓨터를 승인해야 한다.

```bash
sudo apt-get update && sudo apt-get install landscape-client
sudo landscape-config --computer-title "제목" --account-name "standalone" \
  --url https://landscape-url/message-system --ping-url http://landscape-url/ping
```

- **등록 실패 대처**: 호스트 이름이 DNS로 해석되지 않으면 IP 주소를 쓰거나 WSL 인스턴스의 `/etc/hosts`에 호스트 이름을 추가한다.

---

## 3. 스크립트 실행

- **절차(Steps)**: 대상 컴퓨터를 선택하고 상단의 scripts 탭에서 코드 입력란에 스크립트를 넣는다. 예시는 디스크 여유 공간(`df -h`)과 최상위 폴더별 사용량(`du -sh`)을 보여 주는 스크립트다.
- **실행 사용자(Run as user)**: root 또는 원하는 사용자를 입력한다. 이 사용자는 클라이언트 설정에서 허용된 사용자여야 한다.
- **결과 확인**: Run을 누르고 끝나면 성공·실패가 표시되며, 명령 상태를 눌러 스크립트 출력을 볼 수 있다.

---

## 4. 패키지 관리

- **설치(Install)**: Packages 탭의 검색창에 패키지 이름(예: ffmpeg)을 입력하고, 결과에서 설치할 항목을 선택한 뒤 Apply changes를 눌러 작업 완료를 기다린다.
- **업그레이드(Upgrade)**: 전체 업그레이드나 보안 전용 업그레이드를 수행할 수 있다. 가능한 업그레이드는 Packages 탭과 Organization 탭, Alerts 드롭다운에 표시된다.
- **적용 방식**: 알림을 따라가거나 컴퓨터를 선택해 Packages 탭으로 가면 같은 화면에서 제거 또는 업그레이드할 패키지를 고르고 Apply changes로 반영한다.

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
