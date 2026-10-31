# 주식 선택 전문가 시스템의 CLIPS 구현: 변수, 조건 요소, 수치 비교, 제어

앞에서 설계한 주식 선택 전문가 시스템을 CLIPS로 마저 코딩하는 부분이다. 문법은 이미 배웠지만 아직 다루지 않은 기능이 남아 있다. 그래서 저자는 네 가지 질문을 세우고 하나씩 답하면서 지식 베이스를 완성해 간다. 네 질문은 변수로 일반화된 규칙 만들기, AND/OR/NOT 조건 요소, 숫자를 비교하는 `test`, 충돌을 막는 제어 전략이다. 저자의 논지는 변수, 조건 요소, 수치 비교, 입력 통제와 `salience`만 갖추면 규칙 기반 시스템이 유연하면서도 충돌 없는 추천을 낼 수 있다는 것이다. 완성된 전체 코드는 이 장 부록에 있다고 한다.

---

## 1. 풀어야 할 네 가지 질문

- 변수를 써서 더 일반적인 규칙을 어떻게 만드는가
- AND, OR, NOT을 포함한 더 복잡한 불리언 표현을 어떻게 만드는가
- 숫자 정보를 처리하고 비교하는 규칙을 어떻게 만드는가
- 추론 엔진이 서로 상충하는 추천을 내지 못하게 하는 제어 전략을 어떻게 구현하는가

---

## 2. 변수로 일반화한 규칙

주식 지식 베이스의 첫 두 규칙은 특정 섹터 하나가 아니라 어떤 섹터에든 적용되어야 한다. 그래서 변수가 필요하다.

```
R1. If market is up and sector ?x is strong
    THEN buy in sector ?x
R2. IF market is down and sector ?x is weak
    THEN short in sector ?x
```

### 2.1 변수의 문법

CLIPS에서 변수는 물음표 뒤에 심볼 이름을 붙여 표기하며, 물음표와 이름 사이에 공백이 없어야 한다. 이름은 앞서 설명한 유효 심볼 규칙을 따르고, 추가로 문자로 시작해야 한다. 변수 이름은 코드 안에서 하는 역할이 드러나도록 의미 있게 짓는 것이 좋다. 변수는 다른 프로그래밍 언어에서처럼 값을 저장하는 데 쓴다.

### 2.2 R1과 R2의 CLIPS 코드

```
;If market is up and sector is strong, then buy in sector
(defrule R1-market-up
(market up)
(sector ?name strong)
=>
(assert (buy sector ?name)))
;If market is down and sector is weak, then short in sector
(defrule R2-market-down
(market down)
(sector ?name weak)
=>
(assert (short sector ?name)))
```

이렇게 쓰면 `(sector energy strong)`이든 `(sector financial strong)`이든 어느 섹터에나 같은 규칙이 작동한다. 시장이 상승 중이고 `(sector financial strong)`이면 `(buy sector financial)`이 유도된다. 변수가 없다면 섹터마다 규칙을 따로 써야 했을 것이다.

### 2.3 바인딩과 재사용

한 규칙 안에서는 같은 이름의 변수를 여러 곳에 쓸 수 있다. 변수는 LHS에서 처음 참조될 때 값에 바인딩(할당)되고, 규칙 안에서 그 값을 유지한다. 그래서 RHS에서 다시 쓸 수 있다. 책의 예는 이렇다.

```
(defrule Print-Name-and-Age
(person ?name)
(person ?age)
=>
(printout t ?name " is " ?age " years old."))
```

저자는 `(name "John Doe")`와 `(age 57)`을 assert하면 "John Doe is 57 years old."가 출력된다고 설명한다. (본문 코드는 두 패턴 모두 `person`으로 적혀 있는데, 설명과 맞추려면 각각 `name`, `age`가 의도된 것으로 보인다. 추출본의 표기를 그대로 두고 의도만 밝혀 둔다.) 또 저자는 변수가 없었다면 전문가 시스템이 훨씬 덜 유연해서 여러 유형의 전문가 추론을 해내지 못했을 것이라고 강조한다.

---

## 3. AND, OR, NOT 조건 요소

### 3.1 OR이 필요한 규칙

주식 지식 베이스의 `R6`은 OR이 필요하다.

```
R6. IF S&P500 is little-changed OR NASDAQ is little-changed
    THEN market is sideways
```

