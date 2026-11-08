# 젠킨스 설정하기

이 장은 설치를 마친 Jenkins를 실제로 쓸 수 있게 만드는 첫 단계를 다룬다. Jenkins 서버를 켜는 방법, 브라우저로 로그인하는 방법, 시스템 설정 화면의 주요 항목, 비밀번호를 잃어버렸을 때의 복구 절차를 차례로 정리한다. 책은 Windows 환경과 Jenkins 2.289 버전을 기준으로 설명한다.

원서의 스크린샷은 쓰지 않고 글과 표로 풀었다. 책이 인쇄 과정에서 깨진 명령은 문맥으로 복원했고, 불확실한 부분은 본문에 밝혔다.

---

## 1. 핵심 요점

- Jenkins 서버는 .WAR 파일 실행, Windows 서비스, Docker 컨테이너, Linux 서비스 중 하나로 시작한다.
- .WAR 실행은 `--httpListenAddress`와 `--httpPort` 옵션으로 주소와 포트를 정한다.
- Windows 서비스의 주소와 포트는 `$JENKINS_HOME\jenkins.xml`의 `<arguments>`에 적고 서비스를 재시작한다.
- Linux에서 8080 포트가 충돌하면 `/etc/default/Jenkins`의 `HTTP_PORT` 값을 바꾼다.
- Manage Jenkins의 Configure System에서 Home directory, Jenkins URL, 관리자 이메일 주소를 확인한다.
- JENKINS_HOME의 위치는 설정 파일, 환경 변수, Java 시스템 속성 등으로 바꿀 수 있다.
- 비밀번호를 잃으면 `config.xml`의 `useSecurity`를 `false`로 바꿔 들어간 뒤 계정을 삭제하고 새로 만든다.
- 새 관리자는 Jenkins' Own User Database와 Logged-in Users Can Do Anything 설정으로 만든다.

---

## 2. 문서 목록

- [젠킨스 서버 시작하기](젠킨스 서버 시작하기.md): .WAR, Windows 서비스, Docker, Linux 서비스로 서버를 켜고 포트를 바꾸는 방법
- [로그인과 시스템 설정 페이지](로그인과 시스템 설정 페이지.md): 로그인 절차와 Home directory, Jenkins URL, 관리자 이메일 설정
- [비밀번호 복구와 사용자 추가](비밀번호 복구와 사용자 추가.md): 12단계 복구 절차와 새 관리자 계정 만들기
- [요약과 핵심 개념](요약과 핵심 개념.md): 장 요약, 핵심 개념, 명령 모음

<br>
<br>
<br>

[CICD Pipeline Using Jenkins Unleashed](../)
