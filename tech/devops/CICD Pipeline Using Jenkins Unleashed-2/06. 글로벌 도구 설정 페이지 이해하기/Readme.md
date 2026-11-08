# 글로벌 도구 설정 페이지 이해하기

이 장은 Jenkins의 Global Tool Configuration 페이지에서 Maven과 JDK를 설정하는 방법을 다룬다. 잡이 Java나 Maven 같은 도구를 쓸 때 Jenkins가 그 위치를 알고 있어야 하므로, 도구의 이름과 설치 경로, 자동 설치 방법을 한곳에 등록해 둔다.

Maven은 settings.xml 위치 지정과 설치 구성이라는 두 부분으로 나뉘고, JDK는 이름과 JAVA_HOME만 지정하면 된다. 서버에 도구가 없을 때 Jenkins가 대신 설치하게 하는 자동 설치 기능도 함께 정리한다.

---

## 1. 핵심 요점

- Global Tool Configuration 페이지는 Manage Jenkins에서 들어가며, Jenkins에서 쓸 도구의 위치와 설치 방법을 등록하는 곳이다.
- Gradle, Git 같은 다른 도구의 플러그인이 설치되어 있으면 그 도구의 설정도 이 페이지에 나타난다.
- Maven은 글로벌 settings.xml과 사용자 settings.xml 두 파일로 설정하며, 같은 설정이 겹치면 사용자 설정이 우선한다.
- settings.xml이 기본 위치에 있으면 기본 옵션을 두고, 다른 위치에 있으면 Settings File in Filesystem 같은 옵션으로 경로를 적는다.
- Maven 설정의 Name에는 숫자, 공백, 특수문자를 쓰지 않는다. 파이프라인이 이 이름으로 설정을 가리키기 때문이다.
- 서버에 Maven이 있으면 Install Automatically를 해제하고 MAVEN_HOME을 적는다. 없으면 체크하고 압축 파일 설치 방식을 설정한다.
- 압축 설치에서는 Subdirectory of Extracted Archive 값을 압축 해제 후 폴더 이름과 맞춰야 mvn 명령을 찾는다.
- JDK도 같은 방식이며, 이미 있으면 Name과 JAVA_HOME을 적고 없으면 자동 설치를 켠다.

---

## 2. 문서 목록

- [글로벌 도구 설정 페이지 찾아가기](글로벌 도구 설정 페이지 찾아가기.md): 페이지의 역할, 접근 순서, 장에서 다루는 범위
- [Maven 설정 파일과 설치 구성](Maven 설정 파일과 설치 구성.md): settings.xml 두 종류, 위치 지정, 설치 구성, 자동 설치
- [JDK 설정과 자동 설치](JDK 설정과 자동 설치.md): JAVA_HOME 등록, 자동 설치, Maven과의 비교
- [요약과 핵심 개념](요약과 핵심 개념.md): 장 결론, 핵심 개념 표, 다음 장 안내

<br>
<br>
<br>

[CICD Pipeline Using Jenkins Unleashed](../)
