# 편집기와 IDE 연동

Windows에서 익숙한 IDE나 편집기를 쓰면서도, 프로젝트는 실제 Linux 환경(WSL)에서 빌드하고 디버깅할 수 있다. 이 문서에서는 Visual Studio, Visual Studio Code, JetBrains IDE를 WSL과 연동하는 방법을 정리한다.

---

## 1. Visual Studio

- Visual Studio는 기업에서 사실상 표준으로 쓰는 IDE다. WSL과 연동하면 Linux에 배포할 .NET Core, .NET 5.0 앱을 빌드하고 디버깅할 수 있다.
- **16.8 이하**: 확장 관리에서 ".NET Core Debugging with WSL 2 - Preview" 확장을 내려받아 설치한다. 설치를 마칠 때 UAC 확인 창이 뜬다.
- **16.9 이상**: 이 기능이 기본으로 들어 있으므로 Visual Studio Installer에서 켜기만 하면 된다. ".NET Core cross-platform development" 워크로드에 포함하거나, 개별 구성 요소 탭에서 선택한다.
- **디버깅 조건**: 대상이 .NET Core 또는 .NET 5.0이어야 한다. 새 프로젝트를 만들 때 플랫폼으로 Linux를 고르면 호환되는 프로젝트가 만들어진다.
- 호환 프로젝트에서는 디버그 대상 드롭다운에 "WSL 2"가 나타난다. 이를 선택하면 WSL 환경을 준비한 뒤 디버깅 세션을 시작한다.

---

## 2. Visual Studio Code

- **Remote - WSL 확장**: 편집기가 두 부분으로 나뉘어 동작한다. 사용자 인터페이스는 Windows에서, 개발과 디버깅 도구는 WSL에서 실행된다.
- Code 안에서 연 터미널은 WSL의 실제 Bash 셸이다. 그래서 명령줄에서 할 수 있는 일은 모두 할 수 있다.
- 이런 클라이언트-서버 구조 덕분에, WSL에서 실행 중인 코드(예: .NET 웹 앱)에 Windows의 Code에서 중단점을 걸고 디버깅할 수 있다.

### 설치와 연결 절차

1. `Ctrl+P`로 빠른 열기를 열고 `ext install remote-wsl`을 입력해 확장을 설치한다.
2. `Ctrl+Shift+P`를 누르고 `remote-wsl`을 입력한다.
3. "New Window"(기본 배포판) 또는 "New Window using distro"(배포판 선택)를 고른다.
4. "Open Folder"로 WSL 배포판 안의 폴더를 연다.

---

## 3. JetBrains IDE

- 파일 열기 대화상자에 `\\wsl$`라는 특수 경로가 보인다. 이 경로 아래의 프로젝트를 열거나 새로 만들 수 있다.
- `\\wsl$` 경로의 프로젝트에서는 IDE가 WSL 안의 Git을 자동으로 사용한다.
- 빌드와 디버그를 WSL에서 실행하는 기능은 점점 지원이 늘고 있다. 현재 가장 잘 지원되는 경우는 WebStorm의 NodeJS 프로젝트다.
- **WebStorm 설정**: 새 프로젝트를 만들 때 Node interpreter 드롭다운에서 새 인터프리터를 추가하고, WSL 배포판의 `node` 경로(보통 `/usr/bin/node`)를 지정한다. 이후 평소처럼 실행하거나 디버그하면 WSL 안에서 실행된다.
- 간단한 예제를 실행했을 때 출력에 "linux"가 나오면 WSL에서 실행되고 있다는 뜻이다.

---

## 4. 방식 비교

| 도구 | 연동 방식 |
|---|---|
| Visual Studio | .NET Core Debugging with WSL 2 기능, 디버그 대상에서 WSL 2 선택 |
| VS Code | Remote - WSL 확장, UI는 Windows / 도구는 WSL |
| JetBrains | `\\wsl$` 경로로 프로젝트 열기, WebStorm은 WSL의 node 지정 |

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
