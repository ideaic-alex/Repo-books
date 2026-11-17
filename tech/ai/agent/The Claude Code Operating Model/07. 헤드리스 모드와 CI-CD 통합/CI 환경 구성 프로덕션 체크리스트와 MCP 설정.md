# CI 환경 구성: 프로덕션 체크리스트와 MCP 설정

지금까지는 실행이 "되게" 만드는 법이었다. 이 문서는 실제 파이프라인에서 "버티게" 만드는 법을 다룬다. 빠뜨리기 쉽지만 빠뜨리면 비싼 부분들이다. -p와 `--allowedTools` 말고도 프로덕션 배포에는 환경 변수를 의도적으로 설정하고, 권한 범위를 좁히고, 실패가 눈에 보이게 해야 한다. 필수 환경 변수, 성능 조정 변수, 그것들을 모두 적용한 GitHub Actions 템플릿, 그리고 CI에서 MCP 서버를 쓸 때의 `--mcp-config`와 `--strict-mcp-config`를 정리한다.

---

## 1. 필수 환경 변수

### 1-1. 인증과 기능 끄기

| 변수 | 값 | 설명 |
|---|---|---|
| ANTHROPIC_API_KEY | sk-ant-... (자리표시자, 실제 값은 시크릿으로 주입) | API 키 |
| CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC | 1 | 종합 스위치(권장). 자동 업데이트, 텔레메트리, 오류 보고 등 비필수 기능을 한꺼번에 끈다 |
| DISABLE_AUTOUPDATER | 1 | 자동 업데이트 끄기(CI에서 필수) |
| DISABLE_TELEMETRY | 1 | 텔레메트리 끄기 |
| DISABLE_ERROR_REPORTING | 1 | 오류 보고 끄기 |

원서는 기능 끄기에 두 방식을 제시한다. 옵션 1은 종합 변수 하나(권장)이고, 옵션 2는 세밀한 제어를 위한 개별 끄기다. `DISABLE_AUTOUPDATER`는 CI/CD에서 매우 중요하다. 이 변수를 설정하지 않으면 Claude Code가 실행 중 자동 업데이트를 시도해 버전 불일치나 뜻밖의 서비스 중단이 생길 수 있다. 반면 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`는 편리한 "마스터 스위치"로, 모든 비필수 백그라운드 트래픽(자동 업데이트, 텔레메트리, 오류 보고)을 한 번에 끄므로 설정 과정이 단순해진다.

### 1-2. 성능 조정 변수

| 변수 | 원서 예시 값 | 설명 |
|---|---|---|
| BASH_DEFAULT_TIMEOUT_MS | 120000 | Bash 명령의 기본 시간 제한(밀리초). 2분 |
| BASH_MAX_TIMEOUT_MS | 600000 | Bash 명령에 허용되는 최대 시간 제한. 10분 |
| CLAUDE_CODE_MAX_OUTPUT_TOKENS | 32000 | 모델 응답 한 번당 최대 토큰. 기본 32,000, 상한 64,000 |
| MAX_MCP_OUTPUT_TOKENS | 25000 | MCP 도구 응답 한 번당 최대 토큰 |
| CLAUDE_CODE_AUTOCOMPACT_PCT_OVERRIDE | 50 | 자동 압축(auto-compaction) 발동 임계값. 범위 1~100, 컨텍스트 사용률(%)을 뜻한다. 기본 50% |

원서 코드의 주석은 마지막 변수가 "default 50%"라고 쓴다.

## 2. GitHub Actions 완성 템플릿

앞 실습의 리뷰 잡에 이 절의 환경, 권한, 비용 통제를 모두 적용한 것이 아래 템플릿이다. 원서는 "복사해 쓸 만한 버전"이라고 부른다. 단계 이름은 Run Claude Analysis다.

| 구분 | 내용 |
|---|---|
| env | `ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}`, `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC: "1"`, `BASH_DEFAULT_TIMEOUT_MS: "300000"`(기본 Bash 명령 시간 제한 5분) |
| 실행 | `npx @anthropic-ai/claude-code -p "$PROMPT"` |
| 옵션 | `--output-format json`, `--max-turns 10`, `--max-budget-usd 1.00`, `--allowedTools "Read,Grep,Glob"`, `--model claude-sonnet-4-6`, `--fallback-model claude-haiku-4-5` |
| 추가 지시 | `--append-system-prompt "Follow the review guidelines in the CLAUDE.md file at the project root."` |

```yaml
- name: Run Claude Analysis
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
    CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC: "1"
    BASH_DEFAULT_TIMEOUT_MS: "300000"
  run: |
    npx @anthropic-ai/claude-code -p "$PROMPT" --output-format json \
      --max-turns 10 --max-budget-usd 1.00 --allowedTools "Read,Grep,Glob" \
      --model claude-sonnet-4-6 --fallback-model claude-haiku-4-5 \
      --append-system-prompt "Follow the review guidelines in the CLAUDE.md file at the project root."
