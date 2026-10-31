# WSL 2 커널 관리

WSL 2는 실제 리눅스 커널 위에서 동작한다. 이 커널은 배포판 이미지에 들어 있는 커널과 따로 배포된다. 이 문서는 커널을 갱신하고, 상태를 확인하고, 이전 버전으로 되돌리는 방법을 정리한다.

---

## 1. 커널의 위치와 설정

- **ABI 호환**: WSL 2는 리눅스 커널을 그대로 쓰므로 애플리케이션 바이너리 인터페이스(ABI) 호환성을 완전하게 제공한다.
- **별도 배포**: 배포판 안에서 커널 패키지를 바꿔도 WSL이 부팅에 쓰는 커널은 바뀌지 않는다.
- **커널 교체와 커널 명령줄 옵션**: Windows 사용자 디렉터리(`%USERPROFILE%`)에 있는 `.wslconfig` 파일에서 설정한다.
- **관련 내용**: `.wslconfig`의 다른 설정은 WSL 2 설정 부분에서 다룬다. 커널을 직접 빌드하는 방법은 WSL 커스터마이징 장에서 다룬다.

---

## 2. Windows Update로 갱신하기

- **표준 커널**: 기본으로 제공되는 커널은 Windows Update로 갱신된다.
- **필수 설정**: Windows Update 고급 옵션에서 "Windows 업데이트 시 다른 Microsoft 제품의 업데이트 받기"를 켜 둬야 커널 업데이트를 함께 받는다.

---

## 3. 업데이트 확인과 상태 점검

- **업데이트 확인**: `wsl.exe --update`를 실행한다. 새 커널이 없으면 현재 커널 버전이 표시된다.
- **권한 오류**: "requested operation requires elevation" 메시지가 나오면 관리자 권한으로 연 PowerShell에서 실행해야 한다. 이미 열려 있는 PowerShell에서 관리자 터미널을 여는 명령은 아래와 같다.
- **직접 지정한 커널을 쓰는 경우**: 위 방법으로 갱신해도 `.wslconfig`에 지정해 둔 커널은 바뀌지 않는다.
- **상태 확인**: 마지막 업데이트 날짜, 자동 업데이트 여부, 현재 버전을 볼 수 있다.

```powershell
Start-Process WT -Verb runAs
wsl.exe --update
wsl.exe --update --status
```

---

## 4. 업데이트 롤백

- **용도**: 새 커널에 문제가 생겼을 때 바로 이전의 정상 커널로 되돌리는 내장 기능이다.
- **조건**: 관리자 권한 PowerShell에서 실행한다.

```powershell
wsl.exe --update --rollback
```

---

## 5. 정리

| 작업 | 명령 |
|------|------|
| 업데이트 확인 | `wsl.exe --update` |
| 상태 확인 | `wsl.exe --update --status` |
| 롤백 | `wsl.exe --update --rollback` |
| 관리자 터미널 열기 | `Start-Process WT -Verb runAs` |

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
