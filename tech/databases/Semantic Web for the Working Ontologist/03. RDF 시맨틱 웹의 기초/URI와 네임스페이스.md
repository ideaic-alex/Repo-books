# URI와 네임스페이스

두 그래프를 합치려면 "이 노드와 저 노드가 같은 것인가"를 판단해야 한다. RDF는 이 문제를 웹이 이미 풀어 둔 방법, 곧 URI로 푼다. 이 문서는 URI와 URL의 관계, IRI, 지면에서 쓰는 줄임 표기인 CURIE, 네임스페이스의 쓰임, W3C가 정한 표준 네임스페이스, 그리고 rdf:type과 rdf:Property를 다룬다.

---

## 1. 왜 "Shakespeare"라는 이름만으로는 부족한가

지금까지 그림에서는 노드와 간선을 Shakespeare나 Wales 같은 간단한 이름으로 적었다. 하지만 웹 규모에서는 이 이름만으로 같은 것인지 판단할 수 없다. "세상에 셰익스피어는 한 명뿐이고 모두가 그 사람을 말하는 것 아닌가?"라는 생각이 들 수 있다. 책은 웹에서 합의를 말할 때 "모두"라는 말은 절대 쓰지 말라고 경고한다. 어딘가에서는 누군가가 역사 속의 셰익스피어가 아니라 영화 「셰익스피어 인 러브」의 주인공을 가리킬 것이고, 그 인물은 실제 인물과 거의 닮지 않았다. 게다가 셰익스피어는 웹에서 꽤 안정적인 개념이다. "Washington"이나 "Bordeaux" 같은 이름은 가리키는 대상이 훨씬 다양하다.

비유하면 회사 안에서 "김 대리"라고만 부르면 되지만, 전국 규모 명단에서는 "김 대리"로 누군지 알 수 없는 것과 같다. 사번 같은 전역 식별자가 필요하다. 그래서 그래프를 합칠 때는 "Shakespeare를 어떤 뜻으로 쓰는가"를 구체적으로 밝혀야 한다.

---

## 2. URI와 URL

RDF는 이 문제의 해법을 웹의 기초 기술에서 빌려 온다. 그것이 URI(Uniform Resource Identifier, 통합 자원 식별자)다. URI는 자원을 가리키는 전역 이름이다. 일반 사용자에게도 URL의 형태로 익숙하다. 책의 예시는 다음과 같다.

```text
http://www.workingontologist.org/Examples/Chapter3/Shakespeare#Shakespeare
```

URI가 웹 전체에서 공통인 식별자라는 점은 시맨틱 웹만의 약속이 아니라 웹 전체의 약속이다. 이름이 전역이면 효과도 전역으로 퍼진다. 물론 정글 같은 웹에서 셰익스피어를 말하는 모든 데이터 출처가 같은 URI를 쓰리라고 기대할 수는 없다. 같은 개체에 다른 URI가 붙는 경우와, 그때 시맨틱 웹이 제공하는 해법은 5장에서 다룬다.

URL은 URI의 특수한 경우이고 둘은 겉으로 똑같아 보인다. 왜 두 개념이 따로 있을까. 조금 단순하게 말하면 다음과 같다.

- URI는 전 세계 어디서든 통하는 식별자다. 서로 다른 두 웹 애플리케이션이 같은 URI를 쓰면 같은 대상을 말하는 것이다.
- URI 문법은 서버 이름, 프로토콜, 포트 번호, 파일 이름 같은 정보를 담을 수 있어서 역참조(dereference)가 가능하다. 즉 URI에 담긴 정보를 모두 써서 웹 위의 파일이나 파일 속 위치를 찾아갈 수 있다.

역참조는 모든 부분이 제대로 동작할 때 성공한다. 프로토콜이 지정된 포트에서 돌아가는 지정된 서버를 찾아내는 식이다. 그렇게 되면 그 URI는 단순한 URI를 넘어 유효한 HTTP URI가 된다. 모델링 관점에서는 이 차이가 중요하지 않다. 하지만 모델이 전역 웹 인프라에 참여하려면 URI를 역참조할 수 있다는 점이 큰 의미를 가진다. 이 내용은 5장에서 이어진다. 또 URI가 가리키는 자원은 파일만이 아니라는 점도 책은 각주로 덧붙인다. 위키백과의 URI 스킴 문서에는 50가지가 넘는 자원 종류가 나와 있다.

