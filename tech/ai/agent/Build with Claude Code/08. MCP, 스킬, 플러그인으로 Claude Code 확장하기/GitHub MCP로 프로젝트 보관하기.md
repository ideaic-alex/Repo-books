# GitHub MCP로 프로젝트 보관하기

쇼핑 목록 앱이 만들어졌고 Playwright로 테스트도 마쳤다. 이제 이 프로젝트를 영구히 보관할 차례다. GitHub는 전 세계 개발자가 쓰는 코드 버전 관리 플랫폼이다. GitHub MCP 서버를 연결하면 로컬에서 만든 웹 앱을 Claude Code가 알아서 GitHub에 올려 준다.

평소에는 코드를 고칠 때마다 Git 명령을 손으로 입력해 변경 내용을 올려야 한다. 일기장에 비유하면, 매번 직접 일기장을 복사해서 금고에 넣는 대신 비서가 대신 해 주는 셈이다. 사람은 무엇을 만들지에 집중하고 반복되는 보관 절차는 MCP에 맡긴다.

---

## 1. 설치 명령 찾기

GitHub MCP를 설치하려면 서버 주소가 필요하다. 앞서 Notion을 설치할 때처럼 Vibe Index에서 찾는다.

1. 웹 브라우저로 Vibe Index에 들어가 검색창에 GitHub를 입력한다.
2. 검색 결과에서 GitHub를 고른다. Official MCP 표시가 붙은 것인지 확인한다.
3. MCP 상세 페이지 아래쪽의 설치 명령을 복사한다.

복사한 명령은 다음과 같은 모양이다.

```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp -H "Authorization: Bearer YOUR_GITHUB_PAT"
```

GitHub는 API 토큰 인증 방식을 쓴다. 그래서 명령에 사용자 인증과 관련된 옵션이 들어 있다. 하나씩 보자.

- `-H`는 `--header`의 줄임이다. HTTP 요청에 헤더 정보를 덧붙이는 옵션이며, 사용자 인증 정보를 MCP 서버로 보내는 데 쓴다.
- `Authorization: Bearer`는 GitHub가 API에 접근할 때 인증에 쓰는 표준 형식이다. 'Authorization'은 인증 정보를 보낸다는 뜻이고, 'Bearer'는 토큰 기반 방식이라는 뜻이다.
- `YOUR_GITHUB_PAT`은 내 API 키(토큰)를 넣는 자리다. PAT는 개인 액세스 토큰(Personal Access Token)의 약자다.

이로써 GitHub MCP를 설치하려면 API 토큰이 필요하다는 것을 알았다. 다음은 GitHub에서 토큰을 발급받는 단계다.

## 2. GitHub API 토큰 발급

