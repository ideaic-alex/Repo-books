# FIBO 데이터 매핑과 LEI 예제

FIBO의 주된 쓰임새는 데이터 상호 운용이다. 금융 기관은 이미 참조 데이터, 상품, 포지션, 신용 등급 같은 구조화된 데이터를 관리한다. FIBO의 일은 이런 구조화 데이터를 교환하고 비교하기 쉽게 만드는 것이다. 어려운 점은 데이터 출처마다 관리하는 조직이 다르고 구조도 제각각이라는 것이다. 이 문서는 데이터셋이 어떻게 다른지, 그 차이를 FIBO가 어떻게 받아 내는지를 시간 구간과 법인 식별자(LEI) 두 도전 과제로 확인한다. 마지막에는 FIBO가 왜 일부러 복잡한 모양인지 설명한다.

---

## 1. 아직 보지 못한 데이터에 미리 매핑한다

FIBO의 접근법은 각 데이터 출처를 대응시킬 수 있는 모델을 그 출처들의 세부를 보기 전에 미리 갖추는 것이다. 얼핏 불가능해 보인다. 은행, 규제 기관, 투자자, 신용카드 회사, 세무 기관 등 조직마다 데이터를 다른 방식으로 구조화하고, 서로 다른 사용 사례, 응용, 사용자 집단을 강조해 설계했기 때문이다. 하나의 모델이 어떻게 이 모두에 대응할 수 있을까.

이를 이해하려면 여러 출처의 데이터셋이 어떻게 다른지부터 알아야 한다.

| 차이의 종류 | 설명 | 예 |
|---|---|---|
| 이름 차이 | 같은 것을 다른 이름으로 부른다 | 9.3절의 Analyst와 Researcher. 한 도서관에서는 이용자가 책을 check out하고 다른 도서관에서는 borrow한다 |
| 분해 방식(factoring) 차이 | 속성에 같은 이름을 써도 정리하는 방식이 다르다 | 신용카드가 주소를 가진다 / 신용카드는 사람(또는 회사)이 소유하고 그 사람이 주소를 가진다 / 신용카드에 청구 우편번호가 있다 / 카드 소유자가 우편번호를 가진 청구 주소를 가진다 |

이름 차이보다 분해 방식 차이가 더 미묘하다. FIBO 같은 온톨로지는 여러 "주인"을 섬겨야 하고, 매우 다양한 데이터셋과 양방향으로 대응할 수 있어야 한다.

---

## 2. 도전 과제 42: 시간 구간

시작과 끝이 있는 기간을 설명하는 모델이 있다고 하자. 이렇게 모델링할 수 있다.

```turtle
:Period rdf:type owl:Class .
:hasStart rdf:type owl:DatatypeProperty ;
  rdfs:domain :Period ;
  rdfs:range xsd:dateTime .
:hasEnd rdf:type owl:DatatypeProperty ;
  rdfs:domain :Period ;
  rdfs:range xsd:dateTime .
```

날짜와 시간의 구간을 나타내는 간단한 방법이다. 이것을 FIBO에 어떻게 매핑할까.

**풀이.** FIBO는 fibo-fnd-dt-fd:DatePeriod라는 클래스를 이렇게 정의한다.

```turtle
fibo-fnd-dt-fd:DatePeriod rdf:type owl:Class ;
  rdfs:subClassOf [ rdf:type owl:Restriction ;
    owl:maxQualifiedCardinality 1 ;
    owl:onClass fibo-fnd-dt-fd:Date ;
    owl:onProperty fibo-fnd-dt-fd:hasEndDate ] ;
  rdfs:subClassOf [ rdf:type owl:Restriction ;
    owl:maxQualifiedCardinality 1 ;
    owl:onClass fibo-fnd-dt-fd:Date ;
    owl:onProperty fibo-fnd-dt-fd:hasStartDate ] .
```

두 제약 모두 "Date 클래스의 값을 최대 하나까지 가진다"는 한정 기수 제약이다. 시작일과 종료일을 각각 많아야 하나 가진다는 뜻이다.

| 비교 항목 | 도전 과제의 모델 | FIBO |
|---|---|---|
| 클래스 | :Period | fibo-fnd-dt-fd:DatePeriod |
| 시작 | :hasStart | fibo-fnd-dt-fd:hasStartDate |
| 끝 | :hasEnd | fibo-fnd-dt-fd:hasEndDate |
| 관계를 적는 방식 | RDFS의 domain과 range | OWL의 최대 한정 기수 제약 |