| 개념 | 한 줄 정의 | 비고 |
| --- | --- | --- |
| URI | 자원을 가리키는 전역 식별자 | 같은 URI는 어디서나 같은 대상 |
| URL | 위치를 찾아갈 수 있는 URI | URI의 특수한 경우 |
| 역참조 | URI의 정보로 웹의 파일이나 위치를 찾아가는 일 | 서버·프로토콜·포트 등이 모두 맞아야 성공 |
| 유효한 HTTP URI | 역참조에 성공하는 URI | 모델링에는 필수가 아니나 웹 통합에는 중요 |
| IRI | URI를 확장해 모든 언어의 문자를 쓰게 한 것 | 아래에서 설명 |

IRI(Internationalized Resource Identifier, 국제화 자원 식별자)는 URI를 일반화한 것이다. 웹에서 표준 인코딩이 있는 모든 언어의 문자를 쓸 수 있어서, 악센트가 붙은 글자처럼 다른 언어의 문자도 식별자에 넣을 수 있다.

---

## 3. 노드가 같다는 것의 기준

RDF가 URI를 쓰는 방식은 단순하다. 한 그래프의 노드와 다른 그래프의 노드는 URI가 같을 때, 그리고 같을 때만 합쳐진다.

"정체성 문제를 다른 표준에 떠넘겨서 푸는 척하는 것 아닌가"라고 느낄 수 있다. 책도 그런 인상을 인정한다. 하지만 정체성 문제는 시맨틱 웹만이 아니라 웹 전체에 있는 문제이므로, 같은 전략으로 푸는 것이 합리적이라는 입장이다. 바퀴를 새로 만들 이유가 없다.

---

## 4. 지면에서 쓰는 줄임 표기 CURIE

URI를 있는 그대로 적으면 모델을 쓸 때, 특히 인쇄물에서 번거롭다. 그래서 책은 CURIE(Compact URI, 줄인 URI)를 단순화한 형태로 쓴다. 기본형은 네임스페이스와 식별자를 콜론으로 이은 것이다. geo라는 네임스페이스 안의 England라는 식별자는 `geo:England`로 쓴다.

RDF 표준 문법에는 이런 네임스페이스를 `http://` 형태의 전체 URI와 이어 주는 규칙이 자세히 있지만, 책에서는 모든 URI를 단순한 CURIE로 적는다. 다만 기억할 점이 있다. CURIE 자체는 웹의 전역 식별자가 아니다. 전체를 풀어 쓴 URI(예: `http://www.WorkingOntologist.org/Examples/Chapter3/Shakespeare#Shakespeare`)만 전역 이름이다. 따라서 CURIE를 쓸 때는 원칙적으로 네임스페이스 대응 선언이 함께 있어야 한다.

### 4.1 이름 짓기 관례

URI에는 공백을 넣지 않는 것이 웹의 관습이다. 그래서 "part of" 같은 이름은 쓰지 않는다. 대신 여러 단어를 이어 붙이고 각 단어의 첫 글자를 대문자로 쓰는 InterCap(CamelCase) 관례를 따른다.

| 원래 표현 | 식별자 |
| --- | --- |
| part of | partOf |
| Great Britain | GreatBritain |
| Measure for Measure | MeasureForMeasure |

### 4.2 네임스페이스 쓰는 법

한 데이터 안에서, 심지어 트리플 하나 안에서도 여러 네임스페이스를 섞어 쓸 수 있다. 데이터 모델과 표준은 네임스페이스 선택에 제한을 두지 않는다. 다만 관련 있는 식별자는 한 네임스페이스에 모으는 것이 보통이다. 예를 들어 문학 정보는 lit, 지리 정보는 geo라는 이름으로 모은다. 엄밀히는 이 이름이 각각 다음 전체 URI를 줄여 쓴 것이다.

| 접두어 | 줄여 쓴 전체 URI |
| --- | --- |
| lit | `http://www.WorkingOntologist.com/Examples/Chapter3/Shakespeare#` |
| geo | `http://www.WorkingOntologist.com/Examples/Chapter3/geography#` |

