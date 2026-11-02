# HTTP URI 만들기

링크드 데이터를 공개하려면 설명하려는 모든 것에 쓸 URI를 먼저 정해야 한다. 이 일을 URI를 "찍어 낸다"는 뜻으로 민팅(minting)이라고 부른다. 한 번 공개한 URI는 다른 사람이 가져다 쓰고 참조하기 때문에 의존 관계가 생기고, 나중에 바꾸기 어려운 기존 시스템이 된다. 그래서 처음부터 신중하게 설계해야 한다.

이 문서는 URI의 구조, 안정적인 URI를 만드는 조언(Cool URIs), 표 데이터에서 URI를 뽑는 예, CURIE 제약, 그리고 IETF와 DOI의 실제 사례를 다룬다.

---

## 1. URI의 생김새

URI의 일반 형태는 IETF의 RFC 3986에 정의되어 있다. 대괄호 안은 생략할 수 있는 부분이다.

```
scheme:[//[user:password@]host[:port]][/]path[?query][#fragment]
```

이 형태를 따르는 URI의 예로 `urn:animals.org#mycat`이 있다. 웹 데이터에서 권장하는 것은 HTTP URI이며 형태는 다음과 같다.

```
http://host[:port][/]path[?query][#fragment]
```

| 부분 | 의미 | 예 |
|---|---|---|
| scheme | 접근 방식 | `http` |
| host | 서버를 가리키는 도메인 이름 | `animals.org` |
| port | 서버 포트 (생략 가능) | `:8080` |
| path | 경로 | `/cats/mine` |
| query | 질의 문자열 (생략 가능) | `?owner=fabien` |
| fragment | `#` 뒤의 조각 | `#mycat` |

유효한 HTTP URI의 예는 `http://animals.org#mycat`, `http://animals.org/cats/mine`, `http://animals.org/cats/?owner=fabien` 등이다.

HTTP URI가 데이터의 웹에서 유리한 이유는 하이퍼텍스트 웹을 돌리는 인프라 전체를 그대로 쓸 수 있기 때문이다. 그 인프라의 기본 메커니즘이 세 가지다.

| 메커니즘 | 하는 일 |
|---|---|
| DNS(Domain Name Service) | 도메인 이름을 웹 서버의 인터넷 주소와 연결한다 |
| 콘텐츠 협상(Content Negotiation) | 같은 HTTP URI에 대해 클라이언트마다 다른 콘텐츠를 준다 |
| HTTP 리디렉션(Redirection) | 요청을 다른 주소로 돌려보낸다 |

URI의 host 부분(예제의 `animals.org`)은 DNS가 관리한다. 하이퍼텍스트 페이지든 데이터든 웹에 무엇이든 게시하려는 사람은 도메인 이름을 DNS에 등록한다. 등록을 마치면 그 도메인을 host로 쓰는 모든 HTTP URI를 만들고 접근을 통제할 수 있다. path 부분은 길이 제한도 없고 URI를 만드는 사람 마음대로다. 즉 쓸 수 있는 URI 패턴에는 현실적인 제한이 없다.

---

## 2. Cool URIs: 바뀌지 않는 URI

큰 데이터셋에서 충분히 많은 서로 다른 식별자를 지금도 앞으로도 만들어 내는 문제는 시맨틱 웹만의 문제가 아니고, 완벽한 답도 없다. 시맨틱 웹의 HTTP URI에 관한 장단점은 여러 문서에서 논의되었다. 그 중 널리 알려진 제안이 Cool URIs다. 팀 버너스리의 글 "Cool URIs don't change"에서 이름을 따왔다.

핵심은 이름 그대로 URI가 바뀌지 않아야 한다는 것이다. 하이퍼텍스트 웹에서 "404 page not found"는 실망스러운 정도지만, 데이터의 웹에서는 URI가 데이터셋 사이의 연결 지점이라서 치명적일 수 있다. 링크 하나가 끊기면 데이터셋 전체에 접근하지 못할 수도 있다.

Cool URIs의 안정성 조언은 다음과 같다.

