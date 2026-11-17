# 플랫폼 간 통합: GitLab CI, Jenkins, 로컬 스크립트

GitHub Actions에는 공식 액션이 있지만, Claude Code의 헤드리스 모드는 본질적으로 플랫폼에 의존하지 않는다. 실행 환경이 Node.js를 지원하기만 하면 어떤 CI/CD 플랫폼에도 배포할 수 있다. 이 문서는 같은 리뷰 작업을 GitLab CI, Jenkins 선언형 파이프라인, 팀 공유용 로컬 셸 스크립트로 옮긴 세 예시를 정리한다. 세 예시가 공유하는 뼈대는 동일하다. 설치(`npm install -g @anthropic-ai/claude-code`), API 키를 시크릿으로 주입, `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1`, 그리고 `claude -p`에 json 출력과 두 가지 한도와 읽기 전용 도구 허용을 붙이는 것이다.

---

## 1. GitLab CI/CD

GitLab Runner에서 코드 리뷰 작업을 수행하고 결과를 구조화된 형식으로 출력하는 설정이다(파일 `.gitlab-ci.yml`).

| 항목 | 값 |
|---|---|
| 잡 이름 | claude-review |
| image | node:20 |
| variables | `ANTHROPIC_API_KEY: $ANTHROPIC_API_KEY`, `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC: "1"` |
| script 1 | `npm install -g @anthropic-ai/claude-code` |
| script 2 | `claude -p "Review the code changes in this MR" --output-format json --max-turns 10 --max-budget-usd 0.50 --allowedTools "Read,Grep,Glob" > review.json` |
| script 3 | `cat review.json \| jq -r '.result'` |
| rules | `if: $CI_PIPELINE_SOURCE == "merge_request_event"` (머지 리퀘스트 이벤트일 때만) |

