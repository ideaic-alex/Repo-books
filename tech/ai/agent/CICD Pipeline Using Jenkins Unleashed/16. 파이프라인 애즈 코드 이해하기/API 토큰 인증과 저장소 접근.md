# API 토큰 인증과 저장소 접근

앞 장들에서는 Git 저장소(리포지터리)에 접근할 때 사용자 이름과 비밀번호를 쓰는 기본 인증, 공개 키와 개인 키 쌍을 쓰는 SSH 인증을 다뤘다. 이 문서는 세 번째 방법인 API 인증을 설명한다. GitHub와 GitLab에서 토큰을 만드는 절차, 그 토큰으로 저장소를 복제하고 푸시하는 실습을 차례로 정리한다.

비유하면 비밀번호는 집 열쇠 원본이고, API 토큰은 용도와 권한을 정해서 따로 만든 출입 카드다. 카드를 잃어버려도 원본 열쇠는 그대로 두고 카드만 폐기하면 된다. 정확히 말하면 API 토큰은 비밀번호 대신 쓰는 비밀 문자열(시크릿 텍스트)이며, Git 원격 저장소에 API 엔드포인트나 명령줄로 접근할 때 주로 쓴다.

---

## 1. 세 가지 인증 방식 비교

| 방식 | 준비물 | 이 책에서 다룬 곳 |
|---|---|---|
| 기본 인증 | 사용자 이름 + 비밀번호 | 앞 장 |
| SSH 인증 | 공개 키 + 개인 키 쌍 | 앞 장 |
| API 인증 | API 액세스 토큰(비밀번호 자리에 사용) | 이 장 |

표에서 보듯 API 인증은 새로운 계정 정보가 아니라, 비밀번호 칸에 넣는 값만 토큰으로 바꾸는 방식이다. 그래서 Git 명령은 그대로 쓰고 입력값만 달라진다.

## 2. GitHub에서 API 액세스 토큰 만들기

GitHub에서는 Personal Access Token(개인 액세스 토큰)을 만든다. 절차는 다음과 같다.

1. GitHub 사용자 이름과 비밀번호로 로그인한다. 대시보드가 보인다.
2. 대시보드 오른쪽 위의 사용자 아바타를 눌러 Settings 메뉴로 들어간다.
3. Public Profile 페이지가 열리면 왼쪽의 Developer Settings 링크를 누른다.
4. GitHub Apps 페이지에서 Personal access tokens 링크를 누른다.
5. Personal Access Tokens 페이지에서 Generate New Token 버튼을 누른다.
6. New Personal Access Token 페이지의 Note 칸에 토큰의 용도를 알아볼 수 있는 문자열을 적는다.
7. Select Scopes(권한 범위) 영역에서 repo 체크박스를 선택한다. 비공개 저장소에 대한 모든 권한이 한꺼번에 선택된다.
8. 아래로 스크롤해서 Generate Token 버튼을 누른다.
9. 토큰이 표시되면 복사 버튼으로 복사해서 파일에 붙여 넣어 둔다.

중요한 경고가 하나 있다. 이 페이지를 벗어나면 보안상 같은 토큰을 다시 보여 주지 않는다. 그러니 페이지를 떠나기 전에 반드시 복사해서 파일에 저장해 둬야 한다.

## 3. GitHub 토큰으로 비공개 저장소 사용하기

만든 토큰으로 JenkinsBookCalculatorWebApplication 저장소를 복제하고, 코드를 바꾸고, 푸시해 본다.

### 3-1. 저장소 복제

1. 저장소를 받을 빈 폴더를 만든다. 책에서는 D 드라이브에 CloningRepoUsingAPIToken 폴더를 만들었다.
2. 명령 프롬프트를 열고 cd 명령으로 그 폴더에 들어간다.
3. 저장소의 HTTPS URL로 git clone을 실행한다.

```
git clone https://github.com/dpranoday/JenkinsBookCalculatorWebApplication.git
```

4. GitHub 로그인 창이 뜨면 Personal Access Token 칸에 토큰을 넣고 Sign in 버튼을 누른다. 저장소가 복제된다.

한 번 사용자 이름과 비밀번호 또는 토큰으로 저장소에 접근하면 그 자격 증명이 윈도우 자격 증명(Windows Credentials)에 저장된다. 확인하려면 시작 메뉴에서 Windows Credentials를 검색해 Manage Windows Credentials 메뉴를 열고, Generic Credentials 영역을 본다. 여기에 GitHub 사용자 이름과 액세스 토큰 항목이 보인다. 이후 다른 GitHub 비공개 저장소에 접근할 때는 저장된 값을 쓰기 때문에 로그인 창이 다시 뜨지 않는다.

### 3-2. 코드 수정과 푸시

src/main/webapp 디렉터리의 Calculator.html을 열고, 제목과 버튼 배경 색을 green에서 red로 바꾼다. 책의 원래 CSS는 다음과 같다(바꾸기 전 모습).

