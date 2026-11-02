# 속성·스키마 탐색, DISTINCT, FILTER

앞 문서에서는 주어와 목적어 자리에만 변수를 썼다. SPARQL은 서술어 자리에도 변수를 쓸 수 있다. 이 기능 덕분에 낯선 데이터셋(dataset, 한곳에 모인 데이터 묶음)이 무엇을 담고 있는지 질의로 탐색할 수 있다. 이 문서는 그 탐색 질의, 중복을 지우는 DISTINCT, 조건으로 행을 걸러 내는 FILTER를 차례로 다룬다. 마지막에 초보자가 자주 하는 FILTER 실수도 짚는다.

---

## 1. 서술어 자리에 변수 쓰기

질의에 쓰는 문법은 Turtle과 같으므로 세미콜론(같은 주어 이어 쓰기)과 쉼표(같은 주어·서술어 이어 쓰기) 줄임 표기도 쓸 수 있다. 이 장에서는 지금부터 그 표기를 쓴다.

"James Dean에 대해 아는 것을 모두 보여 줘"는 트리플 하나로 된다.

```
SELECT ?property ?value
WHERE { :JamesDean ?property ?value }
```

| ?property | ?value |
|---|---|
| bornOn | 1931-02 (원문 표에는 날짜가 잘려 있다) |
| diedOn | 1955-09-30 |
| playedIn | RebelWithoutaCause |
| playedIn | EastOfEden |
| playedIn | Giant |
| rdf:type | Man |
| rdfs:label | James Dean |

읽는 법: 속성 이름도 값도 몰라도 된다. 이 질의가 해당 개체(instance)에 붙은 모든 속성과 값을 보여 준다. 낯선 데이터셋을 처음 열어 볼 때 쓰는 시작점이다. 시맨틱 웹에서는 이런 일이 자주 생긴다.

원서의 표에서 bornOn 값이 "1931-02"로 끊겨 있고 diedOn은 1955-09-30으로 적혀 있다. 이 장의 다른 예제에서는 James Dean의 사망일이 1955-10-30으로 나오기도 해서, 원서 표기가 서로 일치하지 않는다. 이 노트는 원문 표기를 그대로 옮긴다.

값이 필요 없고 어떤 종류의 정보가 있는지만 알고 싶다면 SELECT에서 ?property만 고르면 된다. 이 질의는 "이 데이터셋은 James Dean에 대해 어떤 종류의 정보를 알고 있나"라는 메타데이터를 묻는 것과 같다.

---

## 2. DISTINCT로 중복 지우기

?property만 골랐더니 결과에 :playedIn이 세 번 나온다. 패턴에 맞는 곳이 데이터에 세 군데 있었기 때문이다. SPARQL의 DISTINCT 키워드가 중복 행을 걸러 준다.

```
SELECT DISTINCT ?property
WHERE { :JamesDean ?property ?value }
```

결과는 bornOn, diedOn, playedIn, rdf:type, rdfs:label로 각각 한 번씩이다.

| 질의 | playedIn이 나오는 횟수 | 이유 |
|---|---|---|
| `SELECT ?property` | 3번 | 일치하는 곳이 세 군데라 행이 셋 |
| `SELECT DISTINCT ?property` | 1번 | 같은 행은 하나로 합친다 |

---

## 3. 스키마를 데이터에서 거꾸로 알아내기

서술어 자리에 변수를 쓸 수 있다는 점은 SPARQL이 다른 질의 언어와 다른 큰 특징이다. 덕분에 스키마(schema, 데이터 구조의 설계 정보) 정보를 데이터 자체에서 거꾸로 추출할 수 있다.

James Dean 대신 Actor 클래스에 속한 모든 개체를 대상으로 질의를 바꾸면 "배우를 설명하는 데 쓰인 속성"이 나온다.

```
SELECT DISTINCT ?property
WHERE { ?q0 a :Actor .
        ?q0 ?property ?object . }
```

결과는 bornOn, diedOn, playedIn, rdf:type, rdfs:label, produced, sang, wrote다. James Dean 한 명에게는 없던 produced, sang, wrote가 다른 배우들 덕분에 더해졌다.

클래스 자체를 모를 때도 물을 수 있다. 상위 클래스 Person 아래의 하위 클래스를 찾는 질의는 다음과 같다.

