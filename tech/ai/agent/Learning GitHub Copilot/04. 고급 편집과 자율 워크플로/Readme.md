# 고급 편집과 자율 워크플로

기본적인 코드 작성과 채팅만으로도 일상 작업은 처리할 수 있지만, 대규모 리팩터링이나 여러 파일에 걸친 변경, 복잡한 수정에는 Copilot의 고급 기능이 필요하다. 이 장은 AI가 더 큰 범위의 변경과 코드 생성을 맡아 주는 기능들을 다룬다.

다음 편집 제안, Copilot Edits, 에이전트 모드, Copilot Vision, 디버깅 지원을 계산기 예제로 따라가 보고, 세 가지 편집 기능을 언제 골라 쓸지 기준도 정리한다.

---

## 1. 핵심 요점

- 다음 편집 제안(NES)은 방금 한 수정을 보고 다음에 고칠 자리를 거터 화살표로 알려 준다. Tab으로 받고 Escape로 거절한다.
- NES를 켜는 설정 키는 `github.copilot.nextEditSuggestions.enabled=true`이고, 대기 중 제안은 편집기에서 포커스를 벗어나면 사라진다. F2로 이름 바꾸기 제안도 받는다.
- Copilot Edits는 Edit 모드에서 내가 고른 여러 파일을 프롬프트 하나로 고치고, Keep/Undo/Done으로 검토한다. Done 전까지는 되돌릴 수 있다.
- 에이전트 모드는 파일을 스스로 찾고 터미널 명령까지 쓰며 목표 달성까지 반복한다. 시간이 더 걸리고 Copilot Free 요금제의 월 상호작용 할당량을 많이 쓸 수 있다.
- 에이전트의 도구 아이콘으로 확장과 기본 도구, 개방형 표준인 MCP를 다룰 수 있다.
- Copilot Vision은 스크린샷이나 목업 같은 이미지를 채팅에 붙여 설명을 듣고 코드를 만들게 한다. 에이전트 모드와 함께 쓰면 이미지를 닮은 웹 화면도 만든다.
- 디버깅에는 `/startDebugging`, Visual Studio의 예외 도우미와 Debug with Copilot, `copilot-debug`, 스크린샷 디버깅이 있고, IDE마다 지원이 다르다.
- 범위로 구분하면 NES는 단일 파일, Edits는 여러 파일, 에이전트 모드는 코드와 터미널과 테스트까지다.

---

## 2. 문서 목록

- [다음 편집 제안](%EB%8B%A4%EC%9D%8C%20%ED%8E%B8%EC%A7%91%20%EC%A0%9C%EC%95%88.md): NES를 켜는 법, Tab과 Escape 흐름, F2 이름 바꾸기, 한계
- [Copilot Edits](Copilot%20Edits.md): Edit 모드, 파일 지정 방법, Keep/Undo/Done, 계산기 예제와 #codebase
- [에이전트 모드](%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EB%AA%A8%EB%93%9C.md): 에이전트의 작업 흐름, 도구와 MCP, 계산기 예제, 시간과 요금제 주의
- [Copilot Vision](Copilot%20Vision.md): 이미지 입력 용도, 이미지 설명과 코드 생성, 에이전트와 결합한 웹 화면 만들기
- [Copilot 디버깅](Copilot%20%EB%94%94%EB%B2%84%EA%B9%85.md): /startDebugging, Visual Studio 기능, copilot-debug, 스크린샷 디버깅
- [기능 비교와 선택](%EA%B8%B0%EB%8A%A5%20%EB%B9%84%EA%B5%90%EC%99%80%20%EC%84%A0%ED%83%9D.md): NES, Edits, 에이전트 모드의 비교표와 선택 기준
- [정리](%EC%A0%95%EB%A6%AC.md): 장 결론과 다음 장으로 이어지는 흐름

<br>
<br>
<br>

[Learning GitHub Copilot](../)
