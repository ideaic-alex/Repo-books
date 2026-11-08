# 젠킨스와 AWS 연동하기

이 장은 젠킨스로 웹 애플리케이션을 AWS 클라우드의 서버에 배포하고, 그 서버를 대상으로 Selenium 테스트를 돌리는 과정을 다룬다. 배포 대상은 AWS의 가상 서버인 EC2 인스턴스이고, 배포할 앱은 앞 장들에서 쓴 Calculator 웹 애플리케이션이다.

실습은 인스턴스 만들기, 웹 서버 준비, SSH 연결 설정, 젠킨스 잡 작성 순서로 이어진다. 이 노트는 원서의 서술 시점을 따르므로 AWS 콘솔의 화면 구성은 이후 바뀌었을 수 있다.

---

## 1. 핵심 요점

- EC2 인스턴스는 AWS의 가상 서버이며 시간 단위로 요금이 붙는다. 안 쓰면 종료해서 비용을 줄인다.
- 인스턴스에 접속하는 키 쌍은 AWS에서 만들고, .pem 개인 키로 RDP 비밀번호를 푼다.
- Windows 인스턴스에 IIS를 설치하고 가상 디렉터리 CalculatorWebApp을 C:\DeployedCalculatorApp에 연결한다.
- SSH 접속을 위해 로컬에서 ssh-keygen으로 키를 만들고, 공개 키를 인스턴스의 authorized_keys에 넣는다.
- 보안 그룹의 인바운드 규칙에 SSH와 HTTP를 추가해야 밖에서 접속할 수 있다.
- scp 명령으로 Calculator.html을 인스턴스에 복사하는 프리스타일 잡을 만든다.
- 배포 잡은 빌드 후 조치로 TestCalculatorWebApplication 잡을 이어 실행하고, 테스트 대상 주소는 EnvVars.csv의 ApplicationURL로 바꾼다.

---

## 2. 문서 목록

- [EC2 인스턴스 이해와 생성](EC2 인스턴스 이해와 생성.md): EC2의 개념, AWS 가입, 인스턴스 생성과 RDP 접속
- [IIS 웹 서버 설치와 설정](IIS 웹 서버 설치와 설정.md): IIS 설치, 배포 폴더와 가상 디렉터리 만들기
- [SSH 연결 설정과 파일 복사](SSH 연결 설정과 파일 복사.md): SSH 키, OpenSSH 서버, 인바운드 규칙, scp 복사, 브라우저 확인
- [젠킨스 잡으로 EC2에 배포하기](젠킨스 잡으로 EC2에 배포하기.md): 배포 잡, 다운스트림 테스트 잡, ApplicationURL 변경, 실행
- [요약과 핵심 개념](요약과 핵심 개념.md): 장 요약, 용어 표, 배포 흐름

<br>
<br>
<br>

[CICD Pipeline Using Jenkins Unleashed](../)
