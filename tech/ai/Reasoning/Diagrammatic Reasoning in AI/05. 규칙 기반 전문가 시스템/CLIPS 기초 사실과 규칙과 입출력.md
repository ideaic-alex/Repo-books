# CLIPS 기초: 사실, 규칙, 신호등 예제와 입출력

CLIPS는 전문가 시스템을 만드는 도구이며, 이 문서는 그 기본 문법과 동작 방식을 다룬다. 먼저 CLIPS의 성격과 세 가지 구성요소를 소개하고, 사실(fact)의 필드 유형과 표기 규칙, 규칙(rule)의 구조를 설명한다. 이어서 교통 신호등 예제를 CLIPS 규칙으로 옮기며 전방 추론이 실제로 어떻게 이어지는지 보이고, 사용자 입력을 받는 규칙과 대화 세션까지 살펴본다. 저자의 논지는 사실과 규칙만 알면 작동하는 전문가 시스템을 짧은 시간에 만들 수 있다는 것이다.

---

## 1. CLIPS 소개

- **CLIPS(C Language Integrated Production System)**: 1986년에 NASA 존슨 우주 센터가 만든 전문가 시스템 개발 도구이다. 원래 C 언어로 작성되었지만, 문법은 AI 프로그래밍 언어인 LISP과 더 닮았다.
- **공개 도메인**: 지금은 공개 도메인이어서 웹에서 무료로 내려받을 수 있고, 문서도 무료로 구할 수 있다.
- **널리 쓰이는 이유**: 무료이고 효율적이며 배우기 쉬워서 오늘날 가장 널리 쓰이는 전문가 시스템 도구가 되었다. 저자는 짧은 시간에 다양한 응용을 만들기에 좋은 선택이라고 평가한다.

### 1.1 세 가지 기본 구성요소

대부분의 전문가 시스템 셸(shell)처럼 CLIPS도 세 요소로 이루어져 있다.

1. **사실 목록(fact list)**: 데이터를 담는 작업 메모리이다.
2. **지식 베이스(knowledge base)**: 규칙들의 모음이다.
3. **추론 엔진(inference engine)**: 규칙의 실행을 제어한다.

### 1.2 이 절의 진행 방식

CLIPS 언어를 이해하려면 사실(작업 메모리)과 IF-THEN 규칙(지식 베이스), 이 두 가지를 알면 된다. 저자는 두 항목의 문법을 먼저 설명한다. 그다음 앞에서 다룬 교통 신호등 문제와 주식 선택 문제를 코드로 옮겨, 사실과 규칙에서 전문가 시스템이 만들어지는 과정을 보여 준다. 추론 엔진은 사실과 규칙을 처리해 추천을 낸다. CLIPS의 추론 엔진은 전방 추론만 하도록 설계되어 있고, 후방 추론은 흉내 낼 방법이 따로 있다고 한다. 기본적인 입출력 함수와 간단한 질의응답 인터페이스까지 다루고 나면, 작업 메모리, 지식 베이스, 추론 엔진, 사용자 인터페이스라는 네 구성요소가 어떻게 함께 작동하는지 이해할 수 있다.

---

## 2. 사실(Facts)

CLIPS에서는 정보를 사실로 표현한다. 사실은 필드 하나로 이루어질 수도 있고 여러 개로 이루어질 수도 있다. 저자가 든 예는 다음과 같다.

```
(animal)
(San-Francisco)
(age 27)
(weight 154.4 kilograms)
(name "Robbie T. Nakatsu")
(place-of-birth Austin Texas USA)
(place-of-birth "Austin, TX USA")
(sex male)
(gives Bob Harry apple)
(grocery-list apples cereal eggs chicken ketchup)
```

사실을 포함해 CLIPS의 모든 명령은 괄호로 감싼다. 이 관습은 LISP에서 이어받은 것이다.

### 2.1 필드의 세 유형

위 예의 필드는 심볼, 문자열, 숫자의 세 종류이다. (저자는 각주에서 CLIPS에 실제로는 여덟 가지 필드 유형이 있다고 밝힌다. 그러나 이 책은 심볼, 문자열, 정수, 부동소수점의 네 가지 기본형만 다룬다. 숫자는 정수와 부동소수점을 합친 복합 유형이다.)

