# settings.xml 설정

Maven은 아무 설정이 없어도 기본값으로 동작한다. 하지만 로컬 저장소 위치를 옮기거나 프록시 서버를 거쳐야 하는 사내망처럼 환경이 다르면 기본값을 바꿔야 한다. 이때 쓰는 파일이 settings.xml이다. 이 문서는 파일의 위치와 쓰는 법을 정리한다.

---

## 1. 언제 필요한가

| 상황 | 바꿀 설정 |
|---|---|
| 로컬 저장소를 기본 위치가 아닌 곳에 두고 싶다 | localRepository |
| 프록시가 있는 네트워크에서 플러그인과 의존성을 내려받아야 한다 | proxies |
| 중앙 저장소 URL을 바꾸고 싶다 | settings.xml로 가능하다고만 원서가 언급 |

원서에서 로컬 저장소의 기본 위치는 사용자 홈 아래 .m2\repository다. Maven이 플러그인과 의존성을 내려받으려면 인터넷이 필요하므로, 프록시 뒤에서는 프록시 정보를 settings.xml에 적어 주어야 한다.

## 2. 파일 위치

settings.xml은 사용자 홈 아래 .m2 디렉터리에 저장한다. 원서는 이 위치를 ${use.homer}\.m2로 적었는데 사용자 홈을 뜻하는 변수명이 잘못 적힌 것으로 보이며, 정확한 표기는 불확실하다. Windows에서는 보통 사용자 폴더 아래의 .m2 폴더를 가리킨다.

## 3. 로컬 저장소 위치만 바꾸기

```xml
<settings>
  <localRepository>D:\MavenRepo</localRepository>
</settings>
```

localRepository 태그에 원하는 경로를 적는다. 위 예에서는 로컬 저장소가 D:\MavenRepo로 바뀐다. 이후 Maven이 내려받는 플러그인과 의존성이 이 폴더에 쌓인다.

## 4. 저장소 위치와 프록시를 함께 설정하기

원서의 예제는 로컬 저장소 위치 변경과 프록시 서버 설정을 한 파일에 담았다.

```xml
<settings>
  <localRepository>D:\MavenRepo</localRepository>
  <proxies>
    <proxy>
      <protocol>http</protocol>
      <host>10.9.1.1</host>
      <port>80</port>
    </proxy>
  </proxies>
</settings>
```

프록시 항목은 아래와 같이 읽는다.

| 태그 | 예제 값 | 의미 |
|---|---|---|
| protocol | http | 프록시에 접속할 때 쓰는 프로토콜 |
| host | 10.9.1.1 | 프록시 서버 주소 |
| port | 80 | 프록시 서버 포트 |

값은 예시이며, 자기 네트워크의 프록시 주소와 포트를 적어야 한다. 이 파일을 .m2 폴더에 저장하면 이후 Maven 실행에 적용된다.

## 5. pom.xml과 settings.xml의 차이

| 구분 | pom.xml | settings.xml |
|---|---|---|
| 위치 | 프로젝트 디렉터리 | 사용자 홈 아래 .m2 |
| 내용 | 프로젝트 정보, 의존성, 빌드 설정 | 로컬 저장소 위치, 프록시 같은 실행 환경 설정 |

이 표는 앞 문서와 이 문서의 내용을 비교한 것이다. 프로젝트마다 달라지는 정보는 pom.xml에, 내 컴퓨터나 네트워크 환경에 따라 달라지는 정보는 settings.xml에 둔다고 이해하면 된다.

<br>
<br>
<br>

[CICD Pipeline Using Jenkins Unleashed](../)
