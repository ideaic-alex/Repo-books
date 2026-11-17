# 사례 연구 간단한 작업 관리자 만들기

이 장은 지금까지의 방법을 Task Manager라는 작은 예제로 처음부터 끝까지 따라가는 실습 장이다. Spring Boot, Vaadin, jOOQ, PostgreSQL, Testcontainers 스택에서 AI 통합 프로세스(AIUP)와 Claude Code를 쓰고, 열 단계를 Git 태그로 하나씩 확인한다. 비전, 요구사항, 엔터티 모델, 유스케이스 다이어그램을 문서로 쌓고, 뼈대와 DB 마이그레이션을 만든 뒤, 첫 유스케이스 UC-006의 스펙과 구현, 그리고 두 종류의 테스트를 같은 스펙에서 파생한다.

마지막으로 스펙을 먼저 바꾸고 나머지를 동기화하는 반복 절차를 우선순위 열 추가 예로 본다. 예제의 값(태그, 파일명, 명령)은 원서를 따랐고, 추출이 깨진 곳은 각 문서에서 밝혔다.

---

## 1. 핵심 요점

- 필요한 것은 Java 25 이상과 Docker이며, `./mvnw spring-boot:test-run`으로 실행을 확인한다. Docker가 꺼져 있으면 연결 오류가 난다.
- 열 단계는 Git 태그(init, requirements, entity_model, use_cases_diagram, scaffolding, database_migration, spec_UC-006, implement_UC-006, test_UC-006, e2e_UC-006)로 대응한다.
- `/docs`(vision, requirements, entity-model, use-cases)가 시스템 행동의 권위 있는 출처다.
- 비전은 손으로 쓰고, 요구사항, 엔터티 모델, 다이어그램은 슬래시 명령이 초안을 제안하며 사람이 검토한다.
- 스캐폴딩은 스택 의존적이라 전용 명령이 없고, 마이그레이션은 엔터티 모델에서 파생한다.
- UC-006 View Team Tasks 스펙에서 `/implement`, `/browserless-test`, `/playwright-test`가 구현과 두 테스트를 만든다.
- 변경은 스펙 갱신, 마이그레이션, 구현 재실행, 테스트 재실행 순서이고 버그도 스펙 확인부터 시작한다.

---

## 2. 문서 목록

- [프로젝트 준비와 도구](프로젝트 준비와 도구.md): 기술 스택, 로컬 환경, 열 단계와 태그, 도구에 대한 입장, 저장소 구조
- [1~4단계 비전, 요구사항, 엔터티 모델, 유스케이스 다이어그램](1~4단계 비전, 요구사항, 엔터티 모델, 유스케이스 다이어그램.md): /docs 문서 네 개를 쌓는 단계
- [5~6단계 스캐폴딩과 DB 마이그레이션](5~6단계 스캐폴딩과 DB 마이그레이션.md): 뼈대 만들기와 Flyway 마이그레이션, task 테이블 발췌
- [7~8단계 첫 유스케이스 스펙과 구현](7~8단계 첫 유스케이스 스펙과 구현.md): UC-006 스펙 구조와 스펙에서 코드로의 생성
- [9~10단계와 반복 UI 단위 테스트, E2E 테스트, 스펙 먼저 바꾸고 동기화](9~10단계와 반복 UI 단위 테스트, E2E 테스트, 스펙 먼저 바꾸고 동기화.md): 브라우저리스와 Playwright 테스트, 반복 절차
- [요약과 핵심 개념](요약과 핵심 개념.md): 장 전체 흐름, 핵심 개념 표, 자주 놓치는 점

<br>
<br>
<br>

[Spec-Driven Development From Specs to Code with AI Agents](../)
