# CLI 시작과 잡 만들기

젠킨스는 마우스로 누르는 화면(GUI) 말고도 명령어로 조작하는 길을 열어 둔다. 이 문서는 젠킨스 CLI(Command-line Interface, 명령줄 인터페이스)가 무엇인지, 어떻게 내려받아 쓰는지, 첫 실습으로 잡을 하나 만들어 보는 과정을 정리한다. 처음 실행하면 인증 오류가 나는데, 그 이유까지 함께 본다.

식당에 비유하면 GUI는 홀에서 메뉴판을 보고 주문하는 방식이고, CLI는 전화나 주문 앱으로 같은 주문을 넣는 방식이다. 주방(젠킨스 서버)은 같고, 주문 창구만 다르다. 창구가 글자로 되어 있으니 스크립트로 자동화하기 쉽다.

---

## 1. 왜 CLI를 쓰는가

화면에서 하던 일을 스크립트나 셸 프로그램이 대신 해야 할 때가 있다. 이때 젠킨스가 주는 프로그래밍용 입구가 CLI와 REST API다. 이 장은 CLI를 다루고, REST API는 다음 장에서 이어진다.

| 방식 | 쓰는 곳 | 특징 |
| --- | --- | --- |
| GUI(그래픽 사용자 인터페이스) | 브라우저 | 지금까지 이 책에서 계속 써 온 화면 조작 |
| CLI(명령줄 인터페이스) | 윈도우 명령 프롬프트, 리눅스 콘솔 셸 | 명령어를 배치 파일이나 셸 스크립트로 묶어 자동화 |

표를 보면 두 방식은 같은 서버를 다른 입구로 쓸 뿐이다. 반복 작업, 서버 이전, 일괄 처리처럼 사람이 클릭하기 번거로운 일이 CLI의 주 무대다.

CLI 앞에서 가장 중요한 문제는 인증이다. 서버에 "누가 요청하는지"를 알려 줘야 하고, 이 장의 상당 부분이 그 방법(API 토큰, SSH)에 쓰인다.

## 2. 명령어 목록 확인하기

젠킨스가 제공하는 CLI 명령은 꽤 많다. 목록과 각 명령의 용도는 젠킨스 화면의 CLI 안내 페이지에서 볼 수 있다.

1. 대시보드 왼쪽의 Manage Jenkins(젠킨스 관리) 링크를 누른다.
2. Manage Jenkins 페이지를 아래로 내려 Tools and Actions 섹션에서 Jenkins CLI 링크를 찾는다.
3. Jenkins CLI 링크를 누르면 명령 목록과 명령별 용도가 나온다.

이 장에서 쓰는 명령은 create-job, build, list-jobs, get-job이다. 이 밖에 잡 삭제, 잡 비활성화, 빌드 콘솔 출력 조회 같은 작업도 CLI로 할 수 있다.

## 3. jenkins-cli.jar 내려받기

CLI를 쓰려면 먼저 jenkins-cli.jar가 필요하다. 이 JAR 파일이 CLI 클라이언트, 곧 명령을 서버로 전달해 주는 프로그램이다.

1. Jenkins CLI 페이지에서 jenkins-cli.jar 링크를 누른다.
2. 내려받은 파일을 적당한 폴더에 둔다.

원서는 이 파일을 D:\JenkinsBookExamples 폴더에 두었다. 그래서 명령 속 경로가 D:\JenkinsBookExamples\jenkins-cli.jar로 적힌다. 독자는 자기 컴퓨터의 경로로 바꿔 쓰면 된다.

원서 실습 환경은 다음과 같다.

| 항목 | 원서 값 | 독자가 할 일 |
| --- | --- | --- |
| 젠킨스 URL | http://192.168.43.10:8080 (IPv4 주소와 기본 포트 8080) | localhost 또는 자기 IP와 포트로 교체 |
| JAR 위치 | D:\JenkinsBookExamples\jenkins-cli.jar | 자기 경로로 교체 |
| 플레이스홀더 표기 | ${} | 실제 값으로 교체 |

원서는 명령 설명에서 ${} 안에 들어간 이름을 실제 값으로 바꿔 쓰라고 약속하고 시작한다. 이 노트도 같은 표기를 쓴다.