```
SELECT DISTINCT ?class
WHERE { ?class rdfs:subClassOf :Person }
```

답은 :Actor, :Actress, :Man, :Woman, :Politician, :Producer다.

데이터에 대해 아무것도 모를 때는 사용된 모든 클래스, 또는 모든 속성을 찾는 질의를 쓴다.

| 목적 | 질의 | 핵심 패턴 |
|---|---|---|
| 데이터에 쓰인 모든 클래스 | `SELECT DISTINCT ?class WHERE { ?q0 a ?class }` | 주어 자리는 아무거나, 타입 자리만 변수 |
| 데이터에 쓰인 모든 속성 | `SELECT DISTINCT ?property WHERE { ?q0 ?property ?q1 }` | 세 자리 전부 변수 |
| 한 클래스의 하위 클래스 | `SELECT DISTINCT ?class WHERE { ?class rdfs:subClassOf :Person }` | 서술어는 고정, 주어 자리가 변수 |
| 한 개체의 속성 | `SELECT DISTINCT ?property WHERE { :JamesDean ?property ?value }` | 서술어 자리가 변수 |

이런 질의가 가능한 이유는 두 가지다. 첫째, RDF에서는 주어, 서술어, 목적어 어느 부분이든 변수로 매칭할 수 있다. 둘째, RDF의 스키마 언어인 RDFS(RDF Schema)도 RDF로 표현되어 있다(8장). 그래서 데이터와 스키마를 같은 질의로 훑을 수 있다. 이 두 성질이 RDF를 대부분의 표현 언어를 넘어서는 "자기 설명적(self-describing)" 언어로 만든다.

---

## 4. 변수, 바인딩, FILTER

지금까지 ?property, ?q0, ?deathdate 같은 것을 "의문사"라고 불렀지만, SPARQL에서는 보통 변수(variable)라고 부른다. 이제부터 변수라고 부른다.

James Dean과 동료 배우들 중에는 젊어서 죽은 사람도 있고 오래 산 사람도 있다. "Giant에 출연한 배우 중 영화 제작 이후 5년을 넘게 산 사람"을 찾아 보자. 먼저 Giant 출연 배우의 사망일을 구한다.

```
SELECT ?actor ?deathdate
WHERE { ?actor :playedIn :Giant ;
               :diedOn ?deathdate . }
```

결과는 RockHudson 1985-10-02, JamesDean 1955-10-30이다. 답은 표 안에 있지만 질문, 곧 "1961년 11월 24일(Giant 제작 5년 뒤) 이후까지 산 사람"에는 아직 답하지 못했다.

이때 FILTER를 쓴다. FILTER는 불리언(참/거짓) 조건을 정해 그 조건을 통과하는 행만 결과에 남긴다.

```
SELECT ?actor
WHERE { ?actor :playedIn :Giant ;
               :diedOn ?deathdate .
        FILTER (?deathdate > "1961-11-24"^^xsd:date ) }
```

Rock Hudson은 조건이 참이므로 남고, James Dean은 거짓이므로 빠진다.

| 구분 | 그래프 패턴 | FILTER |
|---|---|---|
| 역할 | 데이터에서 찾을 모양을 적는다 | 찾은 행 중 남길 행을 고른다 |
| 쓰는 모양 | 중괄호와 트리플 | 소괄호 안 불리언 식 |
| 변수의 값을 만드는가 | 만든다(바인딩) | 만들지 못하고 이미 있는 값만 쓴다 |

읽는 법: FILTER는 패턴이 아니라 시험이다. 그래서 중괄호가 아닌 소괄호로 쓴다.

FILTER에서 쓸 수 있는 시험은 XQuery에서 가져온 것이다. 자세한 목록은 SPARQL 표준에 있다. 대체로 정수, 부동소수, 문자열, 날짜 같은 XML 데이터 타입의 산술과 비교를 쓸 수 있고, XPath 표준의 함수도 쓸 수 있다.

| 종류 | 예 |
|---|---|
| 비교 | `>`, `<` 등 |
| 문자열 정규식 | `REGEX` |
| 논리 연산 | AND(`&&`), OR(`||`), NOT(`!`) |

---

## 5. 흔한 실수: 바인딩되지 않은 변수를 FILTER에 쓰기

