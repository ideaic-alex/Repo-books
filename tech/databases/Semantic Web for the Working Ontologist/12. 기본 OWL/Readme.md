# 기본 OWL

이 장은 RDFS-Plus에서 한 걸음 나아가 OWL의 핵심 도구인 제한(owl:Restriction)을 배운다. 제한은 "이 속성을 이런 식으로 가진 개체들"이라는 묘사로 새 클래스를 만들게 해 준다. 질문지 예시를 따라가며 someValuesFrom, allValuesFrom, hasValue 세 가지 제한을 차례로 익힌다.

이어서 채식주의자 문제, 표 데이터 자동 분류, 클래스-개체 거울 패턴, FOAF 관계 전달 같은 도전 문제를 풀고, OWL 문헌에서 쓰이는 "필요 조건, 충분 조건" 용어를 정리한다.

---

## 1. 핵심 요점

- OWL의 owl:Restriction은 속성 값에 거는 조건으로 이름 없는 클래스를 만드는 도구이며, owl:onProperty로 어떤 속성을 제한하는지 지정한다.
- someValuesFrom은 "값 중 적어도 하나가 클래스 C의 구성원", allValuesFrom은 "값이 있다면 모두 C의 구성원", hasValue는 "특정한 값 A를 가진다"는 조건이다.
- allValuesFrom은 값이 존재한다는 보장이 없고, 제한 클래스 구성원의 값을 모두 C의 구성원으로 추론하게 한다. hasValue는 someValuesFrom의 특수한 경우다.
- 제한을 이름 있는 클래스와 equivalentClass로 묶으면 값에서 클래스로, 클래스에서 값으로 양방향 추론이 된다. subClassOf로 묶으면 한 방향이다.
- rdfs:domain과 range는 전역 규칙이라 부작용이 생기지만, 제한을 클래스에 걸면 해당 구성원에게만 적용되는 로컬 규칙을 만들 수 있다.
- hasValue 제한으로 표의 열 값에 따라 행의 타입을 자동으로 정할 수 있고, 같은 방식이 클래스-개체 거울 패턴이 된다.
- 열린 세계 가정 때문에 "선행 조건이 모두 충족됐는지"는 이 장의 도구만으로 판단하기 어렵고, 개수를 말하는 기수 제한이 필요하다.
- 필요 조건, 충분 조건, 부분 정의, 완전 정의는 일관되지 않게 쓰이므로 subClassOf와 equivalentClass를 그대로 쓰라고 권한다.

---

## 2. 문서 목록

- [제한이란 무엇인가](%EC%A0%9C%ED%95%9C%EC%9D%B4%EB%9E%80%20%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80.md): OWL 버전, 제한이 필요한 이유, 정의와 구성, 이름 없는 클래스
- [someValuesFrom과 답변한 질문](someValuesFrom%EA%B3%BC%20%EB%8B%B5%EB%B3%80%ED%95%9C%20%EC%A7%88%EB%AC%B8.md): 질문지 예시의 데이터 모양, hasSelectedOption, someValuesFrom, AnsweredQuestion 추론
- [allValuesFrom과 질문 의존 관계](allValuesFrom%EA%B3%BC%20%EC%A7%88%EB%AC%B8%20%EC%9D%98%EC%A1%B4%20%EA%B4%80%EA%B3%84.md): allValuesFrom, enablesCandidate로 질문 열기, 선행 질문과 열린 세계 문제
- [hasValue와 우선순위 질문](hasValue%EC%99%80%20%EC%9A%B0%EC%84%A0%EC%88%9C%EC%9C%84%20%EC%A7%88%EB%AC%B8.md): hasValue, 우선순위 클래스, 양방향 추론, 세 제한 비교
- [채식주의자 문제와 로컬 범위 제한](%EC%B1%84%EC%8B%9D%EC%A3%BC%EC%9D%98%EC%9E%90%20%EB%AC%B8%EC%A0%9C%EC%99%80%20%EB%A1%9C%EC%BB%AC%20%EB%B2%94%EC%9C%84%20%EC%A0%9C%ED%95%9C.md): domain과 range의 부작용, allValuesFrom으로 구성원에게만 거는 규칙
- [표 데이터 자동 분류](%ED%91%9C%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EC%9E%90%EB%8F%99%20%EB%B6%84%EB%A5%98.md): 표를 가져올 때 열 값으로 타입을 정하는 hasValue 해법
- [클래스-개체 거울 패턴과 관계 전달](%ED%81%B4%EB%9E%98%EC%8A%A4-%EA%B0%9C%EC%B2%B4%20%EA%B1%B0%EC%9A%B8%20%ED%8C%A8%ED%84%B4%EA%B3%BC%20%EA%B4%80%EA%B3%84%20%EC%A0%84%EB%8B%AC.md): ADA90 정책, FOAF 그룹, 족보 예시
- [필요 조건과 충분 조건 용어](%ED%95%84%EC%9A%94%20%EC%A1%B0%EA%B1%B4%EA%B3%BC%20%EC%B6%A9%EB%B6%84%20%EC%A1%B0%EA%B1%B4%20%EC%9A%A9%EC%96%B4.md): subClassOf, equivalentClass와 문헌 용어의 대응
- [요약과 핵심 개념](%EC%9A%94%EC%95%BD%EA%B3%BC%20%ED%95%B5%EC%8B%AC%20%EA%B0%9C%EB%85%90.md): 장 요약, 핵심 개념, 복습 표, 다음 장 안내

<br>
<br>
<br>

[Semantic Web for the Working Ontologist](../)
