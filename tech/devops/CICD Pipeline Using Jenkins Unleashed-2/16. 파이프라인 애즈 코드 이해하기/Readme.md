# 파이프라인 애즈 코드 이해하기

이 장은 Jenkins가 Git 저장소와 더 깊이 연결되는 방법을 다룬다. 먼저 비밀번호 대신 쓰는 API 토큰을 GitHub와 GitLab에서 만들어 저장소 접근에 쓰고, 그 토큰을 Jenkins 자격 증명으로 등록해 잡을 실행한다. 이어서 파이프라인을 Jenkins 화면이 아닌 젠킨스파일에 쓰는 파이프라인 애즈 코드를 배운다.

마지막으로 GitLab과 GitHub의 웹훅으로 푸시 이벤트가 일어날 때 잡이 자동으로 실행되게 만든다. 실습 값(저장소 이름, IP 주소, 버전 번호)은 책의 예시를 따른다.

---

## 1. 핵심 요점

- API 토큰은 비밀번호 대신 쓰는 비밀 문자열이다. GitHub는 repo, GitLab은 write_repository 권한으로 만들고, 생성 직후 한 번만 볼 수 있으니 복사해 둔다.
- 토큰으로 git clone과 git push를 하면 윈도우 자격 증명에 저장되어 이후에는 입력창이 뜨지 않는다.
- Jenkins에서 토큰을 쓰려면 Secret Text가 아니라 Username with Password 종류의 자격 증명을 만든다. 저장소 접근에는 사용자 이름이 필요하기 때문이다.
- 젠킨스파일은 파이프라인 코드를 소스 저장소에 함께 두는 파일이다. 변경 이력 추적, 코드 리뷰, 공유가 가능해진다.
- 선언형 파이프라인은 pipeline 블록으로 시작하고, environment로 공유 변수를, post로 success, failure, always 후처리를 정의한다.
- archiveArtifacts는 결과물을 작업 공간 밖의 ${JENKINS_HOME}에 보존하고, emailext의 attachLog로 실패 메일에 콘솔 로그를 붙인다.
- 잡의 Definition을 Pipeline script from SCM으로 바꾸고 Script Path에 젠킨스파일 위치를 적어 실행한다.
- 웹훅은 저장소 이벤트를 URL로 알리는 방식이며, 외부에서 Jenkins에 닿으려면 공인 IP와 포트 포워딩이 필요하다.

---

## 2. 문서 목록

- [API 토큰 인증과 저장소 접근](API 토큰 인증과 저장소 접근.md): GitHub와 GitLab에서 토큰을 만들고 clone, push에 쓰는 실습
- [젠킨스에서 API 토큰으로 프리스타일 잡 실행](젠킨스에서 API 토큰으로 프리스타일 잡 실행.md): 자격 증명 종류 선택과 Nexus 릴리스 잡 설정
- [파이프라인 애즈 코드와 젠킨스파일](파이프라인 애즈 코드와 젠킨스파일.md): 젠킨스파일의 장점, 선언형 문법, post 블록, Pipeline script from SCM
- [웹훅으로 잡 트리거하기](웹훅으로 잡 트리거하기.md): 공인 IP와 포트 포워딩, GitLab과 GitHub 웹훅 설정
- [요약과 핵심 개념](요약과 핵심 개념.md): 장 전체 흐름, 핵심 개념 표, 자주 놓치는 점

<br>
<br>
<br>

[CICD Pipeline Using Jenkins Unleashed](../)
