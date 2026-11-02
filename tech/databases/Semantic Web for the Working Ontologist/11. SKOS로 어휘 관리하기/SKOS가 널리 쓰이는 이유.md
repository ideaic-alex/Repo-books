# SKOS가 널리 쓰이는 이유

SKOS는 W3C 권고안이 된 뒤(원서는 두 번째 버전을 2008년으로 적는다) 사용이 크게 늘었다. AGROVOC와 미국 NAL 외에도 Library of Congress Subject Headings, West Key Numbering System, EUROVOC 같은 대규모 시소러스가 SKOS로 공개되었고 작은 규모의 어휘는 셀 수 없이 많다. 이 문서는 SKOS가 인기를 얻은 이유 네 가지를 정리한다.

---

## 1. 단순함

SKOS의 첫 글자 S는 Simple(단순)이다. 위원회는 이 목표를 상당히 이뤘다. 그래서 거의 모든 다른 어휘 체계로 표현된 어휘를 큰 노력 없이 SKOS로 옮길 수 있다. 기본 관계(broader, narrower, related)와 클래스(Concept, ConceptScheme)만으로 어휘의 핵심을 잘 담는다.

---

## 2. 변환이 쉽다

기존 어휘에서 broader, narrower, related 용어를 질의할 수 있다면 곧바로 SKOS로 바꿀 수 있다. 질의 결과를 다음 모양의 트리플로 적으면 끝이다.

```turtle
?narrow skos:broader ?broad .
```

이 단순함 덕에 SKOS 변환이 하나의 작은 산업처럼 생겼다. 스프레드시트, XML, 데이터베이스 같은 저장 형식으로 제공되던 어휘가 SKOS로 공개되는 일이 흔하다. 원서는 14장에서 금융 산업 비즈니스 온톨로지 FIBO(Financial Industry Business Ontology)가 이 방법으로 OWL과 SKOS 두 형식으로 공개되는 사례를 보여 주겠다고 예고한다.

---

## 3. 공식 표준의 빈자리

SKOS 전에는 어휘를 디지털 형태로 표현하는 데 공식(de jure) 표준이 없었다. 놀라운 상황인데, 독점적인 디지털 어휘 형식이 득세했고, 비독점 형식은 주요 표준 기구의 승인을 얻지 못했기 때문이다. ISO, NISO 같은 기관이 지원하는 시소러스 표준은 많지만, 시소러스를 디지털 형태로 어떻게 저장할지에 대한 규범적 권고는 담지 않았다.

---

## 4. 전역 식별자

마지막 이유는 좀 더 미묘하다. 어휘를 SKOS로 옮기려면 개념마다 전역에서 유일한 식별자를 골라야 한다. 대개 어렵지 않다. 이미 지역적으로 유일한 식별자가 있는 시소러스가 많기 때문이다. West Key Numbering System에는 키 번호가 있고 Library of Congress Subject Headings에는 자체 식별자가 있다.

SKOS로 옮기면 이 지역 식별자가 전역 식별자가 된다. 어휘끼리 연결할 때 이 점이 큰 이점이다. 조직이 합병하고 정보가 세계 규모로 공개될수록 어휘 사이를 연결해야 할 필요가 커진다. 웹 이전에 만든 옛 시소러스 표준은 이런 웹 중심의 어휘 관리를 염두에 두지 않았다.

AGROVOC와 NAL 매핑이 이점을 잘 보여 준다. 두 어휘의 "Groundwater"를 한 문장 안에서 말하려면 두 용어가 구별되는 표현이 필요한데, URI가 그 역할을 한다.

---

## 5. 정리 표

| 요인 | 핵심 내용 |
|---|---|
| 단순함 | 기본 관계 셋과 클래스 둘로 어휘의 핵심을 담는다 |
| 쉬운 변환 | broader, narrower, related를 질의할 수 있으면 트리플로 기록하면 된다 |
| 표준의 공백 | 어휘를 디지털로 저장하는 공식 표준이 없었다 |
| 전역 식별자 | 지역 식별자가 URI가 되어 어휘 간 연결이 쉬워진다 |

표를 읽으면, SKOS의 인기는 진입 장벽이 낮고 웹 환경에 맞춰져 있다는 데서 나온다.

<br>
<br>
<br>

[Semantic Web for the Working Ontologist](../)
