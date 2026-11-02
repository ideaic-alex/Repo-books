# URI 이름 짓기

웹처럼 여러 곳에 흩어진 시스템에서는 이름을 어떻게 붙이느냐가 생각보다 큰 영향을 준다. 5장에서는 HTTP URI의 도메인 이름을 고르는 문제와 슬래시 URI, 해시 URI의 차이를 다뤘다. 그런 것을 다 정한 뒤에도 남는 질문이 있다. URI 끝에 붙는 로컬 이름(local name)을 어떻게 지을 것인가. 이 문서는 사람이 읽을 수 있는 이름과 의미 없는 이름 중 무엇을 고를지, 이름을 바꿔야 할 때 어떻게 하는지, 그리고 W3C가 따르는 이름 짓기 관습을 정리한다.

로컬 이름은 슬래시 URI에서는 마지막 슬래시 뒤, 해시 URI에서는 해시 뒤의 부분이다. CURIE(Compact URI, 접두어로 줄여 쓴 URI)에서 콜론 뒤에 나오는 이름이다. `skos:broader`의 로컬 이름은 `broader`, `wikidata:Q41176`의 로컬 이름은 `Q41176`이다.

---

## 1. 읽히는 이름이냐, 의미 없는 이름이냐

로컬 이름을 사람이 읽고 뜻을 알 수 있게 지을지 말지가 첫 번째 질문이다. 둘 다 성공한 사례가 있다.

| 방식 | 설명 | 예 |
|---|---|---|
| 불투명한 이름(opaque local name) | 네임스페이스 안에서 유일하기만 하면 되는 의미 없는 문자열, 보통 숫자 | `wikidata:Q41176`("building"), `agrovoc:c_4397`("Livestock") |
| 읽히는 이름(readable local name) | 사람이 읽고 뜻을 알 수 있는 이름 | `skos:broader`, `owl:someValuesFrom`, `fibo-be-le-lp:LegalPerson` |

두 방식 모두 쓸 만한 선례가 있어서 어느 쪽이 정답이라고 할 수 없다. 장단점을 따져 선택해야 한다.

---

## 2. 불투명한 이름의 장점

위키미디어 재단이 위키데이터에서, 그리고 유엔(UN) 식량농업기구(FAO)가 AGROVOC(농업 분야 어휘집)에서 의도적으로 이 방식을 골랐다. 이유는 다음과 같다.

**이름이 바뀔 수 있다.** 지식이 쌓이면 대표 이름이 바뀔 수 있다. "building"은 안정적인 단어 같아도 영어에 동의어가 있고, 쓰이는 모습을 보면 structure, construction, erection, edifice 중 하나가 더 낫다고 판단될 수 있다. 불투명한 이름이면 수정이 간단하다. 라벨 트리플만 지우고 새로 넣으면 된다.

```turtle
wikidata:Q41176 rdfs:label "building" .
wikidata:Q41176 rdfs:label "structure" .
```

원문은 위의 첫 줄을 지우고 둘째 줄로 바꾼다고 설명한다. URI는 그대로라서 이 URI를 가리키던 다른 곳이 깨지지 않는다.

**여러 언어 문제가 사라진다.** 유엔은 공식 언어가 여섯 개이고 모든 문서를 여섯 언어로 동시에 내야 한다. `c_4397`의 로컬 이름을 읽히게 짓는다면 `agrovoc:Livestock`이어야 할까, `agrovoc:Bétail`이어야 할까. 어느 쪽이든 유엔의 언어 지침에 어긋난다고 볼 수 있다. 불투명한 이름은 이 논쟁을 꺼내지 않고 끝낸다.

**희망적 이름 붙이기를 피한다.** URI에 읽히는 이름을 주지 않으면 모델이 표현하지 않은 의미가 있다고 착각할 일이 줄어든다. 웹의 인프라에서 URI는 원래 의미가 없다. 의미가 있는 척하는 것은 도움이 되지 않는다.

---

## 3. 불투명한 이름의 단점

