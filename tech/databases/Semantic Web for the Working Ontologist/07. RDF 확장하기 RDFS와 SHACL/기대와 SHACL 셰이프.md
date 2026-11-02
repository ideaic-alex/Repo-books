# 기대와 SHACL 셰이프

추론은 "이미 본 데이터에서 더 끌어내는" 일이었다. 이번에는 반대 방향, 아직 보지 못한 데이터가 어떤 모습이어야 하는지 미리 말하는 일을 다룬다. 이것이 SHACL(Shapes Constraint Language)의 몫이다. 이 문서는 왜 기대가 필요한지, 기대가 어떤 세 가지 형태로 나타나는지, 그리고 SHACL 셰이프(shape, 데이터의 기대 모양을 적은 모델) 하나를 줄 단위로 읽는 법을 정리한다.

---

## 1. 왜 기대가 필요한가

웹에서 만나는 데이터는 미리 알 수 없다. 그래서 시맨틱 웹은 열린 세계 가정(open-world assumption, 1.3절)에서 출발한다. 새 데이터가 나타나 뒤집을 수 없는 결론만 내리는 태도다. 웹에서 주워 온 데이터를 해석할 때는 이 가정이 맞다.

하지만 데이터를 해석하는 게 아니라 데이터에 대한 기대를 가지고 행동해야 하는 상황이 있다. 기대는 여러 곳에서 온다.

| 기대의 출처 | 예 |
|---|---|
| 규제 | 대출 신청서에는 차용인의 특정 정보가 들어 있어야 한다 |
| 회사 정책 | 대출을 검토하려면 차용인에 대해 이런 정보가 필요하다 |
| 상식 | 차용인의 생년월일이 미래일 수는 없다 |

이런 기대는 SHACL이 다룬다.

## 2. 기대의 세 가지 형태

| 형태 | 상황 | 목적 |
|---|---|---|
| 데이터 검증(data validation) | 웹에서 만난 데이터가 어떤 종류의 것을 설명한다고 주장하고, 그 종류에 대한 기대가 있다 | 데이터가 기대에 맞는지 확인한다 |
| 사용자 입력 요청(soliciting user input) | 링크드 데이터로 공개된 데이터가 아니라 사용자에게 직접 입력을 받으려 한다 | 사용자에게 기대하는 데이터의 모습을 알린다. 보통 폼이나 마법사(wizard)로 한다 |
| 사용자 입력 검증(validating user input) | 기대를 알려 줬는데도 사용자가 기대와 다른 형태로 입력할 수 있다 | 첫 번째 경우와 같이 데이터를 기대에 비추어 검증한다 |

이 세 가지를 하나의 셰이프로 모두 처리할 수 있다는 점이 다음 문서의 핵심이다.

## 3. 셰이프라는 이름의 뜻

데이터 설명에 대한 기대는 "데이터가 가져야 할 모양(shape)"의 명세로 볼 수 있다. 사용자 입력을 받을 때는 이 비유가 문자 그대로다. 명세로 폼을 만들어 사용자에게 채우게 하기 때문이다. 입력 데이터를 검증할 때는 좀 더 비유적이다.

모양 외에도 기대는 값에 제약을 건다. 성인의 나이는 18(또는 데이터 모양의 의도에 따라 21)보다 커야 하고, 사회보장번호는 XXX-XX-XXXX 형태여야 한다. 이런 직관에서 시맨틱 웹의 기대 모델링 언어 이름이 SHACL이 되었다. SHACL은 기대하는 데이터 설명의 모양과 유효성 제약을 지정하는 수단이다.

## 4. 셰이프 하나 읽기: Account

원서는 Account 셰이프 하나로 세 가지 쓰임을 모두 보여 준다. 먼저 눈여겨볼 점이 두 가지다.

첫째, 이 셰이프도 RDF로 쓰여 있다. 시맨틱 웹의 모든 언어는 RDF로 표현되어서, 그 언어로 쓴 모델도 그 자체로 링크드 데이터셋처럼 웹에 배포될 수 있다(5장).

둘째, sh:로 시작하는 자원이 많다. 첫 줄에서 sh:는 W3C가 관리하는 `http://www.w3.org/ns/shacl#`의 접두어로 선언된다(5.1절). 새 언어를 RDF 위에 만들 때 언어 발행자(여기서는 W3C)가 자기가 관리하는 한 도메인 안에 자원들을 정의하는 전형적인 방식이다. 이 HTTP URI를 역참조(dereference)하면 그 자원에 대한 설명이 나온다. `http://www.w3.org/ns/shacl#`를 브라우저에 붙여 넣으면 SHACL을 설명하는 W3C 권고안 문서가 나온다.