- **심볼(symbol)**: 출력 가능한 ASCII 문자로 시작하고 그 뒤에 0개 이상의 문자가 따르는 필드이다. 공백, 탭, `&`, `|`, `,`, `~`, 큰따옴표, 괄호 같은 구분자는 들어갈 수 없다. 또 `?`나 `$?`로 시작해서도 안 된다. 이 기호들은 변수를 나타내는 데 쓰이기 때문이다.
- **문자열(string)**: 큰따옴표로 시작해서 큰따옴표로 끝난다. 공백이 들어간 이름, 책 제목, 주소, 지시문, 설명 문장처럼 서술 정보를 담을 때 쓴다.
- **숫자(number)**: 정수(`3`, `+5`, `106`, `0`, `-65`) 또는 부동소수점(`1.2`, `-3.4`, `4.976`, `-14.5`, `4.67e10`)이다.

### 2.2 심볼의 유효성

유효한 심볼의 예는 `cat`, `cat-2`, `cat2`, `set-off-alarm`, `567-87-9000`, `!A`, `alert?`이다. 무효한 심볼의 예는 `A&P`(구분자 `&` 포함), `"house"`(따옴표), `|girl`, `?why`(`?`로 시작), `house,100`(쉼표), `~`이다.

### 2.3 심볼과 문자열을 쓰는 곳

지식 베이스의 규칙을 부호화할 때는 대체로 심볼을 쓰고 문자열은 피하는 것이 좋다. 문자열은 길고 오타가 나기 쉬워서, 추론 엔진이 하는 패턴 매칭 작업에 덜 알맞기 때문이다. 문자열은 리터럴 정보를 담은 출력 메시지를 보여 줄 때 가장 잘 어울린다.

---

## 3. 순서 있는 사실과 객체-값 쌍

### 3.1 순서 있는 사실과 없는 사실

필드의 순서가 의미를 갖는 사실을 순서 있는 사실(ordered fact)이라 한다. `(gives Bob Harry apples)`가 그런 예다. 첫 필드는 관계(`gives`), 둘째는 주는 사람 Bob, 셋째는 받는 사람 Harry, 넷째는 건네진 물건 apples를 뜻하므로 자리를 바꾸면 의미가 달라진다. 반면 `(grocery-list apples cereal eggs chicken ketchup)`은 식료품을 늘어놓은 순서가 중요하지 않으므로 순서 없는 사실이다. 다만 첫 필드인 `grocery-list`는 관계를 나타내므로 맨 앞에 와야 한다. 이 점에서는 이 사실도 여전히 순서가 있다.

### 3.2 객체-값 쌍으로 쓰기

사실은 필드 하나로 쓰기보다 객체-값 쌍(object-value pair)으로 쓰는 것이 좋은 관행이다. 이 장 앞부분에서 IF-THEN 규칙을 객체-값 쌍으로 표현한 것과 같은 방식이다. "신호등이 초록이면 행동은 간다"는 규칙은 두 가지로 쓸 수 있다.

- (A) `IF (light green) THEN (action go)`
- (B) `IF (green) THEN (go)`

둘 다 허용되지만 A가 낫다. 사실이 무엇을 뜻하는지 더 분명하기 때문이다. 그래서 저자는 책 전체에서 항상 객체-값 쌍으로 사실을 표기하기로 한다.

### 3.3 사실 목록과 assert, retract

사실 목록은 현재 문제와 관련된 모든 활성 사실을 모아 놓은 것이다. 사용자가 초기 사실로 넣은 사실과 추론 엔진이 유도한 사실이 모두 여기에 놓인다. 사실을 더하려면 `assert` 명령을, 지우려면 `retract` 명령을 쓴다.

```
(assert (age 27))
(assert (weight 154.4 kilograms))
(retract (age 45))
(retract (weight 154.4 kilograms))
```

사실이 괄호로 감싸이고 명령 전체도 다시 괄호로 감싸이므로, 괄호 안에 괄호가 들어간다.

### 3.4 대소문자 구분

CLIPS는 대소문자를 구분한다. 따라서 `(city Los-Angeles)`와 `(city los-angeles)`는 서로 다른 두 도시를 나타내는 별개의 사실로 취급된다.

---

## 4. 규칙(Rules)의 구조

