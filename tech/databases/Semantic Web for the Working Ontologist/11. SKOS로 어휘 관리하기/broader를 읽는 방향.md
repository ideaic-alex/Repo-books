# broader를 읽는 방향

`skos:broader`는 처음 보면 방향이 헷갈리는 속성이다. 많은 사람이 기대하는 방향과 정반대로 읽어야 하기 때문이다. 이 문서는 `rdfs:subClassOf`와 SKOS의 계층 속성이 어디서 닮았고 어디서 다른지, 그리고 그 차이가 왜 혼동을 만드는지 설명한다.

---

## 1. subClassOf와 닮은 점

`skos:narrower`, `skos:broader`의 정의는 `rdfs:subClassOf`, 그리고 RDFS 표준에는 정의되지 않은 superClassOf와 상당히 닮았다. 이 속성 쌍들은 모두 계층을 모델링하려는 것이다.

- 계층을 위로도 아래로도 거슬러 오를 수 있으면 좋다.
- 관계가 전이적이라는 점이 중요하다.

차이도 있다. RDFS에서는 `subClassOf`의 전이성이 모델에 직접 들어 있다. SKOS는 더 정교한 모델을 쓴다. 전이적인 broader와 narrower를 쓸지는 사용자가 정하게 한다(앞 문서의 전이적 상위 속성 패턴).

---

## 2. SKOS에 없는 규칙

`subClassOf`에는 SKOS에 대응 조건이 없는 정의가 하나 있다. RDFS의 타입 전파 규칙이다.

```sparql
CONSTRUCT { ?x rdf:type ?C }
WHERE { ?x rdf:type ?B .
        ?B rdfs:subClassOf ?C . }
```

이 규칙 덕에 `rdfs:subClassOf`는 해석에 혼동이 없다. B의 구성원이 모두 C의 구성원도 되므로 C가 두 클래스 중 더 포괄적이다(구성원 수가 같거나 더 많다). 클래스 간 포함 방향이 추론으로 못 박혀 있는 셈이다.

SKOS의 `skos:broader`에는 이런 규칙이 없다. 그래서 같은 줄을 두 가지로 읽을 수 있다.

```turtle
agrovoc:c_7030 skos:broader agrovoc:c_4397 .
```

| 읽는 방식 | 뜻 |
|---|---|
| (가) | c_7030(Sheep)의 broader term은 c_4397(Livestock)이다 |
| (나) | c_7030(Sheep)이 c_4397(Livestock)보다 더 넓다 (잘못된 읽기) |

SKOS 형식 모델 안에는 어느 쪽인지 알려 주는 것이 없다. 방향은 `skos:broader`, `skos:narrower`에 붙은 비공식 주석에서 얻는다. 이 속성들의 라벨이 각각 "has broader", "has narrower"다. 따라서 의도된 해석은 (가)다. Sheep이 Livestock이라는 더 넓은 용어를 가진다는 뜻이다. (원서는 두 번째 읽기를 "c_4397 is broader than c_7030"으로 적는데, 이는 (가)와 같은 뜻이라 오해를 부른다. 여기서는 헷갈리기 쉬운 잘못된 읽기를 (나)로 적었다.)

---

## 3. 코드에서 마주칠 때

이 책의 SKOS 예제에는 다음과 같은 트리플이 나온다.

```turtle
:Sheep skos:broader :Livestock .
```

"Sheep이 Livestock보다 넓다"로 읽으면 반대다. 주어가 좁은 쪽이고 목적어가 넓은 쪽이다. 원서도 많은 사람에게 이 해석이 기대와 반대라고 인정한다.

| 비교 | `rdfs:subClassOf` | `skos:broader` |
|---|---|---|
| 주어 쪽 | 하위(좁은 쪽) | 좁은 쪽 |
| 목적어 쪽 | 상위(넓은 쪽) | 넓은 쪽 |
| 방향을 보증하는 것 | 타입 전파 규칙 | 속성 라벨의 비공식 주석 |

위 표에서 `subClassOf`와 `broader` 열은 방향이 같다. 둘 다 주어가 좁은 쪽이다. 다만 `subClassOf`는 추론 규칙이 방향을 증명하고, `broader`는 라벨 주석만이 방향을 알려 준다.

추론 기반의 의미 정의가 있었다면 의도된 방향이 명확했을 것이고, Sheep과 Livestock 같은 예제를 보며 방향을 짐작할 필요도 없었을 것이다. 이것이 원서가 짚는 아쉬운 점이다. 실무에서는 `broader`를 "has broader"로 소리 내어 읽는 습관을 들이면 실수를 줄일 수 있다.

<br>
<br>
<br>

[Semantic Web for the Working Ontologist](../)