```turtle
@prefix sh : <http://www.w3.org/ns/shacl#> .
account:Account
  rdf:type sh:NodeShape ;
  rdfs:label "Account" ;
  sh:property [ ... ] ;
  sh:property [ ... ] ;
  sh:property [ ... ] .
```

Account는 노드 셰이프(NodeShape)이고, 그 안에 속성 셰이프 세 개가 들어 있다. 각 속성 셰이프는 sh:path로 어떤 속성에 거는 제약인지 밝힌다.

### lastName: 문자열이고 값은 최대 하나

```turtle
sh:property [
  rdf:type sh:PropertyShape ;
  sh:path account:lastName ;
  sh:datatype xsd:string ;
  sh:name "family name" ;
  sh:maxCount 1 ; sh:minCount 1 ] ;
```

(원서 그림의 이 부분에는 sh:description "the name shared by all members of a family"도 있다.) 본문 설명은 값이 문자열이어야 하고 최대 하나라고 한다. 코드에는 sh:minCount 1도 함께 적혀 있어, 코드를 따르면 값이 정확히 하나여야 한다. 본문 설명과 코드가 약간 다르게 보이는 곳이다.

### ssn: 정확히 하나, 문자열, 패턴 일치

```turtle
sh:path account:ssn ;
sh:datatype xsd:string ;
sh:maxCount 1 ;
sh:minCount 1 ;
sh:name "SSN" ;
sh:pattern
 "[0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9]" ] ;
```

값은 반드시 하나(최소 1, 최대 1)이고 문자열이어야 하며, 정규식 패턴에 맞아야 한다. 원서는 정규식 자체는 다루지 않지만, 이 패턴은 각 X가 0부터 9까지의 숫자인 "XXX-XX-XXXX" 형태를 뜻한다고 설명한다. sh:description은 "US Social Security Number - format XXX-XX-XXXX"다.

### gender: 최대 하나, 목록 안의 값

```turtle
sh:path account:gender ;
sh:datatype xsd:string ;
sh:in ( "female" "male" "other" ) ;
sh:maxCount 1 ;
sh:name "gender" .
```

값은 최대 하나이고, 주어진 목록의 "male", "female", "other" 중 하나여야 한다. 최소 개수는 정하지 않았다.

## 5. 키워드 정리

| 키워드 | 뜻 |
|---|---|
| sh:NodeShape | 어떤 종류의 노드(여기서는 Account)에 대한 셰이프 |
| sh:property | 노드 셰이프 안에 속성 셰이프를 붙인다 |
| sh:path | 제약이 걸리는 속성 |
| sh:datatype | 값의 데이터 타입 |
| sh:minCount, sh:maxCount | 값의 최소, 최대 개수 |
| sh:pattern | 값이 맞아야 하는 정규식 |
| sh:in | 허용하는 값의 목록 |
| sh:name, sh:description | 사람이 읽는 이름과 설명 |

## 6. 세 속성의 제약 비교

| 속성 | 타입 | 개수 | 추가 조건 |
|---|---|---|---|
| account:lastName | 문자열 | 최소 1, 최대 1 (본문은 최대 1이라고만 설명) | 없음 |
| account:ssn | 문자열 | 최소 1, 최대 1 | 정규식 패턴 |
| account:gender | 문자열 | 최대 1 (최소는 정하지 않음) | "female", "male", "other" 중 하나 |

핵심은 "정하지 않은 것은 허용한다"는 점이다. gender는 최소를 정하지 않았으므로 아예 비워도 유효하다.

---

## 7. 정리

- 기대는 규제, 정책, 상식에서 오며, 데이터 검증, 사용자 입력 요청, 사용자 입력 검증의 세 형태로 나타난다.
- SHACL 셰이프는 RDF로 쓰이며 sh: 접두어 자원으로 이루어진다.
- 노드 셰이프 안의 속성 셰이프가 sh:path로 가리킨 속성에 타입, 개수, 패턴, 허용 값 목록 같은 제약을 건다.

<br>
<br>
<br>

[Semantic Web for the Working Ontologist](../)
