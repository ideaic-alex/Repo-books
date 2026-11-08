# 젠킨스 보안 관리

이 장은 Jenkins의 인증과 권한 부여 설정을 다룬다. Configure Global Security 화면에서 로그인 방식, 사용자 출처, 익명 사용자의 접근 범위, 에이전트와 SSH 포트, CSRF 보호, API 토큰을 어떻게 정하는지 하나씩 살펴보고, 회사 계정을 쓰려면 LDAP를 어떻게 연동하는지도 정리한다.

인증은 정상 사용자만 로그인하게 하는 일이고, 권한 부여는 사용자 종류별로 허용 범위를 나누는 일이다. 이 노트는 책의 서술 시점을 따르므로 Jenkins 화면과 메뉴 이름은 이후 버전에서 바뀌었을 수 있다.

---

## 1. 핵심 요점

- 모든 보안 설정은 대시보드의 Configure Global Security 화면에서 한다.
- Security Realm은 사용자 출처를 고른다. 서블릿 컨테이너, Jenkins 자체 데이터베이스, LDAP, None이 있다.
- Allow users to sign up은 누구나 계정을 만들 수 있게 하므로 켜지 않는 것이 좋다.
- Authorization에서 Anyone can do anything과 Legacy mode는 권장하지 않으며, Logged-in users can do anything은 익명 사용자를 읽기 전용으로 묶는다.
- 에이전트 포트와 SSH 서버 포트는 방화벽이 있으면 Fixed, 쓰지 않으면 Disable로 둔다.
- CSRF 보호는 사용자 정보로 만든 crumb 토큰이 없는 변경 요청을 막는다.
- Legacy API 토큰 옵션은 Jenkins 2.129 이상에서 deprecated이며 새 API 토큰을 권한다.
- LDAP는 회사 계정으로 Jenkins에 로그인하게 해 주며, LDAP 플러그인을 설치한 뒤 Security Realm에서 선택한다.

---

## 2. 문서 목록

- [보안 설정 화면과 인증](보안 설정 화면과 인증.md): 설정 화면 위치, Security Realm 선택지, 사용자 만들기, 익명 접근 설정
- [권한 부여 설정](권한 부여 설정.md): Authorization 선택지 비교와 익명 읽기 접근
- [에이전트 포트와 CSRF와 API 토큰](에이전트 포트와 CSRF와 API 토큰.md): 에이전트 포트, CSRF crumb, API 토큰, SSH 서버
- [LDAP 연동](LDAP 연동.md): LDAP 개념, 연동이 필요한 사례, 플러그인 설치와 설정
- [요약과 핵심 개념](요약과 핵심 개념.md): 설정 항목 한눈에 보기와 핵심 개념

<br>
<br>
<br>

[CICD Pipeline Using Jenkins Unleashed](../)
