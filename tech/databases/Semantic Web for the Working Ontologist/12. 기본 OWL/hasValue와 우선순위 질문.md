# hasValue와 우선순위 질문

이 문서는 세 번째 제한인 owl:hasValue를 다룬다. "이 속성의 값으로 바로 이것을 가진 개체들"이라는 가장 구체적인 제한이다. 질문지 예시에서는 질문마다 우선순위를 달고, 우선순위가 높은 항목을 자동으로 분류하는 데 쓴다. 이 제한은 양방향 추론이 된다는 점이 특히 쓸모 있다.

---

## 1. hasValue: "이 값을 가진다"

owl:hasValue 역시 owl:onProperty가 가리키는 속성에 대한 제한이다. "속성 P의 값으로 A를 가진 모든 개체"라는 클래스를 만든다.

```turtle
[ a owl:Restriction ;
  owl:onProperty P ;
  owl:hasValue A ]
```

형식적으로 hasValue는 someValuesFrom의 특수한 경우다. someValuesFrom에서 클래스 C가 원소가 하나뿐인 집합 A일 때가 바로 hasValue다. 그럼에도 OWL 표준은 hasValue를 따로 이름 붙여 둔다. 매우 흔하고 유용한 모델링 형태이기 때문이다.

hasValue의 효과는 특정한 개체 하나에 대한 설명을 클래스 설명으로 바꿔 준다는 점이다. 원서의 예를 보면 "태양 둘레를 도는 모든 행성의 집합"과 "일본에 있는 모든 야구 팀의 집합"이 hasValue 제한으로 정의된다.

| 제한 | 값에 대한 요구 | 예 |
|---|---|---|
| someValuesFrom C | C에 속하는 값이 하나 이상 | AllStarTeam 중 한 곳에서 뛴다 |
| hasValue A | 정확히 그 값 A를 가진다 | orbitsAround의 값으로 TheSun을 가진다 |

두 제한의 차이는 "클래스 중 아무거나"와 "바로 그 개체"의 차이다. 같은 모양의 문장에서 목적어 자리에 클래스가 오면 someValuesFrom, 개체 하나가 오면 hasValue를 쓴다.

## 2. 예 14: 우선순위 질문

질문지의 각 질문에 우선순위를 매긴다고 하자. 먼저 우선순위 수준의 클래스와 그 개체들을 정의한다.

```turtle
q:PriorityLevel a owl:Class .
q:High a q:PriorityLevel .
q:Medium a q:PriorityLevel .
q:Low a q:PriorityLevel .
```

우선순위를 나타내는 속성은 다음과 같다.

```turtle
q:hasPriority rdfs:range q:PriorityLevel .
```

여기서 range만 정의하고 domain은 정의하지 않았다는 점에 주의한다. 질문뿐 아니라 여러 종류의 것에 우선순위를 줄 수 있기 때문이다. domain을 질문으로 못 박으면 질문이 아닌 것에 우선순위를 준 데이터를 읽을 때 그것을 질문이라고 추론하는 부작용이 생긴다. 그래서 domain은 비워 둔다.

### 우선순위 높음 항목 클래스

owl:hasValue로 우선순위가 높은 항목의 클래스를 정의한다.

```turtle
q:HighPriorityItem owl:equivalentClass
  [ a owl:Restriction ;
    owl:onProperty q:hasPriority ;
    owl:hasValue q:High ] .
```

책의 그림 12.8은 이 정의를 보여 준다. 앞에서는 제한 클래스의 하위 클래스나 상위 클래스를 선언했는데 여기서는 owl:equivalentClass를 써서 두 클래스가 같다고 선언했다. 그래서 이름 있는 클래스 q:HighPriorityItem이 이름 없는 제한 클래스와 같은 것이 된다. 이름이 있으면 다른 주장을 덧붙이거나 클래스를 더 제한할 때 쓰기 편하다.

중간과 낮음도 같은 방식이다.

```turtle
q:MediumPriorityItem owl:equivalentClass
  [ a owl:Restriction ;
    owl:onProperty q:hasPriority ;
    owl:hasValue q:Medium ] .
q:LowPriorityItem owl:equivalentClass
  [ a owl:Restriction ;
    owl:onProperty q:hasPriority ;
    owl:hasValue q:Low ] .
```