둘 중 하나만 참으로 확인되어도 충분하다. 지금까지의 규칙은 LHS의 사실이 모두 일치해야 하는 구조였다. 사실들 사이에 암묵적인 AND가 있었던 셈이다. CLIPS에서는 사실들 사이에 OR 조건 요소를 명시적으로 쓸 수도 있다.

```
;If either S&P500 or NASDAQ is little changed, the market is sideways
(defrule R6-market-sideways
(or (SP500 little-changed)
(NASDAQ little-changed))
=>
(assert (market sideways)))
```

### 3.2 전위 표기와 중위 표기

OR 조건 요소는 전위 표기(prefix form)로 쓴다. 연산자(여기서는 논리 연산자 OR)가 인수(패턴이나 사실)보다 앞에 오는 형식이다. 인수가 n개인 OR은 `(or (fact1) (fact2) (fact3) ... (factn))`으로 쓰고, 전체를 괄호로 감싸는 것이 CLIPS의 표기법이다. 우리에게 익숙한 중위 표기(infix form)는 `(fact1) or (fact2) or ... or (factn)`처럼 쓰며 대부분의 절차적 언어가 이 방식을 택한다. 하지만 CLIPS는 그렇지 않다.

### 3.3 AND, OR, NOT 조합

세 요소를 조합하면 더 복잡한 불리언 식을 만들 수 있다. 다음 두 규칙은 신호등 앞에서 멈추어야 하는 조건을 코드로 옮긴 것이다.

```
(defrule stop-at-traffic-light1
(or (light red)
(and (light yellow)
(enough-time false)))
=>
(assert (action stop))
(printout t "Stop." crlf))
```

```
(defrule stop-at-traffic-light2
(or (light red)
(and (light yellow)
(not (enough-time true))))
=>
(assert (action stop))
(printout t "Stop." crlf))
```

### 3.4 두 규칙 풀이

`stop-at-traffic-light1`은 `(light red)`이거나, `(light yellow)`와 `(enough-time false)`가 둘 다 참일 때 발화한다. 들여쓰기를 해 두면 논리 구조를 이해하기가 훨씬 쉽다. 이 규칙은 앞서 본 신호등 규칙들과 정확히 같은 전문성을 담고 있으면서, 그것을 하나의 규칙으로 압축했다.

`stop-at-traffic-light2`는 첫 규칙과 동등하다. `(enough-time false)` 대신 `(not (enough-time true))`를 썼을 뿐이고, 두 표현은 같은 의미의 사실이다. 이렇게 쓸 만한 좋은 이유는 없으며, 오히려 규칙이 불필요하게 복잡해진다. 논리의 층마다 괄호가 필요해서 닫는 괄호가 네 개나 된다.

### 3.5 OR을 피하는 지침

저자의 일반 원칙은 OR 조건 요소를 쓰는 대신 규칙을 두 개로 나누어 쓰라는 것이다. 그렇게 하면 각 규칙이 훨씬 덜 복잡하고 이해하기 쉽다. 예컨대 위의 정지 규칙은 빨간불일 때의 규칙과, 노란불인데 시간이 부족할 때의 규칙으로 나눌 수 있다. 앞의 신호등 여섯 규칙이 택한 방식이 바로 이것이다.

---

## 4. 수치 데이터와 test 조건 요소

### 4.1 대상 규칙

주식 지식 베이스에는 정량 데이터를 쓰는 규칙이 세 개 있다.

| 규칙 | 조건 | 결론 |
|---|---|---|
| `R7` | 유가 상승률이 20%를 초과 | 유가가 높다 |
| `R16` | 이자율이 9%를 초과 | 이자율이 높다 |
| `R17` | 이자율이 6% 미만 | 이자율이 낮다 |

### 4.2 코드

CLIPS는 규칙 LHS에서 숫자와 변수를 비교할 때 `test` 조건 요소를 쓴다. 먼저 패턴으로 값을 변수에 담고, 이어서 `test`로 비교한다.

```
;Oil prices are high when increase > 20%
(defrule R7-classify-oil-prices
(oil-increase ?percent)
(test (> ?percent 20) )
=>
(assert (oil-prices high)))
;Interest rate is high when > 9%
(defrule R16-classify-high-interest-rate
(interest-rate ?percent)
(test (> ?percent 9.0) )
=>
(assert (interest-rate-class high)))
```

```
;Interest rate is low when < 6%
(defrule R17-classify-low-interest-rate
(interest-rate ?percent)
(test (< ?percent 6.0) )
=>
(assert (interest-rate-class low)))
```

