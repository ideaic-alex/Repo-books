# 명령줄에서 Maven 쓰기

앞에서는 Eclipse 안에서 Maven을 썼다. 하지만 Maven은 본래 명령줄 도구여서 셸에서 mvn 명령으로도 쓸 수 있다. 이 문서는 Windows에서 Maven을 내려받아 설치하고, 환경 변수를 설정하고, mvn 명령으로 JAR를 만드는 과정을 정리한다.

---

## 1. Maven 설치

1. Apache Maven 사이트의 바이너리 압축 파일(원서는 apache-maven-3.8.1-bin.zip)을 내려받는다. 원서가 안내한 주소는 https://apachemirror.wuchna.com/maven/maven-3/3.8.1/binaries/apache-maven-3.8.1-bin.zip 이며, 미러 주소여서 지금은 다를 수 있다.
2. 원하는 위치에 압축을 푼다. 원서는 D:\MavenInstallation에 풀었다.
3. 압축을 푼 apache-maven-3.8.1\bin 안에 mvn 명령 파일이 있다. 이것이 Maven CLI이며 명령 프롬프트에서 쓴다.

mvn을 어느 폴더에서든 부르려면 PATH 환경 변수에 등록하고, JAVA_HOME과 M2_HOME 변수를 만들어야 한다.

| 변수 | 값 | 목적 |
|---|---|---|
| M2_HOME | Maven을 푼 위치 | Maven 설치 위치를 가리킴 |
| PATH | %M2_HOME%\bin 항목 추가 | 어느 위치에서나 mvn 실행 |
| JAVA_HOME | JDK가 설치된 위치 | Maven이 사용할 JDK 위치 |

표의 목적 열은 변수 이름에서 풀이한 설명이며, 원서는 값만 안내한다.

## 2. 환경 변수 설정 절차

1. Start 메뉴에서 Edit System Environment Variables를 입력해 찾아 연다.
2. Edit the System Environment Variables 항목을 선택하면 System Properties 창이 열린다.
3. Environment Variables 버튼을 눌러 Environment Variables 창을 연다.
4. System Variables 영역에서 New 버튼을 누른다. New System Variable 창이 열린다.
5. Variable Name에 M2_HOME, Variable Value에 Maven 위치를 넣는다.
6. OK를 누르면 System Variables 목록에 M2_HOME이 추가된다.
7. System Variables 목록에서 PATH 항목을 찾는다.
8. Edit를 누르고, 이어서 New를 눌러 새 항목에 다음 값을 입력한다.

```text
%M2_HOME%\bin
```

9. OK를 누른다.
10. 다시 System Variables 영역에서 New를 눌러 JAVA_HOME 변수를 만든다.
11. Variable Name에 JAVA_HOME, Variable Value에 JDK 위치를 넣는다.
12. 설정이 끝나면 명령 프롬프트에서 아래 명령으로 Maven이 제대로 설정됐는지 확인한다.

```bash
mvn -version
```

버전 정보가 출력되면 설정이 성공한 것이다.
## 3. Maven 명령 실행

설정을 마치면 명령 프롬프트에서 빌드 라이프사이클 단계를 하나씩 제어할 수 있다.

1. 명령 프롬프트를 열고 cd 명령으로 작업 디렉터리를 프로젝트 디렉터리로 옮긴다.
2. 특정 단계를 실행하려면 mvn 다음에 골 이름을 쓴다.

```bash
mvn package
```

Maven 명령은 반드시 pom.xml이 있는 Maven 프로젝트 디렉터리에서 실행해야 한다.
## 4. 앞 단계도 함께 실행된다

Maven에서 어떤 골을 실행하면 그 앞의 골도 모두 함께 실행된다. 그래서 mvn package 한 줄이면 다음 일이 순서대로 일어난다.

| 순서 | 실행되는 일 | 담당 |
|---|---|---|
| 1 | 프로젝트 의존성 내려받기 | maven-resources 플러그인 |
| 2 | API 소스 코드 컴파일 | 컴파일러 플러그인 |
| 3 | 단위 테스트 코드 컴파일 | 컴파일러 플러그인 |
| 4 | 단위 테스트 실행 | maven-surefire-plugin |
| 5 | JAR 파일 생성 | maven-jar-plugin |

표의 2, 3번 담당은 원서가 플러그인 이름을 적지 않았고, 앞 문서의 라이프사이클 설명에 따라 컴파일러 플러그인으로 적었다. 이 동작 덕분에 단계를 하나씩 부르지 않고 마지막 단계만 지정해도 된다.

Eclipse에서 하던 작업과 명령줄 작업을 비교하면 다음과 같다.

| 비교 | Eclipse | 명령줄 |
|---|---|---|
| 실행 방법 | Maven 플러그인을 통해 화면에서 | 셸에서 mvn 명령 |
| 필요한 설치 | Eclipse와 내장 Maven 플러그인 | Maven 압축 해제, M2_HOME, PATH, JAVA_HOME 설정 |

이 표는 원서 내용을 두 방식으로 나누어 정리한 것이다.

<br>
<br>
<br>

[CICD Pipeline Using Jenkins Unleashed](../)