그래도 학생과 개발자들은 불투명한 이름을 좋아하지 않는다. 이유는 뻔하다. 이 책에서 `agrovoc:c_4397`이라고 쓰면 어딘가에 "Livestock이다"라고 주석을 달아야 한다. 개발 현장도 마찬가지다. 온톨로지 관리 도구에서 `agrovoc:c_4397` 같은 참조가 가득한 구조를 보면 뜻을 알 수 없어서 모델 검토가 매우 어렵다.

도구로 어느 정도 풀 수 있다. 대부분의 어휘 도구는 라벨로 리소스를 표시하는 모드가 있다. AGROVOC에는 다음 트리플이 있어서 도구가 이 이름으로 보여 줄 수 있고, 프랑스어로 현지화된 도구라면 Bétail로 바꿔 보여 줄 수도 있다.

```turtle
agrovoc:c_4397 skos:prefLabel "Livestock"@en , "Bétail"@fr .
```

하지만 이 해결책에도 한계가 있다. 미국 국립농업도서관(NAL)에도 시소러스가 있고 AGROVOC와 겹치는 영역이 크며, 거기에도 "Livestock"이라는 리소스가 있다. 두 어휘를 비교하려 할 때, 도구가 아무리 선호 라벨과 다국어를 잘 처리해도 하나는 AGROVOC의 Livestock이고 다른 하나는 NAL의 Livestock이라는 것을 어떻게 보여 줄까. 읽히는 이름이었다면 CURIE로 `agrovoc:Livestock`과 `NAL:Livestock`처럼 바로 구분된다. 라벨만 쓰면 "livestock"과 "livestock"의 관계를 묻게 되고, 그 질문은 "AGROVOC 의미의 livestock과 NAL 의미의 livestock"으로 풀어 써야 말이 된다. CURIE는 이를 정밀하고 간결하게 해 주지만 읽히는 URI일 때만 의미가 있다.

---

## 4. 읽히는 이름의 단점과 FIBO의 사례

읽히는 이름의 문제는 합법적인 HTTP URI가 무엇이냐에서 나온다. URI는 웹에서 리소스를 식별하는 이름으로 네트워크를 건너 전송되므로 전송 규약이 형식에 간섭한다. 특히 로컬 부분에는 괄호, 앰퍼샌드, 공백 같은 특수 문자를 쓸 수 없다. 그런데 많은 대상의 자연스러운 이름에는 이런 문자가 들어간다. `agrovoc:c_2018`은 "dairy cattle"인데 이걸 읽히는 URI로 만들면 공백이 들어가 규약에 어긋난다. 우회 방법은 있지만 모두 URI와 대표 이름의 연결을 끊는다. 전송 규약(HTTP)이 개념의 이름이라는 사람 사이의 소통 방식에 영향을 주게 되는 것이 핵심 문제다.

금융업 비즈니스 온톨로지 FIBO(Financial Industry Business Ontology)는 역사적 이유로 모든 URI를 읽히는 이름으로 지었고, 이름이 바뀐 적도 있다. 기술 용어 Juridical Person은 실제 사람이 아닌 법적 주체, 말하자면 법적 허구를 가리킨다. 어떤 종류의 사람이 사람이 아니라고 정의하는 것은 혼란스럽다는 의견이 많아서 FIBO는 대표 이름을 Legal Entity로 바꿨다. 이때 두 가지 선택이 있었다.

| 선택 | 결과 | 문제 |
|---|---|---|
| URI는 두고 라벨만 변경 | `JuridicalPerson`이라는 URI에 "Legal Entity" 라벨 | 이름과 라벨이 어긋나 혼란이 오히려 커진다 |
| URI도 새 이름으로 변경 | `LegalEntity`에 "Legal Entity" 라벨 | 옛 URI를 참조하던 웹의 애플리케이션이 가리킬 대상을 잃어 데이터를 못 찾는다 |

