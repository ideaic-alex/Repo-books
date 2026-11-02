# RDF 직렬화 형식

지금까지 RDF 트리플은 주어·서술어·목적어 표나 상자와 화살표 그림으로 보여 주었다. 읽기에는 쉽지만 가장 간결하거나 사람이 관계를 파악하기 좋은 형태는 아니다. 게다가 RDF를 웹에 공개하려면 텍스트 형태가 필요하다. 이 문서는 RDF를 텍스트로 적는 여러 방법, 곧 직렬화(serialization) 형식을 비교한다. N-Triples, Turtle, RDF/XML, JSON-LD, 그리고 이름 있는 그래프용 N-Quads와 TriG를 다룬다.

---

## 1. 왜 형식이 여러 개인가

같은 문장을 활자체로도, 필기체로도 쓸 수 있다. 두 글씨는 전혀 달라 보이고 각각 쓰는 이유가 있지만, 필기체를 활자체로 옮겨도 내용은 하나도 빠지지 않는다. RDF 직렬화도 마찬가지다. 같은 트리플을 어느 형식으로든 표현할 수 있고, 취향, 편의, 사용 가능한 도구 같은 사정에 따라 고른다. 한 형식에서 다른 형식으로 바꿔도 정보는 손실되지 않는다.

| 형식 | 한마디 특징 | 접두어 줄임 | 그래프 이름 |
| --- | --- | --- | --- |
| N-Triples | 가장 단순. 전체 URI를 한 줄에 트리플 하나로 | 없음 | 트리플만 표현 |
| Turtle | 사람이 읽기 좋고 간결. 이 책의 기본 | 있음 | 트리플만 표현 |
| RDF/XML | W3C가 처음 권고한 XML 형식 | XML 네임스페이스 | 책에서 다루지 않음 |
| JSON-LD | JSON 개발자를 위한 형식 | @context | 책에서 다루지 않음 |
| N-Quads | N-Triples에 그래프 이름을 더한 것 | 없음 | 넷째 값으로 표현 |
| TriG | Turtle에 그래프 이름을 더한 것 | 있음 | 중괄호 앞에 이름 |

이름 있는 그래프를 직렬화하려면 책이 소개하는 N-Quads나 TriG 같은 확장 형식을 쓴다.

---

## 2. N-Triples

가장 단순한 형식이고 원시 RDF 트리플과 가장 직접 대응한다. 자원은 생략 없는 전체 URI로 쓰며 각 URI는 꺾쇠괄호(`<`, `>`)로 감싼다. 세 자원을 주어, 서술어, 목적어 순으로 쓰고 마침표(`.`)로 끝낸다. 네임스페이스 mfg가 `http://www.WorkingOntologist.org/Examples/Chapter3/Manufacture#`에 해당한다고 하면, 앞의 표에서 만든 첫 타입 트리플은 이렇게 쓴다.

```text
<http://www.WorkingOntologist.org/Examples/Chapter3/Manufacture#Product1>
<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>
<http://www.WorkingOntologist.org/Examples/Chapter3/Manufacture#Product> .
```

책의 지면에서는 줄이 길어 세 줄로 나눠 썼지만, 실제 N-Triples 파일은 트리플 하나를 한 줄에 쓴다. 한 트리플 안에서는 줄바꿈이 허용되지 않기 때문이다. 장점은 파일에서 읽기(파싱)와 쓰기가 쉬워 가져오기와 내보내기에 좋다는 것이다.

---

## 3. Turtle

이 책에서 쓰는 더 간결한 형식이 Turtle이다. N3라는 문법의 부분집합이다. N-Triples의 알아보기 쉬운 트리플 표시에 CURIE의 간결함을 더했다. 책은 현재 예시에 필요한 부분만 소개하고, 자세한 내용은 W3C 권고안을 참고하라고 한다.

### 3.1 접두어 선언과 기본 문장

Turtle은 CURIE를 쓰므로 (지역적인) CURIE와 (전역) URI의 대응을 선언하는 머리말이 먼저 나온다. 앞의 과제에서 필요한 CURIE는 이렇게 정의한다.

