# Copilot으로 디버깅하기

앞 장들에서 코드 설명을 듣는 `/explain` 명령과 버그 수정안을 받는 `/fix` 명령을 다뤘다. 이 문서는 그 밖에 디버깅에 도움이 되는 기능을 정리한다. 디버그 설정 만들기, 디버깅 세션 시작, Visual Studio 전용 기능, 터미널의 copilot-debug 명령, 스크린샷으로 디버깅하는 방법이다.

어떤 기능은 IDE에 따라 쓸 수 있는지가 다르다. 그래서 마지막에 IDE별 차이와 채팅으로 질문하는 요령도 함께 정리한다.

---

## 1. 디버그 설정과 세션 시작 (VS Code)

VS Code에서 Copilot은 디버그 설정을 만들고 손봐 주는 일을 돕는다. `/startDebugging` 슬래시 명령(책에서는 shortcut command라 부른다)으로 launch.json 파일이 없을 때 새로 만들 수 있다. 채팅에 프롬프트로 요청해도 같은 결과를 얻는다.

같은 `/startDebugging` 명령은 디버깅 세션을 시작하는 데도 쓴다. 이때 알맞은 launch 설정이 없으면 Copilot이 먼저 만든다. 같은 대화 안에서 Copilot이 보통 실제 디버그 과정을 시작하는 버튼을 함께 보여 주므로, 그 버튼을 누르면 된다.

| 하고 싶은 일 | 방법 |
|---|---|
| launch.json이 없을 때 만들기 | `/startDebugging` 또는 채팅 프롬프트 |
| 디버깅 세션 시작 | `/startDebugging` 후 Copilot이 보여 주는 시작 버튼 |
| 적절한 launch 설정이 없을 때 | 명령이 먼저 설정을 생성한 뒤 진행 |

---

## 2. Visual Studio 전용 기능

일부 IDE, 예컨대 Visual Studio에서는 Copilot 연동에 예외 도우미(exception helper)가 들어 있다. 디버깅 중 IndexOutOfRangeException 같은 예외가 나면 팝업에 Ask Copilot 옵션이 뜬다. 그러면 Copilot이 오류 설명, 코드 수정 제안을 주고, IDE에서 수정을 미리 보고 바로 적용하기까지 한다.

Visual Studio 2022의 테스트 탐색기(Test Explorer)로 단위 테스트를 하고 있다면 Debug with Copilot 버튼이 있다. 테스트가 실패했을 때 이 기능은 다음을 한다.

- 포괄적인 디버그 계획을 만든다.
- 중단점(breakpoint)을 설정한다.
- 핵심 변수를 지켜본다(watch).
- 디버깅 과정을 안내한다.

그 과정에서 Copilot은 중단점에서 변수 값을 분석하고, 피드백 순환 속에서 안내와 제안을 준다.

> IDE별 기능: 예외 도우미와 테스트 탐색기의 Debug with Copilot은 책이 쓰인 시점에 Visual Studio에서만 쓸 수 있고, VS Code 같은 다른 IDE에서는 안 된다.

---

## 3. copilot-debug 명령

일부 IDE에서 Copilot은 `copilot-debug`라는 명령도 제공한다. 터미널에서 내 애플리케이션과 함께 실행하면 디버그 세션이 시작된다.

```
copilot-debug node app.js
```

> 주의: copilot-debug는 터미널에서 편하지만, IDE가 연결되기를 기다리며 멈추는 경우가 있는 것 같다. 문제가 생기면 `/startDebugging` 명령이나 IDE의 기본 기능으로 디버그 세션을 돌려 본다.

---

## 4. 스크린샷으로 디버깅하기

앞서 본 Copilot Vision과 연결되는 기법이다. 문제를 스크린샷으로 보여 주고 디버깅을 맡길 수 있다.

예를 들어 간단한 C# 코드를 찍은 스크린샷이 있다고 하자(책의 파일명은 Screenshot 2025-04-28 at 12.37.05 PM.png). 이 파일을 채팅에 붙이고 코드의 문제를 디버깅해 달라고 요청한다. 처리 후 Copilot은 0으로 나누는 상황에서 생길 수 있는 처리되지 않은 예외(unhandled exception)를 짚고, 이를 해결하는 코드를 제안했다.

---

## 5. 기능 정리

| 기능 | 어디서 | 하는 일 |
|---|---|---|
| `/explain` | 채팅(앞 장) | 문제가 있을 수 있는 코드를 설명 |
| `/fix` | 채팅(앞 장) | 버그 수정안 제안 |
| `/startDebugging` | VS Code | launch.json 생성, 디버깅 세션 시작 |
| 예외 도우미(Ask Copilot) | Visual Studio | 예외 설명, 수정 제안, 미리 보기와 적용 |
| Debug with Copilot | Visual Studio 2022 테스트 탐색기 | 실패한 테스트에 대해 디버그 계획, 중단점, 변수 감시 |
| `copilot-debug` | 일부 IDE의 터미널 | 터미널에서 앱을 실행하며 디버그 세션 시작 |
| 스크린샷 디버깅 | 채팅(Vision) | 이미지로 문제를 보여 주고 원인과 수정안 요청 |

표를 읽는 법은 간단하다. 기능마다 "어디서" 열에 적힌 환경이 아니면 안 보일 수 있다. 쓰던 IDE에서 안 보이면 내가 잘못한 것이 아니라 그 IDE에 없는 기능일 수 있다.

---

## 6. 가장 좋은 도구는 여전히 채팅

내장 디버깅 기능을 쓰든 안 쓰든, 채팅 인터페이스는 여전히 가장 좋은 도구 중 하나다. 문제가 생겼는데 왜 그런지 모르겠다면 Copilot에게 물어보면 된다. 구체적인 질문이 모호한 요청보다 훨씬 좋은 결과를 준다.

| 질문 방식 | 예 |
|---|---|
| 구체적인 질문(결과가 좋다) | "Why does this API call fail for valid input?" |
| 모호한 요청(결과가 떨어진다) | 상황과 대상을 밝히지 않은 막연한 요청 |

어떤 Copilot 디버그 기능은 모든 IDE에 있지 않다. 그래서 가장 확실한 방법은 문제에 대해 구체적인 "왜" 질문을 채팅으로 하는 것일 수 있다.

<br>
<br>
<br>

[Learning GitHub Copilot](../)
