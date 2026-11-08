# Nexus 저장소 설치와 호스티드 저장소

소스 코드를 담는 곳이 Git이라면, 빌드 결과물을 담는 곳이 Nexus다. 이 문서는 아티팩트가 무엇인지, 왜 아티팩트 저장소가 따로 필요한지, Nexus를 Windows에 설치하고 실행하는 방법, 릴리스를 올릴 호스티드 저장소를 만드는 방법을 정리한다.

---

## 1. 아티팩트와 Nexus 저장소

아티팩트(artifact)는 빌드 과정에서 나오는 모든 결과물이다. 웹 애플리케이션을 `.WAR` 파일로 묶어 배포한다면 그 `.WAR`가 아티팩트다. 이 장의 Java API 프로젝트는 구현을 `.JAR` 파일로 묶는데, 이 `.JAR`가 빌드가 만든 아티팩트다.

Git은 소스 코드의 버전을 보관한다. 하지만 CalculatorAPI에 기능을 더할 때마다 `CalculatorAPI.jar`도 새 버전이 생긴다. 이 결과물의 버전들을 보관할 시스템이 아티팩트 저장소이고, Nexus가 그런 시스템이다. 릴리스한 아티팩트를 올려 두면 사용자가 필요할 때 내려받을 수 있다.

| 구분 | 보관하는 것 | 이 장의 도구 |
| --- | --- | --- |
| 소스 코드 저장소 | 소스 코드의 버전들 | Git, GitLab |
| 아티팩트 저장소 | 빌드 결과물(JAR 등)의 버전들 | Nexus |

원서는 웹의 mvnrepository.com에도 아티팩트를 배포할 수 있다고 말한다. 다만 거기에 올린 아티팩트는 누구나 내려받아 쓸 수 있다. 조직 사람만 접근하는 아티팩트 저장소가 필요하면 조직 네트워크에 Sonatype Nexus 저장소를 직접 세워야 한다.

---

## 2. Nexus 설치

1. https://www.sonatype.com/products/repository-oss-download 에서 Nexus 저장소 ZIP을 내려받는다.
2. 원하는 위치에 압축을 푼다. 원서는 `D:\NexusRepository`에 풀었다.

압축을 풀면 폴더가 두 개 나온다.

| 폴더 | 내용 |
| --- | --- |
| nexus-3.30.1-01 | Nexus 시스템 파일. `bin` 폴더에 Nexus 시작용 `Nexus.exe`가 있다 |
| sonatype-work | 사용자가 만든 여러 아티팩트 저장소의 데이터가 들어간다 |

폴더 이름의 버전 번호는 원서가 쓴 버전이다. 다른 버전을 받으면 이름이 다르다.

---

## 3. Nexus 시작하기

Nexus는 서버다. 컴퓨터의 IP 주소와 특정 포트로 뜬다. 어느 주소와 포트로 띄울지는 Nexus 설치 폴더의 `etc` 폴더 안에 있는 `nexus-default.properties` 파일에서 정한다. 원서 환경에서는 이 파일이 `D:\NexusRepository\nexus-3.30.1-01\etc\nexus-default.properties`다.

| 설정 키 | 의미 | 원서 값 |
| --- | --- | --- |
| application-port | Nexus 서버가 시작될 포트 | 8081 |
| application-host | Nexus 서버를 띄울 컴퓨터의 IP 주소 | 192.168.43.10 |

IP 주소는 `ipconfig` 명령으로 확인한다. 원서의 값은 저자 컴퓨터의 주소이므로 자기 환경에서는 자기 주소를 써야 한다.

설정 후 서버를 실행한다.

1. 명령 프롬프트에서 Nexus 설치 폴더의 `bin` 폴더로 이동한다.
2. 아래 명령을 실행하고 서버가 뜰 때까지 기다린다.

```
Nexus.exe /run
```

처음 설정하는 경우 몇 분이 걸릴 수 있다. 이 과정에서 기본 관리자 계정(사용자 이름 `admin`)이 만들어지고, 비밀번호는 `${NexusInstallationDir}\sonatype-work\nexus3\admin.password` 파일에 저장된다. Windows 보안 경고 창이 뜨면 Allow Access 버튼을 누른다. 그러면 서버가 정상 시작된다.

---

## 4. Nexus를 Windows 서비스로 설치하기

컴퓨터를 켤 때마다 명령 프롬프트로 띄우기 번거로우면 Windows 서비스로 등록할 수 있다.

```
Nexus.exe /install <ServiceName>
```

서비스 이름은 생략해도 된다. 절차는 이렇다.

1. 명령 프롬프트를 열고 `${NexusInstallationDir}\bin`으로 이동한다.
2. `Nexus.exe /install MyNexusService`를 실행한다.
3. Windows 서비스 목록에서 `MyNexusService`가 설치됐는지 확인한다.
4. Start Service 버튼으로 서비스를 시작한다.

---

## 5. Nexus Repository Manager 접속과 초기 설정

1. 브라우저에서 `http://<IP 주소>:<포트>`로 접속한다. 원서는 `http://192.168.43.10:8081`을 썼다.
2. 오른쪽 위의 Signin 버튼을 눌러 로그인 창을 연다.
3. 사용자 이름에 `admin`을 넣고, 비밀번호에는 `sonatype-work\nexus3\admin.password` 파일에서 복사한 값을 넣는다. 원서의 위치는 `D:\NexusRepository\sonatype-work\nexus3`다.
4. 설정 마법사에서 Next를 누르고 새 관리자 비밀번호를 입력한 뒤 Next를 누른다.
5. Disable Anonymous Access를 선택한다. 올바른 자격 증명이 있는 사용자만 접근하게 하는 옵션이다. Next, Finish 순으로 마친다.

익명 접근을 막아 두었기 때문에 뒤에서 Maven이 배포할 때 Nexus의 사용자 이름과 비밀번호를 따로 알려 줘야 한다.

---

## 6. 호스티드 저장소 만들기

릴리스를 올릴 호스티드(hosted) 저장소를 만든다. 호스티드는 Nexus가 직접 아티팩트를 보관하는 저장소 방식이다.

1. Server Administration and Configuration 버튼을 누른다.
2. Repositories 링크를 누르고 Create Repository 버튼을 누른다. Repositories/Select Recipe 페이지가 열린다.
3. 목록에서 Maven2 (hosted)를 고른다.
4. Create Repository: maven2 (hosted) 페이지의 Name 칸에 저장소 이름을 넣는다. 원서의 이름은 `JenkinsBookCalculatorAPI_Release`다.
5. 아래로 스크롤해 Create Repository 버튼을 누른다.
6. Repositories 목록(Manage Repositories 페이지)에 새 저장소가 나타나면 완료다.

Maven2 (hosted)는 Maven 방식으로 아티팩트를 주고받는 Nexus 내부 저장소 유형이다. 다음 문서에서 이 저장소의 URL을 pom.xml에 적는다.

<br>
<br>
<br>

[CICD Pipeline Using Jenkins Unleashed](../)
