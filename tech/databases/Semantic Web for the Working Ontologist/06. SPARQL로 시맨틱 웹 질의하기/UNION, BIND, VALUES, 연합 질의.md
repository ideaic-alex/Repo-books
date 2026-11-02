# UNION, BIND, VALUES, 연합 질의

SPARQL 고급 기능의 마지막 묶음이다. 이 문서는 "또는"을 뜻하는 UNION, 질의 중에 값을 계산하는 BIND, 질의에 데이터를 직접 적는 VALUES, 그리고 여러 데이터 소스를 한 질의로 묶는 연합 질의(SERVICE, GRAPH)를 다룬다. 앞 세 가지는 한 데이터 안에서 질의를 유연하게 하고, 마지막은 웹 전체로 질의를 넓힌다.

---

## 1. UNION: 이거 또는 저거

그래프 패턴은 여러 트리플로 이루어지고 모든 트리플이 매칭되어야 패턴이 매칭된다. 논리로 보면 트리플 사이에 암묵적인 "그리고(AND)"가 있다. 첫째 트리플이 맞고 그리고 둘째 트리플이 맞고 그리고 셋째가 맞아야 한다. "이 트리플이 맞거나 저 트리플이 맞으면 된다"고 하고 싶을 때가 있다. 이때 쓰는 것이 UNION이다.

UNION은 두 그래프 패턴을 합쳐서 각 패턴이 만든 모든 바인딩의 합집합을 결과로 준다. 각 패턴의 변수는 서브쿼리처럼 서로 독립적으로 값을 취하고, 결과만 합쳐진다. Rebel Without a Cause 또는 Giant에 출연한 배우를 구하는 질의는 이렇다(Query 6.60).

```
SELECT ?actor
WHERE {
  {?actor :playedIn :Giant .}
  UNION
  {?actor :playedIn :RebelWithoutaCause . }
}
```

결과에는 Ann Doran, Carroll Baker, Elizabeth Taylor, James Dean, James Dean, Jim Backus, Mercedes McCambridge, Natalie Wood, Rock Hudson, Sal Mineo, Sal Mineo가 나온다. 두 영화에 모두 나온 배우(James Dean, Sal Mineo)는 두 번 나온다. 중복은 DISTINCT로 없앤다.

UNION은 CONSTRUCT에서도 쓴다. 앞서 hasMother, hasFather, hasSon, hasDaughter를 hasParent로 바꾸는 CONSTRUCT 질의를 네 개 따로 썼다. 그 방식은 질의를 돌리는 프로그램이 결과를 한데 모아 주리라는 암묵적 전제(예컨대 같은 트리플 스토어에 모두 추가한다는)가 필요하다. UNION을 쓰면 합친다는 사실을 질의 안에서 분명히 적을 수 있다(Query 6.61).

```
CONSTRUCT {?s :hasParent ?o }
WHERE { {?s :hasMother ?o }
        UNION
        {?s :hasFather ?o }
        UNION
        {?o :hasSon ?s }
        UNION
        {?o :hasDaughter ?s }
}
```

결과는 네 질의를 따로 돌려 합친 것과 같은 hasParent 관계다.

| 구분 | 트리플 사이 | 결과 |
|---|---|---|
| 일반 그래프 패턴 | 암묵적 AND | 모든 트리플이 동시에 맞는 경우 |
| UNION으로 묶은 패턴 | OR | 어느 한쪽이라도 맞는 경우의 합집합 |

읽는 법: 패턴을 점(.)으로 이으면 AND, UNION으로 이으면 OR다.

---

## 2. BIND: 질의 중에 값 계산하기

저자 이름을 "전체 이름"으로 출력하고 싶다고 하자. 데이터에는 이름(first)과 성(last)만 있고 "James Hendler"라는 문자열은 어디에도 없다. 어떻게 만들까.

질의하고 답하는 시스템(tell-and-ask)은 보통 "알려 준" 정보로 답한다. 스프레드시트, 노트, 데이터베이스, RDF 저장소가 모두 그렇다. 하지만 많은 시스템은 직접 알려 주지 않은 정보를 지정하는 방법도 준다. 앞에서 본 집계(합, 평균, 개수)가 바로 그런 예였다. 질의할 때 특정 계산을 넣고 싶을 때도 있다. 스프레드시트는 데이터가 바뀔 때마다 갱신되는 임의의 수식을 쓸 수 있고, 데이터베이스에는 저장 프로시저(stored procedure)가 있다. SPARQL에서는 질의 시점의 할당(assignment)이 비슷한 역할을 한다. 할당은 데이터에서 값을 찾아 매칭하는 대신, 계산해서 변수에 값을 "배정"한다. SPARQL 1.0 표준에는 없고 1.1에서 지원한다. 키워드는 BIND다.

