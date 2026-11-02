# 링크드 데이터

이 장은 RDF 데이터를 웹에서 공개하고 서로 연결하는 방법을 다룬다. 하이퍼텍스트 웹이 HTML 페이지를 링크로 엮었듯, 데이터의 웹은 HTTP URI와 RDF로 데이터를 엮는다. 팀 버너스리의 세 가지 규칙을 출발점으로, URI를 만드는 방법, 웹의 기본 구조(DNS, 콘텐츠 협상, 리디렉션), 해시 URI와 슬래시 URI의 선택, 그리고 DBLP, UniProt, DBpedia, Wikidata 같은 실제 사례를 차례로 살펴본다.

뒷부분에서는 데이터셋 사이에 링크를 거는 방법, 5스타 배포 체계와 링크드 오픈 데이터 클라우드, 그리고 HTTP 동사로 링크드 데이터를 읽고 쓰는 링크드 데이터 플랫폼(LDP)을 다룬다. 책에 실린 웹 사이트 예는 앞으로 바뀔 수 있다는 점을 책이 직접 밝히고 있다.

---

## 1. 핵심 요점

- 링크드 데이터의 세 규칙은 HTTP URI로 이름 붙이기, 접속하면 RDF 같은 표준 형식으로 설명 주기, 설명 안에 다른 HTTP URI 링크 넣기다.
- URI(Uniform Resource Identifier)는 웹에 없는 사람, 고양이, 개념에도 붙는다. 대상과 그 대상을 설명하는 문서는 서로 다른 URI를 써야 한다.
- 좋은 URI는 바뀌지 않는다(Cool URIs). 구현 세부와 버전 정보를 넣지 않고, 원본 데이터의 유일한 ID를 쓰며, CURIE를 위해 알파벳으로 시작한다.
- 웹의 세 기둥은 DNS, 콘텐츠 협상, 리디렉션이다. 도메인 통제권을 잃으면 그 도메인으로 만든 URI의 통제권도 잃는다.
- 웹에 없는 대상의 URI에는 200이나 404가 아니라 303 See Other로 설명 문서를 안내한다.
- 해시 URI는 간단하고 작은 데이터셋에 맞고, 슬래시 URI는 대상별로 조각 전송이 가능하지만 호출이 두 배다. 인위적 프래그먼트(`#this`)로 절충할 수 있다.
- 데이터셋 사이 링크는 URI 재사용, 표준으로 URI 조립, 스키마(어휘) 링크로 만든다. LOV로 기존 어휘를 찾는다.
- 5스타 체계는 웹 공개, 구조화, 비독점 형식, W3C 표준, 링크의 누적 단계다. LDP는 HTTP 동사로 컨테이너와 리소스를 읽고 쓰게 한다.

---

## 2. 문서 목록

- [웹에 데이터를 엮는다는 것](%EC%9B%B9%EC%97%90%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%A5%BC%20%EC%97%AE%EB%8A%94%EB%8B%A4%EB%8A%94%20%EA%B2%83.md): 데이터의 웹, 세 가지 규칙, URI로 이름 붙이기, 디레퍼런싱과 Follow Your Nose
- [HTTP URI 만들기](HTTP%20URI%20%EB%A7%8C%EB%93%A4%EA%B8%B0.md): URI 구조, Cool URIs, 접종 기록 예제, CURIE 제약, IETF와 DOI 사례
- [HTTP와 웹의 세 기둥](HTTP%EC%99%80%20%EC%9B%B9%EC%9D%98%20%EC%84%B8%20%EA%B8%B0%EB%91%A5.md): DNS, 콘텐츠 협상, 리디렉션과 303 See Other
- [해시 URI와 슬래시 URI](%ED%95%B4%EC%8B%9C%20URI%EC%99%80%20%EC%8A%AC%EB%9E%98%EC%8B%9C%20URI.md): 두 방식의 동작, 장단점, 선택 기준, 절충안
- [실제 링크드 데이터 둘러보기](%EC%8B%A4%EC%A0%9C%20%EB%A7%81%ED%81%AC%EB%93%9C%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EB%91%98%EB%9F%AC%EB%B3%B4%EA%B8%B0.md): DBLP, UniProt, DBpedia에서 Wikidata로 링크 따라가기
- [데이터셋 사이에 링크 걸기](%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%85%8B%20%EC%82%AC%EC%9D%B4%EC%97%90%20%EB%A7%81%ED%81%AC%20%EA%B1%B8%EA%B8%B0.md): 외부 링크 네 가지 방법, FIBO, LOV, 데이터투이 비유
- [5스타 원칙과 LOD 클라우드](5%EC%8A%A4%ED%83%80%20%EC%9B%90%EC%B9%99%EA%B3%BC%20LOD%20%ED%81%B4%EB%9D%BC%EC%9A%B0%EB%93%9C.md): 5스타 체계, LOD 클라우드, 중심 출처, LDP와 컨테이너, POST 예
- [요약과 핵심 개념](%EC%9A%94%EC%95%BD%EA%B3%BC%20%ED%95%B5%EC%8B%AC%20%EA%B0%9C%EB%85%90.md): 장 요약, 핵심 개념 네 가지, 헷갈리는 구분

<br>
<br>
<br>

[Semantic Web for the Working Ontologist](../)
