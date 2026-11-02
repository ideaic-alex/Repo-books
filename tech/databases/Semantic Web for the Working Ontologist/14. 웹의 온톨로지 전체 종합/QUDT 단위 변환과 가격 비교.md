# QUDT 단위 변환과 가격 비교

두 단위로 적힌 값을 비교하려면 먼저 "비교해도 되는 값인지" 확인하고, 그다음 한 단위로 맞춰야 한다. 이 문서는 QUDT가 가진 정보로 이 두 일을 SPARQL 쿼리로 하는 방법을 보여 준다. 이어서 변환 쿼리를 함수처럼 이름 붙여 쓰는 방법(SHACL 확장)을 보고, 마지막으로 Schema.org 데이터와 QUDT를 합쳐 두 마사지 가게의 분당 가격을 비교하는 도전 과제를 풀어 본다.

---

## 1. 비교 가능한 단위인지 묻기

단위끼리 변환이 의미 있으려면 같은 종류의 것을 재야 한다. 마일과 킬로미터는 둘 다 길이이므로 변환이 의미 있다. 초와 화씨 온도는 재는 대상이 다르므로 서로 바꿀 수 없다.

QUDT에서는 두 단위가 같은 수량 종류(QuantityKind)를 가지면 비교 가능하다고 본다. 그러므로 피트와 미터가 비교 가능한지는 아래 ASK 쿼리로 확인한다.

```sparql
ASK WHERE {
  unit:M  qudt:hasQuantityKind ?kind .
  unit:FT qudt:hasQuantityKind ?kind .
}
```

같은 변수 ?kind가 두 줄에 모두 쓰였다. 두 단위가 같은 수량 종류를 가리킬 때만 매치되어 TRUE가 나온다. 이 쿼리는 책의 Query 14.1이다.

---

## 2. 변환 곱셈값과 오프셋

비교 가능하다고 확인했다면 값을 변환한다. 각 단위에는 두 속성이 있다.

| 속성 | 뜻 |
|---|---|
| qudt:conversionMultiplier | 변환 곱셈값 |
| qudt:conversionOffset | 변환 오프셋(더하는 값) |

차원(수량 종류)마다 기준 단위가 하나 있고, 그 단위의 곱셈값은 1이고 오프셋은 0이다. 기준 단위가 무엇인지 알 필요는 없다. 곱셈값과 오프셋만 있으면 어떤 두 단위든 이어 변환할 수 있다. 공식은 원본 값에 원본 곱셈값을 곱하고 원본 오프셋을 더한 뒤, 목표 오프셋을 빼고 목표 곱셈값으로 나누는 것이다. 쿼리에서는 이 순서 그대로 쓴다.

10킬로미터를 마일로 바꾸는 쿼리(Query 14.2)는 다음과 같다.

```sparql
SELECT (((((?val * ?M1) + ?O1) - ?O2) / ?M2) AS ?converted)
WHERE {
  BIND (10.0 AS ?val)
  unit:KM qudt:conversionMultiplier ?M1 ;
          qudt:conversionOffset ?O1 .
  unit:MI qudt:conversionMultiplier ?M2 ;
          qudt:conversionOffset ?O2 .
}
```

책에 나온 결과는 6.2137119223733395다. QUDT에는 500개가 넘는 변환 계수가 들어 있어서 수천 가지 변환이 가능하다.

| 종류 | 예 |
|---|---|
| 같은 단위 체계 안의 변환 | 미터와 킬로미터, 초와 시간, 피트와 마일 |
| 체계를 넘나드는 변환 | 마일과 킬로미터, 화씨와 섭씨 |

화씨와 섭씨가 오프셋이 필요한 대표적인 경우다. 곱셈만으로는 되지 않고 더하는 값이 있어야 한다.

---

## 3. 추론이 아니라 쿼리다

위 변환은 SPARQL로 표현할 수 있지만 추론은 아니다. 즉 어떤 양이 마일로 적혀 있다고 해서 추론 엔진이 알아서 킬로미터 값을 만들어 주지는 않는다. 이런 계산은 보통 응용 프로그램 코드에 넣는다.

이 한계를 넘는 방법이 SHACL-Rules(7.1절)다. 앞에서 SHACL-Rules로 쿼리를 온톨로지에 붙이는 법을 봤다. 여기서는 또 다른 활용을 본다.

앞의 쿼리에는 변환할 숫자(10.0), 원본 단위(킬로미터), 목표 단위(마일)가 쿼리 안에 박혀 있다. 다른 변환을 하려면 거의 같은 쿼리를 값만 바꿔 다시 써야 한다. 훨씬 편한 방법은 쿼리를 매개변수화해 함수 정의처럼 만드는 것이다. 함수 인자 자리에 ?arg1, ?arg2, ?arg3 같은 변수를 쓴다(Query 14.3).

```sparql
SELECT (((((?arg1 * ?M1) + ?O1) - ?O2) / ?M2) AS ?value)
WHERE {
  ?arg2 qudt:conversionMultiplier ?M1 ;
        qudt:conversionOffset ?O1 .
  ?arg3 qudt:conversionMultiplier ?M2 ;
        qudt:conversionOffset ?O2 .
}
```

