# 플러그인 관리하기

이 장은 젠킨스가 외부 도구와 연결되는 통로인 플러그인을 다룬다. 플러그인이 무엇인지, 자주 쓰는 플러그인은 무엇인지 살피고, Plugin Manager에서 플러그인을 설치하고 갱신하고 지우는 방법을 차례로 정리한다.

프록시 환경에서 쓰는 설정과 특정 버전을 직접 올리는 방법, 그리고 설치 중에 흔히 만나는 오류 두 가지와 해결책도 포함한다. 책의 서술은 당시 젠킨스 화면을 기준으로 하므로 메뉴 이름과 화면은 이후 버전에서 달라졌을 수 있다.

---

## 1. 핵심 요점

- 플러그인은 젠킨스에 기능을 더하는 확장 부품이며, Git, Maven, 메일 알림 같은 외부 도구와의 연결을 맡는다.
- Git, Maven Integration, Email Extension이 대표적으로 쓰는 플러그인이다.
- Manage Jenkins → Manage Plugins로 Plugin Manager에 들어가며 Updates, Available, Installed, Advanced 네 탭이 있다.
- Install Without Restart는 바로 설치하고, Download Now and Install After Restart는 재시작 때 설치한다.
- 플러그인은 Uninstall 버튼이나 .HPI 파일 삭제로 지우고, 체크박스 해제로 비활성화한다.
- 프록시 뒤에서는 Advanced 탭에 Server, Port, Username, Password, No Proxy Host를 설정해야 한다.
- 특정 버전은 .HPI 파일을 내려받아 Upload Plugin으로 설치한다.
- SHA-1 불일치와 SSL 인증서 경로 오류는 동기화, 프록시, URL 변경, Java 조정으로 해결하고, 끝나면 JDK 1.8 또는 1.11로 되돌린다.

---

## 2. 문서 목록

- [플러그인이란과 대표 플러그인](플러그인이란과 대표 플러그인.md): 플러그인의 필요성, 대표 플러그인 세 가지, Plugin Manager 진입 경로
- [Plugin Manager 탭으로 설치와 삭제](Plugin Manager 탭으로 설치와 삭제.md): Updates, Available, Installed 탭, 설치 버튼 비교, 삭제와 비활성화
- [Advanced 탭과 프록시 설정](Advanced 탭과 프록시 설정.md): 프록시 문제, 설정 항목, .HPI 수동 업로드, Update Center URL
- [설치 오류와 해결 방법](설치 오류와 해결 방법.md): SHA-1 불일치와 SSL 인증서 경로 오류의 원인과 해결 순서
- [요약과 핵심 개념](요약과 핵심 개념.md): 장 요약, 개념 표, 작업별 위치와 오류별 대응

<br>
<br>
<br>

[CICD Pipeline Using Jenkins Unleashed](../)
