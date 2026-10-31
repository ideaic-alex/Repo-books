# WSL API와 DistroLauncher

배포판을 설치할 때 내부에서 어떤 일이 일어나는지는 Microsoft의 WSL-DistroLauncher 템플릿을 보면 알 수 있다. 이 문서는 런처의 구성과 실행 흐름, 그리고 공식 문서가 없는 WSL API 함수를 정리한다.

---

## 1. DistroLauncher 구성

- 전통적인 Win32 C++ 앱인 `launcher.exe`에 스토어용 리소스(에셋)와 rootfs tarball을 함께 담아 UWP 패키지로 만든 것이다.
- 이 코드가 Windows 10의 WSL API를 호출해서 설치 상태 확인, 설치, 배포판 등록을 처리한다.
- 핵심 코드는 `DistroLauncher/DistroLauncher.cpp`에 있다.

---

## 2. 실행 흐름

1. WSL 선택 구성요소가 설치돼 있는지 확인한다. 설치돼 있지 않으면 안내 메시지를 출력한다.
2. 배포판이 등록돼 있는지 확인한다. 등록돼 있지 않으면 설치한다. 이때 `--root` 옵션을 주면 사용자 계정을 만들지 않는다.
3. 설치 결과에 따라 "이미 설치돼 있다"는 메시지나 성공 메시지를 출력하고, 종료 코드를 정한다.

---

## 3. 사용자 생성

- 사용자 생성과 sudo 권한 추가는 `DistroLauncher/DistributionInfo.cpp`에서 처리한다. 이 코드는 배포판 안에서 명령을 직접 실행한다.
- 먼저 `adduser`로 계정을 만든다. 이어서 `usermod -aG`로 그 계정을 `adm`, `cdrom`, `sudo`, `dip`, `plugdev` 그룹에 추가한다.
- 그룹 추가에 실패하면 방금 만든 사용자를 `deluser`로 지우고 실패를 반환한다.

---

## 4. WSL API 함수

- `wslapi.dll`이 제공하는 함수는 `DistroLauncher/WslApiLoader.cpp`에 나와 있다.

| 함수 | 역할(함수명에서 드러나는 범위) |
|---|---|
| `WslIsOptionalComponentInstalled()` | WSL 구성요소 설치 여부 |
| `WslIsDistributionRegistered()` | 배포판 등록 여부 |
| `WslRegisterDistribution()` | 배포판 등록 |
| `WslConfigureDistribution()` | 배포판 설정 |
| `WslLaunchInteractive()` | 대화형 명령 실행 |
| `WslLaunch()` | 명령 실행 |

- 이 API는 별도의 공식 문서가 없다. 그래도 Docker Desktop과 Raft WSL 같은 서드파티 프로젝트가 이 API를 쓰고 있고, 커뮤니티에서는 이 API로 WSL 위에서 동작하는 자체 런처를 만든다.

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
