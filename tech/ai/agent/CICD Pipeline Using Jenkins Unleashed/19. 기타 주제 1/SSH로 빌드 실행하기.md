# SSH로 빌드 실행하기

SSH 인증 준비를 마쳤으니 이제 CLI의 build 명령으로 잡을 실행해 본다. 이 문서는 build 명령의 옵션을 먼저 정리하고, SSH 인증으로 접속하는 두 가지 길을 차례로 보여 준다. 하나는 OpenSSH 같은 SSH 클라이언트를 쓰는 길이고, 다른 하나는 jenkins-cli.jar에 SSH 연결 방식을 쓰게 하는 길이다.

두 길은 같은 목적지로 가는 두 개의 문과 같다. 문은 다르지만 안쪽의 젠킨스 CLI 명령은 똑같다.

---

## 1. build 명령의 옵션

build 명령은 아래 옵션을 선택적으로 받는다.

| 옵션 | 동작 |
| --- | --- |
| -c | 잡에 설정된 SCM(소스 관리, 예를 들어 Git)에 변경이 있는지 검사하고, 변경이 있을 때만 빌드를 시작한다 |
| -f | 빌드 결과에 따른 종료 코드를 돌려준다. 빌드가 성공하면 종료 코드 0이다 |
| -p | 빌드 매개변수를 Key=Value 형식으로 넘긴다 |
| -s | 빌드가 끝나거나 중단될 때까지 기다린다. 이 옵션이 없으면 빌드만 시작하고 완료를 기다리지 않는다 |
| -v | 빌드의 콘솔 출력을 보여 준다 |
| -w | 명령이 시작될 때까지 기다린다 (원서 표현) |

-c는 변경이 없으면 아예 실행하지 않는다는 점이 특징이다. -s와 -v를 함께 쓰면 "끝날 때까지 기다리면서 로그를 보는" 효과가 난다. -w는 원서가 "명령의 시작까지 기다린다"고만 설명해, 정확히 어떤 시점인지는 원서만으로는 확실하지 않다.

SSH로 인증해 CLI를 쓰는 길은 두 가지다.

| 방법 | 쓰는 도구 |
| --- | --- |
| SSH 클라이언트 | OpenSSH 또는 Putty |
| jenkins-cli.jar | 젠킨스 CLI 클라이언트 JAR |

## 2. OpenSSH 클라이언트로 실행

OpenSSH로 build 명령을 보내는 기본 형태는 다음과 같다.

```bat
ssh ${JenkinsUserName}@${JenkinsServerIPAddress} -p ${JenkinsSSHPort} -i ${PrivateKeyFilePath} build ${JOB_NAME}
```

원서의 실제 값은 다음과 같다.

```bat
ssh Pranodayd@192.168.43.10 -p 9090 -i D:\SSHKey\JenkinsCLI build ReleaseCalculatorAPI
```

| 구성 요소 | 값 | 설명 |
| --- | --- | --- |
| 사용자 | Pranodayd | 인증할 젠킨스 사용자 |
| 서버 주소 | 192.168.43.10 | 젠킨스가 도는 머신의 IP |
| -p | 9090 | 앞서 SSH Server 섹션에서 정한 고정 포트 |
| -i | D:\SSHKey\JenkinsCLI | 개인 키 파일 |
| build | ReleaseCalculatorAPI | 실행할 CLI 명령과 잡 이름 |

여기서 -p는 SSH 접속 포트다. 젠킨스 웹 포트(8080)가 아니라 SSH 서버에 정한 포트(9090)임에 주의한다.

### 실행과 확인

1. 명령 프롬프트에서 위 명령을 실행한다.
2. 젠킨스 대시보드로 가 ReleaseCalculatorAPI 잡의 빌드가 시작된 것을 확인한다.

### 옵션을 붙여 다시 실행

```bat
ssh Pranodayd@192.168.43.10 -p 9090 -i D:\SSHKey\JenkinsCLI build ReleaseCalculatorAPI -s -v -c
```

이번에는 대시보드에서 빌드가 시작되지 않는다. -c 옵션이 SCM 변경을 먼저 확인하는데, Git 저장소에 바뀐 것이 없기 때문이다.

그다음 원서는 CalculatorAPI 프로젝트의 pom.xml에서 version을 10.0으로 바꾸고 GitLab 저장소에 푸시했다. 같은 명령을 다시 실행하니 이번에는 빌드가 시작되었고, -v를 줬기 때문에 빌드의 콘솔 로그도 함께 출력되었다.

| 실행 시점 | 저장소 상태 | 결과 |
| --- | --- | --- |
| 첫 번째 (옵션 없음) | 상관없음 | 빌드 시작 |
| 두 번째 (-s -v -c) | 변경 없음 | 빌드가 시작되지 않음 |
| 세 번째 (-s -v -c) | pom.xml의 version을 10.0으로 바꿔 푸시 | 빌드 시작, 콘솔 로그 출력 |

