# Maven으로 Java API 프로젝트 준비하기

이 장은 젠킨스로 자동화할 첫 대상인 자바 API 프로젝트를 준비한다. 자바 API가 개발에서 릴리스까지 어떤 단계를 거치는지 살펴보고, 그 단계를 자동화하는 빌드 도구 Maven으로 간단한 계산기 API(CalculatorAPI)를 만든다. Eclipse에서 프로젝트를 만들고, 명령줄에서 mvn 명령으로 JAR 파일까지 만든다.

여기서 만든 프로젝트는 이후 장에서 젠킨스 잡으로 빌드하고 Nexus 저장소에 릴리스하는 대상이 된다. 그러니 pom.xml과 빌드 라이프사이클을 이해해 두면 뒤 장이 훨씬 쉽다.

---

## 1. 핵심 요점

- 자바 API는 JAR 파일로, 웹 애플리케이션은 WAR 파일로 묶여 각자 다른 곳에 배포된다. 그래서 애플리케이션 종류마다 빌드 단계가 다르다.
- 개발자는 라이브러리 내려받기, 컴파일, 테스트, 패키징, 릴리스를 반복한다. 빌드 도구(Ant, Maven, Gradle)가 이를 자동화한다.
- maven-archetype-quickstart로 만든 프로젝트는 src/main/java, src/test/java, pom.xml 구조를 가진다.
- GroupId, ArtifactId, Version 세 값이 아티팩트 저장소에서 프로젝트를 유일하게 식별한다.
- pom.xml은 프로젝트 식별 정보, 속성, 의존성, 빌드 플러그인을 정의한다. scope가 test인 의존성은 테스트 때만 CLASSPATH에 오른다.
- 빌드 단계는 clean, 의존성 내려받기, 소스 컴파일, 단위 테스트, package, install, deploy 순서이며 단계마다 담당 플러그인이 있다.
- mvn package를 실행하면 앞 단계가 모두 실행되고 target 폴더에 JAR가 만들어진다. 명령은 pom.xml이 있는 폴더에서 실행한다.
- settings.xml로 로컬 저장소 위치와 프록시를 바꿀 수 있다.

---

## 2. 문서 목록

- [자바 API 개발 흐름과 빌드 도구](자바 API 개발 흐름과 빌드 도구.md): 자바 API 개발 단계와 빌드 도구가 필요한 이유
- [Eclipse에서 Maven 프로젝트 만들기](Eclipse에서 Maven 프로젝트 만들기.md): 워크스페이스, 아키타입, GroupId와 ArtifactId 설정 실습
- [프로젝트 구조와 pom.xml](프로젝트 구조와 pom.xml.md): 디렉터리 구조, 계산기 코드 파일, pom.xml 각 섹션, 로컬 저장소
- [빌드 라이프사이클 단계](빌드 라이프사이클 단계.md): clean부터 deploy까지 단계별 플러그인과 산출물 위치
- [명령줄에서 Maven 쓰기](명령줄에서 Maven 쓰기.md): Maven 설치, 환경 변수 설정, mvn package 실행
- [settings.xml 설정](settings.xml 설정.md): 로컬 저장소 위치와 프록시 설정
- [요약과 핵심 개념](요약과 핵심 개념.md): 장 요약, 핵심 용어, 불확실한 부분

<br>
<br>
<br>

[CICD Pipeline Using Jenkins Unleashed](../)
