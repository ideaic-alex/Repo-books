# 승인 모드와 신뢰 경계

Codex CLI의 행동을 막는 단단한 제약을 다루는 장이다. AGENTS.md 같은 지침은 권유에 그치지만, 승인 정책과 샌드박스 모드는 에이전트가 무엇을 시도할 수 있는지, 운영체제가 무엇을 허용하는지를 실제로 강제한다. 이 둘은 서로 독립이어서 두 축으로 보안을 따져 볼 수 있다.

이 장에서는 승인 모드 세 가지, 샌드박스 세 가지, 운영체제별 강제 방식, 프로필과 상속, 그리고 신뢰를 한 칸씩 넓히는 권한 사다리를 배운다. 원서의 권한 사다리 그림도 함께 실었다.

---

## 1. 핵심 요점

- 승인 정책(`--ask-for-approval`)은 언제 묻는지를, 샌드박스(`--sandbox`)는 운영체제가 무엇을 허용하는지를 정한다. 둘은 독립이다.
- 승인 모드는 untrusted, on-request, never 세 가지다. 대화형 개발의 기본은 on-request다.
- 샌드박스는 read-only, workspace-write, danger-full-access 세 가지다. workspace-write는 네트워크가 기본으로 꺼져 있다.
- 네트워크 접근과 웹 검색은 별개 설정이다. 웹 검색은 `cached`, `live`, `disabled` 중에서 고르며 기본은 `cached`다.
- 강제는 macOS의 Seatbelt, Linux의 bwrap과 seccomp, Windows의 제한된 토큰으로 이루어지며 사용자 공간에서 우회할 수 없다.
- `~/.codex/<name>.config.toml` 프로필과 `[permissions.<name>]` 권한 프로필은 서로 다른 체계다. 후자는 `extends`로 상속하고 deny가 이긴다.
- 신뢰는 감사, 감독하의 쓰기, 요청 시 승인, 선택적 자동화의 네 단계로 넓히며, 승인은 명령 하나에만 유효하다.
- `--yolo`는 일회용 격리 컨테이너에서만 쓴다.

---

## 2. 문서 목록

- [신뢰 모델과 두 가지 제어](%EC%8B%A0%EB%A2%B0%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EB%91%90%20%EA%B0%80%EC%A7%80%20%EC%A0%9C%EC%96%B4.md): 승인과 샌드박스가 왜 따로 있는지, 흔한 조합표
- [승인 모드 세 가지](%EC%8A%B9%EC%9D%B8%20%EB%AA%A8%EB%93%9C%20%EC%84%B8%20%EA%B0%80%EC%A7%80.md): untrusted, on-request, never와 never의 사용 범위, 리뷰 생략에 대한 경고
- [샌드박스와 네트워크](%EC%83%8C%EB%93%9C%EB%B0%95%EC%8A%A4%EC%99%80%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC.md): 샌드박스 값, config.toml 설정, 네트워크와 웹 검색, --yolo
- [운영체제별 샌드박스](%EC%9A%B4%EC%98%81%EC%B2%B4%EC%A0%9C%EB%B3%84%20%EC%83%8C%EB%93%9C%EB%B0%95%EC%8A%A4.md): macOS, Linux, Windows의 커널 수준 강제 방식
- [프로필과 권한 설정](%ED%94%84%EB%A1%9C%ED%95%84%EA%B3%BC%20%EA%B6%8C%ED%95%9C%20%EC%84%A4%EC%A0%95.md): 프로필 두 체계, TUI 권한 메뉴, 기본 프로필, 상속, 항목별 승인
- [권한 사다리](%EA%B6%8C%ED%95%9C%20%EC%82%AC%EB%8B%A4%EB%A6%AC.md): 원서 그림과 함께 보는 네 단계와 명령 단위 승인
- [요약](%EC%9A%94%EC%95%BD.md): 장 요약 일곱 가지
- [연습 문제](%EC%97%B0%EC%8A%B5%20%EB%AC%B8%EC%A0%9C.md): 실습 세 문제와 풀이 방향

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
