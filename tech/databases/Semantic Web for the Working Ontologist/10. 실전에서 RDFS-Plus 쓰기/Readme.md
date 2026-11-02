# 실전에서 RDFS-Plus 쓰기

이 장은 앞에서 배운 RDFS-Plus 구성 요소가 실제 서비스에서 어떻게 쓰이는지 네 가지 사례로 보여 준다. 웹 페이지에 구조화 데이터를 심는 Schema.org, 정부의 공개 데이터를 다루는 Data.gov, 사람과 관계를 설명하는 FOAF, Facebook의 Open Graph Protocol(OGP)이다. 모두 RDF 기반이고, 웹에 흩어진 데이터를 모델로 묶어 사용자 집단에 쓸모 있는 서비스를 준다.

사례마다 풀려는 문제가 달라서 모델링 선택도 다르다. 가격 같은 복합 정보의 표현, 야생 데이터의 정리와 검증, 신원 식별과 프라이버시, 단순함과 기존 어휘와의 연결을 차례로 살펴본다.

---

## 1. 핵심 요점

- Schema.org는 Google, Microsoft, Yahoo, Yandex가 만든 공용 어휘로, 가격이나 재고는 상품이 아니라 Offer에 두고 통화와 단위는 별도 노드로 표현한다.
- Schema.org는 rdfs:domain, rdfs:range의 교집합 의미 대신 합집합 의미를 위해 domainIncludes, rangeIncludes를 만들었다. 이 선언만으로는 값의 타입을 결론 낼 수 없다는 차이가 있다.
- Data.gov의 FHEO 데이터는 "1"과 빈칸으로 적힌 신고 근거를 SPARQL CONSTRUCT로 클래스 구성원으로 바꾸고, ASK와 집계 쿼리로 하위 클래스 관계가 데이터와 맞는지 검증한다.
- 카운티 이름과 주를 공통 키로 다른 데이터셋과 합치면 지도에 올릴 수 있는 결과가 나온다. 이런 매시업의 핵심 기술은 SPARQL이다.
- FOAF는 AAA 원칙 아래 어휘를 점진적으로 키운다. 이름, 별명, 홈페이지를 subPropertyOf 같은 간단한 구성 요소로 연결하고, 같은 뜻이 확인되면 equivalentProperty로 묶는다.
- FOAF는 foaf:mbox를 owl:InverseFunctionalProperty로 선언해 신원을 식별하고, 프라이버시를 위해 SHA-1 해시인 foaf:mbox_sha1sum을 둔다. foaf:knows는 일부러 느슨하게 둔다.
- foaf:Group과 foaf:membershipClass의 관계는 인스턴스를 클래스로도 보는 메타모델링의 예다.
- OGP는 단순함을 최우선으로 삼아 작은 어휘를 새로 만들고, rdfs:seeAlso로 FOAF나 지리 어휘와 느슨하게 이어 시맨틱 웹의 공존 원칙을 보여 준다.

---

## 2. 문서 목록

- [실전 사례 한눈에 보기](%EC%8B%A4%EC%A0%84%20%EC%82%AC%EB%A1%80%20%ED%95%9C%EB%88%88%EC%97%90%20%EB%B3%B4%EA%B8%B0.md): 네 사례의 공통점, 사용된 구성 요소, 각 사례가 답하는 질문
- [Schema.org로 상품과 서비스 설명하기](Schema.org%EB%A1%9C%20%EC%83%81%ED%92%88%EA%B3%BC%20%EC%84%9C%EB%B9%84%EC%8A%A4%20%EC%84%A4%EB%AA%85%ED%95%98%EA%B8%B0.md): Product와 Offer, 가격 명세, 단위 표현, Plush Beauty Bar 예제와 SPARQL 질의
- [Schema.org의 모델링 방식과 의미](Schema.org%EC%9D%98%20%EB%AA%A8%EB%8D%B8%EB%A7%81%20%EB%B0%A9%EC%8B%9D%EA%B3%BC%20%EC%9D%98%EB%AF%B8.md): domainIncludes와 rangeIncludes, rdfs:range와의 의미 차이, 적용 순서
- [열린 정부 데이터와 FHEO 사례](%EC%97%B4%EB%A6%B0%20%EC%A0%95%EB%B6%80%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%99%80%20FHEO%20%EC%82%AC%EB%A1%80.md): Data.gov, 날것 데이터, 신고 요인 클래스와 SPARQL CONSTRUCT 변환
- [관계 검증과 지도 매시업](%EA%B4%80%EA%B3%84%20%EA%B2%80%EC%A6%9D%EA%B3%BC%20%EC%A7%80%EB%8F%84%20%EB%A7%A4%EC%8B%9C%EC%97%85.md): ASK와 검증 쿼리, 결과 표, 카운티 데이터와의 결합, 집계
- [FOAF로 사람과 모임 설명하기](FOAF%EB%A1%9C%20%EC%82%AC%EB%9E%8C%EA%B3%BC%20%EB%AA%A8%EC%9E%84%20%EC%84%A4%EB%AA%85%ED%95%98%EA%B8%B0.md): AAA 원칙, Agent, 이름, 별명, 홈페이지, Group과 메타모델링, made와 maker
- [FOAF의 신원 식별과 사람 연결](FOAF%EC%9D%98%20%EC%8B%A0%EC%9B%90%20%EC%8B%9D%EB%B3%84%EA%B3%BC%20%EC%82%AC%EB%9E%8C%20%EC%97%B0%EA%B2%B0.md): 이메일과 InverseFunctionalProperty, SHA-1 해시, foaf:knows
- [Facebook Open Graph Protocol](Facebook%20Open%20Graph%20Protocol.md): like 버튼의 확장, OGP 모델, seeAlso 연결, 페이지에 심는 방법
- [요약과 핵심 개념](%EC%9A%94%EC%95%BD%EA%B3%BC%20%ED%95%B5%EC%8B%AC%20%EA%B0%9C%EB%85%90.md): Data.gov 마무리, 장 요약, 사례 비교, 핵심 개념

<br>
<br>
<br>

[Semantic Web for the Working Ontologist](../)