`(oil-increase 25)`라는 사실이 있으면 `?percent`가 25에 바인딩되고 `(> 25 20)`이 참이 되어 `(oil-prices high)`가 assert된다. 이 비교식도 연산자가 앞에 오는 전위 표기다. 이 과정은 앞서 본 충돌 예에서 유가가 25% 올랐다는 사실이 유가가 높다는 사실로 이어지던 바로 그 단계다.

### 4.3 관계 연산자와 논리 연산자

`>`(초과)와 `<`(미만) 외에 다음 관계 연산자로도 두 수를 비교할 수 있다.

- `=` 같다
- `<>` 같지 않다
- `>=` 크거나 같다
- `<=` 작거나 같다

`test` 안에서도 AND, OR, NOT 논리 연산자를 쓸 수 있다. 다음 규칙은 나이가 45세에서 65세 사이(양 끝 포함)인 사람을 중년으로 분류한다.

```
(defrule classify-middle-aged
(person ?age)
(test (and (>= ?age 45)
(<= ?age 65)))
=>
(assert (age-class middle-aged)))
```

---

## 5. 충돌을 막는 제어 전략

네 번째 질문은 규칙을 처리할 때 왜 제어 전략이 필요한가 하는 것이다. 앞에서 `S&P500 is little-changed`와 `Increase in oil prices = 25%`라는 두 사실이 주어지면 시스템이 서로 상충하는 두 추천에 이른다고 보았다. 첫 번째 사실에서는 시장이 횡보하므로 시장에서 빠지라는 결론이 나온다. 두 번째 사실에서는 유가가 높고 에너지 섹터가 강하므로 에너지 주식을 사라는 결론이 나온다.

### 5.1 방법 1: 입력 요청 통제

충돌을 막는 한 가지 방법은 시스템이 사용자에게 어떤 입력을 요청하는지를 통제하는 것이다. 시장이 횡보할 때는 시장에서 빠지라는 추천만 하고 다른 추천은 하지 않게 하고 싶다고 하자. 그러려면 시장이 상승이나 하락일 때만 유가 정보를 묻도록 규칙을 추가한다.

```
;Get oil price increase; request this input only when market is up or down
(defrule get-oil-price-increase "Oil price increase"
(or (market up)
(market down))
=>
(printout t "Enter oil price increase (in %)." crlf)
(bind ?percent(read))
(assert (oil-increase ?percent)))
```

이 규칙이 있으면 시장이 횡보일 때는 유가 상승률을 아예 묻지 않는다. 그러면 `(oil-increase ...)` 사실이 생기지 않으므로 에너지 매수 추천도 나오지 않는다. 시장이 상승이거나 하락일 때만 질문하기 때문이다. 이처럼 어떤 정보가 언제 시스템에 들어올 수 있는지를 통제해서 충돌을 막는다. 신호등 예제에서 노란불일 때만 시간 여유를 물었던 것과 같은 원리다.

### 5.2 방법 2: salience로 우선순위 부여

앞서 논의한 다른 기법은 가장 중요한 규칙이 먼저 실행되도록 우선순위를 주는 것이다. CLIPS에서는 `salience` 값을 선언해서 이를 구현한다. 값은 -10,000에서 10,000 사이의 숫자이고, 값을 지정하지 않으면 0으로 본다. 값이 클수록 우선순위가 높다. 따라서 `salience`를 지정하면 규칙의 실행 순서를 제어할 수 있다.

```
(defrule high-priority-rule
(declare (salience 50))
(rule high-priority)
=>
(printout t "This will print first."))
(defrule low-priority-rule
(declare (salience -50))
(rule low-priority)
=>
(printout t "This will print second."))
```

두 규칙의 조건이 모두 만족되어 있어도, `salience`가 50인 첫 규칙이 먼저 출력하고 -50인 둘째 규칙이 나중에 출력한다. 앞 절에서 말한 규칙 우선순위 해결책을 CLIPS가 문법으로 직접 지원하는 셈이다.

### 5.3 정리

저자가 보여 준 CLIPS의 제어 수단은 두 가지다. 하나는 입력 요청 규칙으로 정보가 들어오는 것을 통제하는 방법이고, 다른 하나는 `salience`로 규칙의 실행 순서를 통제하는 방법이다. 두 방법 모두 규칙의 조건을 일일이 고쳐 가며 미세하게 조정하지 않고도 충돌을 피할 수 있다.

<br>
<br>
<br>

[Diagrammatic Reasoning in AI](../)
