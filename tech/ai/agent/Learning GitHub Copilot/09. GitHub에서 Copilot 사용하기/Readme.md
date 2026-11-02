# GitHub에서 Copilot 사용하기

Copilot은 IDE뿐 아니라 GitHub 웹에도 들어와 있다. 저장소 화면에서 채팅을 열어 코드베이스를 물어볼 수 있고, 이슈와 풀 리퀘스트(PR) 같은 GitHub의 핵심 기능에서도 AI의 도움을 받는다.

이 장은 GitHub에서 Copilot이 어떻게 연결되어 있는지를 훑고 효과적으로 쓰는 법을 다룬다. 저장소 채팅과 인덱싱, 코드 스캔 경고를 고치는 변경 흐름, PR 리뷰와 요약, 이슈 요약을 차례로 설명한다. 화면과 메뉴 위치는 책을 쓴 시점 기준이라 GitHub가 바뀌면 달라질 수 있다.

---

## 1. 핵심 요점

- GitHub 웹에도 Copilot 채팅이 있다. 저장소의 Copilot 아이콘은 몰입형, 옆 화살표의 Assistive는 보조형 채팅을 연다.
- 보조형 채팅은 열린 항목(저장소, 이슈 등)에 맞는 질문을 미리 채워 주고, 고르면 더 긴 맞춤 프롬프트로 바뀐다.
- 채팅을 열면 저장소 인덱싱이 자동으로 시작된다. 인덱스는 모델 학습에 쓰이지 않고 저장소 접근 권한이 있는 사용자만 혜택을 받는다.
- 코드 스캔 경고는 Create issue로 이슈가 되고, Copilot Autofix의 Generate fix가 수정안을 만들며, 커밋하면 초안 PR이 열리고 CodeQL이 다시 돈다.
- Copilot은 PR의 리뷰어로 추가할 수 있고, 채팅으로 PR 요약도 받는다.
- 채팅에게 URL을 만들게 하면 PR 작성 화면을 링크 한 번으로 열 수 있다. PR 설명 요약 생성은 책의 시점에 유료 요금제 기능이다.
- Files changed 탭에서는 Ask Copilot이 파일 전체를, Attach to current thread가 diff 한 조각을 컨텍스트로 붙인다.
- 이슈 요약과 다음 단계 제안은 유용하지만 세부를 놓칠 수 있고 응답 품질도 들쭉날쭉하므로 직접 확인한다.

---

## 2. 문서 목록

- [GitHub 채팅과 저장소 인덱싱](GitHub%20%EC%B1%84%ED%8C%85%EA%B3%BC%20%EC%A0%80%EC%9E%A5%EC%86%8C%20%EC%9D%B8%EB%8D%B1%EC%8B%B1.md): 채팅을 여는 위치, 보조형과 몰입형, 메뉴, 인덱싱
- [코드 스캔 경고에서 Autofix까지](%EC%BD%94%EB%93%9C%20%EC%8A%A4%EC%BA%94%20%EA%B2%BD%EA%B3%A0%EC%97%90%EC%84%9C%20Autofix%EA%B9%8C%EC%A7%80.md): 경고에서 이슈, 수정안, 초안 PR까지의 흐름
- [풀 리퀘스트 검토와 요약](%ED%92%80%20%EB%A6%AC%ED%80%98%EC%8A%A4%ED%8A%B8%20%EA%B2%80%ED%86%A0%EC%99%80%20%EC%9A%94%EC%95%BD.md): Copilot을 리뷰어로 추가하고 PR을 요약하는 법
- [링크로 PR 만들기와 요약 생성](%EB%A7%81%ED%81%AC%EB%A1%9C%20PR%20%EB%A7%8C%EB%93%A4%EA%B8%B0%EC%99%80%20%EC%9A%94%EC%95%BD%20%EC%83%9D%EC%84%B1.md): URL 생성으로 PR 열기, 변경 요약 자동 작성
- [PR 변경 내용 탐색](PR%20%EB%B3%80%EA%B2%BD%20%EB%82%B4%EC%9A%A9%20%ED%83%90%EC%83%89.md): Files changed 탭의 Copilot 진입점과 컨텍스트 범위
- [이슈 요약과 다음 단계 제안](%EC%9D%B4%EC%8A%88%20%EC%9A%94%EC%95%BD%EA%B3%BC%20%EB%8B%A4%EC%9D%8C%20%EB%8B%A8%EA%B3%84%20%EC%A0%9C%EC%95%88.md): 이슈 요약의 재료와 이점, 검증 시 주의점
- [정리](%EC%A0%95%EB%A6%AC.md): 장 전체 결론과 기능별 요약

<br>
<br>
<br>

[Learning GitHub Copilot](../)
