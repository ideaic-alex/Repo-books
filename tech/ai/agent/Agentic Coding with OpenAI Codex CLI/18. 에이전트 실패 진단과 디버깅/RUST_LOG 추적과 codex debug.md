# RUST_LOG 추적과 codex debug

기록(롤아웃)이 "무슨 일이 있었는지"를 보여 준다면, 로그는 "Codex 내부에서 어떻게 처리됐는지"를 보여 준다. Codex CLI는 Rust의 표준 `tracing` 크레이트 위에 만들어져서 `RUST_LOG` 환경 변수로 로그 수준을 조절할 수 있다. 이 문서는 구조화된 로그를 남기는 법, 모듈별로 좁혀 보는 법, 그리고 `codex debug` 하위 명령으로 프로토콜과 모델 목록을 점검하는 법을 정리한다.

---

## 1. 디버그 로그 남기기

```bash
RUST_LOG=debug codex "your task" 2>debug.log
```

디버그 로그에는 로드된 설정 파일, AGENTS.md 파싱, 도구 호출 디스패치, 샌드박스 적용 이벤트, API 소요 시간과 토큰 수, 에러 스택 트레이스가 담긴다. 저장한 뒤에는 `grep`으로 필요한 부분만 본다.

```bash
grep 'agents_md' debug.log                 # AGENTS.md 로딩
grep '"type":"dispatch"' debug.log | jq    # 도구 호출
grep 'ERROR\|WARN' debug.log               # 에러와 경고
```

## 2. 모듈 단위로 좁혀 보기

Codex CLI 크레이트의 기본 로그 수준은 `info`다. 모듈별로 수준을 지정하면 필요한 서브시스템만 확대해서 볼 수 있어, 잡음에 묻히지 않는다.

```bash
# 핵심 에이전트 루프만 debug, 나머지는 info
RUST_LOG=info,codex_core=debug codex
# 샌드박스 동작 디버그
RUST_LOG=codex_sandbox=debug,codex_process_hardening=debug codex
# MCP 서버 연결 디버그
RUST_LOG=codex_core::mcp=debug codex
```

로그 집계 시스템으로 보내는 등 기계가 파싱해야 한다면 형식을 JSON으로 바꾼다.

```bash
RUST_LOG=debug RUST_LOG_FORMAT=json codex exec "run tests" 2>&1 | tee codex-debug.log
```

로그 파일 위치도 알아 두자. TUI 로그는 `~/.codex/logs/codex-tui.log`에 자동 로테이션과 함께 기록된다. `codex exec` 모드에서는 `~/.codex/logs/codex-tui-<timestamp>.log`처럼 시각이 붙은 로그 파일이 생긴다.

주의할 점은 성능이다. debug와 trace 수준은 처리량을 10~50% 떨어뜨릴 수 있다. 그래서 실제로 문제를 추적하는 동안에만 쓰고, 운영 워크플로에는 켜 두지 않는다.

## 3. codex debug 하위 명령

`codex debug`는 저수준 디버깅 도구의 진입점이다.

```bash
# 사용 가능한 debug 하위 명령 목록
codex debug --help
# V2 app-server 프로토콜을 메시지 하나로 시험
codex debug app-server send-message-v2 "Hello, world"
```

`send-message-v2`는 app-server를 초기화하고, 스레드를 시작하고, 사용자 메시지 한 건을 보낸 뒤, 서버가 보내는 모든 알림을 터미널로 흘려 보낸다. 전체 TUI를 띄우지 않고 프로토콜이 정상 동작하는지 확인하는 방법이다.

## 4. codex debug models로 모델 목록 확인

```bash
codex debug models
```

이 명령은 제공자 API에 물어서 현재 자격 증명으로 쓸 수 있는 모델을 보고한다. 세션이 시작되지 않거나, 예상 못한 모델로 대체되거나, 요청한 모델을 쓸 수 없어서 출력 품질이 떨어질 때 쓴다. 출력에는 API 키로 접근할 수 있는 모든 모델이 나열된다. 흔한 상황은 세 가지다.

- **기업 프록시 뒤의 팀.** 프록시가 API 요청을 고쳐 쓰거나 걸러서 일부 모델을 조용히 막을 수 있다. 이 명령으로 내 네트워크 위치에서 실제로 제공자에게 닿는 모델을 확인한다.
- **조직 수준의 모델 제한.** 엔터프라이즈 OpenAI 계정은 API 키나 프로젝트별로 쓸 수 있는 모델을 제한하는 경우가 많다. 팀원이 "Codex CLI가 안 된다"고 하면, 첫 진단은 그 키가 `config.toml`에 지정한 모델에 접근할 수 있는지 확인하는 것이다.
- **제공자 이전.** OpenAI, Azure OpenAI, 서드파티 제공자 사이를 `OPENAI_BASE_URL`로 바꾸면 모델 이름이 달라진다. 이 명령은 내가 있다고 가정한 모델이 아니라 제공자의 실제 모델 카탈로그를 보여 준다.

특정 모델만 확인하거나 CI에서 빨리 실패시키는 조합도 쓸 수 있다.

```bash
# 특정 모델이 있는지 확인
codex debug models | grep gpt-5.4-mini
# CI에서 기대한 모델이 없으면 즉시 실패
codex debug models | grep -q "gpt-5.4-mini" || echo "ERROR: gpt-5.4-mini not available"
```

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