모델링을 설명할 때는 CURIE 뒤의 자세한 URI가 중요하지 않으므로 앞으로는 대부분 생략한다. 한 예시에서 네임스페이스를 하나만 쓴다면 기본 네임스페이스가 선언되어 있다고 보고, 콜론으로 시작하는 `:Shakespeare`, `:JamesDean`, `:Researcher` 같은 이름을 쓴다. 책에서는 접두어가 활자로 정의되지 않았더라도 모두 정의되어 있다고 가정한다.

### 4.3 CURIE로 쓴 트리플

앞의 두 목록(희곡과 지리)을 CURIE로 쓰면 이렇다.

| 주어 | 서술어 | 목적어 |
| --- | --- | --- |
| lit:Shakespeare | lit:wrote | lit:AsYouLikeIt |
| lit:Shakespeare | lit:wrote | lit:HenryV |
| geo:Scotland | geo:partOf | geo:UK |
| geo:NorthernIreland | geo:partOf | geo:UK |

(전체 목록은 원문의 희곡 8개와 지역 6개이며 위 표는 일부만 보인 것이다.)

항상 이렇게 단순하지는 않다. 한 트리플 안에 서로 다른 네임스페이스가 섞이는 경우가 흔하다. 책의 예에서는 새 네임스페이스 bio가 등장한다.

| 주어 | 서술어 | 목적어 |
| --- | --- | --- |
| lit:Shakespeare | lit:wrote | lit:KingLear |
| lit:Shakespeare | lit:wrote | lit:MacBeth |
| bio:AnneHathaway | bio:married | lit:Shakespeare |
| bio:AnneHathaway | bio:livedWith | lit:Shakespeare |
| lit:Shakespeare | bio:livedIn | geo:Stratford |
| geo:Stratford | geo:isIn | geo:England |
| geo:England | geo:partOf | geo:UK |
| geo:Scotland | geo:partOf | geo:UK |

세 번째 줄은 주어가 bio, 목적어가 lit에서 온다. 이렇게 여러 출처의 어휘를 한 문장 안에서 섞어 쓰는 것이 흔하다. 이 모델이 실제 웹에서 동작하려면 bio가 가리키는 URI를 채워야 하지만, 모델링 관점에서는 중요하지 않다.

---

## 5. 표준 네임스페이스

URI가 전 세계 어디서나 같은 뜻이라는 성질은 표준 기관에도 쓸모가 있다. W3C(World Wide Web Consortium) 같은 기관이 표준 안의 용어 뜻을 정해 놓을 수 있다. 앞으로 보게 될 type, subClassOf, Class, inverseOf 같은 말이 그런 예다. 이 용어도 특별 대우를 받는 예약어가 아니라 다른 자원과 똑같이 URI로 가리킨다. W3C는 웹 기술용 표준 네임스페이스를 여럿 정해 두었고(XML 스키마 정의용 `xsd:`, XML 네임스페이스용 `xmlns:` 등), 시맨틱 웹의 주요 층에도 같은 방식으로 네임스페이스가 있다.

| 접두어 | 용도 | 전체 URI |
| --- | --- | --- |
| rdf: | RDF에서 쓰는 식별자. 정의된 식별자는 아주 적고 RDF의 타입과 속성을 정의하는 데 쓴다 | `http://www.w3.org/1999/02/22-rdf-syntax-ns#` |
| rdfs: | RDFS(RDF Schema)의 식별자. 범위와 의미는 이후 장에서 다룬다 | `http://www.w3.org/2000/01/rdf-schema#` |
| skos: | SKOS(Simple Knowledge Organization System)의 식별자. 웹에서 어휘를 분산 관리하는 스키마이며 11장에서 자세히 다룬다 | `http://www.w3.org/2004/02/skos/core#` |
| owl: | OWL의 식별자. 범위와 의미는 이후 장에서 다룬다 | `http://www.w3.org/2002/07/owl#` |