| 조언 | 피해야 할 것 | 이유와 대안 |
|---|---|---|
| 구현 세부 사항을 최대한 넣지 않는다 | `.PHP`, `.json`, `.rdf` 같은 언어 의존 확장자, `desktop8.inria.fr` 같은 특정 서버 이름, `/wordpress/` 같은 특정 소프트웨어, 서버 포트 번호 | 구현이 바뀌면 URI도 바뀐다 |
| 콘텐츠 협상을 쓴다 | URI에 형식을 박아 넣는 것 | 웹 서버는 클라이언트 정보로 콘텐츠를 협상할 수 있으니 URI에서 구현 세부를 뺀다 |
| 버전 정보를 넣지 않는다 | URI에 v2 같은 표시 | 시맨틱 웹 표준은 URI를 바꾸지 않고 데이터나 메타데이터의 버전을 밝히는 방법을 제공한다 |
| 원본의 기존 식별자를 쓴다 | 새 번호를 따로 만드는 것 | 기본 키, 계좌 번호 같은 식별자가 이미 있으면 URI가 맞는 데이터 요소에 대응하도록 이것을 활용한다 |

---

## 3. 표 데이터에서 URI 만들기: 예방 접종 기록

반려동물 예방 접종 기록 표(CSV 같은 파일)를 링크드 데이터로 만든다고 하자. 책의 표 5.1은 다음과 같다.

| ID | Species | Name | Expiration date |
|---|---|---|---|
| 366863 | dog | Fido | 2020 |
| 851903 | dog | Bastian | 2021 |
| 775304 | cat | Mytsie | 2019 |
| 898202 | cat | Corvus | 2021 |
| 847823 | cat | Fenris | 2019 |
| 399378 | dog | Maddie | 2022 |
| 911236 | cat | Twinkie | 2016 |
| 897991 | dog | Champ | 2019 |
| 032579 | dog | Zeke | 2020 |
| 31450 | cat | Lila | 2019 |
| 87580 | dog | Fido | 2021 |

이름과 만료 연도는 유일하다고 믿을 수 없다. 이 짧은 예에서도 Fido라는 개가 두 마리다. URI를 만드는 방법을 세 가지로 비교해 보자.

| 방법 | 예 | 결과 |
|---|---|---|
| 모든 데이터를 URI에 넣는다 | `http://www.example.com/vac/366863/dog/Fido/2020` | 유일성은 보장되지만 URI가 매우 길어진다. 데이터가 바뀌면 오해를 부른다 |
| ID 칸만 쓴다 | `http://www.example.com/vac/366863` | ID가 접종 기록을 유일하게 식별하므로 안전하다 |
| 이름 칸을 쓴다 | `http://www.example.com/vac/Fido` | 두 가지 문제가 생긴다 |

첫 번째 방법은 데이터 일부가 바뀌었을 때 곤란하다. 새 URI를 새로 만들어야 하는지, 낡은 데이터를 반영한 옛 URI를 그대로 쓰는지 정해야 한다. 두 번째 방법이 맞다. 다만 쓰는 열이 정말 유일한 식별자여야 한다. 이름을 쓰면 다음 문제가 생긴다.

- `http://www.example.com/vac/Fido`를 두 번 만들게 되어 데이터를 올바르게 반영하지 못한다.
- 이름이 겹치지 않더라도 미치가 입양되어 "Missy"라는 새 이름을 받으면, 새 URI를 만들어야 하는지, 아니면 `http://example.com/vac/Mytsie`가 이제 이름이 "Missy"라고 말해야 하는지 애매해진다.

---

## 4. CURIE와 숫자로 시작하는 ID

3장에서 본 것처럼 URI는 네임스페이스와 CURIE(Compact URI, 줄인 URI)로 줄여 쓴다. 접두어 `vac`를 `http://www.example.org/vac/`의 네임스페이스로 정하면 미치의 접종 기록은 `vac:775304`가 될 것 같다. 하지만 CURIE 규격에는 접두어 뒤 이름이 숫자(1, 2, 3...)나 기본 결합 문자(예: 쉼표)로 시작할 수 없다는 제약이 있다. 그래서 `vac:775304`는 유효하지 않다.

CURIE는 여러 곳에서 쓸모가 있으므로, 식별자 맨 앞에 알파벳 한 글자를 붙이는 것이 좋은 습관이다. 책의 표 5.4는 "V"를 붙였다.

| URI | CURIE |
|---|---|
| `http://www.example.com/vac/V366863` | `vac:V366863` |
| `http://www.example.com/vac/V775304` | `vac:V775304` |
| `http://www.example.com/vac/V31450` | `vac:V31450` |
| `http://www.example.com/vac/V87580` | `vac:V87580` |

