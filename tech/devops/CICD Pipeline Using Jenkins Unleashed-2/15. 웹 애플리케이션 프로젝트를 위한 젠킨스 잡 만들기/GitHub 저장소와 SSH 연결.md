# GitHub 저장소와 SSH 연결

이번 장에서는 앞 장까지 쓰던 GitLab 대신 GitHub 저장소를 사용한다. 두 서비스 모두 원격 저장소를 제공하는 웹 플랫폼이라서, 앞에서 배운 Git 개념과 명령은 그대로 통한다. 달라지는 것은 화면과 메뉴 위치 정도다.

이 문서는 계산기 웹 앱과 셀레니움 테스트 프로젝트를 각각 GitHub의 비공개 저장소에 올리는 과정을 정리한다. 젠킨스 잡이 이 저장소들에서 코드를 받아 가려면 먼저 이 준비가 끝나 있어야 한다.

---

## 1. 전체 순서

| 단계 | 할 일 |
| --- | --- |
| 1 | github.com에 가입한다 |
| 2 | 새 저장소를 비공개로 만든다 |
| 3 | `ssh-keygen`으로 SSH 키 쌍을 만든다 |
| 4 | 개인 키 경로를 `.ssh\config` 파일에 적는다 |
| 5 | 공개 키를 GitHub에 등록한다 |
| 6 | 로컬 저장소에서 프로젝트를 master 브랜치로 커밋한다 |
| 7 | master 브랜치를 원격 저장소로 푸시한다 |

1~2는 GitHub 웹에서, 3~5는 키 설정, 6~7은 평소의 Git 작업이다. 이 순서를 계산기 앱 저장소와 테스트 프로젝트 저장소에 각각 한 번씩 적용한다.

## 2. 가입과 저장소 만들기

계정이 없다면 `https://github.com/`에서 사용자 이름, 비밀번호 등 필요한 정보를 넣어 가입한다. 과정은 단순하다.

저장소는 다음과 같이 만든다.

1. 로그인하면 대시보드가 나온다. 왼쪽 위의 `+` 표시를 눌러 New Repository 메뉴를 고른다.
2. Create a New Repository 페이지의 Repository Name 칸에 저장소 이름을 넣는다.
3. Private 라디오 버튼을 골라 비공개 저장소로 만든다.
4. 아래로 내려 Create Repository 버튼을 누른다. 비어 있는 저장소가 생긴다.

## 3. SSH 키 쌍 만들기와 config 등록

SSH 키 쌍(공개 키와 개인 키)은 `ssh-keygen` 명령으로 만든다. 만드는 방법은 13장에서 다룬 내용을 참고하라고 원서는 안내한다.

만든 개인 키 파일의 경로는 `$(user.name)\.ssh\` 폴더의 `config` 파일에 적어야 한다. GitLab 개인 키 경로를 이미 적어 둔 바로 그 파일에, GitHub용 항목을 추가하는 것이다. 이 파일은 "이 서버에 접속할 때는 이 열쇠를 쓰라"고 알려 주는 안내문이다. 원서 Figure 15-7이 항목이 추가된 모습을 보여 준다.

## 4. 공개 키를 GitHub에 등록하기

1. github.com 오른쪽 위의 아바타를 눌러 Settings 메뉴로 들어간다.
2. Public Profile 페이지 왼쪽에서 SSH and GPG keys 메뉴를 고른다.
3. New SSH Key 버튼을 눌러 키 등록 페이지를 연다.
4. 공개 키 내용을 Key 칸에 붙여 넣고 Add SSH Key 버튼을 누른다.

개인 키는 내 컴퓨터에 두고 공개 키만 GitHub에 맡긴다. 자물쇠(공개 키)를 문에 달아 두고 열쇠(개인 키)는 주머니에 갖고 있는 구조다.

## 5. 로컬 커밋과 푸시

프로젝트 폴더로 `cd` 한 뒤 모든 명령을 그 폴더에서 실행한다.

```text
git init
git add .
git commit -m "Committing CalculatorWebApp project"
```

원서 본문은 add 명령을 "현재 디렉터리 전체를 스테이징 영역에 추가한다"로 설명하고, 커밋 옵션을 `--m`처럼 적었다. 일반적인 Git 문법은 `-m`이라서 위 코드는 그렇게 옮겼다. 브랜치를 지정하지 않으면 master 브랜치에 커밋된다.

푸시할 때는 저장소의 SSH 주소가 필요하다. GitHub 저장소 페이지에서 SSH 버튼을 누르고 Copy 버튼으로 복사한다. 그다음 명령 프롬프트에서 푸시한다.

```text
git push git@github.com:dpranoday/JenkinsBookCalculatorWebApplication.git master
```

키 암호(passphrase)를 물으면 입력한다. 성공하면 GitHub 저장소 페이지를 새로 고쳐서 코드가 올라갔는지 확인한다.

## 6. Permission denied 문제 해결

`.ssh\config`에 개인 키 경로를 넣었는데도 SSH 주소로 푸시할 때 Permission denied 같은 오류가 나는 경우가 있다. 원서는 다음 조치를 안내한다.

| 확인 위치 | 조치 |
| --- | --- |
| `(user.name)\.gitconfig` | `[core] sshCommand = ssh -i $HOME/.config/ssh/id_rsa -F /dev/null` 줄이 있으면 삭제한다 |
| 경로 | `-i` 뒤의 경로는 사람마다 다를 수 있다 |

이 줄이 있으면 Git이 `config` 파일 대신 지정된 키만 쓰기 때문에 GitHub용 키가 적용되지 않는다는 것이 일반적인 이유다. 원서는 이유를 따로 설명하지 않았고, 이 해석은 보충 설명이다.

## 7. 두 저장소 정리

| 저장소 | 내용 | 용도 |
| --- | --- | --- |
| `JenkinsBookCalculatorWebApplication` | 계산기 웹 앱 소스 | 빌드와 배포 잡이 사용 |
| `TestWebApplicationWithSeleniumPythonTests` | 셀레니움 Python 자동화 프로젝트 | 테스트 잡이 사용 |

두 번째 저장소는 비공개로 새로 만들고, 웹 앱을 올린 것과 같은 과정으로 테스트 프로젝트를 푸시한다. 원서 본문에는 저장소 이름이 `TestWebApplicationWithSeleniumTests`, `TestWebApplicationWIthSeleniumPythonTest` 등으로 조금씩 다르게 나오는데, 이 노트에서는 실제 푸시 명령에 쓰인 `TestWebApplicationWithSeleniumPythonTests`로 통일한다.

<br>
<br>
<br>

[CICD Pipeline Using Jenkins Unleashed](../)