```

원서 YAML은 들여쓰기가 없고 `env:` 아래 빈 줄과 주석이 섞여 있었다. 키와 값은 그대로이고 들여쓰기만 복원했다. `$PROMPT`는 별도로 정의된 변수(원서에 정의 줄은 없음)라서 앞 단계 env 등으로 주입해야 한다고 읽어야 한다. 이 템플릿이 실습 1의 CLI 방식과 다른 점은 `--fallback-model`로 폴백을 걸고, CLAUDE.md의 리뷰 지침을 따르게 하며, Bash 시간 제한을 5분으로 올린 것이다.

## 3. CI에서의 MCP 서버 설정

CI 작업이 데이터베이스 조회나 외부 API 호출 같은 MCP 서버의 능력을 써야 하면, `--mcp-config` 매개변수로 전용 설정 파일을 읽고 `--strict-mcp-config`로 환경 격리를 보장한다.

```bash
npx @anthropic-ai/claude-code -p "Analyze optimization opportunities in the database schema" \
  --mcp-config ./ci-mcp-config.json --strict-mcp-config \
  --allowedTools "Read,Grep,Glob,mcp__database__query" --max-turns 10
```

- `--mcp-config ./ci-mcp-config.json`: CI 전용 MCP 설정 파일을 지정한다.
- `--strict-mcp-config`: 엄격 모드다. Claude가 `--mcp-config`로 지정한 설정 파일만 쓰도록 강제하고, 사용자 홈 디렉터리나 프로젝트 루트에 있는 다른 MCP 설정은 모두 무시한다. 개발자의 로컬 MCP 설정이 CI에 우연히 섞여 들어가는 것을 막아 주므로 CI 환경에서 중요하다.
- `--allowedTools`에는 MCP 도구도 이름으로 허용 목록에 넣는다. 예시의 `mcp__database__query`는 `mcp__<서버이름>__<도구이름>` 규칙을 따르며, 여기서는 database 서버의 query 도구다.
- 6장 MCP 문서의 원칙대로, DB 같은 연결에는 읽기 전용 계정만 쓰는 것이 안전하다(참고(노트 작성자): 이 연결은 원서가 이 대목에서 직접 말하지는 않았으나 6장의 보안 원칙을 CI에도 적용한 것이다).

---

## 4. 핵심 정리

- 기능 끄기는 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` 하나(권장) 또는 `DISABLE_AUTOUPDATER=1`, `DISABLE_TELEMETRY=1`, `DISABLE_ERROR_REPORTING=1` 개별 설정이다. CI에서는 자동 업데이트를 반드시 끈다.
- 시간·출력·컨텍스트 조정은 `BASH_DEFAULT_TIMEOUT_MS`(120000), `BASH_MAX_TIMEOUT_MS`(600000), `CLAUDE_CODE_MAX_OUTPUT_TOKENS`(32000, 상한 64000), `MAX_MCP_OUTPUT_TOKENS`(25000), `CLAUDE_CODE_AUTOCOMPACT_PCT_OVERRIDE`(50, 범위 1~100)다.
- 완성 템플릿은 `--output-format json`, `--max-turns 10`, `--max-budget-usd 1.00`, `--allowedTools "Read,Grep,Glob"`, `--model claude-sonnet-4-6`, `--fallback-model claude-haiku-4-5`, `--append-system-prompt`를 한 번에 쓴다.
- CI의 MCP는 `--mcp-config`와 `--strict-mcp-config`를 함께 쓰고, MCP 도구는 `mcp__서버__도구` 이름으로 `--allowedTools`에 넣는다.

<br>
<br>
<br>

[The Claude Code Operating Model](../)