이 URI들은 URI와 URL이 어떻게 맞물리는지 보여 주는 좋은 예다. 모델링 관점에서는 이 네임스페이스에 속한 URI(예: `http://www.w3.org/2000/01/rdf-schema#subClassOf`, 줄여서 `rdfs:subClassOf`)는 W3C가 RDFS 표준에서 뜻을 정해 둔 특정 용어를 가리킬 뿐이다. 한편 이 URI는 역참조도 된다. www.w3.org 서버의 2000/01/rdf-schema 위치에 가면 subClassOf에 대한 항목이 있고 보충 정보가 적혀 있다. 모델링에는 역참조가 필수가 아니지만, 웹 통합 관점에서는 역참조가 될 수 있다는 점이 결정적이다. 이렇게 링크드 데이터의 웹을 엮는 원칙은 5장에서 설명한다.

---

## 6. rdf 네임스페이스의 식별자

RDF 데이터 모델은 트리플과 트리플 집합의 병합이라는 개념을 정한다. 거기에 네임스페이스를 더하면 RDF는 웹 인프라를 이용해 "어떤 대상을 어떻게 가리킬지"에 대한 합의를 표현할 수 있다. RDF 표준도 이 인프라를 활용해, 스스로 정의한 네임스페이스 rdf에 표준 식별자 몇 개를 둔다.

### 6.1 rdf:type

rdf:type은 RDF의 기본적인 타입 체계를 이루는 속성이다. 주어는 어떤 식별자든 되고, 목적어는 타입으로 해석된다. 예를 들어 극작가들의 관계를 타입으로 나타내면 이렇다.

```turtle
lit:Shakespeare rdf:type lit:Playwright .
lit:Ibsen       rdf:type lit:Playwright .
lit:Marlowe     rdf:type lit:Playwright .
```

원문에는 Shakespeare, Ibsen, Simon, Miller, Marlowe, Wilder 여섯 명이 모두 Playwright로 나온다. rdf:type을 쓰는 데에는 제한이 없다. 타입에도 타입을 붙일 수 있고, 이것은 끝없이 이어질 수 있다. 책의 예는 다음과 같다.

```turtle
lit:Playwright rdf:type bus:Profession .
bus:Profession rdf:type hr:Compensation .
```

"Playwright는 직업(Profession)의 한 종류이고, Profession은 보수(Compensation)의 한 종류"라는 식이다. 두 번째 줄의 hr:Compensation이라는 이름은 원문 그대로이며, 이 예시는 타입의 타입이 가능하다는 것을 보이려는 것이다.

### 6.2 소리 내어 읽는 법

트리플을 영어 어순대로 읽으면 "Shakespeare type Playwright"가 되는데, 어떻게 억양을 넣어도 어색하다. "Shakespeare has type Playwright"나 "The type of Shakespeare is Playwright"가 더 자연스럽다. 이것은 rdf:type이라는 이름을 고른 W3C의 선택 때문이다. 이름이 rdf:isInstanceOf였다면 읽기 쉬웠을 것이다. 하지만 남이 정한 이름은 바꿀 수 없으니 읽을 때 "has"나 "is"를 끼워 넣어 읽는다. 뒤에서 볼 Turtle 문법에는 rdf:type 대신 `a`라는 키워드가 있어서 "Shakespeare [is] a Playwright"로 한결 읽기 쉬워진다.

### 6.3 rdf:Property

rdf:Property는 어떤 식별자가 주어나 목적어가 아니라 서술어로 쓰인다는 것을 알리는 타입이다. 지금까지 서술어로 쓴 식별자는 모두 이렇게 선언할 수 있다.

```turtle
lit:wrote   rdf:type rdf:Property .
geo:partOf  rdf:type rdf:Property .
bio:married rdf:type rdf:Property .
geo:isIn    rdf:type rdf:Property .
```

원문에는 `bio:livedIn`, `bio:livedWith`도 같은 방식으로 선언되어 있다.

| 식별자 | 하는 일 | 쓰이는 자리 |
| --- | --- | --- |
| rdf:type | 개체와 그 타입을 잇는 관계 | 서술어 |
| rdf:Property | 서술어로 쓰이는 모든 식별자의 타입 | 목적어(타입 자리) |

읽는 법은 이렇다. rdf:type은 "누구는 무엇이다"를 말하는 서술어이고, rdf:Property는 "이 이름은 서술어로 쓴다"를 알리는 타입이다. 둘 다 rdf 네임스페이스가 제공하는 몇 안 되는 식별자다.

<br>
<br>
<br>

[Semantic Web for the Working Ontologist](../)
