# 열린 정부 데이터와 FHEO 사례

정부가 가진 데이터는 양이 많고 쓸모도 크지만, 공개된 모양이 제각각이라 바로 쓰기 어렵다. 이 문서는 미국의 Data.gov를 예로 들어, 정리되지 않은 원자료를 RDFS와 SPARQL로 쓸 만한 데이터로 바꾸는 과정을 따라간다. 주인공은 공정 주택법(Fair Housing Act) 위반 신고 사건 데이터인 FHEO 데이터셋이다.

핵심은 두 가지다. 하나는 "1과 빈칸"으로 적힌 칸을 클래스(종류)로 바꾸는 것이고, 다른 하나는 이 변환에 SPARQL CONSTRUCT를 규칙처럼 쓰는 것이다.

---

## 1. 열린 정부 데이터란

2009년 미국 정부는 공공 정부 데이터를 공개하고 접근 가능하게 하겠다고 공식화했다. 그전에는 정보가 대개 "인포그래픽"이 들어간 보고서 형태로 나왔다. 파이 차트나 연표는 사람이 인쇄해 읽기에는 좋지만 컴퓨터로 처리하기는 매우 어렵다. Data.gov는 수십만 개의 데이터셋을 기계가 읽을 수 있는 여러 형식으로 제공한다. 이 모든 데이터셋의 메타데이터와 500개 넘는 데이터셋의 내용이 2010년 5월 RDF로 공개되었고, RDF가 승인된 데이터 형식 중 하나가 되면서 이후 더 많이 변환되었다.

| 지역 또는 기관 | 원서의 설명 |
|---|---|
| 미국 Data.gov | 데이터셋 수십만 개, 그중 수백 개가 RDF로 제공된다. 계속 변환 중이다 |
| 영국 Data.gov.uk | 정부 데이터셋 다수를 RDF로 직접 공개한다. 학교, 도로, 정부 기관과 기능에 표준 URI를 만들어 연결했다 |
| 기타 | 도시, 주, 지방, 카운티, 부족 단위 정부, World Bank와 UN 기관 같은 NGO도 공개한다 |
| 2010년 말 | RDF로 직접 공개한 곳은 미국과 영국뿐이었다 |
| 2013년 | 40개 넘는 정부의 데이터셋 100만 개 넘게 RDF로 목록화되었다 |

이 표는 시기별로 RDF 공개가 빠르게 퍼진 흐름을 보여 준다. 전 세계의 열린 정부 데이터는 RDF를 포함한 여러 형식으로 공유된다.

### "날것" 데이터

이런 자료는 Tim Berners-Lee가 말한 날것(raw) 데이터, 즉 특정 응용을 염두에 두지 않고 "야생에서" 공개된 기계 가독 파일이다. 장점은 여러 공동체가 만드는 여러 응용에서 재사용할 수 있다는 것이다. 단점은 쓰려면 처리 수단이 필요하다는 것이다. 원서는 이 상태를 데이터 야생(data wilderness)이라 부른다.

## 2. 예제 데이터: FHEO 신고 사건

FHEO(Office of Fair Housing/Equal Opportunity)에 접수된, 공정 주택법 Title VIII 위반 의혹 사건 목록이다. 이 법은 소수자를 주택 분야의 특정 차별에서 보호한다. 데이터는 zip으로 압축된 Excel 파일로 공개되어 있고, 챌린지 1에서 설명한 방법으로 RDF로 바꿀 수 있다. 10만 건이 넘는 항목이 아래와 같은 모양이다.

```turtle
:FHEO_filed_case-0
    rdf:type :FHEO_filed_case ;
    :case_number "06-06-0310-8" ;
    :filing_date "2006-01-01"^^xsd:date ;
    :number_of_filed_cases 1 ;
    :number_of_filed_cases_with_a_disability_basis 1 ;
    :violation_county "Lafayette" ;
    :violation_state "Louisiana" .
```

원서의 실제 예에는 인종, 가족 상태 등 다른 "basis" 속성이 몇 개 더 있으나 지면상 일부만 옮겼다. 같은 주어 `:FHEO_filed_case-0`에 여러 트리플이 붙어 있고, 서술어는 신고 근거(basis), 접수일, 위반 장소를 말한다.

눈여겨볼 곳은 신고 근거의 표현이다. 인종, 종교, 피부색처럼 신고 사유가 된 요인은 값 "1"로 표시하고, 사유가 아니면 값을 아예 적지 않는다. 이런 독특한 표현은 데이터 야생에서 흔하다. 예를 들어 입력 화면에서 사용자가 해당 사유에 체크 표시를 하던 방식에서 나왔을 수 있다고 원서는 추측한다.

