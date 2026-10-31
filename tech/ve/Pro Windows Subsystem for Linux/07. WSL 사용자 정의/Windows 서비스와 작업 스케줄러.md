# Windows 서비스와 작업 스케줄러

터미널이나 IDE를 열지 않아도 Windows에 로그인하면 리눅스 서비스가 시작되게 하려면 Windows 쪽 자동화 도구가 필요하다. 이 문서는 Windows 서비스로 등록하는 방법과, 더 간단한 작업 스케줄러(Task Scheduler) 방법을 정리한다.

---

## 1. Windows 서비스로 등록 (Apache 예시)

먼저 배포판 안에 시작 스크립트를 만든다. 그다음 Windows 배치 파일이 `wsl.exe`로 그 스크립트를 호출하게 하고, 이 배치 파일을 서비스로 등록한다.

1. Apache를 설치하고 `/opt/runapache.sh`를 작성한다. 이 스크립트는 `pgrep`으로 Apache가 실행 중인지 확인하고, 실행 중이 아니면 `/etc/init.d/apache2 start`를 호출한다.
2. 스크립트에 실행 권한을 주고, 소유자를 주 사용자로 바꾼다(`chmod`, `chown`).
3. Windows 홈 폴더에 배치 파일을 만들어 `wsl.exe /opt/runapache.sh`를 호출하게 한다. 홈 경로는 `wslvar USERPROFILE`과 `wslpath`로 구한다.
4. 관리자 권한으로 연 PowerShell에서 `sc create`를 실행해, 자동으로 시작되는 서비스로 등록한다. `=` 뒤에는 반드시 공백이 있어야 한다.
5. 등록하고 나면 Windows 서비스 창에서 시작과 중지를 제어할 수 있다.

```
sc create 'Apache in WSL' binpath= C:\Users\Hayden\runapache.bat type= share start= auto displayname= 'Apache in WSL'
```

---

## 2. wsl.exe 호출 시 유의점

- **기본 배포판**: 옵션 없이 `wsl.exe`를 실행하면 `--setdefault`로 지정한 기본 배포판을 쓴다.
- **다른 배포판 지정**: 그 배포판의 `.exe` 별칭을 쓰거나, `-d`로 배포판 이름을 지정한다.
- **다른 사용자로 실행**: `-u`로 사용자를 지정한다. 단, 명령에 `sudo`가 들어 있으면 그 사용자의 `sudoers`에도 예외를 추가해야 한다.
- **root 사용은 피한다**: `-u root`를 쓰면 `sudoers`를 고치지 않아도 되지만, 웹에서 접근할 수 있는 네트워크 서비스를 root로 돌리는 것은 좋지 않다.
- **동작 확인**: `wsl.exe --exec ps -A`로 프로세스를 확인하고, 배치 파일을 직접 실행해 본다. 바로 다시 실행해도 이미 돌고 있음을 알아채고 두 번째 인스턴스를 띄우지 않는다. 브라우저에서 `localhost`로 접속해 기본 페이지가 뜨는지도 확인한다.

---

## 3. 작업 스케줄러 (Task Scheduler)

스크립트와 배치 파일을 직접 만드는 것이 부담스럽다면 GUI로 작업을 만드는 편이 쉽다. 책에서는 Ubuntu 자동 업그레이드를 예로 든다.

1. "Create Basic Task"에서 작업 이름을 정한다.
2. 트리거는 매일, 시각은 새벽 1시로 둔다.
3. 동작은 "Start a program"으로 하고, 프로그램에 `wsl.exe`를, 인수에 `-u root -e apt update`를 입력한다.
4. 마침 화면에서 속성 대화상자 열기를 체크한다. "Actions" 탭에서 새 동작을 추가하고, 인수에 `-u root -e apt -y upgrade`를 입력한다.
5. 실행 순서는 패키지 목록을 먼저 갱신한 뒤 업그레이드를 적용하는 것이다. 완료하면 Active Tasks에서 작업을 확인하고, "Run"으로 테스트한다.

- 이 작업은 기본 배포판에서 실행된다. 특정 배포판에서 돌리려면 `-d`로 배포판을 지정한다.

---

## 4. 방법별 선택 기준

| 방법 | 시작 시점 | 특징 |
| --- | --- | --- |
| `.bashrc`, `/etc/profile.d/` | 터미널 열 때 | 가장 간단, 환경 변수에 적합 |
| `[boot]` 명령 | 터미널로 배포판 열 때 | 빌드 21286 이상, root 실행 |
| Windows 서비스 | Windows 부팅 시 | 백그라운드 자동 시작, 스크립트와 배치 파일 필요 |
| 작업 스케줄러 | 예약 시각 | GUI로 쉽게 설정, 주기 작업에 적합 |

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
