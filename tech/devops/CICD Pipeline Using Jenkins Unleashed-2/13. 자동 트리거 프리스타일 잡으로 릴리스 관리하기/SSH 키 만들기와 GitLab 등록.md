# SSH 키 만들기와 GitLab 등록

SSH 인증을 쓰려면 먼저 열쇠 한 쌍을 만들고, 그중 자물쇠 역할을 하는 공개 키를 GitLab에 맡겨 두어야 한다. 이 문서는 새 개발자의 컴퓨터에서 ssh-keygen 명령으로 키 쌍을 만들고, GitLab의 SSH Keys 페이지에 공개 키를 등록하는 과정을 단계별로 정리한다.

원서의 실습 환경은 Windows이다. 명령은 명령 프롬프트(command prompt)에서 실행한다. 경로 표기와 키 파일 이름은 원서 예시를 따르며, 독자는 자기 환경에 맞게 바꿔 쓰면 된다.

---

## 1. 준비물, OpenSSH 클라이언트

ssh-keygen은 OpenSSH라는 도구에 들어 있는 프로그램이다. Windows 10(2018년 4월 업데이트) 이상에는 OpenSSH가 기본으로 깔려 있다. 그보다 오래된 Windows라면 먼저 설치해야 한다.

설치 여부를 확인하고 설치하는 순서는 다음과 같다.

1. 설정(Settings) 앱을 열고 Apps & Features 범주를 누른다.
2. Manage Optional Features 링크를 누른다.
3. 목록에 OpenSSH client가 보이지 않으면 Add a feature 버튼을 눌러 설치한다.
4. 설치 후 컴퓨터를 다시 시작해야 할 수도 있다.

OpenSSH client가 설치되어 있으면 키 쌍을 만들 준비가 끝난다.

## 2. 단계 1: 공개 키와 개인 키 만들기

명령 프롬프트를 열고 다음 명령을 실행한다.

```
ssh-keygen
```

실행하면 키 쌍을 저장할 파일 경로를 묻는다. 아무것도 입력하지 않고 Enter를 누르면 기본 위치에 만들어진다. 원서는 기본 위치를 `$(user.home)\.ssh\is_rsa`라고 적었는데, 일반적으로 SSH 기본 키 파일 이름은 `id_rsa`이므로 오타로 보인다. 불확실한 부분이라 원문 표기를 그대로 밝혀 둔다.

원서는 기본 위치를 쓰지 않고 `D:\SSHKey\MyGitlabKeys`를 입력했다. 이어서 암호 문구(passphrase)를 입력하라고 나오는데, 이는 이 SSH 키를 쓸 때마다 요구되는 비밀번호이다.

| 입력 항목 | 원서에서 한 일 | 설명 |
| --- | --- | --- |
| 저장 경로 | `D:\SSHKey\MyGitlabKeys` 입력 | 비워 두면 기본 경로 사용 |
| passphrase | 직접 정해 입력 | 키를 쓸 때마다 물어보는 암호 |

키 생성이 끝나면 지정한 폴더에 파일 두 개가 생긴다. 첫 번째 파일이 개인 키이고, 두 번째 파일이 공개 키이다.

| 파일 | 내용 | 쓰임 |
| --- | --- | --- |
| MyGitlabKeys | 개인 키 | 자기 컴퓨터에 두고 접근할 때 사용 |
| MyGitlabKeys.pub | 공개 키 | GitLab에 등록하는 파일 |

파일 이름 끝에 `.pub`이 붙은 쪽이 공개 키이다. 이 표는 원서의 "첫 번째 파일은 개인 키, 두 번째는 공개 키"라는 설명에 `.pub` 확장자 정보를 더해 정리한 것이다. 원서의 그림 캡션은 폴더를 `D:\SSHKeys`라고도 적어서 `SSHKey`와 `SSHKeys` 표기가 섞여 있다. 같은 폴더를 가리키는 오타로 보이며, 이 노트에서는 자기가 만든 폴더 이름으로 통일해서 쓰면 된다.

## 3. 단계 2: 공개 키를 GitLab에 등록하기

새 개발자는 공개 키를 GitLab 저장소 관리자에게 보내 등록해야 한다고 앞에서 설명했다. 원서는 한 화면에서 이 과정을 보여 주기 위해 GitLab 계정 설정에서 직접 키를 등록한다. 순서는 다음과 같다.

1. GitLab 화면 오른쪽 위의 사용자 아바타(avatar)를 누른다.
2. 메뉴에서 Preferences를 선택한다. Preferences 페이지가 열린다.
3. 페이지 왼쪽에서 SSH Keys 메뉴를 누른다.
4. MyGitlabKeys.pub 파일을 열어 내용을 모두 복사해서 Key 입력란에 붙여 넣는다.
5. Title 입력란에 이 키를 구분할 이름을 쓴다. 원서는 `Pranodayd@LPTSEPT12`라고 썼다.
6. Add key 버튼을 누른다. 키가 GitLab에 등록된다.

| 입력란 | 넣는 값 | 비고 |
| --- | --- | --- |
| Key | `.pub` 파일의 내용 전체 | 개인 키가 아니라 공개 키를 붙인다 |
| Title | 키를 알아볼 이름 | 원서 예시는 `Pranodayd@LPTSEPT12` |

여기서 가장 흔한 실수는 개인 키 파일을 열어서 붙여 넣는 것이다. 공개 키는 `.pub`로 끝나는 파일이라는 점을 기억하면 된다. 등록이 끝나면 이 키를 가진 컴퓨터에서만 SSH로 저장소에 접근할 수 있는 준비가 된 것이다.

## 4. 정리

| 단계 | 할 일 | 도구 또는 화면 |
| --- | --- | --- |
| 0 | OpenSSH client 확인과 설치 | 설정 → Apps & Features → Manage Optional Features |
| 1 | 키 쌍 만들기 | ssh-keygen 명령 |
| 2 | 공개 키 등록 | GitLab → Preferences → SSH Keys |

키를 등록했으니 다음 문서에서는 SSH 주소로 저장소를 복제(clone)하고 새 기능을 추가하는 단계로 넘어간다.

<br>
<br>
<br>

[CICD Pipeline Using Jenkins Unleashed](../)