## 4. CLI로 잡 만들기

잡을 만들려면 두 가지가 필요하다. 하나는 잡 이름, 다른 하나는 그 잡의 설정을 담은 XML 파일이다. 젠킨스 잡의 설정은 내부적으로 XML이라서, 이 XML이 새 잡의 설계도가 된다.

참고로 뷰(view)는 대시보드에서 잡을 탭으로 묶어 정리하는 방법이다. 새로 만든 잡은 기본적으로 All 뷰에 나타난다. 대시보드에 처음 들어갔을 때 보이는 탭이 All이다.

명령의 기본 형태는 다음과 같다.

```bat
java -jar {jenkins-cli.jar 경로} -s ${JENKINS_URL} -webSocket create-job ${JobName} < ${Configuration.xml}
```

| 부분 | 의미 |
| --- | --- |
| java -jar | JAR 파일 실행 |
| -s | 접속할 젠킨스 서버 URL |
| -webSocket | 웹소켓 연결 방식으로 접속 |
| create-job | 실행할 CLI 명령 |
| ${JobName} | 새로 만들 잡 이름 |
| < ${Configuration.xml} | 설정 XML 파일을 입력으로 넘기는 리다이렉션 |

마지막 `<` 기호가 핵심이다. 파일 내용을 명령의 입력으로 흘려 넣는다는 뜻이고, 젠킨스는 그 내용을 읽어 잡을 만든다.

### 템플릿 XML 준비

원서는 이미 있는 Demo 잡의 설정을 템플릿으로 삼아 CLIJob1이라는 잡을 새로 만든다. Demo 잡은 젠킨스 설치 직후 기본으로 있는 잡이고, 설정 파일은 `{JENKINS_HOME}\jobs\Demo\Config.xml` 위치에 있다. 이 파일을 D:\JenkinsBookExamples 폴더로 복사해 Demo.xml로 이름을 바꿨다.

실제 명령은 다음과 같다.

```bat
java -jar D:\JenkinsBookExamples\jenkins-cli.jar -s http://192.168.43.10:8080/ -webSocket create-job CLIJob1 < D:\JenkinsBookExamples\Demo.xml
```

원서의 PDF 추출본에는 하이픈이 긴 줄표(–)로 바뀌어 있었다. 실제로 명령을 칠 때는 일반 하이픈(-)을 써야 한다.

## 5. 첫 실행은 오류가 난다

위 명령을 명령 프롬프트에서 그대로 실행하면 다음 오류가 나온다.

```text
ERROR: anonymous is missing the Overall/Read permission
```

원인은 단순하다. 아직 신원을 밝히지 않았기 때문에 젠킨스는 이 요청을 익명(anonymous) 사용자의 것으로 본다. 서버의 보안 설정상 익명 사용자는 잡을 만들 권한이 없다. 건물 출입증 없이 로비에서 사무실 문을 두드린 것과 같다.

해결은 권한이 있는 사용자로 인증 정보를 함께 보내는 것이고, 방법은 다음 문서에서 다룬다.

## 6. 흔한 문제 정리

| 상황 | 나타나는 증상 | 알아 둘 점 |
| --- | --- | --- |
| 인증 정보를 안 보냄 | anonymous is missing the Overall/Read permission | 익명 사용자는 권한이 없다. -auth로 인증한다 |
| 템플릿 XML에 문법 오류 | 다른 프로세스가 파일을 사용 중이라 접근할 수 없다는 취지의 오류 | 원서는 이 메시지가 실제 원인과 무관해 오해를 부른다고 경고한다 |
| 같은 이름의 잡이 이미 있음 | Job Already Exists 오류 | 다른 이름을 쓰거나 기존 잡을 먼저 처리한다 |

XML 문법 오류일 때 나오는 메시지가 엉뚱하다는 점이 특히 중요하다. 이 메시지가 보이면 파일 잠금을 의심하기 전에 XML 파일이 올바른지부터 확인하는 편이 빠르다. 원서가 적은 영어 오류 문구는 "cannot access the file because it is being used by another process"이다.

다음 문서에서는 인증을 붙여 같은 명령을 성공시킨다.

<br>
<br>
<br>

[CICD Pipeline Using Jenkins Unleashed](../)
