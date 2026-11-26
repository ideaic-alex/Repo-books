# API 키 등록과 연동 테스트

키와 모델 이름을 마련했으니 이제 Claude Code에 연결할 차례다. 이 문서는 6장의 첫 번째 절 마무리로, 프로젝트를 초기화하고 .env 파일을 안전하게 쓰도록 설정하고, 두 모델이 실제로 응답하는지 시험하는 과정을 다룬다.

열쇠를 만들었으면 금고에 넣고 문 열리는지 확인해야 한다. .env가 금고이고, .gitignore는 그 금고를 공개 장소에 내놓지 않게 하는 안전장치다.

---

## 1. 프로젝트 초기화와 키 등록

1. VibeCoding 폴더의 Study-04 폴더에서 마우스 오른쪽 버튼을 눌러 터미널에서 열기를 고른다.
2. 터미널에 claude를 입력해 Claude Code를 실행한다.
3. `/init` 명령으로 프로젝트를 초기화한다. 그러면 Study-04 폴더에 CLAUDE.md 파일이 생긴다. 프로젝트 설정 파일이라는 점은 3장에서 배웠다.
4. OpenRouter 키가 든 .env 파일을 Claude Code가 쓸 수 있게 한다. 아래 프롬프트를 입력한다.

```text
I saved the API key I received from OpenRouter in the .env file.
Please set it up so I can use this key securely.
```

책의 원문 프롬프트는 영어이며, "OpenRouter에서 받은 API 키를 .env 파일에 저장했으니 이 키를 안전하게 쓰도록 설정해 달라"는 뜻이다.

주의할 점이 있다. 보안을 위해 API 키 값 자체를 프롬프트에 직접 입력하는 것은 권장되지 않는다. 키는 파일에 두고, 프롬프트에서는 그 파일을 가리키기만 한다.

설정이 끝나면 Study-04 폴더에 .gitignore 파일과 여러 보조 설정 파일이 새로 생긴다. 터미널의 설명으로 생성된 파일을 확인할 수 있고, 그중 중요한 것은 두 가지다.

| 파일 | 역할 |
|---|---|
| .env | API 키가 든 환경 변수 파일. API를 부를 때마다 참조한다 |
| .gitignore | .env처럼 지정한 파일이 버전 관리에 올라가지 않게 막는 설정 파일 |

## 2. .env와 .gitignore가 필요한 이유

.env는 프로그램의 설정 값을 담는 특별한 파일이다. API 키 같은 민감한 정보를 프로그램 코드와 따로 관리하는 것이 업계의 표준 관행이다. Claude Code가 키를 설정할 때 .env와 .gitignore를 자동으로 만든 것도 이 관행을 따른 것이다. 이 방식의 이점은 세 가지다.

- 키를 코드에 직접 쓰면 GitHub에 올릴 때 누구나 볼 수 있다. 하지만 .env가 커밋 전에 .gitignore에 적혀 있으면 Git이 그 파일을 무시하므로 키가 코드와 함께 공개될 위험이 줄어든다.
- 개발 중에는 무료 API를 쓰다가 실서비스에서는 유료 API로 바꿀 때 코드를 고치지 않고 .env만 바꾸면 된다.
- 팀 프로젝트에서 사람마다 다른 키를 써야 하면 코드는 공유하고 각자 자기 .env를 두어 충돌을 피한다.

## 3. 두 모델이 실제로 동작하는지 시험하기

이미지 인식에는 구글의 Gemma 모델을, 생성형 언어 모델에는 OpenAI의 gpt-oss 모델을 쓴다. 저장해 둔 모델 이름을 확인하고 아래 프롬프트를 입력한다.

```text
Now test whether the prepared API actually works.
For image recognition, use the google/gemma-4-26b-a4b-it:free model,
For text generation, use the openai/gpt-oss-20b:free model.
Test both text and image recognition via the API and let me know the results.
```

팁으로, OpenRouter에서 API를 적용할 때는 모델 이름을 정확히 입력해야 한다. 글자 하나만 달라도 호출이 실패한다. 잠시 뒤 Claude Code가 API 테스트가 성공했다고 알려 준다.

### 실제로 키가 쓰였는지 확인하기

OpenRouter 웹사이트에 로그인해 프로필 아이콘을 누르고 Activity 메뉴를 고르면 확인할 수 있다. 이 페이지의 대시보드에는 총 지출(Total spend), 요청 수(Requests), 토큰 사용량(Token volume)과 방금 호출한 Gemma와 gpt-oss의 모델별 사용 내역이 나온다. 이로써 API 연동이 끝났다. 다음 절에서는 이 외부 AI 모델로 FridgeChef를 만든다.

## 4. 이 절의 핵심과 복습 문제

핵심 정리는 네 가지다.

- API는 외부 AI 서비스와 내 프로그램을 잇는 다리이며, 약속된 통신 규칙으로 복잡한 AI 기능을 간단한 요청으로 쓰게 한다.
- OpenRouter 같은 통합 플랫폼에서는 여러 AI 모델을 한곳에서 비교하고 고를 수 있다.
- API 서비스를 쓰려면 사용자 인증을 위한 API 키를 받아야 한다.
- 여러 AI 모델을 앱에 붙일 때는 Claude Code에게 프로젝트 폴더에 .env와 .gitignore를 만들게 한다.

**복습 문제**(정답은 09장)

1. OpenRouter에서 API를 쓰는 데 필요한 것을 모두 고르시오. (1) API 키 (2) 모델 이름 (3) 자체 서버 (4) .gitignore 파일
2. Claude Code에서 API 키를 관리하는 안전한 방법이 아닌 것을 고르시오. (1) .env 파일에 키 저장 (2) .env를 .gitignore에 추가 (3) 키를 코드에 직접 입력 (4) 프로젝트 폴더 안에서만 키 참조
3. OpenRouter의 Activity 메뉴에서 확인할 수 없는 정보를 고르시오. (1) 사용한 모델 이름 (2) 사용 시각 (3) 호출한 코드 내용 (4) API 호출 내역

<br>
<br>
<br>

[Build with Claude Code](../)
