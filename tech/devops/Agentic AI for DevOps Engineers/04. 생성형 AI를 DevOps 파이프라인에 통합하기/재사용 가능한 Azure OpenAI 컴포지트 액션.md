# 재사용 가능한 Azure OpenAI 컴포지트 액션

앞 문서의 릴리스 워크플로는 모델 호출을 이미 로컬 컴포지트 액션(composite action, 여러 단계를 묶어 하나의 액션처럼 부르는 GitHub Actions 기능)에 맡기고 있었다. 덕분에 `release-ai.yml`은 오케스트레이션(작업 순서 조율)에 집중하고, Azure OpenAI 요청 로직은 한곳에 모인다. 이 문서는 그 액션을 어떻게 만드는지, 여러 워크플로와 저장소에 같은 API 호출 로직을 반복하는 것보다 왜 나은지 설명한다.

---

## 1. 액션 폴더와 파일

`.github` 폴더 안에 `azure-openai-chat` 폴더를 만들고, 그 안에 `action.yml`을 만든다. 최종 경로는 `.github/azure-openai-chat`이다. 이 파일이 Azure OpenAI 호출을 지배하는 로직을 정의하며, 액션 이름과 설명으로 시작해 입력을 정의한다. 이름은 "Azure OpenAI Chat Completion", 설명은 채팅 완성 엔드포인트를 호출해 어시스턴트 메시지를 파일에 쓴다는 내용이다.

## 2. 입력 정의

첫 입력은 필수인 엔드포인트다. 나머지 입력은 아래와 같다.

| 입력 | 필수 여부 | 기본값 |
|---|---|---|
| endpoint | 필수 | 없음 |
| api_key | 필수 | 없음 |
| deployment | 필수 | 없음 |
| api_version | 선택 | 2024-02-15-preview |
| system_prompt_file | 필수 | 없음 |
| user_input_file | 필수 | 없음 |
| output_file | 선택 | release-notes.md |
| temperature | 선택 | 0.1 |

API 버전은 기본값이 있지만 덮어쓸 수 있다. temperature는 모델이 만드는 출력의 성격에 영향을 준다. 값이 낮으면 출력이 더 사실적이고, 높으면 더 창의적이다. 여기서는 창의성이 필요 없어 기본값 0.1을 유지한다. 입력 설명에는 범위가 0.0에서 2.0이고 낮을수록 더 결정적이라고 적혀 있다. 엔드포인트 입력 설명의 예시는 `https://xxxx.openai.azure.com` 형태이며, 실제 값은 자리표시자로만 쓴다.

## 3. 출력 정의

출력은 원본 응답 파일 경로(`response_path`), 생성 결과 경로(`output_path`), HTTP 상태 코드(`http_status`), 호출 시간(`duration_seconds`), 그리고 토큰 사용량 세 가지(`total_tokens`, `prompt_tokens`, `completion_tokens`)다. 각 출력의 `value`는 `steps.call.outputs.*`에서 가져온다. 토큰 값은 Azure OpenAI 응답이 돌려주는 값이다.

## 4. 실행 단계

`runs`에서 `using: "composite"`로 지정하면 다른 워크플로가 참조할 수 있다. 이어지는 단계는 둘이다.

### 4-1. 입력과 의존성 검증

첫 단계는 필수 입력이 있는지 확인하고 하나라도 없으면 오류 메시지와 함께 종료한다. 쉘에서 `set -euo pipefail`을 켜고 다음을 점검한다. `jq` 명령이 설치되어 있는지, 시스템 프롬프트 파일과 사용자 입력 파일이 존재하는지, endpoint, api_key, deployment 입력이 비어 있지 않은지다. 하나라도 어긋나면 메시지를 찍고 `exit 1`로 끝낸다.

### 4-2. Azure OpenAI 호출

두 번째 단계(`id: call`)가 AI를 부른다. 이 로직은 예전에 `release-ai` 워크플로에 직접 정의했던 것과 같다. 하는 일은 세 가지다.

