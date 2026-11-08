# 젠킨스 설치하기

이 장은 젠킨스를 실제로 설치하기 위한 준비와 방법을 다룬다. 최소 하드웨어와 자바 버전 요구 사항을 확인한 뒤, 윈도에서 MSI 설치 파일, WAR 파일, Docker 이미지로 설치하는 세 가지 길을 소개한다. 이어서 설치 후 생기는 JENKINS_HOME 폴더 구조와, 젠킨스가 쓸 자바를 정하는 Jenkins.xml 설정을 살펴본다.

원서는 각 설치 방법의 세부 단계를 공식 문서 링크로 안내하므로 이 노트도 그 범위를 따른다. 설치 후 서버를 시작하고 설정하는 내용은 다음 장에서 이어진다.

---

## 1. 핵심 요점

- 최소 사양은 RAM 256MB, 디스크 1GB이며, Docker 컨테이너로 돌릴 때는 디스크 10GB를 권장한다.
- 젠킨스는 JDK 8과 JDK 11만 지원한다. JDK 11은 젠킨스 2.164 계열부터 지원되고, 더 오래된 자바는 지원하지 않는다.
- 윈도에서는 MSI 설치 파일, WAR 파일, Docker 이미지의 세 방법으로 설치할 수 있다.
- 기본 설치 위치는 사용자 홈의 .jenkins 폴더이며, MSI로 설치하면 직접 고른 폴더가 된다. 이 폴더를 JENKINS_HOME이라 부른다.
- JENKINS_HOME 아래에는 config.xml, plugins, secrets, workspace, jobs 등이 있고, 잡 폴더에는 설정과 빌드별 로그가 남는다.
- Jenkins.xml의 서비스 태그에는 젠킨스가 쓰는 Java.exe 위치가 있으며, 기본은 PATH 환경 변수의 자바다.
- 다른 자바를 쓰려면 `<executable>` 태그에 원하는 Java.exe의 전체 경로를 적는다.

---

## 2. 문서 목록

- [설치 요구 사항과 세 가지 방법](<설치 요구 사항과 세 가지 방법.md>): 하드웨어와 JDK 요구 사항, MSI, WAR, Docker 설치 방식
- [JENKINS_HOME 디렉터리 구조](<JENKINS_HOME 디렉터리 구조.md>): 기본 설치 위치, 폴더별 역할, 잡과 빌드 기록 구조
- [Jenkins.xml과 자바 지정](<Jenkins.xml과 자바 지정.md>): 서비스 설정 파일과 사용할 자바 바꾸기
- [요약과 핵심 개념](<요약과 핵심 개념.md>): 장 흐름과 용어 정리

<br>
<br>
<br>

[CICD Pipeline Using Jenkins Unleashed](../)
