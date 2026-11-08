# 기타 주제 1

이 장은 젠킨스를 화면 대신 명령어로 다루는 젠킨스 CLI(명령줄 인터페이스)를 소개한다. 마우스로 하던 일을 스크립트나 셸 프로그램으로 자동화해야 할 때 쓰는 방법으로, jenkins-cli.jar를 내려받아 잡을 만들고 빌드를 실행하는 과정을 차례로 따라간다.

인증이 이 장의 큰 줄기다. API 토큰으로 접속하는 방법과 SSH 키로 접속하는 방법을 각각 정리하고, 마지막에는 배치 코드로 잡을 한꺼번에 내보내고 가져오는 서버 이전 실습을 다룬다. 같은 주제의 REST API는 다음 장에서 이어진다.

---

## 1. 핵심 요점

- 젠킨스 CLI는 셸이나 배치 파일에서 젠킨스를 조작하는 명령줄 인터페이스다. Manage Jenkins의 Jenkins CLI 페이지에서 명령 목록을 볼 수 있다.
- CLI 클라이언트는 jenkins-cli.jar다. 이 파일로 create-job, build, list-jobs, get-job 같은 명령을 보낸다.
- 인증 없이 보내면 익명 사용자로 처리되어 Overall/Read 권한 오류가 난다. -auth 옵션으로 사용자 이름과 API 토큰을 보내 해결한다.
- SSH 인증을 쓰려면 ssh-keygen -m PEM -t rsa로 키를 만들고, 공개 키를 사용자 설정에 등록하고, SSH Server 포트(Fixed 권장)와 방화벽 인바운드 규칙을 설정한다.
- build 명령에는 -c(변경 있을 때만), -f, -p, -s, -v, -w 옵션이 있다. OpenSSH 클라이언트와 jenkins-cli.jar의 -ssh 모드 두 가지로 SSH 인증을 쓸 수 있다.
- 비기본 IP로 젠킨스를 띄우면 SSHD.hostName 인자가 필요하고, 서비스로 돌린다면 Jenkins.xml의 arguments 태그에 넣는다.
- list-jobs와 get-job을 반복문으로 엮으면 모든 잡을 XML로 내보내고, create-job 반복으로 새 서버에 가져올 수 있다.

---

## 2. 문서 목록

- [CLI 시작과 잡 만들기](CLI 시작과 잡 만들기.md): CLI 소개, jenkins-cli.jar 준비, create-job 실습과 익명 사용자 오류
- [API 토큰으로 인증하기](API 토큰으로 인증하기.md): API 토큰 발급과 -auth 옵션으로 잡 만들기
- [SSH 인증 준비](SSH 인증 준비.md): 키 쌍 생성, 공개 키 등록, SSH Server 포트, 방화벽 인바운드 규칙
- [SSH로 빌드 실행하기](SSH로 빌드 실행하기.md): build 옵션, OpenSSH와 jenkins-cli.jar 두 가지 방법
- [잡 내보내기와 가져오기](잡 내보내기와 가져오기.md): list-jobs, get-job, create-job 배치 코드 해설
- [요약과 핵심 개념](요약과 핵심 개념.md): 장 요약과 개념, 명령 정리

<br>
<br>
<br>

[CICD Pipeline Using Jenkins Unleashed](../)