1. 시스템 프롬프트와 사용자 입력 파일을 읽는다.
2. Azure OpenAI 채팅 완성 요청 본문을 만든다. `jq`로 system과 user 두 메시지와 temperature를 담은 JSON을 만든다.
3. Azure OpenAI를 호출하고, 일시적 실패는 재시도하고, 생성 결과를 파일에 쓰고, 텔레메트리를 GitHub 출력으로 노출한다.

보안과 방어 면에서 눈여겨볼 줄이 있다. 호출 전에 API 키를 마스킹해 로그에 찍히지 않게 한다. 입력 크기가 25000바이트를 넘으면 모델을 부르지 않고 끝낸다. 호출은 `curl`의 POST로 `{endpoint}/openai/deployments/{deployment}/chat/completions?api-version={버전}`에 보내며 헤더는 `api-key`를 쓴다. 최대 3번 재시도하되 대기 시간은 2초에서 두 배씩 늘린다. 응답에서 `.choices[0].message.content`를 꺼내 출력 파일에 쓰고, 파일이 비어 있으면 실패 처리한다. 마지막에 토큰 값을 읽어 `$GITHUB_OUTPUT`에 쓰고 `ai-telemetry.json`을 만든다. 이 세부 내용은 뒤 문서(복잡도 줄이기, 비용과 성능, 관측성)에서 하나씩 다시 다룬다.

```bash
echo "::add-mask::${{ inputs.api_key }}"
MAX_INPUT_BYTES=25000
MAX_RETRIES=3
```

## 5. 릴리스 워크플로 갱신과 경로 오류

컴포지트 액션을 만든 뒤 `release-ai.yml`의 생성 잡에서 직접 호출 로직을 지우고 재사용 액션 호출로 바꾼다. 워크플로가 훨씬 간결해진다. 액션 폴더를 참조하고, 매개변수를 넘기고, Azure OpenAI 호출 로직을 한곳에 모으기 때문이다. 호출 줄은 `uses: ./.github/azure-openai-chat`이며 `with`에 endpoint, api_key, deployment(셋 다 시크릿), api_version, system_prompt_file, user_input_file, output_file, temperature를 넘긴다. 릴리스 출력 아티팩트에는 AI가 돌려준 원본 응답도 넣는다. 처리 전에 AI가 무엇을 돌려줬는지 보여 주므로 감사에 도움이 된다. 필수는 아니다. 완성된 워크플로에서는 같은 아티팩트에 뒤에서 쓸 텔레메트리 파일도 들어 있다.

### 5-1. 경로 수정

커밋하고 푸시하면 로컬 액션 경로가 틀렸거나 GitHub가 `.github/azure-openai-chat/action.yml`을 찾지 못할 때 워크플로가 처음에 실패한다. 워크플로는 `./.github/azure-openai-chat`이라는 상대 로컬 경로로 액션 폴더를 참조해야 한다. 경로를 고친 뒤 브랜치를 갱신해 다시 돌리면 성공하고 녹색 체크가 보인다.

이 직접 푸시 뒤 초안 릴리스를 확인하면 비어 있다. 변경을 브랜치에 직접 푸시해서 PR 메타데이터가 수집되지 않았기 때문이다. 그래도 중요한 부분은 끝났다. AI 모델과의 연결이 이제 재사용 가능해졌고, 같은 컴포지트 액션을 프로젝트와 워크플로 전반에서 쓸 수 있다.

## 6. 핵심 정리

- 모델 호출 로직은 컴포지트 액션 한곳에 두고 워크플로는 순서 조율만 맡는다.
- 입력은 엔드포인트, 키, 배포, API 버전, 프롬프트 파일, 입력 파일, 출력 파일, temperature이며 temperature 기본값은 0.1이다.
- 출력은 응답 경로, 결과 경로, HTTP 상태, 소요 시간, 토큰 사용량 세 종류다.
- 첫 단계는 입력과 의존성(jq) 검증이고 둘째 단계가 호출, 재시도, 파일 쓰기, 텔레메트리다.
- 로컬 액션은 `./.github/azure-openai-chat` 상대 경로로 참조하며 틀리면 워크플로가 실패한다.

참고(노트 작성자): 원서 코드 줄 일부는 줄바꿈이 어긋나게 추출되어(예: 긴 URL 중간) 의미만 정리했다.

<br>
<br>
<br>

[Agentic AI for DevOps Engineers](../)
