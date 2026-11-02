# 데이터 일부 복사와 정렬, LIMIT

이 문서는 두 가지를 다룬다. 하나는 큰 데이터셋에서 필요한 부분만 잘라 복사하는 방법이다(원서의 Challenge 4). 다른 하나는 SPARQL 고급 기능의 첫 묶음인 정렬(ORDER BY)과 개수 제한(LIMIT)이다. 둘 다 SQL을 아는 개발자에게 익숙한 개념이지만, 복사는 CONSTRUCT로 한다는 점이 SPARQL다운 부분이다.

---

## 1. 데이터셋의 일부만 떼어 내는 이유

RDF 데이터셋은 트리플이 매우 많은 경우가 흔하다. 일부만 따로 만들고 싶은 이유는 세 가지다.

| 이유 | 상황 | 얻는 것 |
|---|---|---|
| 접속이 불안정하다 | 데이터셋이 네트워크 자원으로만 제공되고 연결이 들쭉날쭉하다 | 자주 쓰는 정보의 튼튼한 사본 |
| 질의가 느리다 | 데이터셋이 아주 커서 복잡한 질의가 느리다 | 작고 관련 있는 부분만 담은 캐시로 빠른 질의 |
| 민감한 정보가 있다 | 일부 대상에게는 공개하면 안 되는 정보가 섞여 있다 | 덜 민감한 부분만 복사해 공개용으로 제공 |

읽는 법: 세 이유 모두 "전체 중 일부만 따로 보관한다"는 같은 작업이다. 이 작업을 CONSTRUCT 질의로 한다.

---

## 2. 영화 Unforgiven에 관한 모든 정보 가져오기

LinkedMDB에서 영화 Unforgiven은 film:37379다. 이 영화의 배우, 감독, 제작자 등 가능한 모든 정보를 복사하고 싶다. "모든"이 무슨 뜻이냐에 따라 질의가 달라진다. 단계별로 보자.

### 2.1 주어 쪽: 영화가 주어인 트리플

가장 단순한 질의는 이렇다(Query 6.43).

```
CONSTRUCT { film:37379 ?p ?o . }
WHERE { film:37379 ?p ?o . }
```

시시해 보이지만, 영화를 주어로 하는 모든 트리플을 가져온다. 전체 LinkedMDB에서는 수십 개가 나오며 다음이 들어 있다.

```
film:37379
    rdf:type film:film ;
    dcterms:title "Unforgiven" ;
    film:actor actor:25769 ;
    film:actor actor:17281 ;
    film:director director:4614 ;
    film:writer writer:8240 .
```

배우, 감독 정보를 담은 좋은 출발이다. 그런데 이 영화가 Clint Eastwood가 감독과 주연을 겸한 영화임을 알아내는 것은 우리의 몫이다. 게다가 다음 트리플은 이 결과에 없다.

```
director:4614 foaf:made film:37379 .
```

이 트리플에서 영화는 주어가 아니라 목적어이기 때문이다.

### 2.2 목적어 쪽: 영화가 목적어인 트리플

거의 같은 모양으로 반대편을 가져온다(Query 6.44).

```
CONSTRUCT {?s ?p film:37379. } WHERE {?s ?p film:37379 . }
```

영화가 목적어인 모든 트리플이 나오고, 위의 foaf:made 트리플도 들어온다. 이쪽이 "특정 자원에 관한 모든 정보"에 더 가까운 뜻이다.

### 2.3 한 다리 건너: 관련된 대상의 정보

그래도 부족하다. actor:25769가 누구인지는 여전히 알 수 없다. 영화 자체의 정보뿐 아니라 관련된 대상의 정보도 필요하다. 더 긴 패턴으로 구한다(Query 6.45).

```
CONSTRUCT { ?s ?p ?o }
WHERE { film:37379 ?p1 ?s .
        ?s ?p ?o . }
```

`?s ?p ?o`는 데이터의 모든 트리플에 매칭되는 패턴이다. 여기서는 첫 번째 패턴이 ?s를 영화와 어떤 식으로든 관련된 대상으로 이미 묶어 놓았으므로, 두 번째 패턴은 영화와 관련된 대상들이 주어인 모든 트리플을 복사한다. 예를 들어 데이터에 다음이 있으므로

```
film:37379 linkedmdb:actor actor:25769 .
```

actor:25769로 시작하는 트리플이 모두 나오고, 거기에 `actor:25769 film:actor_name "Richard Harris"`도 들어 있다.

| 질의 | 영화의 위치 | 가져오는 것 |
|---|---|---|
| 6.43 | 주어 | 영화 자신의 속성과 관계 |
| 6.44 | 목적어 | 영화를 가리키는 트리플(예: 감독의 foaf:made) |
| 6.45 | 한 다리 건너 | 영화와 연결된 대상(배우 등)의 모든 트리플 |

