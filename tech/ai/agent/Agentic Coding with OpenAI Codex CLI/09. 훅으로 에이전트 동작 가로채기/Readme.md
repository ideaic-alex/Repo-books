# 훅으로 에이전트 동작 가로채기

MCP가 에이전트의 손을 바깥으로 뻗게 해 준다면, 훅(hook)은 에이전트 자신의 생애 주기를 제어하게 해 준다. 세션이 열릴 때부터 서브에이전트가 끝날 때까지 열 지점에서 셸 명령을 실행해 컨텍스트를 넣고, 정책을 강제하고, 동작을 기록하고, 알림을 보낼 수 있다. AGENTS.md는 한 줄도 바꿀 필요가 없다.

이 장은 열 가지 훅 이벤트의 계약, 실제로 쓸 수 있는 스크립트 예제, 타임아웃과 오류 처리 같은 안정적 운영 원칙, 기업용 거버넌스 패턴, 그리고 `/hooks` 브라우저와 OpenTelemetry, 플러그인 배포 같은 운영 도구를 차례로 설명한다. 원서의 훅 생명주기 그림(Figure 9.1)도 함께 실었다.

---

## 1. 핵심 요점

- 훅은 동기로 실행되는 셸 콜백이며 stdout, stderr, 종료 코드로 결과를 전한다. `.codex/hooks.json`과 `config.toml` 인라인 `[[hooks]]` 두 곳에서 설정을 읽고, 편집하면 재시작 없이 반영된다.
- 이벤트는 열 개다. 그중 실행을 막을 수 있는 것은 PreToolUse, PermissionRequest, UserPromptSubmit, SubagentStop 네 개다.
- SessionStart와 UserPromptSubmit은 stdout을 컨텍스트나 프롬프트에 넣는다. 출력은 컨텍스트 윈도를 차지하므로 짧게 줄여야 한다.
- 종료 코드 규약은 0이 성공, 2가 막기(막을 수 없는 이벤트에서는 오류 기록), 그 밖은 조용한 실패다. 의존성 부재 같은 상황은 exit 0으로 넘기고 exit 2는 의도한 정책 거부에만 쓴다.
- PreCompact와 PostCompact로 압축 전에 상태를 저장하고 압축 후에 다시 주입하면 긴 세션의 정보 손실을 줄인다.
- SubagentStart와 SubagentStop은 `agent_type` matcher로 서브에이전트 역할별 컨텍스트 주입과 품질 관문을 건다.
- 기업은 `requirements.toml`로 거버넌스 훅을 의무화할 수 있고, 모든 계층의 훅은 동시에 실행되어 합쳐진다.
- `/hooks` 브라우저로 훅을 켜고 끄며(상태는 `$CODEX_HOME`에 영구 저장), OpenTelemetry 스팬으로 지연과 실패율을 보고, 플러그인에 묶어 팀에 배포한다.

---

## 2. 문서 목록

- [훅 시스템 개요](%ED%9B%85%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EA%B0%9C%EC%9A%94.md): 훅의 성질, 열 이벤트 표, hooks.json과 config.toml 설정, MCP 관찰
- [훅 생명주기 흐름](%ED%9B%85%20%EC%83%9D%EB%AA%85%EC%A3%BC%EA%B8%B0%20%ED%9D%90%EB%A6%84.md): 원서의 생명주기 그림과 이벤트 묶음, 공통 종료 코드 규약
- [세션 시작과 프롬프트 훅](%EC%84%B8%EC%85%98%20%EC%8B%9C%EC%9E%91%EA%B3%BC%20%ED%94%84%EB%A1%AC%ED%94%84%ED%8A%B8%20%ED%9B%85.md): SessionStart 컨텍스트 주입, UserPromptSubmit 보강과 차단
- [도구 호출과 권한 훅](%EB%8F%84%EA%B5%AC%20%ED%98%B8%EC%B6%9C%EA%B3%BC%20%EA%B6%8C%ED%95%9C%20%ED%9B%85.md): PreToolUse, PermissionRequest, PostToolUse와 저장 시 테스트
- [압축과 서브에이전트와 종료 훅](%EC%95%95%EC%B6%95%EA%B3%BC%20%EC%84%9C%EB%B8%8C%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%EC%99%80%20%EC%A2%85%EB%A3%8C%20%ED%9B%85.md): 압축 메모리 패턴, 서브에이전트 경계 훅, Stop
- [튼튼한 훅 작성 원칙](%ED%8A%BC%ED%8A%BC%ED%95%9C%20%ED%9B%85%20%EC%9E%91%EC%84%B1%20%EC%9B%90%EC%B9%99.md): 타임아웃, stdout 크기, 의존성 처리, 상태 표시, 시험 방법
- [실전 패턴 모음](%EC%8B%A4%EC%A0%84%20%ED%8C%A8%ED%84%B4%20%EB%AA%A8%EC%9D%8C.md): 린트, 비밀 값 검사, MITM 탐지, 감사 로그, Slack 알림
- [기업 거버넌스와 자기 진화 루프](%EA%B8%B0%EC%97%85%20%EA%B1%B0%EB%B2%84%EB%84%8C%EC%8A%A4%EC%99%80%20%EC%9E%90%EA%B8%B0%20%EC%A7%84%ED%99%94%20%EB%A3%A8%ED%94%84.md): Pre/PostToolUse 거버넌스와 재학습 루프
- [훅 운영 도구](%ED%9B%85%20%EC%9A%B4%EC%98%81%20%EB%8F%84%EA%B5%AC.md): /hooks 브라우저, OpenTelemetry, 플러그인 번들, 위임 승인 표시
- [요약](%EC%9A%94%EC%95%BD.md): 장 끝 핵심 여덟 가지와 다음 장으로의 연결
- [연습 문제](%EC%97%B0%EC%8A%B5%20%EB%AC%B8%EC%A0%9C.md): 브랜치 컨텍스트, 저장 시 테스트, 전체 통합 실습

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
