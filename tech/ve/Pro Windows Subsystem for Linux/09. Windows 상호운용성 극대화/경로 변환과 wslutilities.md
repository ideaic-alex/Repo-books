# 경로 변환과 wslutilities

WSL과 Windows를 오가며 작업하다 보면 경로 표기와 환경 정보를 맞춰야 하는 일이 잦다. WSL에 내장된 `wslpath`와, 여러 배포판이 기본 포함하는 `wslutilities` 도구 모음은 이 번거로움을 줄여 준다.

---

## 1. wslpath: 경로 상호 변환

- **wslpath**: WSL에 내장된 경로 변환 도구로, Windows 경로와 WSL 경로를 서로 바꿔 준다.
- 기본 방향은 Windows에서 WSL로 변환이며, `-w` 옵션을 쓰면 반대로 WSL 경로를 Windows 경로로 바꾼다.
- 스크립트에서 `\`와 `/`를 `sed`나 `grep`으로 직접 치환하며 이스케이프하는 수고를 덜 수 있다.
- 뒤에서 다룰 `WSLENV`와 함께 쓰면 더 유용하다.

```bash
wslpath 'C:\Users\Hayden'          # /mnt/c/Users/Hayden
wslpath -w /mnt/c/Users/Hayden     # C:\Users\Hayden
```

---

## 2. wslutilities 개요

- **wslutilities**: Patrick Wu가 만든 도구 모음으로, Microsoft Store의 여러 배포판이 채택했다.
- Ubuntu와 Pengwin은 기본 포함하고, SUSE, Alpine, Debian, CentOS, openSUSE 등에도 제공된다.

---

## 3. 도구별 역할

- **wslusc**: Linux 애플리케이션의 바로가기를 Windows 바탕화면에 만든다. GUI 앱이면 `-g`, 이름은 `-n`, 아이콘은 `-i`로 지정하고 마지막에 실행 명령을 붙인다. 단, 공식 GUI 앱 지원이 들어오기 전까지는 Windows 쪽에 X 서버가 떠 있어야 한다.
- **wslsys**: 기본적인 시스템 정보를 보여 준다. WSL 관련 버그를 신고할 때 유용하다. 출력을 `grep`/`sed`로 걸러 Windows 테마(light/dark) 같은 값을 스크립트에서 쓸 수도 있다.
- **wslfetch**: `neofetch` 같은 정보 화면에 Windows 10 빌드 번호 등 호스트 정보를 더해 보여 준다.
- **wslvar**: `%APPDATA%`, `%USERPROFILE%` 같은 Windows 환경 변수 값을 가져온다.
- **wslview**: WSL 안에서 기본 웹 브라우저 역할을 하며, URL을 Windows의 기본 브라우저로 연다. URL뿐 아니라 파일도 Windows에서 지정된 기본 앱으로 연다(예: `.txt`는 메모장).

---

## 4. wslpath와 wslvar 조합

- 공유할 스크립트에서 `/mnt/c/Users/<이름>`처럼 사용자명을 하드코딩하면 다른 사람 환경에서 깨진다.
- `wslvar`로 Windows 변수를 읽고 `wslpath`로 변환하면 사용자와 무관하게 동작하는 경로를 얻는다.

```bash
cp hello $(wslpath $(wslvar USERPROFILE))
wslview https://example.com
wslview textfile.txt
```

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