```turtle
@prefix mfg: <http://www.WorkingOntologist.com/Examples/Chapter3/Manufacturing#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
```

(원문 추출본에서는 rdf 접두어의 URI 끝에 `#`이 빠져 있다. 추출 과정의 누락이거나 원서의 오타로 보이며, 앞 문서에서 본 rdf 네임스페이스에 맞춰 `#`을 붙여 적었다. 이 문서의 코드는 원문의 한 줄 공백 삽입을 정리해 적은 것이고, 원서 줄바꿈 위치와는 다를 수 있다.)

접두어를 선언한 뒤에는 CURIE로 쓴 세 자원을 순서대로 적고 마침표로 끝내면 트리플 하나가 된다.

```turtle
mfg:Product1 rdf:type mfg:Product .
```

마침표 앞의 공백은 눈에 잘 띄게 하려는 것이고 있어도 없어도 된다.

### 3.2 세미콜론: 주어가 같을 때

표에서 가져온 데이터는 주어가 같은 트리플이 여러 개 나오기 쉽다. Turtle은 첫 트리플을 평소처럼 쓰되 마침표 대신 세미콜론(`;`)을 찍어 같은 주어의 트리플이 이어진다고 알린다. 다음 트리플에서는 서술어와 목적어만 쓰면 된다. 앞의 표에서 Product1 부분은 이렇게 쓴다.

```turtle
mfg:Product1 rdf:type mfg:Product ;
    mfg:Product_Division "Manufacturing support" ;
    mfg:Product_ID "1" ;
    mfg:Product_Manufacture_Location "Sacramento" ;
    mfg:Product_ModelNo "ZX-3" ;
    mfg:Product_Product_Line "Paper Machine" ;
    mfg:Product_SKU "FB3524" ;
    mfg:Product_Available "23" .
```

여덟 줄이 모두 주어가 `mfg:Product1`인 트리플 하나씩이다. 마지막 줄만 마침표로 끝난다. Product2도 같은 모양으로 쓴다(원문 예시에서 Product2의 모델은 "ZX-3P", SKU는 "KD5243", 재고는 "4"이다).

### 3.3 쉼표: 주어와 서술어가 같을 때

주어와 서술어가 모두 같으면 목적어만 쉼표(`,`)로 나열한다. 셰익스피어의 세 자녀 수잔나, 주디스, 햄넷은 이렇게 쓴다.

```turtle
lit:Shakespeare b:hasChild b:Susanna, b:Judith, b:Hamnet .
```

이 한 줄은 트리플 세 개와 같다.

```turtle
lit:Shakespeare b:hasChild b:Susanna .
lit:Shakespeare b:hasChild b:Judith .
lit:Shakespeare b:hasChild b:Hamnet .
```

### 3.4 키워드 a

Turtle에는 가독성을 높이는 줄임 표기가 여럿 있고, 책은 몇 가지만 쓴다. 가장 많이 쓰는 줄임은 `a`가 rdf:type을 뜻한다는 것이다. 보통 "Product1은 Product다", "셰익스피어는 극작가다"라고 말하므로, 그에 맞춰 이렇게 쓴다.

```turtle
mfg:Product1 a mfg:Product .
lit:Shakespeare a lit:Playwright .
```

| 기호 | 뜻 | 쓰는 때 |
| --- | --- | --- |
| `.` | 트리플(문장)의 끝 | 항상 |
| `;` | 같은 주어에 서술어와 목적어를 더 이어 씀 | 주어가 같을 때 |
| `,` | 같은 주어·서술어에 목적어를 더 이어 씀 | 주어와 서술어가 같을 때 |
| `a` | rdf:type | 타입 선언 |
| `@prefix` | 접두어와 전체 URI의 대응 선언 | 파일 머리말 |

읽는 법은 이렇다. 마침표는 문장의 끝, 세미콜론은 "같은 주어로 계속", 쉼표는 "같은 주어와 서술어로 계속"이다.

