# SKOS로 어휘 관리하기

이 장은 용어 사전, 시소러스, 분류 체계 같은 통제 어휘를 웹에서 주고받고 서로 연결하는 표준인 SKOS(Simple Knowledge Organization System)를 다룬다. 유엔 식량농업기구의 농업 시소러스 AGROVOC를 예로 들어, 개념과 라벨, 상하 관계, 다른 어휘와의 매핑, 개념 체계, 무결성 조건을 차례로 살펴본다.

핵심은 SKOS가 새로운 추론 규칙을 만든 것이 아니라 앞 장에서 배운 RDFS-Plus 기능(하위 속성, 역관계, 전이성, 대칭성)을 조합해 어휘 구조를 정의했다는 점이다. 그 덕에 용어마다 URI를 가진 어휘를 웹 어디서나 참조하고 연결할 수 있다.

---

## 1. 핵심 요점

- SKOS는 통제 어휘, 시소러스, 분류 체계, 폭소노미를 분산되고 연결 가능한 방식으로 표현하는 W3C 권고안이다. 기존 시소러스 표준을 대체하지 않고 시맨틱 웹의 분산 성격을 더해 준다.
- `skos:Concept`은 RDFS 클래스와 달리 수학적 대응이 없는 분류 범주다. 다국어 어휘는 이름 대신 숫자 URI를 쓰고 언어 태그로 라벨을 붙인다.
- 라벨은 `prefLabel`, `altLabel`, `hiddenLabel` 세 가지이고 모두 `rdfs:label`의 하위 속성이다. 문서화 속성 여섯 개도 `skos:note`의 하위 속성이다.
- `broader`와 `narrower`는 서로 역관계이며 각각 전이적 상위 속성(`broaderTransitive`, `narrowerTransitive`)을 둔다. `related`는 대칭이지만 전이적이지 않다.
- `skos:broader`는 "has broader"로 읽는다. `rdfs:subClassOf` 같은 타입 전파 규칙이 없어 방향이 라벨 주석에만 의존한다.
- `exactMatch`, `closeMatch`, `broadMatch`, `narrowMatch`, `relatedMatch`는 서로 다른 어휘의 용어를 잇는다. 의미는 추론보다 정보 검색 관례에 가깝고, `owl:sameAs`보다 약한 약속이다.
- 개념 체계(`ConceptScheme`)는 권한과 작업 절차를 반영한다. 원서는 체계 단위, 소속 전파, 최상위 개념 표시에 관한 다섯 가지 권장 관행을 제안한다.
- 무결성 조건은 46개이며 RDFS의 domain/range와 SPARQL ASK로 표현한다. 단순함, 쉬운 변환, 공식 표준의 빈자리, 전역 식별자가 SKOS가 널리 쓰이는 이유다.

---

## 2. 문서 목록

- [SKOS란 무엇인가](SKOS%EB%9E%80%20%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80.md): SKOS의 목적, AGROVOC 사례, 개념과 클래스의 차이, 다국어 처리
- [라벨과 노트 속성](%EB%9D%BC%EB%B2%A8%EA%B3%BC%20%EB%85%B8%ED%8A%B8%20%EC%86%8D%EC%84%B1.md): 세 가지 라벨, rdfs:label로의 추론, 노트 속성 여섯 개
- [의미 관계와 계층](%EC%9D%98%EB%AF%B8%20%EA%B4%80%EA%B3%84%EC%99%80%20%EA%B3%84%EC%B8%B5.md): broader, narrower, related, 전이적 상위 속성 패턴, AGROVOC 추론 따라가기
- [broader를 읽는 방향](broader%EB%A5%BC%20%EC%9D%BD%EB%8A%94%20%EB%B0%A9%ED%96%A5.md): subClassOf와의 비교, 타입 전파 규칙의 부재, 읽는 방향
- [어휘 사이 매핑](%EC%96%B4%ED%9C%98%20%EC%82%AC%EC%9D%B4%20%EB%A7%A4%ED%95%91.md): 매핑 속성 다섯 가지, 관례적 의미, subPropertyOf 구조, AGROVOC-NAL 사례
- [개념 체계와 권장 관행](%EA%B0%9C%EB%85%90%20%EC%B2%B4%EA%B3%84%EC%99%80%20%EA%B6%8C%EC%9E%A5%20%EA%B4%80%ED%96%89.md): ConceptScheme, 최상위 개념, 다섯 가지 권장 관행, exactMatch와 sameAs
- [SKOS 무결성 검사](SKOS%20%EB%AC%B4%EA%B2%B0%EC%84%B1%20%EA%B2%80%EC%82%AC.md): 규범적 조건, RDFS 제약, SPARQL ASK 예제
- [SKOS가 널리 쓰이는 이유](SKOS%EA%B0%80%20%EB%84%90%EB%A6%AC%20%EC%93%B0%EC%9D%B4%EB%8A%94%20%EC%9D%B4%EC%9C%A0.md): 단순함, 변환의 쉬움, 표준의 공백, 전역 식별자
- [요약과 핵심 개념](%EC%9A%94%EC%95%BD%EA%B3%BC%20%ED%95%B5%EC%8B%AC%20%EA%B0%9C%EB%85%90.md): 장 결론, 핵심 개념, 속성 지도

<br>
<br>
<br>

[Semantic Web for the Working Ontologist](../)
