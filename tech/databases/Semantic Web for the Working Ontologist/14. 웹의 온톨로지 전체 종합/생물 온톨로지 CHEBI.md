# 생물 온톨로지 CHEBI

생물학과 생명과학은 수십 년, 어떻게 보면 수백 년 동안 온톨로지를 써 온 분야다. 최근에는 생물 정보가 폭발적으로 늘면서 그것을 정리해 줄 온톨로지에 대한 관심도 같이 커졌다. 이 문서는 생물 온톨로지의 목록을 훑지 않는다. 대신 CHEBI(Chemical Entities of Biological Interest, 생물학적 관심 화학 물질)라는 한 온톨로지를 골라, 모델링 방식이 어떻게 생겼고 시맨틱 웹에서 어떻게 쓰이는지 자세히 본다. 특히 OBO 온톨로지가 즐겨 쓰는 "클래스끼리 제약으로 잇는" 설계 패턴과, 그 패턴이 추론에 주는 이점을 이해하는 것이 목표다.

---

## 1. 생물 온톨로지가 하는 일

QUDT가 그랬듯 생물 온톨로지도 시맨틱 웹에서 여러 목적에 쓰인다.

| 목적 | 설명 | 왜 중요한가 |
|---|---|---|
| 모호하지 않은 참조 | 유전자, 질병, 화학 물질, 생물체 같은 수만 개의 개념에 분명한 이름을 준다 | 서로 다른 연구실에서 나온 정보를 정리하는 데 필수다. 특정 유전자에 대해 의심스러운 점이 있는 연구자가 방대한 논문에서 관련 자료를 찾을 때도 분명한 이름이 있으면 훨씬 쉽다 |
| 이름 체계의 통역(로제타석) | 이미 존재하는 여러 이름 체계를 서로 연결한다 | 단백질, 화학 물질 등에는 이미 여러 이름 체계가 있다. 시맨틱 웹은 어휘끼리의 상호 운용에 특히 알맞은 기반이다 |
| 복잡한 검색 | 화학, 유전체학, 단백질체학처럼 상세한 도메인 지식이 필요한 검색 문제를 푼다 | 온톨로지에 훨씬 높은 요구 수준이 걸리는데, 요즘 공개된 많은 온톨로지는 충분한 상세함을 갖췄다 |

CHEBI는 유럽 생물정보학 연구소(European Bioinformatics Institute)가 개발하고 유지하며, 2만 개가 넘는 화학 화합물 정보를 담는다. (본문 다른 곳에서는 개념 수가 "10만 개 남짓"이라고 서술한다. 화합물 수와 전체 개념 수를 따로 센 것으로 보이나 책이 명확히 구분하지는 않는다.) OBO Foundry에 게시되어 있는데, OBO Foundry는 과학 기반 온톨로지를 모으는 일종의 위키 공간이다. OWL 등 여러 형식으로 온톨로지를 제공하며, OWL 형식에는 특정 온톨로지 설계 패턴이 쓰인다. CHEBI는 CC BY 4.0 라이선스다.

---

## 2. 모호하지 않은 참조와 교차 참조

CHEBI는 정의하는 모든 화학 물질에 URI를 준다. 하지만 화학 물질을 식별하는 자원이 CHEBI만 있는 것은 아니다. 다른 자원은 CHEBI처럼 생물학적 관심 물질에 집중하지 않아도 겹치는 범위가 꽤 크다. 그래서 CHEBI는 각 화학 물질에 여러 교차 참조를 포함한다. 제초제 글리포세이트(상품명 Roundup)의 CHEBI 표현에서 발췌하면 다음과 같다.

```turtle
obo:CHEBI_27744 rdfs:label "glyphosate" ;
  oboInOwl:hasDbXref "KEGG:C01705" ;
  oboInOwl:hasDbXref "CAS:1071-83-6" ;
  oboInOwl:hasDbXref "DrugBank:DB04539" ;
  chebi:formula "C3H8NO5P" ;
  chebi:mass "169.07310" .
```

(원문은 첫 줄 끝에 마침표를 잘못 인쇄했다. 여기서는 문법에 맞게 세미콜론으로 고쳤다. 원문에는 이 밖에 Beilstein, Gmelin 참조와 SMILES 문자열(chebi:smiles)도 함께 나온다.)

