# 컨텍스트 엔지니어링

Claude Code의 모든 기능은 컨텍스트 윈도라는 제약에서 출발한다. 이 장은 컨텍스트 윈도를 CPU, RAM, 하드디스크처럼 다루는 법을 설명한다. 좋은 결과를 내는 개발자는 프롬프트를 잘 쓰는 사람이 아니라 컨텍스트를 잘 설계하는 사람이라는 관점이다.

중심 도구는 CLAUDE.md다. 무엇을 넣고 뺄지, 스킬, MCP, 서브에이전트, 훅과 비용을 어떻게 비교할지, 자동 압축을 어떻게 다룰지, 세션이 끝나도 지식을 어떻게 남길지를 다룬다. 비개발 분야의 재무 계획 사례와 Anthropic 내부 팀의 활용 사례도 함께 나온다.

---

## 1. 핵심 요점

- **CLAUDE.md는 항상 켜져 있다**: 모든 요청에 주입되므로 줄마다 비용이 든다. 500줄 이내로 유지하고, Claude가 스스로 알아낼 수 없는 것만 적는다.
- **기능마다 비용이 다르다**: CLAUDE.md와 MCP는 매 요청, 스킬은 설명만 매 요청이고, 서브에이전트는 분리되며, 훅은 0이다. `disable-model-invocation: true`를 쓰면 스킬 비용도 0이 된다.
- **자동 압축은 약 95%에서 일어난다**: 80%쯤에서 `/compact`로 직접 압축하는 편이 낫다. CLAUDE.md의 Compact Instructions 섹션은 압축 후에도 보존된다.
- **/rewind의 "Summarize from here"**: 막다른 탐색 구간만 골라 요약해서 쓸모 있는 작업은 그대로 둔다. `/context`로는 사용량을 진단한다.
- **세션이 끝나도 지식은 남긴다**: 세션 종료 시 CLAUDE.md 업데이트로 지식을 쌓고, 반복되는 실수는 정밀한 지시로 패치한다. 스펙 문서는 압축과 재시작을 견딘다.
- **서브에이전트는 컨텍스트 격리 수단이다**: 서브에이전트 열네 개를 조율한 뒤에도 메인 컨텍스트는 200,000 토큰 중 143,000 토큰(71%)이었다.
- **훅으로 동적 상태를 준다**: SessionStart 훅은 PR 상태나 최근 커밋 같은 현재 상황을 한 번 주입한다.
- **CLAUDE.md는 코드 밖에서도 쓴다**: 재무 계획 사례와 디자이너용 설정처럼, 사용자와 분야에 맞춰 쓸 수 있다.

---

## 2. 문서 목록

- [CLAUDE.md 기본기](CLAUDE.md%20%EA%B8%B0%EB%B3%B8%EA%B8%B0.md): 계층 구조, /init, @path import, 500줄 기준, 넣을 것과 뺄 것
- [컨텍스트 비용과 기능 선택](%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%20%EB%B9%84%EC%9A%A9%EA%B3%BC%20%EA%B8%B0%EB%8A%A5%20%EC%84%A0%ED%83%9D.md): 기능별 비용 비교, 선택 기준, 수동 전용 스킬, 예산 점검
- [자동 압축과 컨텍스트 관리](%EC%9E%90%EB%8F%99%20%EC%95%95%EC%B6%95%EA%B3%BC%20%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%20%EA%B4%80%EB%A6%AC.md): 자동 압축, Compact Instructions, /compact, /rewind, PreCompact 훅, /context, 세션 포크
- [세션을 넘어 쌓이는 지식](%EC%84%B8%EC%85%98%EC%9D%84%20%EB%84%98%EC%96%B4%20%EC%8C%93%EC%9D%B4%EB%8A%94%20%EC%A7%80%EC%8B%9D.md): 제도적 기억, 같은 실수 막기, 개선 루프, 스펙 문서, 비개발 사례, 페르소나 적응형
- [AGENTS.md와 서브에이전트 격리](AGENTS.md%EC%99%80%20%EC%84%9C%EB%B8%8C%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EA%B2%A9%EB%A6%AC.md): AGENTS.md 표준, 서브에이전트 격리, SessionStart 훅
- [컨텍스트 엔지니어링 종합](%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%20%EC%97%94%EC%A7%80%EB%8B%88%EC%96%B4%EB%A7%81%20%EC%A2%85%ED%95%A9.md): 여덟 가지 구성 요소와 선택표
- [핵심 정리](%ED%95%B5%EC%8B%AC%20%EC%A0%95%EB%A6%AC.md): 장 끝 Key Takeaways를 풀어 쓴 열 가지 요점

<br>
<br>
<br>

[Claude Code The Definitive Guide to Agentic Development-2](../)
