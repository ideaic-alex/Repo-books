# JDK 설정과 자동 설치

Jenkins로 Java 프로젝트를 빌드하려면 JDK(Java 개발 도구 모음)가 필요하다. 이 문서는 Global Tool Configuration 페이지에서 JDK를 등록하는 방법을 정리한다. Maven 설정과 흐름이 거의 같으므로, 앞 문서를 읽었다면 어렵지 않다.

---

## 1. 이미 설치된 JDK를 등록하는 방법

빌드 서버에 Java가 이미 있다면 그 위치를 Jenkins에 알려 주는 것으로 끝난다.

1. Global Tool Configuration 페이지의 JDK 구역에서 Add JDK 버튼을 누른다.
2. Installed Automatically 체크박스를 해제한다. 원문은 JDK 쪽 체크박스를 이 이름으로 적는다. Maven 쪽은 Install Automatically로 적혀 있는데, 같은 기능의 체크박스다.
3. Name 칸에 알아보기 쉬운 이름을 적는다.
4. JAVA_HOME 칸에 Java 설치 디렉터리의 절대 경로를 적는다.
5. 페이지 아래의 Save 버튼으로 저장한다. 원문은 JDK 부분에서 저장 단계를 따로 적지 않지만, 앞의 Maven 설정과 같은 페이지이므로 저장해야 반영된다고 보면 된다.

| 입력칸 | 넣는 값 | 설명 |
|---|---|---|
| Installed Automatically | 해제 | 서버에 Java가 이미 있을 때 |
| Name | 알아보기 쉬운 이름 | 다른 곳에서 이 JDK를 가리킬 때 쓰는 이름 |
| JAVA_HOME | Java 설치 디렉터리의 절대 경로 | 상대 경로가 아니라 절대 경로를 적는다 |

원문은 JDK 이름에 대해서는 글자 제한을 따로 말하지 않는다.

## 2. JDK를 자동으로 설치하게 하는 방법

서버에 JDK가 없고 필요할 때 Jenkins가 설치해 주길 원하면 Installed Automatically 체크박스를 켜고 설치 방법(installer)을 설정한다. 설정 방법은 앞의 Maven 자동 설치와 같은 방식이라고 원문이 안내한다. 원문은 JDK 설치기의 세부 입력칸과 값을 따로 풀어 쓰지 않는다.

| 상황 | 체크박스 | 입력할 것 |
|---|---|---|
| JDK가 이미 설치됨 | 해제 | Name, JAVA_HOME |
| JDK가 없어서 Jenkins가 설치하게 함 | 체크 | 설치 방법(installer) 설정 |

Maven 자동 설치와 비교해서 기억하면 쉽다. 체크박스를 켜면 이미 있는 위치 대신 어디서 받아 올지를 알려 주는 입력칸이 나타난다는 점이 같다.

## 3. Maven과 JDK 설정 비교

| 비교 항목 | Maven | JDK |
|---|---|---|
| 구역에서 누르는 버튼 | Add Maven | Add JDK |
| 설치 경로 입력칸 | MAVEN_HOME | JAVA_HOME |
| 자동 설치 체크박스 | Install Automatically | Installed Automatically (원문 표기) |
| 이름 입력칸 | Name | Name |
| 별도 설정 파일 | settings.xml 두 개 | 원문에 언급 없음 |

둘의 구조가 거의 같으므로, 새 도구를 만나도 이름, 설치 경로, 자동 설치 여부 세 가지를 확인하는 습관을 들이면 된다.

<br>
<br>
<br>

[CICD Pipeline Using Jenkins Unleashed](../)