```
BIND ( expression(...) AS ?var )
```

식에는 산술식(+, -, *, / 등)이나 함수 호출 연쇄, 이미 매칭되었거나 묶인 다른 변수에 대한 참조가 들어간다. 관계형 데이터베이스의 저장 프로시저처럼 함수 호출에 여러 프로그래밍 언어로 쓴 임의의 프로그램을 넣을 수도 있다. 원서의 예제에서는 XML의 XPath 명세에서 가져온 표준 함수만 쓴다.

데이터에 책과 저자가 있다고 하자.

```
:DeanAllemang rdf:type :Person ;
    :firstName "Dean" ;
    :lastName "Allemang" .
:JimHendler rdf:type :Person ;
    :firstName "James" ;
    :lastName "Hendler" .
:WorkingOntologist rdf:type :Book ;
    dc:creator :DeanAllemang, :JimHendler, :FabienGandon .
```

원서에는 Fabien Gandon도 같은 형태로 들어 있으며 위에서는 줄였다. 문자열을 이어 붙이는 함수는 CONCAT이다(Query 6.62).

```
SELECT ?fullname
WHERE { :WorkingOntologist dc:creator ?author .
        ?author :firstName ?first .
        ?author :lastName ?last .
        BIND (CONCAT(?first, " ", ?last) AS ?fullname) }
```

결과는 James Hendler, Dean Allemang, Fabien Gandon이다. 데이터에는 Jim이 아니라 James로 저장되어 있다는 점을 눈여겨보자.

### 2.1 계산 결과를 다시 검색에 쓰기

BIND의 진가는 중간 계산에서 나온다. 계산 결과를 이어지는 검색의 조건으로 쓸 수 있다. 이 책 저자들의 이름을 조합한 이름을 가진 배우가 영화 데이터베이스에 있는지 찾아보자. 먼저 두 저자의 first name 조합을 만든다(Query 6.63).

```
SELECT ?n1 ?n2
WHERE { authors:WorkingOntologist dc:creator ?a1 .
        authors:WorkingOntologist dc:creator ?a2 .
        ?a1 authors:firstName ?n1 .
        ?a2 authors:firstName ?n2 . }
```

저자 세 명 중 두 자리를 고르는 모든 조합이라 3 x 3 = 9행이 나온다(Dean Dean, Dean James, Dean Fabien, James Dean, James Fabien, James James, Fabien Dean, Fabien James, Fabien Fabien). 같은 사람끼리의 조합은 FILTER로 빼고, BIND로 두 이름을 이어 붙여 검색 후보(probe)를 만든다(Query 6.64).

```
FILTER (?a1 != ?a2)
BIND (CONCAT(?n1, " ", ?n2) AS ?probe)
```

남는 후보는 "Dean James", "Dean Fabien", "James Dean", "James Fabien", "Fabien Dean", "Fabien James" 여섯 개다. 이제 이 후보를 영화 데이터에서 찾는다. 배우는 영화에 출연한(:playedIn) 사람으로 본다(Query 6.65).

```
SELECT DISTINCT ?who
WHERE {
  ... (위의 패턴, FILTER, BIND) ...
  ?who movies:playedIn ?any .
  ?who rdfs:label ?probe .
}
```

답은 movies:JamesDean이다. 이 책 저자들의 first name을 이어 붙인 이름을 가진 배우가 실제로 데이터베이스에 있다. 인쇄본의 Query 6.65에는 BIND 줄의 괄호가 하나 더 많은 오타가 있어 위에서는 생략 표기로 적었고, 쓸 때는 앞의 6.64 형태를 따르면 된다.

| 단계 | 하는 일 | 쓰는 문법 |
|---|---|---|
| 1 | 저자 이름 쌍을 모두 만든다 | 그래프 패턴 |
| 2 | 같은 사람끼리의 쌍을 뺀다 | FILTER |
| 3 | 두 이름을 이어 검색 후보를 만든다 | BIND와 CONCAT |
| 4 | 후보를 이름(label)으로 가진 배우를 찾는다 | 그래프 패턴 |

