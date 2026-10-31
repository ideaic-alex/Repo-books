# codex와 codex exec

Codex CLI를 실행하는 방식은 크게 둘이다. 인자 없이 `codex`를 치는 대화형 방식과, 한 번 실행하고 끝나는 `codex exec`다. 이 문서는 두 방식의 차이와 언제 무엇을 쓸지 고르는 기준을 정리한다.

---

## 1. codex: 대화형 REPL

`codex`를 인자 없이 실행하면 대화형 REPL(입력하면 바로 응답하는 반복형 환경)이 뜬다. 대화 기록이 유지되는 지속형 세션이다. 코드베이스를 탐색하거나, 여러 단계로 이루어진 과제를 하거나, 도구를 익힐 때처럼 사람이 오가며 진행하는 작업에 쓴다.

앞의 첫 세션 실습이 이 방식이다. 에이전트가 하는 일을 보면서 방향을 조정할 수 있다는 것이 장점이다.

## 2. codex exec: 비대화형 실행

`codex exec`는 비대화형으로 실행되고, 작업이 끝나면 종료한다. 스크립트로 짠 작업, CI/CD 파이프라인, 목표가 분명한 자동화에 알맞다. 원문의 예시 두 가지는 다음과 같다.

```
codex exec "update all TypeScript interfaces in src/types/ to add the new userId field"
codex exec --json "analyse test coverage and report modules under 80 per cent"
```

첫 번째는 src/types/ 아래 TypeScript 인터페이스에 새 userId 필드를 추가하는 작업이다. 두 번째는 `--json` 플래그를 붙여 테스트 커버리지를 분석하고, 80퍼센트 미만인 모듈을 보고하게 한다. 출력을 JSON으로 받으면 다른 도구가 결과를 읽어 처리하기 쉽다.

## 3. 어느 쪽을 쓸까

책이 주는 어림 기준은 간단하다.

> 터미널에 직접 칠 만한 일이면 REPL을, Makefile에 적을 만한 일이면 `codex exec`를 쓴다.

사람이 지켜보며 상호작용할 일인지, 사람 없이 반복 실행될 일인지를 가르는 기준이다.

| 구분 | codex | codex exec |
|---|---|---|
| 방식 | 대화형 REPL, 대화 기록 유지 | 비대화형, 끝나면 종료 |
| 용도 | 탐색, 여러 단계 과제, 학습 | 스크립트 작업, CI/CD, 자동화 |
| 사람 개입 | 중간에 오가며 조정 | 지시 후 결과만 확인 |
| 비교 기준 | 터미널에 치는 일 | Makefile에 쓰는 일 |

## 4. 연습으로 이어 보기

연습 문제 2-3은 같은 과제를 두 방식으로 돌려 보고, 대화형 세션이 보여 준 것 중 `codex exec`가 보여 주지 않은 것이 무엇인지 비교하게 한다. 자세한 문제는 '연습 문제' 문서에 있다.

또 자동화에 쓰는 인증 환경 변수(`CODEX_API_KEY`, `CODEX_ACCESS_TOKEN`)는 `codex exec` 같은 비대화형 실행을 염두에 둔 값이다. 이 내용은 '설정 위치와 환경 변수' 문서에서 이어서 본다.

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