표현은 RDFS와 OWL로 다르지만 대응은 직접적이다. hasStart의 의미는 hasStartDate의 의미와 같다. 이 대응은 OWL로 이렇게 쓴다.

```turtle
fibo-fnd-dt-fd:hasStartDate owl:equivalentProperty :hasStart .
fibo-fnd-dt-fd:hasEndDate owl:equivalentProperty :hasEnd .
```

이 두 줄이면 :hasStart로 적힌 데이터도 FIBO 모델에서 hasStartDate 데이터로 읽힌다.

---

## 3. 도전 과제 43: 법인 식별자(LEI)

금융 상품 규제에서 흔한 문제가 법인 식별이다. 증권사가 많은 다른 회사에 지분을 가지고 있다고 하자. 정부 규정이 증권사 자신이 큰 지분을 가진 회사의 주식은 거래할 수 없다고 정한다면, 이를 어떻게 알 수 있을까. 증권사가 거래하는 주식을 발행한 회사를 식별하고, 그 회사를 증권사가 어느 정도 소유하는지 찾아봐야 한다.

금융 업계는 전 세계 회사에 부여하는 식별자 LEI(Legal Entity Identifier)를 관리해 이 문제를 푼다. LEI는 글자와 숫자의 고유한 나열이고 꽤 길다. 예제에서는 짧은 LEI를 쓰는 것으로 가정한다.

### 3.1 단순한 모델

회사와 LEI 목록으로 이루어진 단순한 데이터셋을 생각할 수 있다(그림 14.5).

```turtle
:Company a owl:Class .
:hasLEI a owl:DatatypeProperty ;
  rdfs:domain :Company ;
  rdfs:range xsd:string .
plush:BeautyBar :hasLEI "1234ABC" .
```

스프레드시트나 Schema.org 마크업에서 기대할 만한 단순한 데이터 표현이다. LEI로 개체를 찾아볼 수 있다.

### 3.2 GLEIF의 정교한 모델

이번에는 작은 회사가 LEI를 등록해 투자자에게 알리려는 경우가 아니라, 전 세계 모든 LEI를 담은 데이터셋을 본다고 하자. LEI는 Global LEI Foundation(GLEIF)이 관리하며 더 정교한 표현을 쓴다(그림 14.6, Rivett 외, 2019). GLEIF는 OWL로 LEI 등록을 표현해 게시한다.

```turtle
gleif-L1:LegalEntityIdentifier a owl:Class ;
  rdfs:subClassOf [ a owl:Restriction ;
    owl:onProperty gleif-base:identifies ;
    owl:onClass gleif-L1:RegisteredEntity ;
    owl:qualifiedCardinality 1 ] .
lei:L1234ABC a gleif-L1:LegalEntityIdentifier ;
  gleif-base:hasTag "1234ABC" ;
  gleif-base:identifies plush:BeautyBar .
plush:BeautyBar a gleif-L1:RegisteredEntity .
```

위는 GLEIF 모델의 핵심 줄만 옮긴 것이다. 원문은 gleif-base:Identifier 클래스에도 hasTag(문자열 하나)와 identifies(기수 1) 제약을 둔다.

왜 이렇게 복잡한 모델을 쓸까. 더 단순한 모델로 충분해 보이는데도 그렇다. GLEIF는 식별되는 개체와 번호 외에 식별자 자체에 대해서도 많은 것을 알아야 하기 때문이다. GLEIF는 LEI를 발급할 권한이 있는 LOU(Local Operating Unit, 지역 운영 단위) 여러 곳과 일한다. GLEIF 입장에서 LEI 모델은 LEI에 대한 정보, 특히 어느 LOU에 등록되었는지를 표현해야 하고, LOU는 다시 등록 비용 지불 같은 정보를 기록한다. LEI를 등록하고 매년 갱신하는 데는 약간의 수수료가 든다. 즉 GLEIF에게 LEI는 사업의 중심이므로 식별 대상과 별개로 모델링해야 한다.

### 3.3 FIBO의 모델

FIBO는 GLEIF 모델에 꽤 직접 대응된다. 관련된 FIBO 조각은 그림 14.7이다.

