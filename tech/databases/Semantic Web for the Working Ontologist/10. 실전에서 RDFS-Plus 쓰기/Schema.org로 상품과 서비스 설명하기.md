# Schema.org로 상품과 서비스 설명하기

웹 페이지의 내용은 사람이 읽으면 금방 이해되지만, 프로그램이 거기서 데이터를 뽑아내기는 어렵다. 페이지가 약속된 표기(마크업)를 따르지 않으면 어디가 제목이고 어디가 가격인지 알 방법이 없다. Schema.org는 이 문제를 풀려고 Google, Microsoft, Yahoo, Yandex가 함께 시작한 사업으로, 웹 페이지에 구조화된 데이터를 심을 때 쓰는 공용 온톨로지를 제공한다.

이 문서는 Schema.org가 무엇인지, 상품 한 개를 어떻게 트리플로 쓰는지, 가격처럼 한 줄로 끝나지 않는 정보를 어떻게 모델링하는지를 다룬다. 예제는 넥타이 상품과 데이 스파(Plush Beauty Bar)의 마사지 상품이다.

---

## 1. Schema.org가 하는 일

앞서(4.1절) 본 것처럼 RDFa, Microdata, JSON-LD 같은 형식으로 RDF를 웹 페이지에 심을 수 있다. 그런데 형식만 있다고 되는 것은 아니고, 모두가 같은 뜻으로 쓰는 어휘가 있어야 한다. Schema.org가 그 어휘를 모아 둔 중앙 창고 역할을 한다.

- 수백만 개의 사이트가 Schema.org 어휘로 페이지를 표시해 검색과 사용자 경험을 개선한다.
- 동기는 주요 검색 엔진에 미치는 효과였을 수 있지만, 심어 둔 데이터는 누구나 어떤 웹 응용에서든 쓸 수 있다.
- 형식 대부분이 W3C 표준이라 누구나 파싱할 수 있다. 그래서 재사용이 쉽다.

Schema.org의 클래스 계층에는 웹 페이지에서 설명할 만한 것들이 들어 있다.

| 분류 | 예 |
|---|---|
| 사람, 조직, 장소 | Person, Organization, Place |
| 행사 | Event |
| 창작물 | Creative work |
| 페이지에 삽입된 비문자 객체 | Image, Video, Audio |
| 상품과 판매 조건 | Products and offers |
| 평가 | Reviews and ratings |
| 행위 | Actions (검색, 거래, 갱신 등) |

이 표는 원서가 "흔히 쓰는 클래스"로 든 것이며 전체 목록이 아니다.

## 2. 상품 하나를 트리플로 쓰기

4장에서 본 검색 결과의 "리치 스니펫"(제목 아래에 가격, 평점 등이 같이 나오는 검색 결과)을 예로 들자. 남성용 넥타이 상품 페이지를 어떻게 표시하면 리치 스니펫이 나올까.

Schema.org의 네임스페이스는 `http://schema.org`이고, 여기서는 접두어 `schema:`로 줄여 쓴다. 클래스 `schema:Product`가 출발점이다. 브라우저에 `http://schema.org/Product`를 입력하면 이 클래스에 쓸 수 있는 속성과 마크업 예시를 담은 문서가 나온다. 링크를 따라가며 알아내는 방식(follow-your-nose)이다.

넥타이를 `bnb:Buffalo`라고 부르면 가장 간단한 트리플은 상품이라는 사실과 이름이다.

```turtle
bnb:Buffalo a schema:Product ;
    schema:name "Buffalo Plaid Tie - Blade and Blue" .
```

이름만으로는 페이지 제목 이상의 정보가 없다. 가격이나 재고는 어떻게 쓸까.

## 3. 가격은 Offer에 둔다

Schema.org는 "상품이나 서비스를 팔겠다는 제안"을 `schema:Offer`라는 별도 클래스로 둔다. 가격과 재고 여부는 상품이 아니라 이 제안이 가진다. 제안은 `schema:offers` 속성으로 상품과 이어진다. 여기서는 제안을 빈 노드(이름 없는 노드)로 쓰는데, 3.9절에서 배운 대괄호 표기다.

```turtle
bnb:Buffalo a schema:Product ;
    schema:name "Buffalo Plaid Tie - Blade and Blue"@en ;
    schema:offers [ a schema:Offer ;
        schema:availability schema:InStock ;
        schema:price "49" ;
        schema:priceCurrency "USD"@en ] .
```

이 데이터를 받아 무엇을 할지는 응용이 정한다. 예를 들어 Google 검색은 이 정보를 검색 결과의 이름 바로 아래에 보여 준다. 리뷰와 평점도 비슷한 방식으로 다룬다.

## 4. 확장되는 어휘: Good Relations

Schema.org의 온톨로지는 계속 커진다. 2012년에는 Good Relations 온톨로지가 Schema.org에 통합되어 상품, 서비스, 제안을 더 자세히 설명할 수 있게 되었다. 아래 데이 스파 예제는 대체로 Good Relations에서 온 어휘를 쓴다.

## 5. 예제: Plush Beauty Bar

데이 스파를 `plush:BeautyBar`라 하자. 이 예제의 정보는 교육용이며 실제 Plush Beauty Bar의 상품과 무관하다고 원서가 밝힌다. 이 가게는 여러 서비스를 내놓고 그중 하나가 마사지다. Plush가 정의한 자원에는 `plush:` 접두어를 쓴다.

```turtle
plush:BeautyBar a schema:DaySpa ;
    schema:makesOffer plush:Offer1 ;
    schema:makesOffer plush:Offer2 ;
    schema:makesOffer plush:Offer3 .
plush:Offer1 rdfs:label "Hour and a half massage" .
```