```css
.title{
    margin-bottom: 10px;
    text-align:center;
    width: 210px;
    color:green;
    border: solid black 2px;
}
input[type="button"]
{
    background-color:green;
    color: black;
    border: solid black 2px;
    width:100%
}
```

바꿀 곳은 `color:green;`(제목 글자색)과 `background-color:green;`(버튼 배경색) 두 줄이다. 저장한 뒤 로컬 저장소에 커밋하고 푸시한다.

```
git add .
git commit -m "Changing title color and button control background color to red"
git push https://github.com/dpranoday/JenkinsBookCalculatorWebApplication.git master
```

변경은 기본 브랜치인 master에 커밋된다. 토큰이 이미 저장되어 있으므로 푸시할 때 토큰을 다시 묻지 않는다. GitHub 저장소 페이지를 새로 고치면 변경 내용이 보인다.

## 4. GitLab에서 API 액세스 토큰 만들기

GitLab도 흐름은 같지만 메뉴 이름이 다르다.

1. GitLab 사용자 이름과 비밀번호로 로그인한다.
2. 오른쪽 위 사용자 아바타를 눌러 Preferences 메뉴로 들어간다.
3. 왼쪽의 Access Tokens 링크를 누르면 Personal Access Tokens 페이지가 열린다.
4. Token Name 칸에 토큰의 용도를 적는다.
5. Select scopes 영역에서 write_repository 체크박스를 선택한다. 비공개 저장소에 대한 전체 제어 권한을 얻기 위해서다.
6. 아래의 Create Personal Access Token 버튼을 누른다.
7. Access Token 페이지에서 Copy Personal Access Token 버튼으로 복사해 파일에 붙여 넣는다.

GitHub와 마찬가지로 페이지를 벗어나면 토큰을 다시 볼 수 없다.

| 항목 | GitHub | GitLab |
|---|---|---|
| 진입 메뉴 | Settings 후 Developer Settings | Preferences |
| 토큰 메뉴 | Personal access tokens | Access Tokens |
| 용도 입력 칸 | Note | Token Name |
| 선택하는 권한 | repo | write_repository |
| 생성 버튼 | Generate Token | Create Personal Access Token |

두 서비스 모두 권한 범위를 체크박스로 고르고, 생성 직후에만 토큰을 보여 준다는 점이 같다.

## 5. GitLab 토큰으로 비공개 저장소 사용하기

이번에는 JenkinsBookCalculatorAPI 저장소로 같은 실습을 한다.

### 5-1. 저장소 복제

1. 빈 폴더를 만든다. 책에서는 D 드라이브에 CloningCalculatorAPIRepoUsingAPIToken 폴더를 만들었다.
2. 명령 프롬프트에서 그 폴더로 이동한다.
3. 윈도우 자격 증명 관리자에 이전 GitLab 자격 증명이 있으면 먼저 지운다. Manage Your Credentials 창에서 GitLab 항목의 Remove 버튼을 누르고, 삭제 확인 창에서 Yes를 누른다. 저장된 값이 남아 있으면 로그인 창이 뜨지 않기 때문이다.
4. GitLab 저장소의 HTTPS URL로 복제한다.

```
git clone https://gitlab.com/Pranoday/Jenkinsbookcalculatorapi.git
```

5. Git Credential Manager 대화상자가 뜨면 User Name 칸에 GitLab 사용자 이름을, Password 칸에 GitLab 액세스 토큰을 넣고 OK를 누른다.

### 5-2. 코드 수정과 푸시

src/main/java/Pranodayd/CalculatorAPI 아래의 Calculator.java를 열어 Addition 함수의 변수 이름을 Res에서 R로 바꾼다.

```java
public int Addition(int num1,int num2)
{
      int R=num1+num2;
      return R;
      ///return 0;
}
```

저장하고 커밋한 뒤 푸시한다.

```
git add .
git commit -m "Changed variable name in Addition function"
git push https://gitlab.com/Pranoday/Jenkinsbookcalculatorapi.git master
```

이번에도 토큰을 다시 묻지 않고 master 브랜치에 푸시된다. GitLab 저장소 페이지를 새로 고치면 변경이 보인다.

## 6. 핵심 정리

- API 토큰은 비밀번호 대신 쓰는 비밀 문자열이고, GitHub와 GitLab 모두 설정 메뉴에서 권한 범위를 골라 만든다.
- 토큰은 생성 직후 한 번만 보여 주므로 파일에 복사해 둔다.
- Git 명령은 그대로 쓰고, 로그인 창의 비밀번호 칸에 토큰을 넣는다.
- 윈도우 자격 증명에 값이 저장되므로 이후에는 입력창이 뜨지 않는다. 계정을 바꾸려면 저장된 항목을 지워야 한다.

<br>
<br>
<br>

[CICD Pipeline Using Jenkins Unleashed](../)
