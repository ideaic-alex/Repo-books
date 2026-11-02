# RDFS-Plus

이 장은 RDFS에서 한 걸음 나아가 웹 온톨로지 언어인 OWL의 일부를 가져와 쓰는 방법을 다룬다. 저자들은 RDFS와 크게 다르지 않으면서 실무에서 쓸모가 큰 구성 요소들을 골라 RDFS-Plus라고 부른다. 속성의 방향을 뒤집는 inverseOf, 연쇄를 따라가는 TransitiveProperty, 같음을 말하는 equivalentClass와 sameAs, 같은지 자동으로 따지는 FunctionalProperty와 InverseFunctionalProperty가 중심이다.

각 구성 요소의 의미는 앞에서처럼 추론 규칙으로 정해지고, 장 전체는 25번까지 이어지는 도전 과제를 풀며 진행된다. 구성 요소 하나하나보다 이들을 어떻게 조합해서 족보, 워크플로, 서로 다른 데이터베이스 통합 문제를 푸는지가 이 장의 핵심이다.

---

## 1. 핵심 요점

- RDFS-Plus는 OWL의 부분집합이다. 학습하기 쉽고, 정보 통합 실무에서 쓸모가 크며, 다양한 추론 기술로 구현할 수 있어서 골랐다.
- `owl:inverseOf`는 속성의 주어와 목적어를 뒤집는다. `subPropertyOf`와 함께 쓰면 방향이 반대인 속성도 하나로 합칠 수 있고, `superClassOf` 같은 새 어휘도 만들 수 있다.
- `owl:SymmetricProperty`는 자기 자신이 inverse인 속성이다. `owl:inverseOf` 자신을 대칭으로 선언하면 inverse가 양방향으로 추론된다.
- `owl:TransitiveProperty`는 연쇄를 하나의 관계로 합친다. 추이성은 상위 속성(조상, 전체-부분, 선행)에만 붙이고 하위 속성은 직접 관계를 유지하는 패턴이 반복된다.
- `equivalentClass`, `equivalentProperty`, `sameAs`는 각각 클래스, 속성, 개체가 같다고 말한다. 앞의 둘은 `subClassOf`와 `subPropertyOf`로도 표현할 수 있고, `sameAs`는 개체 수준의 새 능력이다.
- `FunctionalProperty`는 값이 하나뿐인 속성이고, `InverseFunctionalProperty`는 값 하나에 주어가 하나뿐인 속성이다. 같은 값을 가진 두 주어를 같은 개체로 추론하므로 관계형 데이터베이스의 키와 비슷하지만, 오류 대신 같다는 결론을 낸다.
- `ObjectProperty`, `DatatypeProperty`, `owl:Class`는 추론에는 영향이 없지만 도구가 모델을 올바르게 다루게 한다.
- OWL로 같은 대상인지 판단하는 일은 시맨틱 웹의 본업이 아니다. 판단된 사실을 정확하고 분산된 방식으로 기록해서 재사용하게 하는 것이 역할이다.

---

## 2. 문서 목록

- [RDFS-Plus 소개와 inverseOf](RDFS-Plus%20%EC%86%8C%EA%B0%9C%EC%99%80%20inverseOf.md): RDFS-Plus를 고른 이유, inverseOf의 뜻과 규칙, 방향이 다른 속성 합치기(도전 과제 13~14)
- [대칭 속성과 어휘 확장](%EB%8C%80%EC%B9%AD%20%EC%86%8D%EC%84%B1%EA%B3%BC%20%EC%96%B4%ED%9C%98%20%ED%99%95%EC%9E%A5.md): superClassOf 만들기, AAA 원칙의 한계, SymmetricProperty, inverseOf를 양방향으로 만들기(도전 과제 15~17)
- [추이적 속성](%EC%B6%94%EC%9D%B4%EC%A0%81%20%EC%86%8D%EC%84%B1.md): TransitiveProperty의 규칙, 부모와 조상, 추이적·비추이적 partOf 함께 두기(도전 과제 18~19)
- [의존 관계 네트워크](%EC%9D%98%EC%A1%B4%20%EA%B4%80%EA%B3%84%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC.md): 아이스크림 레시피로 보는 선행·후행 단계 계산, inSameRecipe와 otherStep 비교(도전 과제 20~22)
- [같음을 표현하는 세 가지 방법](%EA%B0%99%EC%9D%8C%EC%9D%84%20%ED%91%9C%ED%98%84%ED%95%98%EB%8A%94%20%EC%84%B8%20%EA%B0%80%EC%A7%80%20%EB%B0%A9%EB%B2%95.md): equivalentClass, equivalentProperty, sameAs의 규칙과 셰익스피어 예제
- [서로 다른 데이터베이스 합치기](%EC%84%9C%EB%A1%9C%20%EB%8B%A4%EB%A5%B8%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4%20%ED%95%A9%EC%B9%98%EA%B8%B0.md): 두 제품 표를 sameAs로 이어 연합 쿼리하기와 그 한계(도전 과제 23)
- [함수형 속성과 역함수형 속성](%ED%95%A8%EC%88%98%ED%98%95%20%EC%86%8D%EC%84%B1%EA%B3%BC%20%EC%97%AD%ED%95%A8%EC%88%98%ED%98%95%20%EC%86%8D%EC%84%B1.md): sameAs 자동 추론, 키와의 비교, 식별 번호 모델링(도전 과제 24~25)
- [데이터 타입 속성과 클래스 선언](%EB%8D%B0%EC%9D%B4%ED%84%B0%20%ED%83%80%EC%9E%85%20%EC%86%8D%EC%84%B1%EA%B3%BC%20%ED%81%B4%EB%9E%98%EC%8A%A4%20%EC%84%A0%EC%96%B8.md): ObjectProperty와 DatatypeProperty, rdfs:Class와 owl:Class
- [요약과 핵심 개념](%EC%9A%94%EC%95%BD%EA%B3%BC%20%ED%95%B5%EC%8B%AC%20%EA%B0%9C%EB%85%90.md): 구성 요소 표, 도전 과제 모음, 장 전체의 교훈

<br>
<br>
<br>

[Semantic Web for the Working Ontologist](../)