---

## 4. RDF/XML

Turtle은 사람이 보기 편하고 지면에도 간결하다. 하지만 웹 인프라는 HTML이나 더 일반적으로 XML로 정보를 표현하는 데 익숙하다. 그래서 W3C는 역사적으로 먼저 RDF의 XML 직렬화인 RDF/XML을 권고했다. Product1과 Product2의 정보는 RDF/XML에서 다음처럼 보인다(앞 부분만 옮긴다).

```xml
<rdf:RDF xmlns:mfg="http://www.WorkingOntologist.com/Examples/Chapter3/Manufacturing#"
         xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <mfg:Product rdf:about="http://www.WorkingOntologist.com/Examples/Chapter3/Manufacturing#Product1">
    <mfg:Available>23</mfg:Available>
    <mfg:Division>Manufacturing support</mfg:Division>
    <mfg:ProductLine>Paper machine</mfg:ProductLine>
    <mfg:SKU>FB3524</mfg:SKU>
    <mfg:ModelNo>ZX-3</mfg:ModelNo>
  </mfg:Product>
</rdf:RDF>
```

원문에는 `mfg:ManufactureLocation`도 있고, Product2도 이어진다. 위 예는 지면 사정상 일부 줄만 보인 것이다.

여기서 주어(Product1, Product2)는 XML 속성 rdf:about으로 가리키고, 그 주어를 가진 트리플들은 이 정의 안의 하위 요소로 들어간다. RDF/XML의 문법은 자세한 규칙이 많아서 이 책의 범위를 넘으며 W3C 권고안에서 찾을 수 있다. Turtle과 정보량은 같다. mfg:와 rdf:의 선언도 들어 있다. RDF/XML에는 문서에 언급된 자원의 전체 URI를 정하는 규칙이 여럿 있는데, 꽤 복잡하며 이 책의 예시에는 쓰지 않는다.

---

## 5. JSON-LD

웹 애플리케이션에서 컴포넌트 사이에 데이터를 넘기는 더 현대적인 방법은 JSON(JavaScript Object Notation)이다. RDF 링크드 데이터를 JSON을 쓰는 애플리케이션에서 더 쉽게 쓰도록 W3C는 JSON-LD(JSON for Linked Data)를 권고했다. JSON-LD는 RDF 트리플과 직접 대응하므로 또 하나의 RDF 직렬화 형식이다.

JSON에는 익숙하지만 그래프 데이터나 분산 데이터에는 낯선 개발자가, 순수한 JSON만으로도 링크드 데이터와 호환되는 애플리케이션을 만들 수 있다는 것이 JSON을 바탕으로 한 직렬화를 두는 동기 중 하나다. Product1 부분은 이렇게 쓴다.

```json
{
  "@graph": [{
    "@id": "mfg:Product1",
    "@type": "mfg:Product",
    "mfg:Available": "23",
    "mfg:Division": "Manufacturing support",
    "mfg:ModelNo": "ZX-3",
    "mfg:SKU": "FB3524"
  }],
  "@context": { "mfg": "http://www.workingontologist.com/Examples/Chapter3/Manufacturing#" }
}
```

원문에는 `mfg:ManufactureLocation`, `mfg:ProductLine`, Product2, 그리고 rdf 접두어의 정의도 함께 있다.

문서는 `@graph`와 `@context`로 이루어진다.

| 키 | 역할 | Turtle로 비유하면 |
| --- | --- | --- |
| `@context` | 네임스페이스 줄임과 그 전체 URI의 정의 | `@prefix` 선언 |
| `@graph` | 데이터 본문. 가능한 한 객체 구조로 정리 | 트리플 본문 |
| `@id` | 객체가 가리키는 자원의 URI | 트리플의 주어 |
| `@type` | 자원의 타입(선택). 값은 다른 자원으로 해석 | rdf:type 또는 `a` |
| 그 밖의 키 | JSON 필드 이름이 서술어, 값이 목적어 | 서술어와 목적어 |

