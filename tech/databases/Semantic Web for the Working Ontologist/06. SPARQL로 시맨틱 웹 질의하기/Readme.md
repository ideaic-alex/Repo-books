# SPARQL로 시맨틱 웹 질의하기

RDF로 모은 데이터는 꺼내 쓸 수 있어야 쓸모가 있다. 이 장은 RDF 그래프를 위한 질의 언어 SPARQL을 다룬다. 핵심은 변수가 섞인 작은 그래프, 곧 그래프 패턴을 데이터 그래프에 맞춰 보는 것이다. 이 방식으로 표를 가져오는 SELECT, 참/거짓을 답하는 ASK, 새 트리플을 만드는 CONSTRUCT를 모두 쓴다.

앞부분은 알려주고 묻는 시스템의 구조에서 시작해 SELECT, FILTER, OPTIONAL, ASK, CONSTRUCT를 익힌다. 뒷부분은 CONSTRUCT를 규칙으로 쓰는 법, 전이 질의, 같은 대상 연결, 정렬과 집계, 서브쿼리, UNION, BIND, 그리고 여러 데이터 소스를 묶는 연합 질의로 나아간다.

---

## 1. 핵심 요점

- SPARQL은 그래프 패턴(변수를 포함한 작은 그래프)을 데이터 그래프에 맞춰 보는 질의 언어다.
- SELECT는 표를, ASK는 참/거짓을, CONSTRUCT는 새 RDF 그래프를 답으로 준다.
- OPTIONAL은 없어도 되는 정보를 덧붙이고, FILTER NOT EXISTS는 없어야 하는 조건을 건다.
- CONSTRUCT는 "조건 패턴에서 결론 트리플로"라는 규칙을 표현한다. 규칙은 필요한 만큼 좁게 적용해야 틀린 결론을 피한다.
- 속성 뒤의 `*`, `+`로 몇 단계든 이어진 관계를 따라가고, FILTER로 군더더기를 걷어 내며 같은 대상은 skos:exactMatch로 기록한다.
- ORDER BY, LIMIT, 집계(COUNT, SUM 등), GROUP BY, HAVING, 서브쿼리로 SQL 못지않은 요약 질의를 쓴다.
- UNION, BIND, VALUES로 질의의 표현력을 늘리고, SERVICE로 DBpedia 같은 원격 엔드포인트와 묶는 연합 질의를 쓴다.
- 질의의 결과는 SPARQL 프로토콜을 통해 웹으로 공개되며, 이를 제공하는 서버가 SPARQL 엔드포인트다.

---

## 2. 문서 목록

- [알려주고 묻는 시스템](%EC%95%8C%EB%A0%A4%EC%A3%BC%EA%B3%A0%20%EB%AC%BB%EB%8A%94%20%EC%8B%9C%EC%8A%A4%ED%85%9C.md): 데이터를 넣고 질문하는 시스템의 기본 구조와 SPARQL의 자리
- [SELECT와 그래프 패턴](SELECT%EC%99%80%20%EA%B7%B8%EB%9E%98%ED%94%84%20%ED%8C%A8%ED%84%B4.md): 기본 SELECT 질의, 그래프 패턴, 변수 이름의 의미
- [속성과 스키마 탐색, DISTINCT, FILTER](%EC%86%8D%EC%84%B1%EA%B3%BC%20%EC%8A%A4%ED%82%A4%EB%A7%88%20%ED%83%90%EC%83%89%2C%20DISTINCT%2C%20FILTER.md): 서술어 자리 변수로 데이터셋 탐색, 중복 제거, 조건 거르기
- [OPTIONAL, 부정, ASK](OPTIONAL%2C%20%EB%B6%80%EC%A0%95%2C%20ASK.md): 없어도 되는 정보, 없어야 하는 조건, 참/거짓 질의
- [CONSTRUCT와 결과 활용](CONSTRUCT%EC%99%80%20%EA%B2%B0%EA%B3%BC%20%ED%99%9C%EC%9A%A9.md): 새 그래프 만들기, 결과의 활용, SPARQL 프로토콜과 엔드포인트
- [SPARQL을 규칙으로 쓰기](SPARQL%EC%9D%84%20%EA%B7%9C%EC%B9%99%EC%9C%BC%EB%A1%9C%20%EC%93%B0%EA%B8%B0.md): CONSTRUCT 규칙, 삼촌 정의의 함정, 가족 관계 통일 변환
- [전이 질의와 같은 대상 찾기](%EC%A0%84%EC%9D%B4%20%EC%A7%88%EC%9D%98%EC%99%80%20%EA%B0%99%EC%9D%80%20%EB%8C%80%EC%83%81%20%EC%B0%BE%EA%B8%B0.md): `*`와 `+`, LinkedMDB의 같은 사람 연결과 FILTER 정리
- [데이터 일부 복사와 정렬, LIMIT](%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EC%9D%BC%EB%B6%80%20%EB%B3%B5%EC%82%AC%EC%99%80%20%EC%A0%95%EB%A0%AC%2C%20LIMIT.md): Unforgiven 부분 복사, ORDER BY, DESC, LIMIT
- [집계와 그룹, 서브쿼리](%EC%A7%91%EA%B3%84%EC%99%80%20%EA%B7%B8%EB%A3%B9%2C%20%EC%84%9C%EB%B8%8C%EC%BF%BC%EB%A6%AC.md): COUNT, SUM, GROUP BY, HAVING, 서브쿼리
- [UNION, BIND, VALUES, 연합 질의](UNION%2C%20BIND%2C%20VALUES%2C%20%EC%97%B0%ED%95%A9%20%EC%A7%88%EC%9D%98.md): OR 패턴, 값 계산, 질의 속 데이터, SERVICE로 DBpedia 질의
- [요약과 핵심 개념](%EC%9A%94%EC%95%BD%EA%B3%BC%20%ED%95%B5%EC%8B%AC%20%EA%B0%9C%EB%85%90.md): 장 요약, 핵심 개념, 도구 한눈에 보기

<br>
<br>
<br>

[Semantic Web for the Working Ontologist](../)