읽는 법: 앞 단계의 계산(BIND) 결과를 뒤 단계의 조건으로 쓰는 것이 포인트다. 계산한 값이 데이터 어디에도 없어도 데이터와 맞춰 볼 수 있다.

---

## 3. VALUES: 질의에 데이터 적어 넣기

보통 질의는 데이터 소스에서 데이터를 가져온다. 하지만 작은 데이터를 질의 안에 직접 적는 편이 편할 때가 있다. 저자 이름이 세 쌍뿐이라면 따로 데이터셋을 두지 않고 질의에 적으면 된다(Query 6.66).

```
SELECT *
WHERE {
  VALUES (?firstname ?lastname) {("James" "Hendler")
                                 ("Dean" "Allemang")
                                 ("Fabien" "Gandon")}
  BIND (CONCAT(?firstname, " ", ?lastname) AS ?fullname)
}
```

결과는 세 행이며 열은 ?firstname, ?lastname, ?fullname이다(예: James, Hendler, James Hendler). VALUES는 변수 목록과 값의 묶음을 적어 마치 데이터에서 매칭된 것처럼 변수에 값을 넣어 준다. 위 질의는 데이터 소스 없이 질의 혼자서 돌아가는 예다.

---

## 4. 연합 질의: 여러 데이터 소스를 한 질의로

지금까지는 책과 저자 정보, 영화 정보가 모두 하나의 그래프에 있다고 가정했다. 여러 그래프를 하나로 합쳐서 질의하는 것은 개념상 단순한 일이다. 하지만 항상 가능하지는 않다. 데이터셋이 아주 크면 질의 전에 합치기가 비현실적일 수 있고, 웹에서만 제공되며 접근이 제한될 수도 있다.

그래서 질의를 여러 데이터 소스에 걸쳐 연합(federate)하는 기능이 필요하다. 여기서 연합은 질의에서 데이터 소스를 가상으로 결합하되 각 소스가 자기 정체성을 유지한다는 뜻이다. 데이터 소스를 제공하는 방법은 여럿이다.

| 데이터 소스 형태 | 설명 | 질의에서 쓰는 키워드 |
|---|---|---|
| SPARQL 엔드포인트 | 웹에 공개된 원격 데이터셋 | SERVICE 뒤에 엔드포인트 URL |
| 이름 있는 그래프(named graph) | 한 데이터 소스 안에서 이름을 붙인 트리플 묶음 | GRAPH 뒤에 그래프를 나타내는 URL |

읽는 법: 두 키워드는 비슷한 문법이며 둘 다 연합 질의에 쓸 수 있다. 원격 서비스면 SERVICE, 같은 저장소 안의 이름 붙은 그래프면 GRAPH다.

### 4.1 DBpedia에 물어보기