변경이 있을 때만 빌드가 돌게 하려는 스크립트에서 -c가 쓸모 있다. 같은 명령을 여러 번 보내도 바뀐 것이 없으면 빌드가 쌓이지 않는다.

## 3. jenkins-cli.jar로 SSH 연결

앞에서는 jenkins-cli.jar를 HTTP 연결 방식으로 썼다. 이번에는 같은 JAR를 SSH 연결 방식으로 쓰는 방법이다.

### 비기본 IP로 젠킨스를 띄울 때

젠킨스를 기본이 아닌 IP 주소로 시작한다면, 시작할 때 `org.jenkinsci.main.modules.sshd.SSHD.hostName`이라는 인자에 젠킨스 머신의 IP를 값으로 넣어야 한다.

jenkins.war로 직접 띄우는 경우의 형태는 다음과 같다.

```bat
java -Dorg.jenkinsci.main.modules.sshd.SSHD.hostName=<IPAddress> -jar <PATH of Jenkins jar> --httpListenAddress=<IPAddress>
```

원서의 실제 값은 다음과 같다. 원문에는 jenkins.war와 --httpListenAddress 사이에 공백이 빠진 듯 보이나, PDF 추출 때문인지 원문 오타인지는 확실하지 않다. 아래는 공백을 넣어 복원했다.

```bat
java -Dorg.jenkinsci.main.modules.sshd.SSHD.hostName=192.168.43.10 -jar D:\jenkins\jenkins.war --httpListenAddress=192.168.43.10
```

원서는 -D와 인자 이름 사이에 공백이 있으면 안 된다고 짚는다. -D 뒤에 바로 이름이 붙어야 자바가 시스템 속성으로 읽는다.

### 서비스로 띄우는 경우

젠킨스를 윈도우 서비스로 돌린다면 Jenkins.xml 파일을 열어 같은 인자를 `<arguments>` 태그 안에 추가한다. 원서의 Figure 19-1이 이 위치를 보여 주는데, 화면 모양은 추출본에서 확인되지 않는다. 설정이 끝나면 젠킨스 서비스를 재시작한다.

| 시작 방식 | 인자를 넣는 곳 | 마무리 |
| --- | --- | --- |
| jenkins.war 직접 실행 | java 명령줄의 -D 옵션 | 서버를 새로 시작 |
| 서비스 | Jenkins.xml의 arguments 태그 | 서비스 재시작 |

### SSH 연결 방식으로 명령 실행

서버가 시작되면 jenkins-cli.jar로 CLI 명령을 보낼 수 있다. 기본 형태는 다음과 같다.

```bat
java -jar ${Jenkins-cli.jar 경로} -s ${JENKINSURL} -i ${PrivateKeyPATH} -ssh -user ${UserName} ${CLI 명령} ${CLI 옵션}
```

Demo 잡을 빌드하는 원서의 실제 명령이다.

```bat
java -jar D:\JenkinsBookExamples\jenkins-cli.jar -s http://192.168.43.10:8080 -ssh -user Pranodayd -i D:\SSHKey\JenkinsCLI -p 9090 build Demo
```

| 옵션 | 의미 |
| --- | --- |
| -ssh | SSH 연결 방식을 쓰겠다는 표시. 반드시 넣어야 한다 |
| -user | 사용자 ID. -ssh를 쓰면 이 옵션도 반드시 함께 보낸다 |
| -i | 개인 키 파일 경로 |
| -p | SSH 포트. 기본값과 다를 때만 지정한다 |
| -s | 젠킨스 URL |

jenkins-cli.jar는 기본적으로 젠킨스가 도는 호스트와 포트에서 SSH 연결을 얻으려 한다. 그런데 이 장에서는 SSH 포트를 9090으로 따로 정했으므로 -p 9090을 지정해야 한다. 이 옵션을 빼면 엉뚱한 포트로 가려 하니 SSH 서버 포트를 바꿨다면 꼭 챙긴다.

원서 본문에는 `Jenkins-client.jar`라고 쓴 곳이 한 군데 있으나 jenkins-cli.jar의 오기로 보인다.

## 4. 두 방법 비교

| 구분 | OpenSSH 클라이언트 | jenkins-cli.jar (-ssh) |
| --- | --- | --- |
| 실행 파일 | ssh | java -jar jenkins-cli.jar |
| 사용자 지정 | 사용자@주소 | -user 사용자 |
| 포트 | -p SSH 포트 | -p SSH 포트 |
| 키 | -i 개인 키 | -i 개인 키 |
| 추가 설정 | SSH 서버와 방화벽 설정 | 비기본 IP이면 SSHD.hostName 인자도 필요 |

SSH 클라이언트가 이미 설치된 환경이라면 앞쪽이 간단하고, 젠킨스 JAR 하나로 통일하고 싶으면 뒤쪽이 편하다.

<br>
<br>
<br>

[CICD Pipeline Using Jenkins Unleashed](../)
