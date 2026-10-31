# Claude Code에서 Codex CLI로 옮기기

수렴 계층의 표준 덕분에 Claude Code에서 Codex CLI로 넘어오는 일은 다시 짜는 작업이 아니라 대부분 설정을 기계적으로 옮기는 작업이다. 다른 마이그레이션과 마찬가지로 계획을 세우고, 조금씩 옮기고, 단계마다 검증하면 된다. 옮겨야 할 요소는 다섯 가지다. 지침 파일, 스킬, 서브에이전트, 훅, 설정이다.

---

## 1. 지침 파일: CLAUDE.md에서 AGENTS.md로

AGENTS.md는 Linux Foundation 산하 Agentic AI Foundation(AAIF)이 관리하는 개방형 표준이다. OpenAI가 2025년 8월에 오픈소스로 공개했고, 2025년 12월에 AAIF에 기증했다. Anthropic, Block, OpenAI가 창립 지원에 참여했다. 반면 CLAUDE.md는 Claude Code 전용이다.

CLAUDE.md는 지우지 말고 구조를 바꾼다.

- 모든 도구에 공통인 규칙(코드 스타일, 빌드 명령, 테스트 실행 방법, 아키텍처 메모)은 AGENTS.md로 옮긴다.
- CLAUDE.md에는 Claude 전용 지시(훅 참조, 서브에이전트 정의, 메모리 설정)만 남긴다.
- CLAUDE.md에 "빌드 명령, 아키텍처, 규칙은 @AGENTS.md를 보라"는 상호 참조 줄을 넣는다.

파일 두 개를 유지하기 어렵다면 Codex CLI가 CLAUDE.md를 대체 파일로 읽게 설정한다.

```toml
# ~/.codex/config.toml
project_doc_fallback_filenames = ["CLAUDE.md", "COPILOT.md"]
project_doc_max_bytes = 65536
```

집필 시점의 탐색 방식은 이렇다. Codex는 저장소 루트에서 작업 디렉터리까지 각 디렉터리를 내려가며 차례로 확인한다. 같은 수준에서 AGENTS.override.md가 있으면 AGENTS.md를 대체하고, 그다음 AGENTS.md, 그다음 project_doc_fallback_filenames에 적은 이름들 순이다. 이어 붙인 전체 사슬에 적용되는 기본 바이트 제한 project_doc_max_bytes는 32 KiB(32768바이트)이며, 큰 모노레포에서는 65536으로 올리라고 원서는 권한다.

## 2. 스킬

스킬은 호환성이 가장 좋다. SKILL.md 형식이 Agent Skills 개방형 표준을 따르므로 같은 파일이 Claude Code, Codex CLI, Cursor, Gemini CLI에서 모두 동작한다. 달라지는 것은 디렉터리 이름뿐이다.

| 도구 | 스킬 위치 |
|---|---|
| Claude Code | .claude/skills/<name>/SKILL.md |
| Codex CLI | .agents/skills/ |

.claude/skills/를 .agents/skills/로 복사하면 된다. frontmatter(파일 머리의 메타데이터)에 name, description, allowed-tools, disable-model-invocation만 쓰는 스킬은 수정 없이 작동한다. 다른 키는 하나씩 점검한다. 특히 context: fork 키는 스킬을 격리된 서브에이전트에서 돌리는 Claude Code 확장이므로, 기대기 전에 Codex CLI가 지원하는지 확인해야 한다.

## 3. 서브에이전트

서브에이전트는 구조 차이가 가장 큰 부분이다. Claude Code의 서브에이전트는 Markdown 파일로 정의하고, 부모 에이전트가 추론 과정을 보고 실시간으로 개입하는 대화형 조율을 지원한다. Codex CLI의 서브에이전트는 TOML로 정의하며, 작업을 나눠 주고 결과를 모으는 병렬 배치 작업에 맞는다.

옮기는 방법은 다음과 같다.

- 서브에이전트마다 TOML 에이전트 정의로 다시 쓴다. 위치는 프로젝트용 .codex/agents/ 또는 개인용 ~/.codex/agents/다.
- .codex/config.toml에서 features.multi_agent = true로 멀티 에이전트 작업을 켠다.
- agents.max_depth의 기본값은 1이라서 서브에이전트가 별도 설정 없이 또 다른 서브에이전트를 낳을 수 없다.
- Codex CLI 서브에이전트는 같은 일을 단일 에이전트로 할 때보다 실행당 토큰을 더 쓴다. 비용 비교에 반영해야 한다.

## 4. 훅

집필 시점에 Claude Code는 stdin/stdout 위의 JSON 프로토콜로 스물 몇 가지가 넘는 생명주기 훅 이벤트를 제공한다. Codex CLI는 열 가지 훅 이벤트를 지원한다. SessionStart, UserPromptSubmit, PreToolUse, PermissionRequest, PostToolUse, SubagentStart, SubagentStop, Stop이 확인되고, 나머지 두 개는 앞뒤로 짝을 이루는 Pre/Post 이벤트다(추출본에서 이름이 깨져 있어 정확한 이름은 확인하지 못했다). Claude Code에서 옮길 때 가장 중요한 다섯 가지는 SessionStart, PreToolUse, PostToolUse, UserPromptSubmit, Stop이다.