JSON-LD는 다른 객체를 가리킬 수도 있다. JSON 객체 문법에 `@id`로 가리킬 객체의 정체를 적는다. Product1이 Product2의 일부라고 말하려면 이렇게 쓴다.

```json
{
  "@graph": [{
    "@id": "mfg:Product1",
    "mfg:partOf": { "@id": "mfg:Product2" }
  }]
}
```

JSON-LD는 기존 자바스크립트 환경을 벗어나지 않고도 애플리케이션끼리 그래프 데이터를 교환하는 편리한 방법이다. RDF와 일관되므로 애플리케이션이 분산 데이터의 웹에 매끄럽게 들어갈 수 있다.

---

## 6. 이름 있는 그래프를 위한 형식

지금까지는 트리플의 직렬화를 말했다. 트리플을 하나 이상의 이름 있는 그래프 맥락 속에서 직렬화하려면 어떻게 할까. W3C는 트리플 직렬화를 간단히 확장한 형식을 제공한다.

### 6.1 N-Quads

가장 단순한 것이 N-Quads다. N-Triples처럼 CURIE도 접두어도 쓰지 않는다. 트리플을 쿼드로 쓰므로 주어, 서술어, 목적어, 그래프를 순서대로 적는다. N-Triples 예시를 확장해서, Product1이 그래프 `http://www.WorkingOntologist.org/Examples/Chapter3/Manufacture`에 속한 Product라고 하면 이렇게 쓴다.

```text
<http://www.WorkingOntologist.org/Examples/Chapter3/Manufacture#Product1>
<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>
<http://www.WorkingOntologist.org/Examples/Chapter3/Manufacture#Product>
<http://www.WorkingOntologist.org/Examples/Chapter3/Manufacture> .
```

실제 파일에서는 이것이 한 줄이라 책 지면에는 어울리지 않을 만큼 길다. 하지만 쓰고 읽기는 간단하다. 줄임도 접두어도 없이 주어, 서술어, 목적어, 그래프, 마침표만 있다.

### 6.2 TriG

TriG는 앞의 Turtle을 확장한 형식이다. 네임스페이스 접두어와 세미콜론, 쉼표 줄임 같은 Turtle의 모든 편의 기능을 갖는다. 가장 큰 차이는 파일 속 트리플 모두에 대해 그래프 URI를 지정할 수 있다는 점이다. 방법은 간단하다. 그래프에 속하는 트리플을 모두 중괄호(`{`, `}`) 안에 넣고, 그 앞에 그래프 이름을 쓴다. 제조 제품 예를 이름이 `<http://www.WorkingOntologist.org/Examples/Chapter3/Manufacture>`인 그래프에 넣으면 이렇다.

```turtle
<http://www.WorkingOntologist.org/Examples/Chapter3/Manufacture>
{
  mfg:Product1 rdf:type mfg:Product ;
      mfg:Product_Division "Manufacturing support" ;
      mfg:Product_ID "1" ;
      mfg:Product_SKU "FB3524" .
}
```

원문은 Product1과 Product2의 모든 속성을 중괄호 안에 넣는다. 이렇게 하면 한 파일 안에 여러 그래프를 표현할 수 있다.

| 비교 | N-Quads | TriG |
| --- | --- | --- |
| 바탕 | N-Triples | Turtle |
| 접두어·줄임 | 없음 | 있음 |
| 그래프 지정 방식 | 줄마다 넷째 값으로 | 중괄호로 트리플 묶음을 감싸고 앞에 이름 |
| 읽고 쓰기 | 기계에 쉬움 | 사람에게 쉬움 |

읽는 법은 이렇다. N-Triples와 N-Quads는 기계가 다루기 좋은 쌍이고, Turtle과 TriG는 사람이 읽기 좋은 쌍이다. 각 쌍에서 뒤쪽이 이름 있는 그래프를 지원하는 확장판이다.

<br>
<br>
<br>

[Semantic Web for the Working Ontologist](../)