규칙은 LHS(left-hand side, 조건부)와 RHS(right-hand side, 행동부) 두 부분으로 나뉜다. 그림 5.3은 규칙의 일반 문법을 보여 주며, 요점은 다음과 같다.

- 규칙은 `defrule` 다음에 규칙 이름, 선택 사항인 주석 문자열, 패턴들, `=>`, 행동들의 순서로 쓴다.
- 규칙 이름은 고유해야 한다.
- LHS에는 패턴(사실)을 몇 개든 둘 수 있다.
- `=>` 기호가 LHS와 RHS를 가른다.
- RHS에는 행동을 몇 개든 둘 수 있다.
- 규칙 전체를 여는 괄호는 마지막 괄호로 닫아야 하므로, 괄호를 하나도 빠뜨리지 말고 모두 닫아야 한다.

### 4.1 매칭과 발화

CLIPS는 LHS의 패턴을 사실 목록의 사실과 맞춰 본다. 추론 엔진의 중요한 기능이 바로 이 LHS 패턴 매칭이다. LHS의 모든 패턴이 사실 목록에서 발견되면 그 규칙이 발화(fired) 또는 활성화(activated)되었다고 하며, 이때 RHS에 적힌 행동들이 실행된다.

---

## 5. 교통 신호등 예제 코드

앞에서 설계한 신호등 전문가 시스템의 규칙 여섯 개는 아래와 같이 코딩된다. 먼저 초록, 빨강 신호를 다루는 두 규칙이다.

```
(defrule green-light "Go when green."
(light green)
=>
(assert (action go))
(printout t "Go." crlf))
(defrule red-light "Stop when red."
(light red)
=>
(assert (action stop))
(printout t "Stop." crlf))
```

노란불은 시간 여유에 따라 두 규칙으로 나뉜다.

```
(defrule yellow-light1 "Yellow Light: enough time"
(light yellow)
(enough-time true)
=>
(assert (action go))
(printout t "Proceed with caution." crlf))
(defrule yellow-light2 "Yellow Light: not enough time"
(light yellow)
(enough-time false)
=>
(assert (action stop))
(printout t "Stop." crlf))
```

마지막 두 규칙은 `action` 사실을 받아 실제 조작으로 바꾼다.

```
(defrule press-gas-pedal "Press on gas pedal."
(action go)
=>
(assert (gas-pedal press))
(printout t "Press on gas pedal." crlf))
(defrule press-brake "Press on brake."
(action stop)
=>
(assert (brake press))
(printout t "Press on brake." crlf))
```

### 5.1 암묵적 AND

이 규칙들은 각각 패턴을 한 개나 두 개 가진다. 한 규칙에 패턴이 여러 개이면 그 사이에 암묵적 AND가 있어서, 모든 패턴이 참이어야 규칙이 발화한다. 예를 들어 `yellow-light1`은 `(light yellow)`와 `(enough-time true)`가 둘 다 참일 때만 발화한다.

### 5.2 전방 추론의 연쇄

모든 규칙은 `assert` 행동을 하나씩 가지고 있어서 사실 목록에 새 사실을 더한다. `green-light`는 `(action go)`를 사실 목록에 올린다. 이 사실이 `press-gas-pedal`의 LHS에 있는 패턴과 맞으면 그 규칙이 발화하고, `(gas-pedal press)`가 추가된다. 이렇게 한 규칙이 사실을 만들고 그 사실이 다른 규칙의 발화를 부르는 과정이 CLIPS에서의 전방 추론이다. 새 사실이 계속 쌓이면 규칙이 차례로 발화하다가 마침내 최종 추천에 이른다.

---

## 6. 입출력

### 6.1 printout

여섯 규칙에는 모두 출력 행동도 들어 있다. `printout` 함수는 사용자의 화면에 메시지를 보여 주며, 문법은 `(printout t "text" crlf)`이다. 여기서 `t`는 컴퓨터의 표준 출력 장치, 대개 화면을 가리킨다. `crlf`는 캐리지 리턴과 줄바꿈이어서 새 줄을 시작하게 하며, 화면 모양을 정돈하는 데 쓴다. 이 함수로 전문가 시스템의 추천과 안내 메시지를 사용자에게 알려 줄 수 있다.

### 6.2 입력 규칙이 필요한 이유