## 3. 추론의 양방향

### 값에서 클래스로

질문의 우선순위를 입력하면 해당 클래스의 구성원이라고 추론된다.

```turtle
d:WhatProblem q:hasPriority q:High .
d:InternetSymptom q:hasPriority q:Low .
```

그러면 다음이 추론된다.

```turtle
d:WhatProblem a q:HighPriorityItem .
d:InternetSymptom a q:LowPriorityItem .
```

### 클래스에서 값으로

hasValue는 "거꾸로"도 쓸 수 있다. d:TVsymptom이 HighPriorityItem이라고 선언했다고 하자.

```turtle
d:TVsymptom a q:HighPriorityItem .
```

owl:equivalentClass의 의미 때문에, d:TVsymptom은 제한 클래스의 구성원이 되고, 따라서 그 제한이 요구하는 조건을 지켜야 한다. 그래서 다음이 추론된다.

```turtle
d:TVsymptom q:hasPriority q:High .
```

| 방향 | 입력한 사실 | 추론되는 사실 |
|---|---|---|
| 값에서 클래스로 | d:WhatProblem q:hasPriority q:High | d:WhatProblem a q:HighPriorityItem |
| 값에서 클래스로 | d:InternetSymptom q:hasPriority q:Low | d:InternetSymptom a q:LowPriorityItem |
| 클래스에서 값으로 | d:TVsymptom a q:HighPriorityItem | d:TVsymptom q:hasPriority q:High |

이 표를 보면 equivalentClass 덕분에 두 문장이 같은 정보를 다르게 말하는 관계가 된다. 한쪽을 입력하면 다른 쪽이 따라 나오므로 어느 쪽으로 데이터를 입력해도 모델 전체가 일관되게 유지된다.

### 클래스 정의가 말해 주지 않는 것

HighPriorityItem의 정의에는 그 항목이 질문이어야 한다는 조건이 없다. 질문 외의 것에도 우선순위를 둘 수 있기 때문이다. d:TVsymptom이 q:Question이라는 사실은 이미 선언해 둔 트리플에서만 알 수 있고, 이 정의에서 따라 나오지 않는다.

원서는 다음 장에서 집합 연산을 써서 "질문이면서 우선순위가 높은 것"처럼 제한과 다른 클래스를 합쳐 정의하는 방법을 보이겠다고 예고한다.

## 4. 세 제한 한눈에 비교

지금까지 본 세 제한을 같은 질문지 예시로 나란히 놓으면 차이가 분명하다.

| 제한 | 질문지에서의 쓰임 | 입력한 사실이 하는 일 | 추론되는 것 |
|---|---|---|---|
| someValuesFrom | q:AnsweredQuestion | 질문이 Answer 개체를 선택 옵션으로 가진다 | 그 질문이 AnsweredQuestion의 구성원 |
| allValuesFrom | 선택된 답의 enablesCandidate 제한 | 선택된 답이 어떤 질문을 후보로 가진다 | 그 질문이 EnabledQuestion의 구성원 |
| hasValue | q:HighPriorityItem | 항목이 q:High를 우선순위 값으로 가진다 | 그 항목이 HighPriorityItem의 구성원(반대 방향도 가능) |

표가 보여 주는 것은 추론의 대상이다. someValuesFrom과 hasValue는 값을 가진 쪽이 클래스에 편입되고, allValuesFrom은 값을 가진 쪽에서 값 쪽으로 타입이 번진다.

## 5. 정리

- hasValue는 someValuesFrom의 특수한 경우지만 자주 쓰이므로 독립된 키워드로 있다.
- 개체 하나에 대한 설명을 클래스 설명으로 바꿔 주는 것이 핵심 효과다.
- owl:equivalentClass와 함께 쓰면 값에서 클래스로, 클래스에서 값으로 두 방향 모두 추론된다.
- domain을 일부러 비워 두면 속성을 질문 이외의 것에도 자유롭게 쓸 수 있다.

<br>
<br>
<br>

[Semantic Web for the Working Ontologist](../)
