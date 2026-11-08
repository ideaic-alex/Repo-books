# Eclipse에서 Maven 프로젝트 만들기

이 문서는 Eclipse(자바 통합 개발 환경)에서 Maven 프로젝트를 새로 만드는 실습을 단계별로 따라간다. 원서에는 화면 스크린샷이 많은데, 여기서는 각 화면에서 무엇을 보고 무엇을 입력하는지를 글과 표로 풀어 적는다.

실습 결과로 만들어지는 프로젝트(CalculatorAPI)는 이후 장에서 젠킨스 잡으로 빌드하고 릴리스하는 대상이 된다.

---

## 1. 준비물

실습 전에 두 가지를 설치해 둔다.

| 준비물 | 용도 |
|---|---|
| JDK(Java Development Kit) | 자바 코드를 컴파일하고 실행하는 기본 개발 키트 |
| Eclipse(최신 버전) | 프로젝트를 만들고 편집하는 개발 환경 |

## 2. 워크스페이스 만들기

Eclipse 워크스페이스는 Eclipse에서 만드는 모든 프로젝트가 저장되는 작업용 폴더다. 젠킨스의 작업 공간(워크스페이스)과 이름은 같지만 서로 다른 개념이다.

1. Eclipse를 실행하면 워크스페이스 위치를 묻는 창이 뜬다.
2. 원하는 폴더 경로를 입력한다. 어느 폴더든 상관없다.
3. Launch 버튼을 누르면 Eclipse 환영 페이지가 나타난다.

## 3. Maven 프로젝트 생성

### 3.1 Maven 플러그인 확인

Maven은 명령줄 도구(CLI)여서 셸에서 명령을 실행해 쓰는 것이 기본이다. Eclipse 안에서 쓰려면 Eclipse용 Maven 플러그인이 설치되어 있어야 한다. 최신 Eclipse에는 이미 들어 있고, 오래된 버전이라면 직접 설치해야 할 수 있다.

설치 여부는 Window → Preferences 메뉴로 여는 Preferences 창에서 Maven 항목이 보이는지로 확인한다.

참고로, Maven이 플러그인과 프로젝트 의존성(dependency, 프로젝트가 필요로 하는 라이브러리)을 내려받으려면 인터넷 연결이 필요하다. 프록시가 설치된 네트워크라면 사용자 홈 아래 .m2 폴더에 settings.xml 파일을 만들고 프록시 정보를 적어야 한다. 이 내용은 settings.xml 문서에서 다룬다.

### 3.2 프로젝트 만들기 절차

1. File → New → Other 메뉴를 선택한다. Select a Wizard 창이 열린다.
2. 목록에서 Maven 항목을 펼친다.
3. Maven Project를 선택하고 Next 버튼을 누른다. New Maven Project 창이 열린다.
4. 이 창에서 다시 Next를 누르면 Select an Archetype(아키타입 선택) 창이 열린다.
5. Filter 입력란에 maven-archetype-quickstart를 입력하고 Next를 누른다.
6. Maven이 아키타입에 필요한 아티팩트 플러그인을 내려받는다. 시간이 걸릴 수 있다.
7. 내려받기가 끝나면 GroupId, ArtifactId, Version을 입력하는 창이 나타난다. 값을 채운다.
8. Finish 버튼을 누르면 프로젝트가 만들어진다.

### 3.3 아키타입이란

Maven은 이런 작업을 플러그인으로 처리한다. 애플리케이션 종류마다 필요한 디렉터리 구조가 다르다. 예를 들어 웹 애플리케이션에는 WEB-INF 폴더와 index.html 파일이 필요하고, EJB 애플리케이션은 또 다른 구조를 요구한다. 이런 구조를 알맞게 만들어 주는 것이 아키타입(archetype) 플러그인이다. 건축으로 치면 집 종류별 설계도 견본이라고 보면 된다.

| 아키타입 | 만드는 구조 | 이 책에서 쓰는가 |
|---|---|---|
| maven-archetype-webapp | 웹 애플리케이션에 필요한 디렉터리 구조 | 쓰지 않음 |
| maven-archetype-quickstart | 단순 자바 프로젝트 구조 | 사용 |

이 장에서는 단순한 자바 API 프로젝트를 만들므로 maven-archetype-quickstart를 고른다. 웹 애플리케이션을 만든다면 maven-archetype-webapp이 맞다.

## 4. GroupId, ArtifactId, Version

프로젝트 정보 입력 창에서 세 값을 채운다. 이 셋의 조합이 MvnRepository나 Nexus 같은 아티팩트 저장소에서 프로젝트를 유일하게 가리키는 주소가 된다. 아파트로 치면 단지, 동, 호수 같은 관계다.

| 항목 | 의미 | 원서에서 입력한 값 |
|---|---|---|
| GroupId | 프로젝트의 소유자, 또는 비슷한 종류의 프로젝트를 묶는 그룹 | Pranodayd |
| ArtifactId | 프로젝트의 이름 | CalculatorAPI |
| Version | 아티팩트 저장소에서 내려받을 수 있는 프로젝트의 특정 릴리스 | 1.0 |

표의 마지막 열은 원서가 예로 든 값이므로, 직접 실습할 때는 자기 이름이나 조직에 맞게 바꿔도 된다. 다만 뒤 장의 설명과 맞추려면 같은 값을 쓰는 편이 편하다.

## 5. 생성 직후 확인할 것

Finish를 누르면 ArtifactId와 같은 이름의 프로젝트 디렉터리가 만들어진다. 디렉터리 구조와 pom.xml 파일의 의미는 다음 문서에서 자세히 설명한다.

<br>
<br>
<br>

[CICD Pipeline Using Jenkins Unleashed](../)