국제 표준인 FIBO에게 두 번째는 받아들일 수 없는 결과다. FIBO는 둘을 절충했다. 옛 URI는 남기되 "폐기(deprecated)" 표시를 하고, `owl:equivalentClass`로 새 URI와 연결하며, 정의·제약·역관계 같은 추가 정보는 새 URI로 옮겼다. 원문의 트리플은 다음과 같다.

```turtle
fibo-be-le-lp:JuridicalPerson rdfs:label "juridical person" ;
    owl:deprecated true ;
    owl:equivalentClass fibo-be-le-lp:LegalEntity .
fibo-be-le-lp:LegalEntity a owl:Class ;
    rdfs:label "legal entity" ;
    rdfs:subClassOf fibo-be-le-lp:LegalPerson ;
    owl:disjointWith fibo-be-le-lp:LegallyCompetentNaturalPerson ;
    ... .
```

원문은 마지막 `owl:disjointWith` 뒤에 줄임표로 나머지를 생략한다. 이 방식은 라벨 일관성을 지키고, 기존 사용자를 만족시키며, 필요할 때 핵심 개념의 이름을 바꿀 수 있게 해 준다. 읽히는 URI에서 이름이 바뀌는 문제를 상당히 줄인다.

정리하면 두 관습 중 어느 쪽이 압도적으로 낫지는 않다. 그래서 성공한 오픈 온톨로지에서 두 방식이 다 보인다. 위 분석은 프로젝트별로 결정할 때 고려할 걱정거리를 대부분 다뤘다.

| 항목 | 불투명한 이름 | 읽히는 이름 |
|---|---|---|
| 이름 변경 | 라벨만 바꾸면 되어 쉽다 | URI 변경이나 폐기 처리가 필요하다 |
| 다국어 | 언어 중립이다 | 어느 언어를 고를지 문제가 생긴다 |
| 읽기 편의 | 도구 지원이 필요하다 | 사람이 바로 읽는다 |
| 어휘 간 구분 | 라벨만으로는 모호하다 | CURIE로 명확히 구분된다 |
| URI 문자 제약 | 영향 없다 | 공백, 괄호 등을 쓸 수 없다 |

읽는 법은 간단하다. 유지보수와 다국어가 중요하면 불투명한 쪽이, 사람의 가독성과 어휘 간 비교가 중요하면 읽히는 쪽이 유리하다.

---

## 5. 이름 짓기 관습

읽히는 URI를 쓸 때는 공백 같은 제약 때문에 허용되는 이름이 제한된다. 이런 사정에서 RDFS와 OWL 모델의 로컬 이름에 대한 사실상의 관습(de facto convention)이 생겼다. XML 등 다른 웹 모델링 언어의 이름 관습과 대체로 맞고, W3C 자신과 이 책 전체가 따르는 방식이다.

| 규칙 | 설명 | 예 |
|---|---|---|
| CamelCase로 쓴다 | 여러 단어를 공백 없이 쓰고 각 단어를 대문자로 시작한다 | `rdfs:subClassOf`, `owl:InverseFunctionalProperty` |
| 클래스 이름은 대문자로 시작한다 | | `owl:Restriction`, `owl:Class` |
| 속성 이름은 소문자로 시작한다 | 첫 글자만 빼고 CamelCase | `rdfs:subClassOf`, `owl:inverseOf` |
| 개체 이름은 대문자로 시작한다 | | `lit:Shakespeare`, `ship:Berengaria` |
| 클래스 이름은 단수 명사로 한다 | | `owl:DatatypeProperty`, `owl:SymmetricProperty`, `lit:Playwright`(`lit:Playwrights`가 아니다) |

표의 예에서 `rdfs:subClassOf`가 CamelCase 규칙과 속성 규칙에 모두 나오는 점에 주목한다. 규칙들은 한 이름에 동시에 적용된다. 단수 이름 규칙은 뒤에서 보듯 클래스를 "구성원의 집합"으로 읽을 때 문장이 자연스럽게 읽히게 해 준다.

<br>
<br>
<br>

[Semantic Web for the Working Ontologist](../)
