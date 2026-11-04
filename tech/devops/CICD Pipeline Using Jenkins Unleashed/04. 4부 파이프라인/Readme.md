# 4부 개요 (Part IV)

프라노데이 딩가레(Pranoday Pramod Dingare)의 『CI/CD Pipeline Using Jenkins Unleashed』(Apress, 2022) 4부는 14장부터 16장까지 세 개 장으로, 화면 클릭으로 만들던 프리스타일 잡에서 코드로 적는 파이프라인으로 넘어가는 과정을 다룬다. 14장은 파이프라인의 기본 개념과 문법을, 15장은 웹 애플리케이션을 배포하고 UI 테스트까지 돌리는 매개변수 잡과 파이프라인을, 16장은 Jenkinsfile과 웹훅을 이용한 Pipeline as Code를 설명한다.

이 노트는 번역이 아니라 책의 내용을 이해한 뒤 자기 말로 다시 정리한 학습 노트다. 책의 화면은 2021년경 Jenkins 기준이므로 최신 버전의 메뉴 이름은 다를 수 있다.

> **이 부를 한 문장으로**
> 빌드 절차를 클릭 설정에서 코드로 옮기고, 그 코드를 소스 저장소에 함께 두어 저장소의 푸시 이벤트가 곧바로 빌드를 일으키게 만드는 이야기다.

---

## 0. 먼저 알아 둘 것

- **프리스타일 잡(Freestyle job)**: 화면의 설정 항목을 채워 만드는 Jenkins의 기본 잡. 앞부분 장에서 이미 다뤘다.
- **Git과 저장소**: `git add`, `commit`, `push` 같은 기본 명령과 GitLab, GitHub 같은 원격 저장소 사용법을 알고 있으면 읽기 쉽다.
- **Maven 빌드 생명주기**: 컴파일, 테스트, 패키징, `deploy`로 이어지는 단계를 알면 14장의 예제가 이해된다.
- **Groovy**: 파이프라인 스크립트의 바탕 언어다. 깊은 지식은 필요 없지만 중괄호 블록과 문자열 따옴표 규칙 정도는 눈에 익혀 두자.

## 1. 읽는 순서

| 순서 | 문서 | 이런 질문에 답한다 |
|:---:|------|------------------|
| 1 | [14장 Jenkins 파이프라인 이해](14%EC%9E%A5%20Jenkins%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%20%EC%9D%B4%ED%95%B4.md) | 파이프라인이란 무엇이고 선언형과 스크립트형은 어떻게 다른가? |
| 2 | [15장 웹 애플리케이션 프로젝트 잡](15%EC%9E%A5%20%EC%9B%B9%20%EC%95%A0%ED%94%8C%EB%A6%AC%EC%BC%80%EC%9D%B4%EC%85%98%20%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%20%EC%9E%A1.md) | 배포와 UI 테스트를 두 잡으로 나누고 매개변수로 잇는 방법은? |
| 3 | [16장 Pipeline as Code](16%EC%9E%A5%20Pipeline%20as%20Code.md) | Jenkinsfile과 웹훅은 무엇이 좋고 어떻게 설정하나? |
| 4 | [핵심 정리](%ED%95%B5%EC%8B%AC%20%EC%A0%95%EB%A6%AC.md) | 4부 전체를 빠르게 복습하려면? |

- **14장**: 파이프라인의 장점, 네 가지 개념, 두 가지 문법, `Snippet Generator`, CalculatorAPI 배포
- **15장**: 계산기 웹 앱, Selenium UI 테스트, 상위·하위 매개변수 잡, 확장 이메일, 파이프라인 버전
- **16장**: API 토큰 인증, Jenkinsfile, `post` 블록, `Pipeline script from SCM`, GitLab·GitHub 웹훅

## 2. 4부에 자주 나오는 용어

| 용어 | 쉬운 설명 |
|------|-----------|
| Pipeline | 빌드, 테스트, 배포 전 과정을 정의한 코드 |
| Node | 파이프라인을 실행할 수 있는 머신. 스크립트형에서는 최상위 블록 이름이기도 하다 |
| Stage / Step | 단계(빌드, 테스트 등)와 그 안의 낱개 작업 |
| Declarative / Scripted | 틀이 정해진 `pipeline` 블록 문법과, `node` 블록의 자유로운 Groovy 문법 |
| Snippet Generator | 화면 입력으로 step 코드를 만들어 주는 도구 |
| Upstream / Downstream | 먼저 실행되어 다른 잡을 호출하는 잡과, 호출을 받는 잡 |
| Selenium WebDriver | 브라우저 화면을 자동으로 조작하는 오픈소스 UI 테스트 도구 |
| API access token | 비밀번호 대신 저장소 접근에 쓰는 비밀 문자열 |
| Jenkinsfile | 저장소에 함께 두는 파이프라인 스크립트 파일 |
| Webhook | 저장소의 이벤트가 URL로 POST 요청을 보내 Jenkins를 깨우는 설정 |

## 3. 이 부의 흐름

프리스타일 잡에서 파이프라인으로, 다시 Pipeline as Code로 이어지는 세 걸음이다.

| 단계 | 장 | 빌드 절차가 사는 곳 | 시작시키는 방법 |
|------|----|--------------------|-----------------|
| 프리스타일 잡 | 앞 장들 | Jenkins 화면의 설정 | 수동, 주기, SCM 폴링 |
| 화면의 파이프라인 | 14장, 15장 | Jenkins 화면의 코드 편집기 | 수동, SCM 폴링, 상위 잡 호출 |
| Pipeline as Code | 16장 | 저장소 안의 Jenkinsfile | 웹훅의 푸시 이벤트 |

<br>
<br>
<br>

[CICD Pipeline Using Jenkins Unleashed](../)