위 여섯 규칙에는 사용자가 신호등 색을 알려 줄 방법이 없다. 시스템이 추천하려면 초기 사실이 필요하므로, 입력용 규칙을 적어도 두 개 더 둔다.

```
;get input from user on the color of the traffic light
(defrule get-light-color
=>
(printout t "What is the color of the traffic light?" crlf)
(bind ?color(read))
(assert (light ?color)))
```

```
;get input from user if yellow light.
(defrule get-enough-time
(light yellow)
=>
(printout t "There is enough time to go through the intersection. Enter true or false." crlf)
(bind ?truefalse(read))
(assert (enough-time ?truefalse)))
```

### 6.3 get-light-color 풀이

첫 규칙은 화면에 "What is the color of the traffic light?"라고 묻는다. 그리고 사용자가 입력한 값을 `read`로 읽어 `bind`로 변수 `?color`에 저장(바인딩)한다. 그다음 `(light ?color)`를 assert하는데, 이때 `?color`의 값은 사용자가 입력한 값이다. 사용자가 `green`을 입력하면 `(light green)`이 사실 목록에 올라간다.

### 6.4 조건 없는 규칙과 주석

이 규칙은 LHS에 패턴이 하나도 없다. 이것도 유효한 코딩 방식이며, 규칙이 조건 없이 언제나 발화한다는 뜻이다. 주석은 세미콜론 뒤에 쓰며, 추론 엔진은 세미콜론부터 줄 끝까지를 무시한다. 주석은 지식 베이스 어디에나 넣을 수 있으므로 규칙의 역할을 적어 두는 데 쓸 수 있다.

### 6.5 get-enough-time 풀이

둘째 규칙은 시간 여유가 있는지 묻고, 있다고 답하면 `(enough-time true)`를, 없다고 답하면 `(enough-time false)`를 assert한다. LHS에 `(light yellow)`가 있으므로 노란불일 때만 실행된다. 초록이나 빨강일 때는 이 질문이 의미가 없기 때문이다.

### 6.6 질의응답의 흐름 통제

이 예는 전문가 시스템이 지식 베이스를 따라 질의응답의 흐름을 이끌 수 있음을 보여 준다. 사용자가 생각할 수 있는 모든 입력을 미리 넣을 필요는 없다. 추론 엔진이 규칙에 따라 필요한 때에만 정보를 요청하기 때문이다. 이는 지식 베이스 설계의 좋은 관행으로 평가된다. 또 `printout`과 `bind`를 합치면 아주 단순한 입출력 사용자 인터페이스가 되어, 사용자와 시스템이 텍스트로 대화할 수 있다. 기초적인 수준이지만 다양한 상호작용을 구성할 수 있다.

---

## 7. 대화 세션 (그림 5.4)

신호등 지식 베이스를 올린 CLIPS에서 상담이 이루어지는 과정은 다음과 같다. 사용자는 프롬프트 `CLIPS>`에서 `(reset)`을 입력해 작업 메모리, 곧 사실 목록을 비우고 새 세션을 시작한다. 이어서 `(run)`을 입력하면 시스템이 실행되어 첫 질문을 던진다. 그림 5.4는 `(reset)`과 `(run)`으로 시작하는 세 가지 세션을 보여 준다.

| 세션 | 사용자 입력 | 시스템 출력 |
|---|---|---|
| 1 | `green` | Go. / Press on gas pedal. |
| 2 | `yellow`, 이어서 `true` | Proceed with caution. / Press on gas pedal. |
| 3 | `yellow`, 이어서 `false` | Stop. / Press on brake. |

세션 2와 3에서는 노란불을 입력한 뒤에야 시간 여유를 묻는 두 번째 질문이 나온다. 앞 절에서 설명한 조건부 질문이 실제로 작동하는 장면이다.

### 7.1 이 인터페이스의 한계

저자는 이런 질의응답으로 할 수 있는 일이 매우 제한적이어서 더 나은 방식이 필요하다고 인정한다. 그래픽과 다이어그램을 이용해 사용자 인터페이스를 개선하는 방법, 그리고 더 투명하고 유연하며 사용자 친화적인 인터페이스를 만드는 여러 접근은 다음 장에서 본격적으로 다룬다.

<br>
<br>
<br>

[Diagrammatic Reasoning in AI](../)