### 가격에 통화가 필요하다

서비스에는 값이 있다. `:cost`라는 속성으로 제안과 숫자를 바로 잇는다고 해 보자. 금액은 나타내지만 사업에서는 통화도 알아야 한다. 즉 "제안과 값을 잇는 관계" 위에 정보를 더 얹어야 한다. 3장에서 배운 리이피케이션(reification, 관계 자체를 하나의 노드로 만들어 거기에 정보를 붙이는 방법)이 이 문제의 해법이다. Schema.org는 가격 전체를 설명하는 클래스 `UnitPriceSpecification`을 둬서 해결한다.

```turtle
plush:Offer1 a schema:Offer ;
    schema:priceSpecification plush:PriceSpec1 ;
    rdfs:label "Hour and a half massage" .
plush:PriceSpec1 a schema:UnitPriceSpecification ;
    schema:price "80.0" ;
    schema:priceCurrency "USD" .
```

마사지 제안의 가격이 미화 80달러라는 뜻이다.

### 서비스와 시간 표현

제안에는 가격과 라벨은 있지만 어떤 서비스인지는 아직 없다. 제안 하나에 여러 서비스가 들어갈 수 있는데, 여기서는 한 시간 반짜리 마사지 하나다. 먼저 서비스의 종류를 정의한다.

```turtle
plush:Massage a schema:Service ;
    rdfs:label "Relaxing Massage" .
```

이제 한 시간 반짜리 마사지를 만든다. 이것은 `schema:TypeAndQuantityNode`이고, 이름 그대로 종류와 양을 한 노드에 묶는다.

```turtle
plush:Massage1_5 a schema:TypeAndQuantityNode ;
    schema:amountOfThisGood "1.5" ;
    schema:unitCode unit:HR ;
    schema:typeOfGood plush:Massage .
```

"한 시간 반"은 단위(`schema:unitCode`)와 그 단위로 잰 양(`schema:amountOfThisGood`)으로 표현한다. 단위는 CURIE(접두어로 줄여 쓴 URI) `unit:HR`로 가리킨다. `unit:` 네임스페이스는 `http://qudt.org/vocab/unit/`의 줄임이고, 양, 단위, 차원, 유형을 다루는 QUDT 온톨로지(14.2절에서 자세히 다룬다)를 가리킨다.

### 전체를 모으기

마지막으로 가게, 제안, 가격 명세, 서비스 노드를 하나로 이으면 완성된다. 원서는 이를 Turtle 코드와 그래프 그림으로 보여 준다. 연결 구조를 표로 정리하면 다음과 같다.

| 주어 | 서술어 | 목적어 |
|---|---|---|
| plush:BeautyBar | schema:makesOffer | plush:Offer1 |
| plush:Offer1 | schema:priceSpecification | plush:PriceSpec1 |
| plush:Offer1 | schema:includesObject | plush:Massage1_5 |
| plush:PriceSpec1 | schema:price / schema:priceCurrency | "80.0" / "USD" |
| plush:Massage1_5 | schema:typeOfGood | plush:Massage |
| plush:Massage1_5 | schema:amountOfThisGood / schema:unitCode | "1.5" / unit:HR |

표를 위에서 아래로 따라가면 가게에서 제안, 가격과 서비스로 갈라지는 가지 모양이 보인다. 가격 쪽 가지와 서비스 쪽 가지가 모두 제안 노드에서 시작한다는 점이 핵심이다.

## 6. SPARQL로 물어보기

이렇게 구조를 잡아 두면 "100달러 미만인 서비스 이름을 보여 줘" 같은 질문에 답할 수 있다.

```sparql
SELECT ?service
WHERE {
  plush:BeautyBar schema:makesOffer ?offer .
  ?offer schema:priceSpecification ?amount .
  ?amount schema:priceCurrency "USD" ;
          schema:price ?price .
  ?offer schema:includesObject ?node .
  ?node schema:typeOfGood ?type .
  ?type rdfs:label ?service .
  FILTER (xsd:decimal(?price) < 100)
}
```

쿼리는 가게에서 제안, 가격 명세로 내려가 통화가 USD인 가격을 잡고, 같은 제안의 서비스 노드를 거쳐 서비스 라벨을 꺼낸다. 마지막 FILTER가 가격을 십진수로 바꿔 100과 비교한다. 가격이 문자열 "80.0"으로 저장되어 있으므로 비교 전에 형 변환이 필요하다.

이 데이터는 보통 사람이 읽는 형태로 웹 페이지에 공개된다. Schema.org 용어로 표시를 달아 두면 이런 필터링을 자동으로 할 수 있다.

## 7. 정리

| 질문 | Schema.org의 답 |
|---|---|
| 가격과 재고는 어디에 두나 | 상품이 아니라 Offer에 둔다 |
| 값 옆에 통화를 붙이려면 | UnitPriceSpecification으로 가격 전체를 하나의 노드로 만든다 |
| "1.5시간" 같은 양은 | TypeAndQuantityNode에 양, 단위, 종류를 묶는다 |
| 단위 정의는 어디서 가져오나 | QUDT 같은 외부 온톨로지를 가리킨다 |

값 하나를 속성으로 직접 잇는 대신 "관계를 노드로 만드는" 방식이 반복해서 나온다. 실제 비즈니스 데이터는 숫자 하나로 끝나는 경우가 드물기 때문이다.

<br>
<br>
<br>

[Semantic Web for the Working Ontologist](../)
