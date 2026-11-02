# SKOS 무결성 검사

SKOS의 많은 부분은 추론으로 정의되지 않고 관례에 맡겨져 있다. 그래도 SKOS에는 어떤 SKOS 모델이든 표준을 지키는지 점검할 수 있는 무결성 조건(integrity conditions)이 있다. 입력 폼에서 "필수 항목", "중복 금지" 같은 규칙을 거는 것과 비슷한 역할이다. 이 문서는 그 조건이 어떤 성격인지, 그리고 RDFS와 SPARQL ASK로 어떻게 표현하는지 예제로 살펴본다.

---

## 1. 무결성 조건의 성격

- 이 조건들은 규범적(normative)이다. 조건을 위반한 모델은 표준을 따른다고 말할 수 없다.
- SKOS 핵심 온톨로지에는 이런 조건이 46개 있다. 원서는 모두 다루지 않고 몇 개만 살펴 SKOS가 어떻게 쓰이도록 의도됐는지를 보여 준다.
- 이 조건의 표현 수단은 두 가지다. RDFS로 쓸 수 있는 것은 RDFS로, 나머지는 SPARQL로 쓴다.

---

## 2. RDFS로 표현되는 조건

앞서 본 속성 구조(그림 11.2의 모든 관계)는 SKOS 제약의 일부다. 여기에 도메인과 레인지(domain/range, 속성의 주어와 목적어가 속해야 할 클래스) 정보가 더해진다.

```turtle
skos:inScheme rdfs:range skos:ConceptScheme .
skos:semanticRelation rdfs:domain skos:Concept .
skos:semanticRelation rdfs:range skos:Concept .
```

| 선언 | 의미 |
|---|---|
| `skos:inScheme`의 range가 `skos:ConceptScheme` | 개념 C가 체계 S에 속하면 S는 `skos:ConceptScheme`의 구성원이어야 한다 |
| `skos:semanticRelation`의 domain이 `skos:Concept` | 의미 관계의 주어는 개념이어야 한다 |
| `skos:semanticRelation`의 range가 `skos:Concept` | 의미 관계의 목적어도 개념이어야 한다 |

`skos:semanticRelation`의 하위 속성에는 broader, narrower, related와 모든 매칭 속성이 포함된다. 따라서 이 속성들로 이어진 두 리소스는 모두 `skos:Concept`의 구성원이다.

---

## 3. SPARQL ASK로 표현되는 조건

RDFS로 쓰기 어려운 조건은 SPARQL로 쓴다. ASK 질의는 참/거짓을 돌려준다. 여기서는 "제약 위반이 있으면 참"이 되도록 짠다. 참이 나오면 문제가 있다는 신호다.

### 예 1. 언어별 대표 이름은 하나

한 리소스는 언어 태그 하나당 `skos:prefLabel`을 한 개까지만 가질 수 있다.

```sparql
ASK
WHERE { ?c skos:prefLabel ?l1 .
        ?c skos:prefLabel ?l2 .
        FILTER ( lang(?l1) = lang(?l2) )
        FILTER ( ?l1 != ?l2 )
}
```

`lang(?x)`는 문자열의 언어 태그를 돌려주는 함수다(영어면 "en", 프랑스어면 "fr"). 같은 개념에 언어 태그는 같고 문자열은 다른 대표 이름이 둘 있으면 이 질의가 참이 되어 위반을 알린다.

### 예 2. related와 broader는 함께 쓰지 않는다

`skos:related`와 `skos:broaderTransitive`는 서로소(disjoint)로 정해져 있다. 두 개념이 related이면 한쪽이 다른 쪽의 broader일 수 없다.

```sparql
ASK
WHERE { ?a skos:related ?b .
        ?a skos:broader* ?b }
```

`?a`와 `?b`가 related인데 한쪽이 다른 쪽보다 (전이적으로) broader이면 위반이다. 속성 경로 `skos:broader*`는 broader를 0번 이상 따라가는 경로를 뜻한다.

| 위반 사례 | 검사 방법 | 이유 |
|---|---|---|
| 같은 언어의 대표 이름이 둘 | ASK와 `lang()` 비교 | 개념의 공식 이름은 언어마다 하나여야 한다 |
| related이면서 broader 관계 | ASK와 `skos:broader*` | 위아래 관계가 있으면 따로 related로 잇는 중복을 피한다 |
| 의미 관계의 양 끝이 개념이 아님 | RDFS domain/range | 관계는 개념끼리만 잇는다 |

---

## 4. 무결성 조건이 지키려는 것

SKOS의 무결성 제약은 어휘가 질서 있게 유지되어 정보 검색 환경에서 쓰고 다시 쓰기 좋게 만든다. 한 개념이 같은 언어에 대표 이름을 둘 갖는 것은 곤란하다. 한 개념이 다른 개념의 broader임을 이미 알면 이를 줄여 쓰려고 related로 한 번 더 잇는 일은 필요 없다.

<br>
<br>
<br>

[Semantic Web for the Working Ontologist](../)