| 속성 | 담는 정보 |
|---|---|
| rdfs:label | 이름(glyphosate) |
| oboInOwl:hasDbXref | 다른 데이터베이스에서의 식별자(KEGG, CAS, Beilstein, DrugBank, Gmelin) |
| chebi:formula | 화학식 |
| chebi:mass | 질량 |
| chebi:smiles | 분자 구조를 문자열로 쓴 표기 |

글리포세이트의 CHEBI 번호는 27744이고, 실제 URI는 Chebi:CHEBI_27744 꼴이다. CHEBI의 모든 개체는 이런 번호를 받고, 번호가 URI에 들어간다. 이런 이름 짓기 방식의 장단점은 15.2절에서 다룬다. 외부 권위 기관의 참조 번호가 있으므로 CHEBI는 자신이 설명하는 화학 물질에 대해 이 자원들 사이의 번역 서비스 구실을 한다.

---

## 3. 복잡한 검색을 위한 CHEBI 구조

CHEBI 복잡성의 상당 부분은 화학 물질 사이의 연결에 있다. OBO 온톨로지는 정의하는 개체들 사이에 복잡한 관계를 두는 것이 특징이다. CHEBI는 크기가 비교적 작고(개념 10만 개 남짓) 화학 물질 사이의 관계 종류도 적어서 OBO 스타일을 배우기에 좋은 예다.

글리포세이트가 제초제라는 사실은 CHEBI에서 이렇게 표현한다.

```turtle
obo:CHEBI_24527 a owl:Class ; rdfs:label "herbicide"@en .
obo:CHEBI_27744
  a owl:Class ;
  rdfs:label "glyphosate"@en ;
  rdfs:subClassOf [ a owl:Restriction ;
    owl:onProperty obo:has_role ;
    owl:someValuesFrom chebi:CHEBI_24527 ] .
```

여기서 눈여겨볼 점들이 있다.

- **모든 개념이 owl:Class다.** 화학 물질 "glyphosate"도, 역할 "herbicide"도 클래스다. 개체(인스턴스)가 아니라 클래스로 둔다.
- **관계는 제약으로 만든다.** 글리포세이트는 owl:Restriction의 하위 클래스다. 이 제약은 obo:has_role 속성에 걸려 있고, 값이 하나 이상은 herbicide 클래스에서 온다(owl:someValuesFrom)는 뜻이다. 11장에서 본 제약이 그대로 쓰였다.
- **속성은 OBO 네임스페이스에서 온다.** OBO Foundry에는 생물 개체를 설명하는 속성이 수십 개 있고, CHEBI는 그중 자기 영역과 관련된 열두 개 미만을 쓴다.

| 속성 | 쓰임 |
|---|---|
| obo:has_role | 어떤 역할을 가진다 |
| obo:has_part | 구성 화학 물질을 가진다 |
| obo:is_conjugate_acid_of | 짝산 관계 |
| obo:is_conjugate_base_of | 짝염기 관계 |
| obo:has_parent_hydride | 모체 수소화물을 가진다 |

has_role과 herbicide의 이 패턴은 CHEBI 안에서 약 12,000번 되풀이되며 화학 물질과 그 성분, 짝산과 짝염기, 모체 수소화물 등을 잇는다. 이 패턴은 OBO 온톨로지의 전형이고 OBO Foundry 전체에서 수천 번 쓰인다.

---

## 4. 왜 트리플 하나로 쓰지 않는가

이 패턴은 사실상 "글리포세이트는 제초제 역할을 한다"는 것이다. 그렇다면 왜 아래 한 줄로 쓰지 않았을까. (책의 이 줄은 글리포세이트 번호를 27733으로 적고 있는데, 앞의 27744와 맞지 않는 표기 불일치로 보인다. 27744가 맞는 것으로 보이나 원문의 의도는 확인하지 못했다.)

```turtle
chebi:CHEBI_27744 obo:has_role chebi:CHEBI_24527 .
```

늘 그렇듯 답은 추론에 있다. 더 넓은 맥락에서 글리포세이트를 봐야 이유가 보인다. 그림 14.2는 CHEBI 안의 글리포세이트 주변을 보여 준다. 구조를 표로 풀어 본다.

| 출발점 | 관계 | 도착점 |
|---|---|---|
| glyphosate | 제약: has_role 일부 값이 herbicide | herbicide |
| herbicide | subClassOf | pesticide |
| glyphosate | 긴 subClassOf 사슬(glycine derivatives, amino acids, phosphonic acids 등)을 거쳐 | has_part 일부 값이 phosphorus 인 제약 |
| glyphosate | 긴 subClassOf 사슬(organic amino compound 등)을 거쳐 | has_parent_hydride 일부 값이 ammonia 인 제약 |

