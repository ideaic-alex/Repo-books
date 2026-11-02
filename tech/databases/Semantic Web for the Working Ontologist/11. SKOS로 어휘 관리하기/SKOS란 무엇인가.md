# SKOS란 무엇인가

도서관의 주제 분류표나 회사의 표준 용어 사전을 떠올려 보자. "양", "면양", "가축" 같은 용어가 있고, 용어마다 더 넓은 말과 더 좁은 말, 비슷한 말이 정해져 있다. 이런 용어 체계를 컴퓨터 네트워크에서 주고받고 서로 연결하려고 만든 표준이 SKOS(Simple Knowledge Organization System, 단순 지식 조직 체계)다. 이 문서는 SKOS가 무엇이고 왜 만들어졌는지, 그리고 실제 사례인 AGROVOC 어휘 일부를 Turtle로 어떻게 쓰는지 살펴본다.

SKOS는 앞 장들에서 배운 RDF, RDFS, RDFS-Plus 기능을 그대로 가져다 쓴다. 그래서 SKOS로 만든 어휘는 다른 어휘뿐 아니라 RDF로 표현된 어떤 데이터셋과도 연결할 수 있다.

---

## 1. SKOS의 정체

SKOS는 W3C(World Wide Web Consortium)의 권고안(Recommendation)이다. 통제 어휘(controlled vocabulary, 쓸 말을 미리 정해 둔 용어 목록), 시소러스(thesaurus, 용어 사이의 상하·유사 관계를 정리한 사전), 분류 체계(taxonomy), 폭소노미(folksonomy, 사용자가 자유롭게 붙인 태그 체계) 같은 "지식 조직 체계"를 분산되고 연결 가능한 방식으로 표현하는 수단이다.

이런 체계는 도서관학에서 오래전부터 형식을 갖춰 써 왔다. 하지만 이를 컴퓨터 네트워크에서 표현하고 교환하는 수단은 없었다.

### 이미 시소러스 표준이 있는데 왜 또 만들었나

시소러스 표준은 여러 개 있다. 그런데도 SKOS가 나온 까닭은 SKOS가 시맨틱 웹 위에서 출발했다는 점에 있다.

- 처음부터 웹 전체에서 재사용하고 참조할 수 있는 모듈형 지식 조직을 만들 수 있게 설계했다.
- 기존 표준을 대체하려는 것이 아니다. 기존 표준에 시맨틱 웹의 분산 성격을 더해 주는 것이 목적이다.
- 어떤 시소러스 표준이든 SKOS로 꽤 쉽게 옮길 수 있도록 하는 것도 설계 목표였다.

| 구분 | 기존 시소러스 표준 | SKOS |
|---|---|---|
| 기반 | 웹 이전에 설계된 형식이 많다 | RDF, RDFS, 링크드 데이터 |
| 다른 어휘와 연결 | 설계 목표가 아니었다 | 용어마다 URI가 있어 웹에서 참조 가능 |
| 역할 | 각자 독립된 표준 | 기존 표준을 대체하지 않고 보강 |
| 연결 대상 | 같은 계열의 어휘 | 어휘뿐 아니라 RDF로 된 모든 데이터셋 |

표를 읽는 법은 간단하다. SKOS의 차별점은 용어 하나하나가 웹 주소(URI)를 갖고 RDF 위에 올라간다는 것이고, 그 덕에 어휘끼리 서로 링크를 걸 수 있다.

---

## 2. 사례: AGROVOC

유엔 식량농업기구(FAO)는 오랫동안 AGROVOC라는 시소러스를 관리해 왔다. 농업 관련 문서를 분류하는 용도다. 이 시소러스의 SKOS 공개본에서 개념 여섯 개를 뽑아 보면 구조가 한눈에 들어온다. 이 개념들은 SKOS 핵심 어휘에 정의된 여러 속성으로 서로 연결된다. 각 속성은 다른 속성과의 관계 속에서 정의되어 있어서, 몇 가지 유용한 추론이 가능하다.

여섯 개념은 다음과 같다.