변수는 이름이 아니라 그래프 패턴 속 트리플에서 의미를 얻는다. 변수 이름을 ?actress라고 지었다고 여성만 매칭되지는 않았다. 마찬가지로, FILTER에서 의미 있는 이름의 변수를 썼다고 그 변수가 값을 갖는 것은 아니다. 초보자가 자주 하는 실수다. "East of Eden에 출연했고 1930년 1월 1일 이후에 태어난 배우"를 이렇게 쓴다고 하자.

```
SELECT ?actor
WHERE { ?actor :playedIn :EastOfEden .
        FILTER (?birthday > "1930-01-01"^^xsd:date ) }
```

결과는 없다. ?birthday가 패턴 어디에도 나오지 않아 값이 전혀 없기 때문이다. 변수가 뜻 없는 이름이라는 점을 떠올리면 이 질의는 ?birthday를 ?q0로 바꾼 아래 질의와 같다.

```
SELECT ?actor
WHERE { ?actor :playedIn :EastOfEden .
        FILTER (?q0 > "1930-01-01"^^xsd:date ) }
```

패턴에 ?q0가 무엇인지 알려 주는 것이 없으니 비교가 성립하지 않는다. 올바른 질의는 생일을 이어 주는 트리플을 넣는 것이다.

```
SELECT ?actor
WHERE { ?actor :playedIn :EastOfEden ;
               :bornOn ?birthday .
        FILTER (?birthday > "1930-01-01"^^xsd:date ) }
```

이제 ?birthday에 값이 있어 1930년 1월 1일과 비교할 수 있다. FILTER 문법은 이런 잘못된 사용을 막지 않는다. 경험칙은 하나다. FILTER에서는 그래프 패턴에 이미 나온 변수만 참조한다.

---

## 6. FILTER를 여러 개 쓰기

1960년대에 태어난 사람을 찾을 때는 FILTER를 두 개 쓴다. 여러 FILTER는 모두 참이어야 그 행이 결과에 남는다.

```
SELECT ?person
WHERE { ?person a :Person ;
                :bornOn ?birthday .
        FILTER (?birthday > "Jan 1, 1960"^^xsd:date )
        FILTER (?birthday < "Dec 31, 1969"^^xsd:date ) }
```

한 FILTER 안에서 불리언 연산자로 조건을 합칠 수도 있다.

```
FILTER (?birthday < "Jan 1, 1960"^^xsd:date &&
        ?birthday > "Dec 31, 1969"^^xsd:date )
```

주의할 점이 있다. 원서에 실린 이 두 번째 형태(Query 6.20)는 부등호 방향이 앞의 질의와 반대로 되어 있어서, 글자 그대로는 1960년 이전이면서 동시에 1969년 이후인 날짜를 요구하게 된다. 그런 날짜는 없으니 원서의 오류로 보인다. 같은 뜻으로 쓰려면 부등호 방향을 첫 번째 질의와 맞춰야 한다. 날짜 문자열 형식("Jan 1, 1960" 등)도 원서 표기 그대로이고, 실제 xsd:date는 "1960-01-01" 같은 형식이다. 이 노트는 확실히 알 수 없는 부분은 원문대로 두었다.

여기서도 ?person이 :Person이라는 것을 보장하는 것은 변수 이름이 아니라 첫 트리플 `?person a :Person`이다.

| 조합 방법 | 의미 |
|---|---|
| FILTER를 여러 개 나열 | 모든 FILTER가 참이어야 한다 |
| 한 FILTER 안에서 `&&`, `||`, `!` | 불리언 식 전체가 참이어야 한다 |

---

## 7. 정리

- 서술어 자리에도 변수를 쓰면 "이 개체는 어떤 속성을 가졌나", "이 데이터에는 어떤 클래스와 속성이 쓰였나"를 질의할 수 있다.
- DISTINCT는 겹치는 행을 한 줄로 합친다.
- 변수의 의미는 이름이 아니라 패턴 속 트리플이 정한다. FILTER에서 쓰는 변수는 패턴에서 먼저 바인딩(값을 얻음)되어 있어야 한다.
- FILTER는 불리언 시험으로 행을 걸러 내며, 소괄호로 쓴다.

<br>
<br>
<br>

[Semantic Web for the Working Ontologist](../)