1. GitHub 홈페이지(https://www.github.com)에 로그인한다. 계정이 없으면 Sign up for GitHub 버튼으로 만들고, 있으면 Sign in으로 로그인한다.
2. 오른쪽 위의 프로필을 눌러 Settings를 고른다.
3. 왼쪽 사이드바를 내려 Developer settings 메뉴를 누른다.
4. 왼쪽 사이드바에서 Personal access tokens, Tokens (classic) 순으로 들어간다. 화면 가운데 Generate new token 드롭다운에서 Generate new token (classic)을 고른다.
5. 새 토큰 만들기 화면에서 Note에 원하는 이름을 쓰고 Expiration(만료)은 30일로 설정한다.
6. Select scopes는 이 토큰이 가질 권한의 범위다. 다음 세 가지를 선택하고 Generate Token 버튼을 누른다. `repo`는 비공개 저장소의 전체 제어, `user`는 사용자 데이터 전체 접근, `project`는 프로젝트 전체 제어다.
7. 토큰이 발급되면 복사 아이콘을 눌러 어딘가에 저장해 둔다.

주의할 점이 있다. 다른 API 키와 마찬가지로 GitHub 토큰도 화면에 한 번만 보인다. 반드시 복사해서 따로 안전한 곳에 저장해 둬야 한다. 또 토큰은 비밀번호와 같으니 남에게 보이거나 공개 저장소에 올리면 안 된다.

참고(노트 작성자): 위 권한 세 가지는 이 실습에서 책이 고른 선택이다. 더 좁은 권한으로도 동작하는지는 원서에 없다. 토큰 메뉴 이름과 구성은 책이 쓰인 시점 기준이다.

## 3. 설치 완료하기

발급한 토큰으로 GitHub MCP를 Claude Code에 설치한다.

1. 터미널을 열고 앞서 준비한 GitHub MCP 설치 명령을 준비한다.
2. 명령의 인증 부분에 발급받은 토큰을 넣어 터미널에서 실행한다.

```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp -H "Authorization: Bearer <YOUR_GITHUB_TOKEN>"
```

`<YOUR_GITHUB_TOKEN>` 자리에 내 토큰을 넣는다. 설치 완료 메시지가 나오면 `claude`로 Claude Code를 실행하고 `/mcp`를 입력한다. GitHub MCP가 설치되었고 연결(connected)로 보이면 끝이다.

Notion MCP와 비교하면 인증 방법이 다르다는 점이 보인다. Notion은 설치 뒤 브라우저에서 로그인하는 방식이었고, GitHub는 설치 명령 안에 토큰을 직접 넣는 방식이다.

## 4. 프로젝트 올리기

GitHub MCP가 설치되었으니 저장소를 만들고 쇼핑 목록 앱을 올린다. `Study-06` 폴더 위치에서 Claude Code를 실행하고 프롬프트를 입력한다.

```text
I want to save the shopping list app created in the current folder to GitHub. Use github mcp to create a repository named shopping-list-app and upload it.
```

프롬프트는 '현재 폴더의 쇼핑 목록 앱을 GitHub에 저장하고 싶다, GitHub MCP로 `shopping-list-app`이라는 이름의 저장소를 만들어 올려라'는 뜻이다. Claude Code가 저장소를 만들고 add, commit 같은 명령을 실행하는 권한을 요청한다. `1. Yes`를 눌러 push까지 쭉 진행한다.

완료되면 GitHub에서 해당 URL을 열어 확인한다. `shopping-list-app`이라는 새 저장소가 만들어져 있고, `CLAUDE.md`와 `shopping-list.html` 파일이 잘 올라가 있다.

## 5. Git 기본 용어: add, commit, push

GitHub는 코드를 온라인에 저장하고 관리하는 클라우드 기반 버전 관리 플랫폼이다. 다른 사람과 협업할 수 있고, 코드 변경 기록을 남겨 두었다가 언제든 이전 버전으로 되돌릴 수 있다. 올리는 흐름은 세 단계다.

| 단계 | 하는 일 | 쉬운 비유 |
|---|---|---|
| add | 계정에 원격 저장소를 만들고, 올릴 파일을 골라 스테이징 영역에 담는다 | 상자에 보낼 물건을 담는다 |
| commit | 스테이징 영역에서 확정된 파일을 로컬 저장소에 저장한다. 변경 한 묶음을 가리키기도 한다 | 상자를 테이프로 봉하고 이름표를 붙인다 |
| push | 로컬 저장소의 커밋을 원격 저장소로 올린다. 팀원이 변경 이력을 볼 수 있게 된다 | 상자를 택배로 보낸다 |

Claude Code의 GitHub MCP는 이 과정을 자동으로 처리해서 GitHub 사용이 더 편해진다. 순서는 반드시 add, commit, push다. 복습 문제에 이 순서를 묻는 문제가 나온다.

## 6. 여기까지의 의미와 핵심 정리

지금까지 MCP로 테스트부터 보관까지의 전 과정을 자동화했다. Playwright MCP가 기능 테스트를 자동화하고, GitHub MCP가 프로젝트의 버전 관리를 마무리한다. 이 둘이 AI 개발 환경의 자동화 뼈대를 이룬다. 개발자는 '무엇을 만들까'에 집중하고, 반복적이고 복잡한 기술 절차는 MCP에 맡길 수 있다. 다음 절에서는 앱을 외부 데이터베이스에 연결해 저장하고 클라우드에서 계속 운영하는 구조로 간다.

책은 일곱 가지 키워드로 정리한다.

- 테스트는 코드가 의도대로 돌고 오류가 없는지 확인하는 과정이다.
- 버전 관리는 코드 변경 이력을 기록하고 필요하면 이전 상태로 되돌리게 한다.
- Playwright는 웹사이트를 자동으로 테스트하고 화면을 검증하는 브라우저 자동화 도구다.
- GitHub에 올릴 파일을 골라 스테이징 영역에 담는 과정을 add라 한다.
- 스테이징 영역에 담은 파일을 확정해 올리기 직전의 로컬 저장소에 저장하는 과정을 commit이라 한다.
- 커밋한 파일을 로컬 저장소에서 원격 저장소로 올리는 과정을 push라 한다.

## 7. 복습 문제

정답은 부록 장에 있다.

1. Playwright MCP가 테스트를 마친 뒤 만드는 폴더 이름을 고르시오. 보기는 (1) `.test-results`, (2) `.playwright-mcp`, (3) `.automation`, (4) `.screenshots`다.
2. GitHub에 코드를 올리는 올바른 순서를 고르시오. 보기는 (1) commit, add, push, (2) push, add, commit, (3) add, commit, push, (4) add, push, commit이다.
3. MCP 서버 주소를 찾는 가장 효과적인 방법 두 가지를 서술하시오.

<br>
<br>
<br>

[Build with Claude Code](../)