SHACL 확장(Steyskal 외, 2017)을 쓰면 이런 쿼리에 이름을 붙일 수 있다. 이름은 그 자체로 RDF 자원이다. 이름 붙은 쿼리를 함수라고 부른다. 이 함수를 qudtsh:convert라 하면 10킬로미터 변환은 이렇게 간단해진다(Query 14.4).

```sparql
SELECT (qudtsh:convert(10.0, unit:KM, unit:MI) AS ?value)
WHERE {}
```

책에 나온 답은 6.21이다. 모든 일을 함수 호출이 하고, WHERE 절에는 매치할 것이 하나도 없다. 32도 화씨를 섭씨로 바꾸는 쿼리(Query 14.5)도 똑같은 모양이다.

```sparql
SELECT (qudtsh:convert(32.0, unit:DEG_F, unit:DEG_C) AS ?value)
WHERE {}
```

답은 0.0이다.

---

## 4. 도전 과제 40: 좋은 관계로 가격 비교하기

QUDT로 단위를 바꿀 수 있게 되었으니 Schema.org 데이터에 적용해 물건값을 비교해 본다. 예제 9(그림 10.2)에는 90분 마사지가 80.00달러인 가게 Plush가 있었다. 근처 경쟁 가게 Style Cafe는 15분짜리 의자 마사지를 내놓았다고 하자. 아래는 핵심 줄이다.

```turtle
style:Offer10 rdf:type schema:Offer ;
  schema:priceSpecification style:PriceSpec10 ;
  schema:includesObject style:ChairMassage .
style:PriceSpec10 rdf:type schema:UnitPriceSpecification ;
  schema:price "15.0" ; schema:priceCurrency "USD" .
style:ChairMassage a schema:TypeAndQuantityNode ;
  schema:amountOfThisGood "15" ; schema:unitCode unit:MIN .
```

15분에 15달러인 쪽과 90분에 80달러인 쪽을 비교하려면 단위를 맞춰야 한다. 정보는 이미 모두 있다. 두 데이터는 같은 모양을 따르므로, 서로 다른 값만 변수로 바꾸면 하나의 쿼리가 된다(Query 14.6). 변수 이름은 그래프에서의 역할을 알려 주도록 지었다. ?pricespec은 UnitPriceSpecification, ?qunit은 QUDT 단위다.

```sparql
SELECT * WHERE {
  ?spa a schema:DaySpa ; schema:makesOffer ?offer .
  ?offer a schema:Offer ;
    schema:priceSpecification ?pricespec ;
    schema:includesObject ?tqn ; rdfs:label ?offering .
  ?pricespec a schema:UnitPriceSpecification ;
    schema:price ?price ; schema:priceCurrency ?currency .
  ?tqn a schema:TypeAndQuantityNode ;
    schema:amountOfThisGood ?duration ;
    schema:unitCode ?qunit ; schema:typeOfGood plush:Massage .
}
```

이제 분당 가격을 계산한다. 단위는 분으로 골랐지만 초나 시간을 골라도 상관없다. 양(?duration)과 그 단위(?qunit)를 분으로 변환하고, 가격을 그 값으로 나눈다. 아래가 Query 14.7의 새로 추가된 부분이다.

```sparql
BIND ((?price / qudtsh:convert(?duration, ?qunit, unit:MIN))
      AS ?cost_per_min)
} ORDER BY (?cost_per_min)
```

앞쪽 패턴은 Query 14.6과 같고, SELECT는 ?offering ?currency ?cost_per_min이다. 결과는 낮은 값부터 정렬된다.

| offering | currency | cost_per_min |
|---|---|---|
| Hour and a half massage | USD | 0.8889 |
| Chair massage | USD | 1 |

90분 마사지는 80달러를 90분으로 나눈 0.8889달러, 의자 마사지는 15달러를 15분으로 나눈 1달러다. 분당 값으로는 90분 마사지가 더 이득이다. 책은 이 쪽을 "Relaxing Massage"라고 부르며 분당 값이 더 낫다고 쓴다.

---

## 5. 이 예제가 보여 주는 것

| 역할 | 맡은 쪽 | 내용 |
|---|---|---|
| 서로 다른 사업체의 상품 표현을 통일 | Schema.org | 제안, 가격, 양, 단위를 일관된 구조로 적게 해 준다 |
| 계산 서비스 제공 | QUDT | 단위 변환 |
| 연결 | Schema.org의 외부 참조 | 세부 정의를 외부(QUDT)에 맡기고 참조하므로 두 제안을 쉽게 이을 수 있다 |

핵심은 모델이 데이터 출처들을 이어 주는 방식이다. 각 사업체는 자기 데이터에 단위 URI만 적었을 뿐이다. 그런데 그 URI가 QUDT를 가리키므로 아무 협의 없이도 비교가 가능해졌다.

<br>
<br>
<br>

[Semantic Web for the Working Ontologist](../)