```turtle
fibo-be-le-lei:LegalEntityIdentifier a owl:Class ;
  rdfs:subClassOf fibo-fnd-arr-id:Identifier ;
  rdfs:subClassOf [ rdf:type owl:Restriction ;
    owl:onClass fibo-be-le-lp:LegalPerson ;
    owl:onProperty fibo-fnd-aap-agt:identifies ;
    owl:qualifiedCardinality 1 ] .
fibo-be-le-lei:LEIRegisteredEntity
  rdfs:subClassOf fibo-be-le-lp:LegalPerson ;
  owl:equivalentClass [ rdf:type owl:Restriction ;
    owl:onProperty fibo-fnd-aap-agt:isIdentifiedBy ;
    owl:someValuesFrom fibo-be-le-lei:LegalEntityIdentifier ] .
```

그림의 나머지 부분인 Identifier 클래스(hasTag에 문자열 제약)와 plush:BeautyBar 예시 데이터는 생략했다. 위 코드는 책의 그림을 바탕으로 핵심만 옮긴 것이다.

---

## 4. 두 모델의 차이가 말해 주는 것

FIBO는 GLEIF 모델과 가깝게 맞춰져 있지만 차이도 있다. 예제는 그 한 가지를 보여 준다. (예제를 위해 FIBO와 GLEIF의 관련 부분을 단순화했지만 결론은 전체 모델에서도 같다.)

| 모델 | Beauty Bar의 타입 | 그 타입에서 추론되는 것 |
|---|---|---|
| GLEIF | gleif-L1:RegisteredEntity | 더 추론할 것이 없다. RegisteredEntity는 어떤 것의 하위 클래스도 아니다 |
| FIBO | fibo-be-le-lei:LEIRegisteredEntity | LegalPerson의 하위 클래스이므로 Beauty Bar는 LegalPerson이다 |

FIBO에서 LegalPerson은 책임 능력(liability capacity)이 있다. 즉 법적으로 소송을 당할 수 있다. GLEIF 모델은 이에 동의하지 않는다. 등록된 개체 중에는 법인이 아닌 것(특히 지점과 펀드)이 있고, 그런 것은 반드시 소송을 당할 수 있는 것은 아니기 때문이다.

이 간단한 예가 FIBO가 걷는 줄타기를 보여 준다. 한편으로는 "Plush는 LEI가 있나. 있다면 무엇인가" 같은 질문에 답해야 하고, 다른 한편으로는 규제 기관이 "Plush Beauty Bar를 법적으로 고소할 수 있나"라고 물을 때 필요한 변이도 수용해야 한다. 더 단순한 모델은 이 둘 중 하나에 답할 수 있고 실제로 단순한 모델이 흔히 배포된다. 하지만 그런 단순한 모델을 쓰는 시스템을 통합하려면 두 모델의 모든 변이를 아우르는 모델이 필요하다. 이것이 FIBO 설계의 주된 근거다.

---

## 5. FIBO가 일부러 복잡한 이유

FIBO는 금융 업계 데이터셋을 위한 일종의 온톨로지 공용어(interlingua)로 설계되었다. LEI 예제는 이런 온톨로지가 맞닥뜨리는 설계 문제를 되도록 단순하게 보여 주려고 골랐다. FIBO를 얼핏 보면 조각이 왜 이렇게 많은지 의아할 수 있다. 예를 들어 LEIRegisteredEntity와 LegalEntity를 왜 구분하나. 그 구분의 세부는 무엇이고, 언제 어느 쪽을 써야 하나.

사용 사례만으로는 FIBO의 설계를 이해하기 어렵다. 주된 사용 사례가 아직 만나지 못한 데이터셋 사이의 상호 운용이기 때문이다. 그러려면 금융 업계 데이터셋의 구조를 미리 예상해, 그 모두에 자연스러운 추상화를 내놓아야 한다. 이 예에서 한 데이터셋은 조직의 법적 책임에 관심이 있고, 다른 데이터셋(GLEIF의 자체 관리)은 자금 조달 모델이나 지위에 신경 쓰지 않고 회사를 식별하는 방법에 관심이 있다. FIBO에게는 이 둘 중 하나를 고르는 호사가 없다. 둘 모두를 예상하고, 둘을 포함하는 일관된 모델을 지어야 한다.

| 질문 | 필요한 모델 |
|---|---|
| 이 회사의 LEI는 무엇인가 | 단순한 LEI 모델로 충분하다 |
| 이 개체를 법적으로 고소할 수 있는가 | 법인과 책임 능력을 구분하는 모델이 필요하다 |
| 위 두 질문이 서로 다른 시스템에서 나온다 | 두 모델의 변이를 모두 포함하는 FIBO 같은 모델이 필요하다 |

<br>
<br>
<br>

[Semantic Web for the Working Ontologist](../)