읽는 법: 세 질의를 합치면 영화에 관한 포괄적인 캐시가 된다. 원서는 이 장의 예제 데이터 파일 대부분이 이 방법으로 만들어졌다고 밝힌다.

---

## 3. 정렬: ORDER BY

James Dean이 출연한 영화와 개봉 연도를 구해 보자(Query 6.46).

```
SELECT ?movie ?date
WHERE { :JamesDean :playedIn ?m .
        ?m rdfs:label ?movie .
        ?m dc:date ?date . }
```

답은 Giant 1956, EastOfEden 1955, RebelWithoutaCause 1955다. 이 순서는 아무 보장이 없다. SPARQL 구현체는 어떤 순서로든 내놓을 수 있고, 같은 구현체라도 때에 따라 순서가 바뀔 수 있다. 순서를 정하려면 ORDER BY를 쓴다. ORDER BY는 그래프 패턴 뒤에 오며, 순서를 정하는 기준으로 쓸 변수를 하나 이상 지정한다. 날짜순(Query 6.47)과 제목순(Query 6.48)은 다음과 같다.

```
ORDER BY ?date
ORDER BY ?title
```

두 질의 모두 나머지 부분은 같으며 변수 이름만 ?title로 바꾸어 `SELECT ?title ?date`로 썼다.

| 정렬 기준 | 결과 순서 |
|---|---|
| `ORDER BY ?date` | EastOfEden 1955, RebelWithoutaCause 1955, Giant 1956 |
| `ORDER BY ?title` | EastOfEden 1955, Giant 1956, RebelWithoutaCause 1955 |

읽는 법: 같은 데이터를 어떤 변수로 정렬하느냐에 따라 순서가 달라진다. 값의 종류에 따라 순서 개념이 단순하게 정해져 있다. 숫자는 크기순, 문자열은 사전순이다.

---

## 4. 개수 제한: LIMIT

화면에 몇 개씩만 보여 주거나 "상위 10개"만 보고서에 담고 싶을 때가 있다. LIMIT는 가져올 결과의 최대 개수를 정한다. ORDER BY와 함께 쓰면 정렬된 앞쪽에서 개수만큼 가져온다. ORDER BY 없이 LIMIT만 쓰면 구현체가 일치하는 결과 중 아무거나 지정한 개수만큼 가져온다. 가장 이른 James Dean 영화는 날짜순에 LIMIT 1을 붙인다(Query 6.49).

```
SELECT ?title
WHERE { :JamesDean :playedIn ?m .
        ?m rdfs:label ?title .
        ?m dc:date ?date . }
ORDER BY ?date
LIMIT 1
```

답은 East Of Eden이다. 날짜가 같은 영화(East of Eden과 Rebel, 둘 다 1955)가 있는데 그중 하나가 나온다는 점에 유의하자. 동점일 때 누가 먼저인지는 이 질의만으로는 정해지지 않는다(원서는 이 점을 따로 다루지 않으며, 이 문장은 이 노트의 보충이다).

원서의 다음 예는 "Rebel Without a Cause"의 세 주연(James Dean, Natalie Wood, Sal Mineo)이 모두 비극적으로 젊어서 세상을 떠났는데 누가 먼저였는가 하는 질문이다(Query 6.50).

```
SELECT ?first
WHERE { ?who :playedIn :RebelWithoutaCause .
        ?who rdfs:label ?first .
        ?who :diedOn ?date . }
ORDER BY ?date
LIMIT 1
```

답은 James Dean이다. 기본 정렬은 오름차순이다. 뒤집으려면 DESC를 쓴다. 가장 오래 산 사람(Query 6.51)은 `ORDER BY DESC(?date)`와 `LIMIT 1`을 쓰고, 답은 Sal Mineo다.

| 키워드 | 하는 일 | 주의 |
|---|---|---|
| ORDER BY | 결과 순서를 지정한다 | 없으면 순서는 보장되지 않는다 |
| DESC(...) | 내림차순으로 뒤집는다 | 기본은 오름차순이다 |
| LIMIT n | 결과를 최대 n개로 자른다 | ORDER BY 없이 쓰면 어떤 n개가 나올지 정해지지 않는다 |

---

## 5. 정리

- 데이터셋 일부 복사는 CONSTRUCT로 한다. 주어 쪽, 목적어 쪽, 한 다리 건너 쪽 질의를 합치면 포괄적인 캐시가 된다.
- 복사하는 이유는 불안정한 접속, 느린 질의, 민감한 정보 세 가지다.
- 결과 순서는 ORDER BY로 정하고, DESC로 뒤집는다.
- LIMIT는 결과 수를 자르며, "가장 ~한 것" 하나를 찾을 때 ORDER BY와 함께 쓴다.

<br>
<br>
<br>

[Semantic Web for the Working Ontologist](../)
