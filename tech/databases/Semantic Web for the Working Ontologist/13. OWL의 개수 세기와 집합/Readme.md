# OWL의 개수 세기와 집합

이 장은 OWL이 12장의 제약 위에 얹은 집합 언어와 개수 세기 기능을 다룬다. 합집합, 교집합, 여집합으로 클래스와 제약을 조합하고, 개체를 열거하거나 서로 다르다고 선언해 열린 세계의 일부를 닫는 방법을 본다. 이어서 기수 제약으로 개수를 세는 추론, 서로소 클래스, 선수 조건 모델링을 살핀다.

장의 후반은 모델이 스스로의 문제를 드러내는 방식을 다룬다. 모순과 만족 불가능한 클래스를 짚고, 정의만으로 클래스 사이의 관계를 추론하는 방법과 개체 추론과 클래스 추론의 차이를 설명한다. 책은 제임스 딘의 영화를 두고 나누는 대화로 이 내용을 이끌어 간다.

---

## 1. 핵심 요점

- OWL은 owl:unionOf, owl:intersectionOf, owl:complementOf로 클래스와 제약을 집합처럼 조합한다. 여집합은 단독으로 쓰면 범위가 우주 전체로 넓어지므로 보통 교집합과 함께 쓴다.
- owl:oneOf는 클래스의 멤버를 전부 나열해 그 부분만 세계를 닫는다. 멤버가 서로 다르다는 보장은 주지 않으므로 owl:differentFrom이나 owl:AllDifferent가 따로 필요하다.
- 기수 제약(owl:cardinality, minCardinality, maxCardinality)은 속성의 서로 다른 값의 개수로 클래스를 정한다. 비유일 이름 가정 때문에 개수를 세려면 개체가 서로 다르다는 선언이 꼭 필요하다.
- 한정 기수(OWL 2.0)는 owl:onClass로 지정한 클래스의 값만 센다. 0과 1 같은 작은 기수는 필수, 유일, 금지 같은 의미로 쓴다.
- owl:disjointWith와 owl:AllDisjointClasses는 클래스 단위의 differentFrom 구실을 하며, someValuesFrom과 함께 최소 개수를 이끌어 낸다.
- allValuesFrom은 값의 존재를 보장하지 않지만 someValuesFrom과 hasValue는 보장한다. 기수 0이나 개수 세기로 "조건이 모두 충족되었다"를 추론할 수 있다.
- 단언들이 함께 참일 수 없으면 모순이고, 멤버가 있을 수 없는 클래스는 만족 불가능하다. 이 상태는 하위 클래스, someValuesFrom, 정의역과 치역, 서로소의 교집합을 통해 번진다.
- OWL은 정의만으로 클래스 관계를 추론한다(T-box 추론). 개체 추론(A-box)과 달리 데이터 없이도 가능해서 모델의 컴파일처럼 동작한다.

---

## 2. 문서 목록

- [합집합과 교집합](%ED%95%A9%EC%A7%91%ED%95%A9%EA%B3%BC%20%EA%B5%90%EC%A7%91%ED%95%A9.md): unionOf와 intersectionOf, 제약과의 조합, 우선순위가 높은 후보 질문 예제
- [세계 닫기와 열거](%EC%84%B8%EA%B3%84%20%EB%8B%AB%EA%B8%B0%EC%99%80%20%EC%97%B4%EA%B1%B0.md): oneOf, differentFrom, AllDifferent로 열린 세계를 닫고 소거법으로 추론하기
- [기수 제약](%EA%B8%B0%EC%88%98%20%EC%A0%9C%EC%95%BD.md): cardinality, min/max, 한정 기수, 0과 1의 쓰임, 제임스 딘 영화 개수 세기
- [여집합과 서로소 집합](%EC%97%AC%EC%A7%91%ED%95%A9%EA%B3%BC%20%EC%84%9C%EB%A1%9C%EC%86%8C%20%EC%A7%91%ED%95%A9.md): complementOf의 함정, disjointWith, AllDisjointClasses, 영화 개수 세기
- [선수 조건 다시 보기](%EC%84%A0%EC%88%98%20%EC%A1%B0%EA%B1%B4%20%EB%8B%A4%EC%8B%9C%20%EB%B3%B4%EA%B8%B0.md): 선수 조건이 없는 경우와 개수를 세는 방법, 값의 존재 보장 비교
- [모순과 만족 불가능한 클래스](%EB%AA%A8%EC%88%9C%EA%B3%BC%20%EB%A7%8C%EC%A1%B1%20%EB%B6%88%EA%B0%80%EB%8A%A5%ED%95%9C%20%ED%81%B4%EB%9E%98%EC%8A%A4.md): 모순, 만족 불가능한 클래스, 전파 경로
- [클래스 관계 추론](%ED%81%B4%EB%9E%98%EC%8A%A4%20%EA%B4%80%EA%B3%84%20%EC%B6%94%EB%A1%A0.md): 하위 클래스 추론 패턴, 객체지향과의 차이, 야구 모델, A-box와 T-box
- [요약과 핵심 개념](%EC%9A%94%EC%95%BD%EA%B3%BC%20%ED%95%B5%EC%8B%AC%20%EA%B0%9C%EB%85%90.md): 장 요약, 핵심 개념 표, 다음 장 안내

<br>
<br>
<br>

[Semantic Web for the Working Ontologist](../)
