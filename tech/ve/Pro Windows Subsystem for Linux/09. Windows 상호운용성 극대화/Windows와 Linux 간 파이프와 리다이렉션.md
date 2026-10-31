# Windows와 Linux 간 파이프와 리다이렉션

셸의 파이프, 파일 리다이렉션, 히어독은 명령을 이어 붙여 복잡한 작업을 짧게 처리하는 도구다. WSL에서는 이 흐름이 Windows와 Linux의 경계를 넘나들 수 있어서, 하나의 파이프라인에서 두 환경을 여러 번 오갈 수도 있다.

---

## 1. 파이프(piping)의 기본

- **파이프(pipe)**: `|` 기호로 앞 명령의 출력을 뒤 명령의 입력으로 넘긴다. 별도 프로그램을 작성하지 않아도 명령을 이어 붙일 수 있다.
- 예를 들어 압축(`gzip`), 텍스트 인코딩(`base64`), PGP 서명(`gpg --clear-sign`)을 파이프 두 번으로 연결할 수 있다.
- 기본 GPG 키가 없으면 `gpg --full-gen-key`로 만든다. "Inappropriate ioctl for device" 오류가 나면 `export GPG_TTY=$(tty)`를 설정한다.

---

## 2. WSL에서 Windows로

- **clip.exe**: WSL의 출력을 Windows 클립보드로 보낸다. Windows의 PATH가 WSL로 전달되므로 `.exe` 파일을 바로 실행할 수 있다. PATH에 없는 실행 파일은 전체 경로로 호출한다.
- **PowerShell 연동**: `powershell.exe`에 COM API를 쓰는 짧은 스크립트를 붙이면, 파이프로 받은 입력을 Outlook 새 메일의 본문으로 넣을 수 있다. 예를 들어 `git format-patch` 결과에 서명한 뒤 메일 본문으로 보낸다.
- 스크립트를 `sendmail.ps1` 같은 파일로 저장해 두고 `-File`로 다시 쓸 수 있다.
- WSL의 Bash에서 Windows 경로를 쓸 때는 `/`로 구분하는 편이 안전하다. Bash에서 `\`는 특수 문자라 두 번 써야 한다. PowerShell은 `\`도 괜찮지만, 다른 프로그램은 까다로울 수 있다.

```bash
cowsay "Hi" | clip.exe
git format-patch --stdout HEAD~1 | gpg --clear-sign | powershell.exe -File C:/Users/me/sendmail.ps1
```

---

## 3. Windows에서 WSL로

- 반대로 Windows 명령의 출력을 `wsl.exe`로 넘겨 WSL 도구로 처리할 수도 있다. 예를 들어 `Get-Service` 결과를 WSL의 `grep`으로 걸러서 Xbox 관련 서비스만 본다.
- `grep` 대신 `awk`로 두 번째 열만 뽑아 다시 PowerShell cmdlet에 넘기면, 걸러낸 서비스를 한꺼번에 시작하거나 중지할 수 있다(관리자 권한 필요).
- `ssh-agent` 서비스가 시작되지 않으면 `Set-Service ssh-agent -StartupType Manual`로 수동 시작을 허용한다.

```powershell
Get-Service | wsl.exe -d Ubuntu-20.04 grep Xbox
```

---

## 4. 파일 리다이렉션

- **입력 리다이렉션(`<`)**: 파일 내용을 명령의 입력으로 넣는다.
- **출력 리다이렉션(`>`)**: 명령의 출력을 파일에 저장한다.
- 파일 이름을 인자로 받는 명령은 리다이렉션 없이도 쓸 수 있다. 리다이렉션은 그렇지 않은 명령에 쓸모가 있다.
- Windows의 명령 프롬프트와 PowerShell도 리다이렉션을 지원하므로, Windows 파일을 WSL 명령의 입력으로 넣을 수 있다. 예를 들어 Windows의 hosts 파일 내용을 `tee`로 WSL 배포판의 `/etc/hosts`에 복사한다.

```bash
wsl.exe -u root tee /etc/hosts < C:\Windows\System32\drivers\etc\hosts
```

---

## 5. 히어독(heredoc)

- **히어독(heredoc)**: `<<` 뒤에 종료 표지 단어를 적고, 그 단어가 한 줄에 단독으로 나올 때까지의 여러 줄 텍스트를 명령의 입력으로 넘긴다. 임시 파일이 필요 없다.
- 종료 표지는 본문에 자연스럽게 나오지 않는 단어면 무엇이든 된다(보통 `EOF`). 줄 맨 앞에 공백 없이 써야 한다. 히어독은 명령이나 파이프라인의 맨 끝에 둔다.
- Windows 명령에도 쓸 수 있다. 앞에서 만든 `sendmail.ps1`에 여러 줄 본문을 넘겨 Outlook 메일을 작성하는 식이다.

```bash
powershell.exe -File C:/Users/me/sendmail.ps1 <<EOF
메일 본문 여러 줄
EOF
```

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