| 식별자 | 영어 대표 이름 | 프랑스어 대표 이름 | 비고 |
|---|---|---|---|
| agrovoc:c_4397 | Livestock | Bétail | 대체 이름 Animal stock, Farm animals |
| agrovoc:c_7030 | Sheep | Ovin | 대체 이름 Ovis aries. 위로 c_4397, 아래로 나머지 넷 |
| agrovoc:c_2746 | Ewes | Brebis | 대체 이름 Gimmers, Ewe hoggs, Antenaise(프랑스어) |
| agrovoc:c_4163 | Lambs | Agneau | |
| agrovoc:c_6443 | Rams | Bélier | 대체 이름 Tups |
| agrovoc:c_8369 | Wethers | Mouton | 대체 이름 Wether hoggs, Hoggets. 설명 노트 있음 |

개념 사이의 관계는 Sheep이 Livestock 아래에 있고, Ewes·Rams·Wethers·Lambs가 Sheep 아래에 있는 2단 트리다.

일부를 Turtle로 쓰면 이렇다.

```turtle
agrovoc:c_4397 a skos:Concept ;
    skos:prefLabel "Bétail"@fr , "Livestock"@en ;
    skos:altLabel "Animal stock"@en , "Farm animals"@en .

agrovoc:c_7030 a skos:Concept ;
    skos:prefLabel "Sheep"@en , "Ovin"@fr ;
    skos:altLabel "Ovis aries"@en , "Ovis aries"@fr ;
    skos:broader agrovoc:c_4397 ;
    skos:narrower agrovoc:c_2746 , agrovoc:c_6443 ,
                  agrovoc:c_8369 , agrovoc:c_4163 .
```

첫 블록은 Livestock 개념이고, 둘째 블록은 Sheep 개념이다. Sheep은 위로 Livestock을 `skos:broader`로 가리키고, 아래로 네 개념을 `skos:narrower`로 가리킨다. 나머지 네 개념(Ewes, Lambs, Rams, Wethers)도 같은 형태로 `a skos:Concept`와 라벨들을 갖는다. Wethers 개념에는 `skos:scopeNote`로 "거세한 수컷 양"이라는 설명이 영어와 프랑스어로 붙어 있다.

---

## 3. 개념(Concept)은 클래스와 무엇이 다른가

`skos:Concept`을 처음 보면 RDFS의 클래스와 같은 것인지 헷갈린다. 비유하자면 클래스는 "수학 집합"에 가깝고, 개념은 "도서관 서가의 분류 표지"에 가깝다.

- SKOS의 동기는 도서관학이다. 출판물을 설명하는 방법이 필요했고, 개념은 그 한 가지 방법이다.
- RDFS의 클래스와 달리 개념에는 수학적으로 엄밀한 대응물이 없다. 개념은 출판물을 분류하는 범주일 뿐이다.
- 그래서 SKOS의 용어는 RDFS나 OWL의 용어만큼 엄격한 정의를 갖지 않는다.
- 다만 SKOS는 개념이 어떻게 동작하고 서로 어떻게 연결되는지를 RDFS-Plus의 형식적 구조로 정의한다. 이 내용은 뒤 문서들에서 차례로 본다.

| 비교 항목 | RDFS 클래스 | SKOS 개념 |
|---|---|---|
| 용도 | 개체를 묶는 집합 | 출판물 등을 분류하는 범주 |
| 수학적 대응 | 집합 | 없음 |
| 정의의 엄격함 | 엄격하다 | 상대적으로 느슨하다 |

---

## 4. 다국어와 식별자

AGROVOC은 영어, 프랑스어 등 여러 언어로 관리된다. 개념마다 여러 언어의 라벨이 있고, 어느 언어도 다른 언어보다 우선하지 않는다. 그래서 유엔은 URI를 만들 때 이름이 아니라 숫자를 쓴다. `agrovoc:c_7030`처럼 숫자 기반 식별자를 쓰고, 사람이 읽는 이름은 따로 문자열로 붙인다.

Turtle 문자열에는 선택적으로 언어 태그를 붙일 수 있다. XML 표준에서 가져온 방식이며, `"Sheep"@en`은 영어, `"Ovin"@fr`은 프랑스어를 뜻한다. 이 예제에서는 영어(en)와 프랑스어(fr) 라벨만 남겼다.

이름을 URI에 넣어 버리면 그 언어가 다른 언어보다 앞서는 셈이 되므로 숫자를 쓴다.

다음 문서에서는 이 예제에 나온 `prefLabel`, `altLabel`을 비롯한 라벨 속성을 자세히 본다.

<br>
<br>
<br>

[Semantic Web for the Working Ontologist](../)
