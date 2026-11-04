# 2부 개요 (Part II) 보안과 사용자

프라노데이 프라모드 딩가레(Pranoday Pramod Dingare)의 『CI/CD Pipeline Using Jenkins Unleashed』(Apress, 2022)는 Jenkins로 CI/CD 파이프라인을 구축하는 입문서다. 2부는 7장부터 9장까지 세 개 장으로, Jenkins를 여러 사람이 안전하게 쓰기 위한 세 축을 다룬다. 로그인과 권한의 큰 틀(보안), 외부 도구에 접속할 때 쓰는 비밀 정보 보관(자격 증명), 팀원별 권한 배정(사용자 관리)이다.

이 노트는 번역이 아니라 책의 내용을 풀어 다시 정리한 학습 노트다. 책의 화면과 메뉴는 2021년경 Jenkins 기준이므로 최신 버전과 다를 수 있다. 보안 장이어서 실제 계정 값이나 비밀번호는 이 노트에 적지 않고 자리표시자로 대신했다.

> **이 부를 한 문장으로**
> 누가 Jenkins에 들어올 수 있는지(인증), 들어와서 무엇을 할 수 있는지(인가), 외부 도구에 접속할 비밀 정보를 어떻게 숨겨 두는지를 한꺼번에 정리하는 부분이다.

---

## 0. 먼저 알아 둘 것

- **인증(authentication)과 인가(authorization)**: 인증은 로그인 가능한 사용자인지 확인하는 것, 인가는 사용자 종류별로 허용 범위를 나누는 것이다.
- **관리자 화면 경로**: 대부분의 설정이 `Manage Jenkins` 아래에 있다. `Configure Global Security`, `Manage Users`, `Manage Credentials` 등이 2부의 주요 진입점이다.
- **플러그인**: LDAP 연동과 역할 기반 권한 관리는 별도 플러그인을 설치해야 쓸 수 있다.

## 1. 읽는 순서

| 순서 | 문서 | 이런 질문에 답한다 |
|:---:|------|------------------|
| 1 | [7장 보안 관리](07%EC%9E%A5%20%EB%B3%B4%EC%95%88%20%EA%B4%80%EB%A6%AC.md) | 로그인과 권한의 기본 설정은 어디에 있고 무엇을 고르나? |
| 2 | [8장 자격 증명 관리](08%EC%9E%A5%20%EC%9E%90%EA%B2%A9%20%EC%A6%9D%EB%AA%85%20%EA%B4%80%EB%A6%AC.md) | Git이나 Nexus 접속용 계정과 키를 어떻게 안전하게 쓰나? |
| 3 | [9장 사용자 관리](09%EC%9E%A5%20%EC%82%AC%EC%9A%A9%EC%9E%90%20%EA%B4%80%EB%A6%AC.md) | 팀원마다 다른 권한을 어떻게 주나? |
| 4 | [핵심 정리](%ED%95%B5%EC%8B%AC%20%EC%A0%95%EB%A6%AC.md) | 2부를 빠르게 복습하려면? |

- **7장 보안 관리**: Security Realm, Authorization 옵션, 에이전트·SSH 포트, CSRF crumb, API 토큰, LDAP 연동
- **8장 자격 증명 관리**: 자격 증명의 종류, Scope(Global, System), Domain, Credentials Provider, Types
- **9장 사용자 관리**: 사용자 생성, 역할 기반 권한, Matrix 기반 권한, 프로젝트 기반 Matrix

## 2. 용어

| 용어 | 쉬운 설명 |
|------|-----------|
| Security Realm | 로그인 정보를 어디서 확인할지 정하는 설정(자체 DB, LDAP 등) |
| Authorization | 로그인한 사용자가 할 수 있는 일을 정하는 설정 |
| LDAP | 조직의 사용자 정보를 한곳에 모아 둔 디렉터리 프로토콜 |
| crumb | CSRF 공격을 막기 위해 요청에 붙이는 사용자별 토큰 |
| Credentials ID | 저장한 자격 증명 항목을 작업에서 부르는 고유 이름 |
| Scope | 자격 증명을 쓸 수 있는 범위(Global, System) |
| Domain | 자격 증명 항목을 대상별로 묶고 걸러 주는 그룹 |
| Global/Item Role | 역할 기반 권한에서 전체 권한용 역할과 작업 이름 패턴용 역할 |
| Matrix 권한 | 사용자와 권한을 표로 놓고 체크해 부여하는 방식 |

## 3. 이 부의 흐름

1. 7장은 Jenkins 전체의 출입 규칙(인증과 인가의 기본값)을 정한다.
2. 8장은 Jenkins가 외부 도구에 접속할 때 쓰는 비밀 정보를 금고처럼 보관하는 법을 다룬다.
3. 9장은 사용자별로 권한을 나누는 구체적 방법(역할, Matrix, 프로젝트 기반 Matrix)을 보여 준다.

<br>
<br>
<br>

[CICD Pipeline Using Jenkins Unleashed](../)
