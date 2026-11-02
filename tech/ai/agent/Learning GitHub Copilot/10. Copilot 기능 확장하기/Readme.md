# Copilot 기능 확장하기

GitHub Copilot은 확장(extension)을 통해 다른 도구와 연결해 쓸 수 있다. 확장은 채팅 창에서 @이름으로 불러 쓰며, 공개된 확장을 설치해 쓰거나 직접 만들 수 있다. 이 장은 확장이 무엇인지, 마켓플레이스에서 어떻게 설치하는지, 어떤 유형으로 만드는지를 다룬다.

직접 만드는 방법으로는 에이전트, 스킬셋, VS Code용 확장 세 가지가 있다. 각각 예제 코드와 GitHub App 설정, 서버 준비까지 순서대로 정리했다.

---

## 1. 핵심 요점

- 확장은 Copilot Chat에 외부 앱과 데이터를 연결하는 수단이며, 문서 조회, AI 보조 코딩, 데이터 가져오기, 작업 실행에 쓴다.
- Copilot 확장은 채팅이 되는 모든 곳(IDE, GitHub)에서 돌아가고 GitHub App이 필요하다. VS Code용 확장은 VS Code에서만 돌아가고 별도 앱이 필요 없다.
- 마켓플레이스 확장은 설치 후 GitHub App 승인, 앱 재시작, 첫 호출 때 작업 공간 승인을 거쳐 @이름으로 부른다.
- 에이전트는 통제가 가장 크지만 구현이 복잡하고, 스킬셋(최대 5개 스킬)은 API 호출 같은 단순한 일에 알맞다.
- 모든 Copilot 확장에는 GitHub App, 공개 엔드포인트 서버, 백엔드 구현이 필요하다. 개발 중에는 ngrok이나 Codespace 포트 포워딩(포트를 Public으로)을 쓴다.
- 에이전트의 성패는 LLM에 주는 상세한 프롬프트에 달렸고, 스킬셋은 스킬의 Inference description이 프롬프트와 핸들러를 이어 준다.
- VS Code용 확장은 채팅 참여자를 만들며 버튼이나 파일 트리 같은 대화형 요소와 자체 슬래시 명령을 낼 수 있다.

---

## 2. 문서 목록

- [확장이란 무엇인가](%ED%99%95%EC%9E%A5%EC%9D%B4%EB%9E%80%20%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80.md): Copilot 확장과 VS Code용 확장의 구분, 사용 사례, 공개 범위
- [마켓플레이스에서 확장 설치하기](%EB%A7%88%EC%BC%93%ED%94%8C%EB%A0%88%EC%9D%B4%EC%8A%A4%EC%97%90%EC%84%9C%20%ED%99%95%EC%9E%A5%20%EC%84%A4%EC%B9%98%ED%95%98%EA%B8%B0.md): PerplexityAI 확장 설치, GitHub App 승인, 첫 호출
- [확장 유형과 구성 요소](%ED%99%95%EC%9E%A5%20%EC%9C%A0%ED%98%95%EA%B3%BC%20%EA%B5%AC%EC%84%B1%20%EC%9A%94%EC%86%8C.md): 에이전트와 스킬셋 비교, GitHub App과 엔드포인트 서버
- [에이전트 방식 확장 만들기](%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EB%B0%A9%EC%8B%9D%20%ED%99%95%EC%9E%A5%20%EB%A7%8C%EB%93%A4%EA%B8%B0.md): @meta-files 예제, 프롬프트 보강, SDK, 서버와 앱 설정
- [스킬셋 방식 확장 만들기](%EC%8A%A4%ED%82%AC%EC%85%8B%20%EB%B0%A9%EC%8B%9D%20%ED%99%95%EC%9E%A5%20%EB%A7%8C%EB%93%A4%EA%B8%B0.md): Go 예제 gover-ext와 스킬 정의
- [VS Code용 확장 만들기](VS%20Code%EC%9A%A9%20%ED%99%95%EC%9E%A5%20%EB%A7%8C%EB%93%A4%EA%B8%B0.md): 채팅 참여자, API 파인더 예제 코드, 테스트
- [정리](%EC%A0%95%EB%A6%AC.md): 세 유형 총정리와 앱 설정 차이

<br>
<br>
<br>

[Learning GitHub Copilot](../)