훅은 ~/.codex/hooks.json(프로젝트 수준은 .codex/hooks.json)에 JSON으로 설정한다. 훅은 기본으로 켜져 있고, config.toml의 [features] 아래에 있는 hooks 토글로 끌 수 있다. 관리형 설정이 이 값을 고정할 수도 있다. 구조는 다음과 같다(원서 예시에서 두 항목만 옮긴다).

```json
{
  "hooks": {
    "SessionStart": [
      { "hooks": [
        { "type": "command", "timeout": 15,
          "command": "~/.codex/hooks/on-session-start.sh" } ] }
    ],
    "PreToolUse": [
      { "matcher": "Bash", "hooks": [
        { "type": "command", "timeout": 5,
          "command": "~/.codex/hooks/pre-tool.sh" } ] }
    ]
  }
}
```

원서 예시는 같은 형태로 Stop(스크립트 on-stop.sh, timeout 10), UserPromptSubmit(on-prompt.sh, timeout 5), PostToolUse(post-tool.sh, matcher Bash, timeout 10)도 설정한다.

matcher는 도구 이름에 적용되는 정규식이다. 집필 시점에 PreToolUse와 PostToolUse는 Bash, 파일 편집 도구인 apply_patch, 그리고 mcp__filesystem__read_file 같은 MCP 도구 이름에 매치한다. 옮기는 요령은 이렇다.

- 셸 명령을 가로채는 Claude Code PreToolUse 훅은 "matcher": "Bash"로 그대로 옮긴다.
- 파일 편집을 가로채는 훅은 "matcher": "apply_patch"로 매치한다.
- 로깅, Slack 알림, 감사 기록 같은 부수 효과 훅은 Stop과 SessionStart를 쓴다.
- 파일 쓰기 도구를 이름으로 가로채던 Claude Code 훅은 같은 이름의 Codex CLI 도구가 없어서 그대로 대응되지 않는다. apply_patch를 매치하거나, sandbox_mode 또는 AGENTS.md 지시로 파일 쓰기 정책을 강제한다.

## 5. 설정

Claude Code는 5층 JSON 계층(캐스케이드)을 쓰며 지금 어느 층이 적용 중인지가 암묵적이다. Codex CLI는 이름 붙은 프로필을 써서, 내가 골랐으니 어떤 설정이 켜져 있는지 항상 안다. 프로필은 config.toml 안의 [profiles.<name>] 표가 아니라 별도 파일 ~/.codex/<name>.config.toml에 최상위 키로 적는다. codex --profile <name>을 실행하면 ~/.codex/config.toml을 먼저 읽고 그 위에 프로필 파일을 덧씌운다.

```toml
# ~/.codex/config.toml
model = "gpt-5.5"
model_reasoning_effort = "medium"
approval_policy = "untrusted"

# ~/.codex/strict.config.toml
model_reasoning_effort = "high"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
```

원서는 fast 프로필도 보여 준다. ~/.codex/fast.config.toml에 model = "gpt-5.4-mini", model_reasoning_effort = "low", approval_policy = "never", sandbox_mode = "read-only"를 적는 식이다. 프로필은 codex --profile strict "review the auth module"처럼 CLI에서 바꾼다. 이 명령은 기본 config.toml을 읽은 뒤 strict.config.toml을 덧씌운다.

모델 이름도 도구마다 다르다. Claude Code는 claude-opus-4-8, claude-sonnet-4-6 같은 Anthropic 모델 이름을 쓰고 Codex CLI는 OpenAI 모델 이름을 쓴다. 모델 이름은 자주 바뀌므로 CI 파이프라인에 하드코딩하기 전에 OpenAI 문서에서 현재 이름을 확인해야 한다.

## 6. 이전 후 권장 배치

원서가 권하는 마이그레이션 후 레이아웃은 다음과 같다.

- 저장소 루트에 AGENTS.md와 CLAUDE.md를 나란히 둔다.
- 서브에이전트 정의는 .codex/agents/(프로젝트) 또는 ~/.codex/agents/(개인) 아래 TOML 파일로 둔다.
- .agents/skills/를 두 도구가 함께 읽는 공유 스킬 디렉터리로 쓴다.

## 7. 이 문서에서 기억할 것

- 다섯 요소(지침, 스킬, 서브에이전트, 훅, 설정)를 하나씩 옮기고 단계마다 검증한다.
- 스킬은 거의 그대로 복사되고, 서브에이전트는 Markdown에서 TOML로 다시 써야 한다.
- 훅은 Bash와 apply_patch matcher로 옮기며, 파일 쓰기 도구 이름은 대응되지 않는다.
- 설정은 암묵적 캐스케이드 대신 이름 붙은 프로필 파일로 바뀐다.

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