```yaml
claude-review:
  image: node:20
  variables:
    ANTHROPIC_API_KEY: $ANTHROPIC_API_KEY
    CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC: "1"
  script:
    - npm install -g @anthropic-ai/claude-code
    - claude -p "Review the code changes in this MR" --output-format json --max-turns 10 --max-budget-usd 0.50 --allowedTools "Read,Grep,Glob" > review.json
    - cat review.json | jq -r '.result'
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

원서는 `claude -p` 명령을 `- |` 블록으로 여러 줄에 나눠 썼다. 위에서는 한 줄로 합쳤고 옵션과 값은 같다. 참고(노트 작성자): 이 이미지에서 jq가 설치되어 있는지는 원서가 확인하지 않는다. 기본 node 이미지에 jq가 없을 수 있으므로 필요하면 설치 단계를 추가해야 한다(원서에 없는 보충).

### GitLab 공식 연동에 관한 안내

위 설정은 범용 CI 설정이다. 원서는 Anthropic과 GitLab이 연동을 깊게 하고 있다고 덧붙인다. GitLab은 이제 공식 AI 기능(베타)을 제공하며 `AI_FLOW_INPUT`, `AI_FLOW_CONTEXT`, `AI_FLOW_EVENT` 같은 전용 변수가 있어 프롬프트 컨텍스트를 손으로 조립할 필요가 줄었다. 또 `gitlab-mcp-server`가 MCP를 통해 GitLab API를 모델에 노출한다(도구 이름 `mcp__gitlab`). 현재의 설정은 Anthropic의 GitLab CI/CD 가이드에 있으며, 변수 이름이 아직 바뀌고 있으니 이 쪽 말고 가이드를 확인하라고 원서는 당부한다.

## 2. Jenkins 파이프라인

Jenkins에서는 선언형 파이프라인으로 Claude Code를 쉽게 붙일 수 있다. 예시는 자격 증명을 안전하게 관리하고, 헤드리스로 리뷰하고, 구조화된 출력을 파싱한다.

| 구분 | 내용 |
|---|---|
| agent | any |
| environment | `ANTHROPIC_API_KEY = credentials('anthropic-api-key')`, `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC = '1'` |
| stage | AI Code Review |
| steps 1 | `sh 'npm install -g @anthropic-ai/claude-code'` |
| steps 2 | `sh '''claude -p "Review the most recent code changes, focusing on logical errors and code standards" --output-format json --max-turns 10 --max-budget-usd 0.50 --allowedTools "Read,Grep,Glob" > review.json'''` |
| steps 3 | `script` 블록에서 `readJSON file: 'review.json'`로 읽어 `review.result`와 `review.total_cost_usd`를 echo |

```groovy
environment {
  ANTHROPIC_API_KEY = credentials('anthropic-api-key')
  CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC = '1'
}
script {
  def review = readJSON file: 'review.json'
  echo "Review result: ${review.result}"
  echo "Cost: \$${review.total_cost_usd}"
}
```

API 키는 Jenkins 자격 증명(credentials) 저장소의 `anthropic-api-key` 항목에서 `credentials()`로 꺼내 환경 변수에 연결한다. 코드에 키를 적지 않는 것이 핵심이다. `readJSON`은 Jenkins의 Pipeline Utility Steps 플러그인이 제공하는 스텝이다(참고(노트 작성자): 이 플러그인 이름은 원서에 없는 보충이다).

## 3. 로컬 자동화 스크립트

CI/CD 플랫폼 말고도 헤드리스 모드는 로컬 스크립트로 포장하기에 알맞다. 팀원이 코드를 제출하기 전에 스스로 점검하거나 로컬 자동화 도구 모음의 일부로 쓸 수 있다. 원서는 환경 점검, 동적 파일 필터링, 구조화된 보고서 생성, 오류 처리를 갖춘 강화판 review.sh를 보여 준다.

### 3-1. 단계별 동작

| 단계 | 내용 |
|---|---|
| 준비 | `set -e`, 첫 인자를 `TARGET`으로(기본값 `.`) |
| 사전 점검 | `ANTHROPIC_API_KEY`가 비어 있으면 오류 메시지 후 종료. `command -v claude`로 설치 확인, 없으면 종료 |
| 파일 목록 | TARGET이 디렉터리면 `find`로 .ts, .js, .py 파일을 찾아 앞 20개(`head -20`)만, 파일이면 그 파일 하나 |
| 리뷰 실행 | `claude -p`에 목록과 출력 형식(마크다운 보고서, 문제마다 파일명과 줄 번호)을 요구. `--output-format text`, `--max-turns 15`, `--max-budget-usd 0.50`, `--allowedTools Read,Grep,Glob`. stdout은 /tmp/review-out.txt, stderr은 /tmp/review-err.txt |
| 실패 처리 | 명령이 실패하면 stderr 파일을 표준 오류로 내보내고 `exit 1` |
| 보고서 저장 | `review-$(date +%Y%m%d-%H%M%S).md`에 제목, 날짜, 대상, 구분선, 결과를 써서 저장하고 "Report saved: 파일명" 출력 |

```bash
if ! claude -p "Review the code quality and security issues in the following files: $FILES ..." \
    --output-format text --max-turns 15 --max-budget-usd 0.50 \
    --allowedTools Read,Grep,Glob > /tmp/review-out.txt 2> /tmp/review-err.txt; then
    cat /tmp/review-err.txt >&2
    exit 1
fi
```

### 3-2. 왜 `RESULT=$(claude ...)`로 받지 않았나

원서의 주석이 핵심을 짚는다. `RESULT=$(claude -p ...)`처럼 명령 치환으로 받으면 `set -e`가 켜져 있어도 안쪽 명령의 종료 코드가 가려져 실패가 숨는다. 그래서 `if ! claude ... > 파일; then` 형태로 종료 코드를 직접 검사하고 결과는 파일에서 읽는다. 원서 코드는 줄 끝 `\`와 긴 프롬프트가 쪽 경계에서 어긋나 있어 위처럼 복원했다.

---

## 4. 핵심 정리

- 헤드리스 모드는 Node.js만 되면 어떤 CI에서도 돈다. 공식 액션이 없어도 같은 옵션 묶음을 쓴다.
- GitLab: image `node:20`, 변수 두 개, `rules`에 `$CI_PIPELINE_SOURCE == "merge_request_event"`. GitLab 공식 AI 기능(`AI_FLOW_INPUT`, `AI_FLOW_CONTEXT`, `AI_FLOW_EVENT`, `gitlab-mcp-server`)은 아직 변하는 중이므로 가이드를 확인한다.
- Jenkins: `credentials('anthropic-api-key')`로 키를 주입하고 `readJSON`으로 결과와 비용을 읽는다.
- 로컬 `review.sh`: 키와 설치 사전 점검, 파일 20개 제한, `if !` 형태의 종료 코드 검사, 날짜가 붙은 보고서 저장.

<br>
<br>
<br>

[The Claude Code Operating Model](../)
