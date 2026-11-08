# 기타 주제 2

이 장은 Jenkins를 프로그램으로 제어하는 방법과 파이프라인 코드를 재사용하는 방법을 다룬다. 앞 장의 CLI로는 부족할 때 Jenkins가 제공하는 REST API를 curl과 파이썬(Python-Jenkins)으로 호출해 설정 조회, 잡 생성, 빌드 실행을 해 본다. 이어서 여러 잡이 같은 빌드 단계를 공유하도록 공유 라이브러리를 만들고 쓰는 과정을 따라간다.

책의 마지막 장이기도 해서 끝에는 책 전체를 맺는 짧은 요약이 있다. 이 노트는 책의 서술 시점을 따르므로 화면 구성이나 버전은 이후 바뀌었을 수 있다.

---

## 1. 핵심 요점

- Jenkins 원격 접근 API는 REST 비슷한 방식으로 `.../api/` 주소에서 열리며 XML, JSON, Python 형식을 제공한다.
- REST API는 GET(조회)과 POST(생성, 실행) 같은 메서드를 쓰고, 값은 쿼리, 경로, 헤더 파라미터로 보낸다.
- curl로 `config.xml` 조회, `createItem?name=`으로 잡 생성, `build`와 `buildWithParameters`로 빌드 실행을 할 수 있다.
- 모든 호출에는 `사용자이름:API토큰` 형태의 인증 정보가 필요하다.
- Python-Jenkins를 쓰면 같은 일을 `get_job_config`, `create_job`, `build_job`, `delete_job` 같은 함수로 처리한다.
- 공유 라이브러리는 `vars` 또는 `src` 폴더의 `.groovy` 파일에 `call` 함수를 두고 공통 파이프라인을 담는다.
- Manage Jenkins의 Global Pipeline Libraries에 등록하고 잡에서 `@Library`로 불러 쓴다. 프로젝트마다 다른 값은 인자로 넘긴다.

---

## 2. 문서 목록

- [원격 접근 API 기초](원격 접근 API 기초.md): 원격 API의 형식과 주소, REST 메서드, 파라미터 세 종류, curl 준비
- [curl로 잡 제어하기](curl로 잡 제어하기.md): 설정 조회, 잡 생성, 파라미터 있는 잡과 없는 잡 실행
- [Python-Jenkins로 제어하기](Python-Jenkins로 제어하기.md): 파이썬 래퍼 소개, 설치, 예제 함수와 curl 대응표
- [공유 라이브러리 만들고 쓰기](공유 라이브러리 만들고 쓰기.md): 라이브러리 작성, GitLab 푸시, Jenkins 등록, 잡에서 호출
- [요약과 핵심 개념](요약과 핵심 개념.md): 장 요약, 핵심 개념표, 체크리스트

<br>
<br>
<br>

[CICD Pipeline Using Jenkins Unleashed](../)