나머지 접종 기록(851903, 898202, 847823, 399378, 911236, 897991, 032579)도 똑같이 V를 붙이면 된다. 표에서 보듯 숫자 ID 앞에 글자 하나만 붙이면 CURIE로 줄여 쓸 수 있는 URI가 된다.

---

## 5. 실제 사례 1: IETF의 RFC

IETF는 인터넷 표준을 개발하고 알리는 열린 표준 기구다. 이미 본 표준인 URI 자체도 여기서 나왔고, DNS 등록 관리와 URI 형식도 IETF가 관리한다. IETF의 공식 문서를 RFC라고 한다. URI의 표준 명세인 최신 RFC는 RFC 3986(제목: Uniform Resource Identifier (URI): Generic Syntax)이다.

IETF는 RFC를 게시하고 안정적인 참조를 제공하려고 여러 URI 만들기 규칙을 채택했다. RFC 번호를 `https://tools.ietf.org/html/rfc` 뒤에 이어 붙이면 HTML 버전의 기본 URL이 된다.

| 버전 | RFC 3986의 URI |
|---|---|
| HTML | `https://tools.ietf.org/html/rfc3986` |
| 텍스트 | `https://tools.ietf.org/rfc/rfc3986` |
| PDF | `https://tools.ietf.org/pdf/rfc3986` |

장점은 안정적이라는 것이다. 새 버전이 나와도 최신 RFC의 HTML 표현에 같은 URI를 쓸 수 있다. 단점은 RFC 3986 자체를 가리킬 수 없고, 그것에 대한 특정 문서만 가리킬 수 있다는 점이다. 문서에 구현 정보를 넣지 말라는 URI 지침과 어긋난다. 이 문제는 콘텐츠 협상으로 풀 수 있고, 뒤의 문서에서 다룬다.

또 이 방식은 "URI의 마지막 부분을 알파벳으로 시작하라"는 CURIE 제안을 따른다(여기서는 항상 "r"). 하지만 공통 접두어가 없어서 각 방식마다 접두어가 필요하다는 약점이 있다. 즉 `https://tools.ietf.org/rfc/`, `https://tools.ietf.org/pdf/`, `https://tools.ietf.org/txt/`에 각각 다른 접두어를 정해야 한다.

---

## 6. 실제 사례 2: ISO의 DOI

두 번째 예는 국제표준화기구(ISO)가 표준(ISO 26324)으로 관리하는 식별자 계열인 DOI다. 책, 논문, 데이터셋, 동영상 같은 디지털 리소스를 오래 유지될 수 있게 식별하고 참조하는 데 쓴다. 예를 들어 Springer가 출판한 논문 "Distributed Artificial Intelligence for Distributed Corporate Knowledge Management"의 DOI는 다음과 같다.

```
doi:10.1007/3-540-45741-0_18
```

ISO는 DOI를 조회해서 대응하는 HTTP URI를 알려 주는 온라인 서비스(https://www.doi.org/)를 제공한다. 이 DOI는 아래 HTTP URI로 변환되고, 이 주소로 접속하면 DOI가 가리키는 대상의 설명 쪽으로 리디렉션된다.

```
http://doi.org/10.1007/3-540-45741-0_18
```

| 장점 | 단점 |
|---|---|
| 안정적이다. ISO가 특정 리소스의 DOI는 바뀌지 않게 보장한다 | 마지막 구성 요소가 숫자로 시작해서 CURIE로 만들 수 없다 |

---

## 7. 정리

| 질문 | 책의 답 |
|---|---|
| URI에 쓸 방식은? | HTTP URI |
| 안정성을 높이려면? | 구현 세부와 버전을 빼고 콘텐츠 협상을 쓴다 |
| 표 데이터에서 URI를 뽑으려면? | 유일성이 확실한 기존 ID 열을 쓴다 |
| CURIE로 줄이려면? | 식별자를 알파벳으로 시작한다 |
| 실제 사례에서 배울 점은? | RFC는 안정적이지만 접두어가 여럿 필요하고, DOI는 안정적이지만 CURIE를 못 만든다 |

<br>
<br>
<br>

[Semantic Web for the Working Ontologist](../)