## 3. 챌린지 26: RDFS로 이 데이터를 어떻게 정리할까

### 해법의 방향: 요인마다 클래스를 만든다

더 유연한 표현은 요인마다 클래스를 정의하고, 신고 전체를 대표하는 클래스 하나를 두는 것이다.

```turtle
FHEO:Asian rdfs:subClassOf FHEO:Complaint .
FHEO:Black rdfs:subClassOf FHEO:Complaint .
FHEO:Disability rdfs:subClassOf FHEO:Complaint .
FHEO:Race rdfs:subClassOf FHEO:Complaint .
FHEO:Religion rdfs:subClassOf FHEO:Complaint .
```

원서는 아래 19개 요인 모두에 이런 줄을 둔다. 위 코드는 그중 다섯 줄이다.

| 번호 | 클래스 | 번호 | 클래스 |
|---|---|---|---|
| 1 | Asian | 11 | NA |
| 2 | AsianAndWhite | 12 | NABlack |
| 3 | Black | 13 | NAWhite |
| 4 | BlackAndWhite | 14 | Other |
| 5 | Color | 15 | Race |
| 6 | Disability | 16 | Religion |
| 7 | FamilialStatus | 17 | Retaliation |
| 8 | NationalOrigin | 18 | Sex |
| 9 | Hispanic | 19 | White |
| 10 | HPI | | |

이제 장애 차별 사건은 트리플 한 줄이면 된다.

```turtle
:FHEO_filed_case-0 a FHEO:Disability .
```

`FHEO:Disability`가 `FHEO:Complaint`의 하위 클래스이므로, 타입 전파 규칙(하위 클래스의 구성원은 상위 클래스의 구성원이기도 하다는 RDFS 추론 규칙)으로 이 사건이 `FHEO:Complaint`라는 사실도 추론된다. 원서 본문은 이 사건을 `:entry1`이라 부르지만 앞뒤 예와 같은 대상이다.

### 데이터는 아직 안 바뀌었다

이 모델은 신고를 간결하게 서술하게 해 주지만 실제 데이터를 바꾸지는 않는다. 데이터는 여전히 "1"과 빈칸 형태다. 그렇다면 장애 속성에 "1"이 있는 항목은 `:Disability` 구성원이 되게, 인종 속성에 "1"이 있는 항목은 `:Race` 구성원이 되게 바꿀 수 있을까.

### SPARQL CONSTRUCT로 변환한다

각각은 SPARQL CONSTRUCT(쿼리 결과로 새 트리플을 만들어 내는 쿼리 형태)로 쉽게 처리된다.

```sparql
CONSTRUCT {?e a :Disability}
WHERE {?e a :FHEO_filed_case ;
          :number_of_filed_cases_with_a_disability_basis "1" . }
```

법에서 인정한 차별 요인마다 이런 쿼리를 하나씩, 19개 정의한다. 위 쿼리는 `:FHEO_filed_case-0 a FHEO:Disability` 트리플과 다른 요인의 해당 트리플을 만들어 낸다.

### 추론 방법으로서의 SPARQL

원서는 여기서 중요한 관점을 짚는다. 이렇게 쓰는 SPARQL도 일종의 추론 방법이다. RDFS와 RDFS-Plus가 추론 방법인 것과 같다. 차이는 RDFS와 RDFS-Plus가 정해진 규칙 집합인 데 비해, SPARQL CONSTRUCT는 아주 맞춤형 규칙을 표현할 수 있다는 점이다. 여기서는 데이터가 발견된 모양을 우리가 원하는 모양으로 바꾸는 규칙을 CONSTRUCT로 정의했다.

| 방법 | 규칙의 성격 | 이 사례에서의 역할 |
|---|---|---|
| RDFS | 정해진 규칙(하위 클래스, domain, range 등) | 타입 전파로 Complaint 구성원 추론 |
| RDFS-Plus | RDFS에 OWL 일부를 더한 정해진 규칙 | 같은 종류의 추론 방법으로 원서가 비교 대상으로 든다 |
| SPARQL CONSTRUCT | 직접 쓰는 맞춤형 규칙 | "1"이 있는 항목을 클래스 구성원으로 변환 |

이 표를 읽을 때 기억할 점은, 정해진 규칙으로 안 되는 것은 CONSTRUCT로 메울 수 있다는 것이다. 다만 규칙을 직접 관리해야 하는 부담이 따른다.

<br>
<br>
<br>

[Semantic Web for the Working Ontologist](../)
