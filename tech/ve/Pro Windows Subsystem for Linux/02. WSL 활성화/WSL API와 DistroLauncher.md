# WSL API와 DistroLauncher

배포판 설치 때 내부에서 무슨 일이 일어나는지는 Microsoft의 WSL-DistroLauncher 템플릿을 보면 알 수 있다. 이 문서는 런처의 구성과 흐름, 그리고 문서화되지 않은 WSL API 함수를 정리한다.

---

## 1. DistroLauncher 구성

- 고전적인 Win32 C++ 앱인 `launcher.exe`에 스토어 에셋과 rootfs tarball을 묶어 UWP 패키지로 만든 것이다.
- 이 코드가 Windows 10의 WSL API를 호출해 설치 상태 확인, 설치, 배포판 등록을 수행한다.
- 주 코드는 `DistroLauncher/DistroLauncher.cpp`에 있다.

---

## 2. 실행 흐름

1. WSL 선택 구성요소가 설치돼 있는지 확인하고, 없으면 안내 메시지를 출력한다.
2. 배포판이 등록돼 있는지 확인하고, 없으면 설치한다. `--root` 옵션이 주어지면 사용자 계정을 만들지 않는다.
3. 설치 결과에 따라 이미 존재한다는 메시지 또는 성공 메시지를 출력하고, 종료 코드를 정한다.

---

## 3. 사용자 생성

- 사용자 생성과 sudo 추가는 `DistroLauncher/DistributionInfo.cpp`에서 처리하며, 배포판 안에서 명령을 직접 실행한다.
- 먼저 `adduser`로 계정을 만들고, 이어서 `usermod -aG`로 `adm`, `cdrom`, `sudo`, `dip`, `plugdev` 그룹에 추가한다.
- 그룹 추가가 실패하면 만든 사용자를 `deluser`로 지우고 실패를 반환한다.

---

## 4. WSL API 함수

- `wslapi.dll`이 제공하는 함수는 `DistroLauncher/WslApiLoader.cpp`에 나온다.

| 함수 | 역할(함수명에서 드러나는 범위) |
|---|---|
| `WslIsOptionalComponentInstalled()` | WSL 구성요소 설치 여부 |
| `WslIsDistributionRegistered()` | 배포판 등록 여부 |
| `WslRegisterDistribution()` | 배포판 등록 |
| `WslConfigureDistribution()` | 배포판 설정 |
| `WslLaunchInteractive()` | 대화형 명령 실행 |
| `WslLaunch()` | 명령 실행 |

- 이 API는 별도로 문서화돼 있지 않다. 그럼에도 Docker Desktop과 Raft WSL 같은 서드파티 프로젝트가 사용하고, 커뮤니티는 이를 이용해 WSL 위에 사용자 정의 런처를 만든다.

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
