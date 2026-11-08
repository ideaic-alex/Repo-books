# 웹 애플리케이션 프로젝트를 위한 젠킨스 잡 만들기

이 장은 HTML 파일 하나로 된 계산기 웹 애플리케이션을 대상으로 젠킨스 잡을 만든다. 저장소에서 코드를 받아 IIS 웹 서버에 배포하고, Selenium과 Python으로 만든 UI 자동화 테스트를 돌린 뒤, 결과 보고서를 이메일로 받는 전 과정을 다룬다. 같은 흐름을 프리스타일 잡과 파이프라인 잡으로 각각 구현한다.

두 잡이 서로를 부르는 업스트림, 다운스트림 구조와 파라미터 전달이 이 장의 중심이다. 예제의 경로, 포트, 저장소 이름은 저자의 환경이라 독자의 환경에 맞게 바꿔야 한다.

---

## 1. 핵심 요점

- 계산기 앱은 HTML, CSS, JavaScript가 한 파일에 든 단순한 앱이라서 컴파일이나 패키징 없이 파일 복사만으로 배포된다.
- 배포 위치는 IIS 별칭 `CalculatorWebApp`이 가리키는 폴더이고, 저자의 접속 주소는 `http://localhost:8082/CalculatorWebApp/Calculator.html`이다.
- UI 자동화 테스트는 Selenium WebDriver, Python, pytest, pytest-html로 만들며, 프로젝트 전용 가상 환경(virtualenv)에서 실행한다.
- 테스트는 RegressionTest, SmokeTest 같은 그룹으로 묶여 있어 `pytest -m`으로 골라 돌릴 수 있다.
- 이번 장은 GitLab 대신 GitHub 비공개 저장소를 쓰며 SSH 키로 연결한다. 푸시할 때 Permission denied가 나면 `.gitconfig`의 sshCommand 줄을 확인한다.
- Parameterized Trigger 플러그인으로 업스트림 잡이 `TestType` 값을 다운스트림 잡에 넘긴다. 보내는 이름과 받는 이름이 같아야 한다.
- Email Extension 플러그인으로 사용자 지정 본문과 `**/${TestType}Result.html` 같은 첨부 파일을 보낸다. 전역에는 공통 설정만 둔다.
- 파이프라인에서는 `build job:` 스텝, `params.이름`, `try`/`finally`, `emailext` 스텝으로 같은 흐름을 구현한다.

---

## 2. 문서 목록

- [계산기 웹 앱과 IIS 배포](계산기 웹 앱과 IIS 배포.md): 앱 구조, 자바스크립트 함수, 빌드가 필요 없는 이유, IIS 별칭과 접속 주소
- [셀레니움 UI 자동화 테스트](셀레니움 UI 자동화 테스트.md): E-E 테스트 개념, 테스트 프로젝트 구조, 필요한 소프트웨어, 가상 환경과 pytest 실행
- [GitHub 저장소와 SSH 연결](GitHub 저장소와 SSH 연결.md): 비공개 저장소 만들기, SSH 키 등록, 커밋과 푸시, 오류 해결
- [파라미터 프리스타일 잡 두 개 연결](파라미터 프리스타일 잡 두 개 연결.md): 업스트림과 다운스트림 잡, 파라미터, 폴링, 수동과 자동 실행
- [확장 이메일 알림 설정](확장 이메일 알림 설정.md): Email Extension 전역 설정, 잡별 알림, 첨부 패턴, 발송 조건
- [파이프라인 잡으로 다시 만들기](파이프라인 잡으로 다시 만들기.md): 세 스테이지 스크립트, try/finally, 문자열 변수 규칙, 비교
- [요약과 핵심 개념](요약과 핵심 개념.md): 장 전체 흐름, 개념과 규칙 정리

<br>
<br>
<br>

[CICD Pipeline Using Jenkins Unleashed](../)
