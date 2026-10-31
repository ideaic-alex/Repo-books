# 부록 C 문제 해결

Claude Code를 쓰면서 겪는 문제를 증상별로 모아 둔 부록이다. 원문은 서술 없이 "증상, 원인, 해결" 순서로 훑어보게 만들어져 있고, 이 노트도 같은 순서를 따르되 원인을 조금 더 풀어 설명한다.

문제는 크게 다섯 갈래로 나뉜다. bash 환경과 컨텍스트 관리, 진단 도구, 훅, 실수 반복과 복구, 그리고 MCP와 실시간 시스템의 한계다.

---

## 1. 핵심 요점

- bash 명령은 매번 새 셸에서 실행된다. 작업 디렉터리만 유지되므로 환경 변수는 `&&`로 묶거나 파일에 써서 `source`로 읽어 들인다.
- 지시를 잊는 문제는 대개 컨텍스트 윈도가 찬 것이 원인이다. 꼭 지킬 규칙은 CLAUDE.md의 "Compact Instructions"에 둬야 압축 후에도 남는다.
- 자동 압축의 기본 기준은 약 95%이며 `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`로 바꿀 수 있다. 낮추면 여유가 늘고 세부는 줄어든다.
- 이상 동작의 첫 단계는 `claude doctor`다. 훅이나 도구 호출 추적에는 `Ctrl+O`와 `claude --debug`를 쓴다.
- 체크포인트는 Write/Edit 도구의 변경만 추적한다. bash 명령으로 바뀐 파일은 git으로 복구해야 하므로 위험한 작업 전에 커밋한다.
- 같은 실수는 CLAUDE.md에 틀린 방식과 맞는 방식을 함께 적어 막는다. 세션이 사라지면 `claude -c`, `claude -r`, `claude --resume`으로 복구한다.
- 훅이 동작하지 않으면 실행 권한, 셔뱅, 매처의 대소문자, `disableAllHooks`를 본다. JSON이 무시되면 stdout에 다른 텍스트가 섞였는지 본다.
- WebSocket 확장성과 FIX 프로토콜은 Claude가 뼈대만 만든다. 요구를 명시하고 사람이 검토하며 부하 테스트와 적합성 테스트로 검증한다.

---

## 2. 문서 목록

- [bash 환경과 컨텍스트 문제](bash%20%ED%99%98%EA%B2%BD%EA%B3%BC%20%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8%20%EB%AC%B8%EC%A0%9C.md): 환경 변수 유실, 지시 망각, 압축 시점 조정, 서브에이전트 결과 관리
- [진단과 디버깅 도구](%EC%A7%84%EB%8B%A8%EA%B3%BC%20%EB%94%94%EB%B2%84%EA%B9%85%20%EB%8F%84%EA%B5%AC.md): `claude doctor`, 프록시와 게이트웨이 확인, 상세 출력과 `--debug`
- [훅 문제 해결](%ED%9B%85%20%EB%AC%B8%EC%A0%9C%20%ED%95%B4%EA%B2%B0.md): 훅이 실행되지 않는 원인과 JSON 파싱 오류 대처
- [실수 반복과 작업 복구](%EC%8B%A4%EC%88%98%20%EB%B0%98%EB%B3%B5%EA%B3%BC%20%EC%9E%91%EC%97%85%20%EB%B3%B5%EA%B5%AC.md): 반복 실수 방지, 체크포인트 한계, 세션 복구, 재시작 판단, 과한 복잡도 억제
- [MCP와 실시간 시스템 한계](MCP%EC%99%80%20%EC%8B%A4%EC%8B%9C%EA%B0%84%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%ED%95%9C%EA%B3%84.md): MCP 연결 끊김, WebSocket 확장성, FIX 프로토콜

<br>
<br>
<br>

[Claude Code The Definitive Guide to Agentic Development-2](../)
