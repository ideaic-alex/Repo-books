# Copilot의 다른 활용법

GitHub Copilot은 JavaScript나 Python 같은 대표 언어만이 아니라, 모델이 학습한 모든 언어와 형식에서 쓸 수 있다. 이 장은 다른 장과 달리 하나의 기능이 아니라 서로 다른 대표 사례 몇 가지를 모아서 다룬다.

관계형 데이터베이스의 SQL, Kubernetes가 쓰는 선언형 YAML, 까다로운 정규식, 테스트용 데이터 생성, 그리고 GitHub CLI에 들어 있는 Copilot 기능을 차례로 살펴본다. 각 사례마다 프롬프트 예, 얻는 결과, 조심할 점을 정리했다.

---

## 1. 핵심 요점

- 스키마 파일을 워크스페이스에 열어 두면 Copilot이 실제 테이블 이름과 칼럼 이름으로 SQL 쿼리와 테이블 정의를 만든다.
- 저장 프로시저는 채팅에 문장으로 요청하며, 입력 매개변수와 포함할 정보까지 구체적으로 적을수록 결과가 좋아진다.
- SQL 최적화는 인덱스 같은 내장 장치를 쓰는 방식과 기존 쿼리를 고치는 방식이 있고, Copilot은 왜 더 낫고 어떤 조건에서 그런지도 설명한다.
- Kubernetes 배포 명세는 원하는 상태를 자연어로 적으면 YAML로 나오고, 실행 방법(`kubectl`)과 Python, Go 코드로의 변환까지 같은 채팅에서 이어서 요청할 수 있다.
- 정규식은 한 줄 요청으로 식, 조각별 설명, 맞는 입력과 틀린 입력을 보여 주는 사용 예까지 받는다.
- 생성된 테스트 데이터는 학습 데이터 기반이라 정확성과 최신성을 보장하지 않으며, 일부만 나오면 `remaining`으로 이어 요청하고 공개 코드와 일치해 막히면 조건을 바꿔 다시 요청한다.
- GitHub CLI에서는 `gh extension install github/gh-copilot` 설치 후 `gh copilot explain`과 `gh copilot suggest`로 명령을 설명받고 제안받는다.

---

## 2. 문서 목록

- [SQL 질의와 스키마 작성](SQL%20%EC%A7%88%EC%9D%98%EC%99%80%20%EC%8A%A4%ED%82%A4%EB%A7%88%20%EC%9E%91%EC%84%B1.md): 스키마를 컨텍스트로 삼아 조회 쿼리와 새 테이블 정의를 만드는 법
- [저장 프로시저와 SQL 최적화](%EC%A0%80%EC%9E%A5%20%ED%94%84%EB%A1%9C%EC%8B%9C%EC%A0%80%EC%99%80%20SQL%20%EC%B5%9C%EC%A0%81%ED%99%94.md): 저장 프로시저 생성, 인덱스 제안, 기존 쿼리 최적화
- [YAML과 Kubernetes](YAML%EA%B3%BC%20Kubernetes.md): 배포 명세 작성, 실행 방법, Python과 Go 코드로의 변환
- [정규식 만들기](%EC%A0%95%EA%B7%9C%EC%8B%9D%20%EB%A7%8C%EB%93%A4%EA%B8%B0.md): 사회보장번호와 국제 전화번호 검사 식과 사용 예
- [테스트 데이터 생성](%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EC%83%9D%EC%84%B1.md): 데이터 생성 프롬프트와 정확성, 일부 출력, 공개 코드 일치 문제
- [GitHub CLI와 Copilot](GitHub%20CLI%EC%99%80%20Copilot.md): 사전 준비, 명령 목록, explain과 suggest 흐름
- [정리](%EC%A0%95%EB%A6%AC.md): 장 전체 요약과 영역별 비교

<br>
<br>
<br>

[Learning GitHub Copilot](../)