즉 글리포세이트는 세 갈래의 제약 클래스의 하위 클래스다. 이 구조를 이용하면 이런 질문에 답할 수 있다. "인을 포함하고 모체 수소화물이 암모니아인 살충제를 찾아라." 그림 13.6과 rdfs:subClassOf, owl:someValuesFrom, owl:onProperty의 의미를 알면 글리포세이트가 답임을 알 수 있다. 하지만 이 조건에 맞는 화학 물질을 어떻게 찾아낼 수 있을까.

---

## 5. 찾는 대상을 OWL 클래스로 정의하기

찾으려는 것을 OWL로 정의한다. 세 제약의 교집합이다. 주석(#)으로 개념 이름을 병기했다.

```turtle
:MyChemical a owl:Class ;
  owl:intersectionOf (
    [ a owl:Restriction ; owl:onProperty obo:has_role ;
      owl:someValuesFrom chebi:CHEBI_25944 ]  # pesticide
    [ a owl:Restriction ; owl:onProperty obo:has_parent_hydride ;
      owl:someValuesFrom chebi:CHEBI_16134 ]  # ammonia
    [ a owl:Restriction ; owl:onProperty obo:has_part ;
      owl:someValuesFrom chebi:CHEBI_28659 ]  # phosphorus
  ) .
```

OWL 추론을 돌리면 글리포세이트가 :MyChemical의 하위 클래스임이 추론된다. (책은 이 결과를 chebi:CHEBI_27733 rdfs:subclassOf :MyChemical로 적었는데, 앞의 번호 불일치와 같은 문제로 보인다.) 즉 글리포세이트가 조건에 맞는다.

OWL 의미 체계는 그림 14.2의 모든 복잡성을 알아서 처리했다. 글리포세이트가 속한 이름 있는 클래스의 사슬도, 선언된 역할 herbicide와 요구된 역할 pesticide 사이의 하위 클래스 사슬도 마찬가지다. 요구 조건 정의에는 이 중 어느 것도 나오지 않는다. 그것들은 CHEBI 모델과 OWL 의미 체계가 담당한다.

---

## 6. 이 모델로 할 수 없는 추론

CHEBI 모델로 끌어낼 수 없는 추론도 있다. 실험실에 샘플 화학 물질이 있고 실험 결과 인을 부분으로 가지며 모체 수소화물이 암모니아라고 하자. 그러면 그림 14.2 위쪽의 해당 제약 두 개의 멤버라는 사실은 추론할 수 있다. 그러나 이 샘플이 글리포세이트와 어떤 관계인지는 아무것도 추론할 수 없다. CHEBI는 이미 분류된 화학 물질을 검색하는 데는 유용하지만, 샘플을 식별하는 데는 쓸 수 없다.

| 할 수 있는 일 | 할 수 없는 일 |
|---|---|
| 조건에 맞는 분류된 화학 물질 찾기 | 실험실 샘플이 어느 화학 물질인지 식별 |
| 제초제가 살충제의 하위 클래스라는 사실을 거쳐 질문에 답하기 | 샘플의 성분 정보로 글리포세이트와의 관계 추론 |

---

## 7. 한 줄이 아니라 클래스 관계로 모델링한 이유

위 예시들이 CHEBI 저자들이 글리포세이트의 제초제 역할을 단일 트리플 대신 someValuesFrom으로 클래스 사이의 관계로 정의한 동기를 보여 준다. 클래스와 someValuesFrom으로 모델링하면 글리포세이트 클래스가 관련 사실(예를 들어 살충제와 제초제의 관계)을 담은 더 포괄적인 모델 안에 들어간다. 그러면 모델이 OWL 의미 체계와 함께 해당 질문에 답하는 일의 상당 부분을 대신 처리한다. 질문하는 사람이 알 필요가 없는 방식으로 모델이 정보를 담고 있다.

비유하면 도서관 분류 체계와 같다. "이 책은 요리책이다"라고만 적은 것보다 "요리책은 실용서의 한 갈래이고 실용서는 비소설이다"까지 분류 체계에 넣어 두면, 비소설을 찾는 사람에게 이 책도 저절로 나온다.

<br>
<br>
<br>

[Semantic Web for the Working Ontologist](../)
