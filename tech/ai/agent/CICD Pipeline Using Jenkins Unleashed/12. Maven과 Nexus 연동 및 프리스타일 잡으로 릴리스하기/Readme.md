# Maven과 Nexus 연동 및 프리스타일 잡으로 릴리스하기

이 장은 앞 장에서 만든 Java API 프로젝트(CalculatorAPI)를 소스 저장소에서 가져와 빌드하고, 결과물인 JAR 파일을 Nexus 저장소에 릴리스하는 과정을 다룬다. 소스 코드는 Git과 GitLab으로 관리하고, 빌드 결과물은 아티팩트 저장소인 Nexus에 보관한다.

마지막에는 젠킨스 프리스타일 잡이 두 저장소를 이어 준다. 개발자가 새 기능을 브랜치에 올려 Master에 병합하면, 잡이 Maven으로 빌드하고 Nexus에 새 버전을 올린다.

---

## 1. 핵심 요점

- Git은 분산 버전 관리 시스템이고, GitLab과 GitHub는 웹에 두는 중앙 저장소 서비스다. 로컬 저장소와 중앙 저장소를 함께 쓴다.
- 로컬 저장소는 `git init`으로 만들고, `git add`와 `git commit`으로 브랜치에 기록하며, `git push`로 GitLab에 올린다. `.gitignore`로 추적하지 않을 파일을 정한다.
- Master 브랜치를 기본 브랜치로 두고, 기능 브랜치는 Merge Request로 합친다. 릴리스는 Master의 코드로 만든다.
- 아티팩트는 빌드 결과물이고, Nexus는 그 버전들을 보관하는 아티팩트 저장소다. Maven2 (hosted) 유형으로 릴리스용 저장소를 만든다.
- Nexus 서버의 IP와 포트는 `nexus-default.properties`에서 정하고, `Nexus.exe /run`으로 실행하거나 Windows 서비스로 설치한다.
- Maven은 pom.xml의 `<distributionManagement>`에 저장소 URL을, settings.xml에 로그인 정보를 둔다. 두 `<id>`는 같아야 한다.
- `mvn deploy`는 컴파일, 테스트, 패키징을 거쳐 JAR를 Nexus에 배포한다.
- 젠킨스에서는 Maven 설치를 등록하고, Git 자격 증명을 만든 뒤, Invoke Top-Level Maven Targets 스텝에 `deploy`를 넣은 프리스타일 잡으로 2.0 릴리스를 만든다.

---

## 2. 문서 목록

- [버전 관리와 Git 이해하기](버전 관리와 Git 이해하기.md): 버전 관리 세 종류, Git 설치, Git과 GitHub/GitLab의 관계
- [Git 로컬 저장소와 GitLab 저장소 실습](Git 로컬 저장소와 GitLab 저장소 실습.md): 로컬 저장소, GitLab 저장소, 커밋, 푸시, Master 브랜치 설정
- [Nexus 저장소 설치와 호스티드 저장소](Nexus 저장소 설치와 호스티드 저장소.md): 아티팩트 개념, Nexus 설치와 실행, 서비스 등록, 호스티드 저장소 생성
- [Maven과 Nexus 연동하고 배포하기](Maven과 Nexus 연동하고 배포하기.md): pom.xml과 settings.xml 설정, `mvn deploy`, Nexus에서 확인
- [프리스타일 잡으로 릴리스하기](프리스타일 잡으로 릴리스하기.md): 젠킨스 Maven 설정, 잡 생성, 기능 추가와 병합, 실행과 확인
- [요약과 핵심 개념](요약과 핵심 개념.md): 장 요약, 개념 표, 명령어 표, 다음 장 안내

<br>
<br>
<br>

[CICD Pipeline Using Jenkins Unleashed](../)