엔드포인트가 SPARQL로 공개되어 있으면 서브쿼리를 각 엔드포인트로 보낼 수 있다. SERVICE 키워드 뒤에 엔드포인트 URL을 적고 그래프 패턴을 붙인다. Giant에 출연한 배우의 이름과 같은 label을 가진 항목이 DBpedia(http://dbpedia.org/sparql)에 있는지 묻는다(Query 6.67).

```
SELECT ?entry
WHERE {?actor :playedIn :Giant .
       ?actor rdfs:label ?name .
       SERVICE <http://dbpedia.org/sparql>
       {?entry rdfs:label ?name . }
}
```

답은 Carroll_Baker, Elizabeth_Taylor, James_Dean, Mercedes_McCambridge, Rock_Hudson, Sal_Mineo의 DBpedia 자원 주소(http://dbpedia.org/resource/ 아래)다.

여기서 ?name은 로컬 데이터의 두 번째 트리플에서 정해진 변수인데 SERVICE 안에서 다시 쓰였다. 즉 로컬 데이터셋의 값이 원격 데이터셋(DBpedia)에 미리 묶인 바인딩으로 전달된 셈이다. DBpedia 엔드포인트 쪽에서 보면 ?name은 더 이상 변수가 아니라 바깥에서 이미 정해진 값이다. 서브쿼리에서 찾은 ?entry는 전체 질의의 결과로 쓰인다.

이 질의는 이미 아는 대상의 DBpedia 참조를 찾았을 뿐이라 별로 흥미롭지 않다. 모르는 정보를 묻는 편이 더 낫다. 예컨대 배우의 본명이다(Query 6.68).

```
SELECT DISTINCT ?name ?realname
WHERE {?actor :playedIn :Giant .
       ?actor rdfs:label ?name .
       SERVICE <http://dbpedia.org/sparql>
       { ?entry rdfs:label ?name .
         ?entry dbpedia:birthname ?realname } }
```

원서 인쇄본에는 SERVICE 뒤 URL이 겹쳐 인쇄되는 깨짐이 있어 위처럼 복원했다. 결과는 다음과 같다.

| ?name | ?realname |
|---|---|
| Elizabeth Taylor | Elizabeth Rosemond Taylor |
| Rock Hudson | Roy Harold Scherer, Jr. |
| Sal Mineo | Salvatore Mineo, Jr. |

읽는 법: 6명 중 3명만 나오는 이유는 DBpedia에 birthname 정보가 있는 배우만 매칭되기 때문이다. 이 이유는 원서가 명시하지는 않았으며 결과 표에서 추정한 것이다.

### 4.2 rdfs:label로 찾는 방법의 약점과 exactMatch

위 질의는 rdfs:label이 DBpedia에서 자원을 식별하기에 적절하다고 가정한다. 하지만 DBpedia에는 사람, 영화, 장소, 나라 등 수백만 개의 것이 있다. 위키백과 항목이 있는 거의 모든 것이 들어 있어서, 서로 다른 두 대상이 같은 rdfs:label을 가질 가능성이 높다.

더 나은 방법은 DBpedia URL을 직접 가리키는 것이다. 질의 속에서 할 수 있는 일은 아니고 데이터 소스가 자기 자원과 DBpedia 사이의 연결을 가지고 있어야 한다. 예컨대 이렇다.

```
:ElizabethTaylor skos:exactMatch dbpedia:Elizabeth_Taylor .
:RockHudson skos:exactMatch dbpedia:Rock_Hudson .
:SalMineo skos:exactMatch dbpedia:Sal_Mineo .
```

그러면 질의를 이렇게 바꿀 수 있다(Query 6.69).

```
SELECT DISTINCT ?name ?realname
WHERE {?actor :playedIn :Giant .
       ?actor skos:exactMatch ?db .
       SERVICE <http://dbpedia.org/sparql>
       { ?db dbpedia:birthname ?realname } }
```

질의가 더 짧아질 뿐 아니라 잘못될 여지가 적다. "Sal Mineo"나 "Elizabeth Taylor"라는 이름의 다른 사람이 있어도, 데이터에 exactMatch가 들어 있으므로 DBpedia 질의에서 올바른 자원이 쓰인다. 원서는 이것이 5장에서 권고한 방식, 즉 데이터셋끼리 링크를 걸어 링크드 데이터의 웹을 짜는 일의 한 예라고 말한다. 요즘은 공개 데이터셋이 DBpedia 같은 데이터 소스로 가는 이런 링크를 달아 모호함을 없애는 일이 흔하다. DBpedia는 유명인, 장소, 예술 작품처럼 위키백과에 언급된 모든 것의 사실상 이름 등록소가 되었다.

SPARQL 질의 하나에 SERVICE를 몇 개든 쓸 수 있으므로 여러 데이터 소스에 걸친 질의도 쓸 수 있다.

---

## 5. 정리

| 기능 | 한 줄 요약 | 대표 예 |
|---|---|---|
| UNION | 두 패턴 중 어느 쪽이든 맞으면 된다 | Giant 또는 Rebel의 배우, hasParent 합치기 |
| BIND | 질의 중에 계산한 값을 변수에 배정한다 | CONCAT으로 전체 이름 만들기 |
| VALUES | 질의 안에 작은 데이터를 직접 적는다 | 저자 이름 세 쌍 |
| SERVICE | 원격 SPARQL 엔드포인트에 서브쿼리를 보낸다 | DBpedia에서 본명 가져오기 |
| GRAPH | 이름 있는 그래프를 대상으로 질의한다 | 한 저장소 안의 분리된 그래프 |

읽는 법: UNION은 패턴을 합치고, BIND와 VALUES는 값을 만들거나 넣고, SERVICE와 GRAPH는 질의의 범위를 넓힌다. 원서가 GRAPH의 구체 예를 보여 주지는 않아서 위 표의 GRAPH 예는 설명 수준으로만 적었다.

<br>
<br>
<br>

[Semantic Web for the Working Ontologist](../)
