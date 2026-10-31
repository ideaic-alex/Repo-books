# 부록 A 주식 선택 전문가 시스템 CLIPS 지식 베이스

이 문서는 장 중에 설계한 주식 선택 전문가 시스템의 전체 CLIPS 지식 베이스를 모아 놓은 'Appendix A'를 해설한다. 부록은 거의 코드로만 이루어져 있으므로, 입력 규칙과 네 개의 규칙 군집(Cluster)이 각각 무슨 일을 하는지, 서로 어떻게 연쇄되는지를 말로 풀어 쓴다. 이 시스템은 시장 추세, 유가 상승률, 금리라는 세 종류의 입력에서 출발해 어떤 업종과 종목을 사거나 공매도할지 추론한다.

---

## 1. 전체 구성

부록의 지식 베이스는 입력 수집 규칙 네 개와 번호가 붙은 규칙 R1부터 R23까지로 이루어진다. 규칙은 네 개의 군집으로 나뉜다.

| 구분 | 내용 | 규칙 |
|---|---|---|
| 입력 수집 | 사용자에게 값을 물어 사실로 등록 | 네 개의 입력 규칙 |
| 군집 I | 일반 규칙 | R1~R3 |
| 군집 II | 시장 추세 판정 | R4~R6 |
| 군집 III | 유가 상승 관련 | R7~R15 |
| 군집 IV | 금리 관련 | R16~R23 |

모든 규칙은 앞쪽의 CLIPS 설명에서 본 `defrule` 형식을 따른다. 좌변(LHS)에서 사실의 패턴을 맞추고, 우변(RHS)에서 `assert`로 새 사실을 추가한다. 필요하면 `printout`으로 권고를 화면에 출력한다.

---

## 2. 사용자 입력 규칙

입력 규칙은 좌변에 조건이 없거나 간단하다. 사용자에게 질문을 출력하고, `read`로 답을 받아 `bind`로 변수에 담은 뒤 사실로 등록한다.

- **`get-SP500-trend`**: S&P500 추세를 묻는다. 답은 up, down, little-changed 가운데 하나이며 `(SP500 ?trend)` 사실이 된다.
- **`get-NASDAQ-trend`**: 같은 방식으로 NASDAQ 추세를 묻고 `(NASDAQ ?trend)` 사실을 만든다.
- **`get-oil-price-increase`**: 유가 상승률(%)을 묻고 `(oil-increase ?percent)`를 만든다. 단, 좌변이 `(or (market up) (market down))`이므로 시장이 오르거나 내릴 때만 질문한다.
- **`get-interest-rate`**: 금리(%)를 묻고 `(interest-rate ?percent)`를 만든다. 이 규칙도 시장이 up 또는 down일 때만 실행된다.

유가와 금리를 시장이 횡보하지 않을 때만 입력받는 이유는 주석에 적혀 있다. 시장이 횡보인데도 사용자에게 유가 상승률을 물으면, 시스템이 상충하는 권고를 동시에 낼 수 있다. 시장에서 빠지라는 권고와 에너지 업종을 사라는 권고가 함께 나오는 경우다. 이 규칙들은 입력을 통제해 충돌을 미리 막는 장치다.

---

## 3. 군집 I 일반 규칙

시장 상태와 업종 상태를 결합해 행동을 정하는 가장 일반적인 규칙들이다.

- **`R1-market-up`**: 시장이 상승(market up)이고 어떤 업종이 강하면(sector ?name strong) 그 업종을 매수한다(`buy sector ?name`). 업종 이름은 변수 `?name`으로 일반화되어 있어 어느 업종에도 적용된다.
- **`R2-market-down`**: 시장이 하락이고 업종이 약하면 그 업종을 공매도한다(`short sector ?name`).
- **`R3-market-sideways`**: 시장이 횡보이면 `stay-out` 사실을 등록하고 "시장에서 빠져 있으라"는 문구를 출력한다.

---

## 4. 군집 II 시장 추세 판정

두 지수의 추세를 모아 시장 전체의 방향을 결론짓는 규칙들이다.

- **`R4-market-up`**: S&P500과 NASDAQ이 모두 up이면 시장은 up이다.
- **`R5-market-down`**: 두 지수가 모두 down이면 시장은 down이다.
- **`R6-market-sideways`**: 둘 중 하나라도 little-changed이면 시장은 sideways이다. 좌변에 `or` 조건 요소가 쓰였다.

두 지수가 엇갈려 하나는 up이고 다른 하나는 down인 경우를 직접 다루는 규칙은 부록에 없다. 이 경우 위 세 규칙이 모두 맞지 않으므로 시장 추세 사실이 만들어지지 않는다. 이는 규칙을 읽고 확인할 수 있는 사실일 뿐, 저자가 이 점을 따로 논평한 것은 아니다.

---

## 5. 군집 III 유가 상승 관련 규칙

이 군집의 중심은 유가 상승률에서 시작해 에너지 업종 매수와 운송 업종 공매도로 이어지는 연쇄다.

### 5.1 분류와 업종 판단

- **`R7-classify-oil-prices`**: `test` 조건 요소로 유가 상승률이 20을 넘는지 비교하고, 넘으면 유가가 높다(`oil-prices high`)고 분류한다.
- **`R8-sector-energy-strong`**: 유가가 높으면 에너지 업종은 강하다.
- **`R9-sector-transportation-weak`**: 유가가 높으면 운송 업종은 약하다.

### 5.2 매수 연쇄

- **`R10-buy-sector-energy`**: 에너지 업종이 강하면 에너지 업종을 매수한다(`buy sector energy`).
- **`R11-buy-ExxonMobil`**와 **`R12-buy-BP`**: 에너지 업종 매수가 결정되면 개별 종목으로 ExxonMobil과 BP를 매수하고 각각 권고 문구를 출력한다.

### 5.3 공매도 연쇄

- **`R13-short-sector-transportation`**: 유가가 높으면 운송 업종을 공매도한다(`short sector transportation`).
- **`R14-short-United-Airlines`**와 **`R15-short-American-Airlines`**: 운송 업종 공매도가 결정되면 United Airlines와 American Airlines를 공매도하고 문구를 출력한다.

입력 하나가 규칙 여러 개를 거쳐 종목 권고로 이어지는 이 사슬은, 전방 추론이 결론을 단계적으로 쌓아 가는 모습을 보여 준다. 유가가 높다는 사실 하나에서 R8과 R9, R13이 동시에 맞는다는 점도 눈여겨볼 만하다.

---

## 6. 군집 IV 금리 관련 규칙

이 군집은 금리에서 금융 업종의 강약을 판단하고, 이어서 두 금융주에 대한 권고를 낸다.

- **`R16-classify-high-interest-rate`**: 금리가 9.0을 넘으면 금리 등급이 높음(`interest-rate-class high`)이다.
- **`R17-classify-low-interest-rate`**: 금리가 6.0 미만이면 금리 등급이 낮음(`interest-rate-class low`)이다.
- **`R18-sector-financial-weak`**: 금리가 높으면 금융 업종은 약하다.
- **`R19-sector-financial-strong`**: 금리가 낮으면 금융 업종은 강하다.

6.0 이상 9.0 이하의 중간 금리는 어느 등급도 만들지 않으므로 금융 업종의 강약도 판정되지 않는다.

이어서 종목 수준 규칙이 네 개 있다.

1. **`R20-buy-Countrywide-Financial`**과 **`R21-buy-BankofAmerica`**: 금융 업종 매수(`buy sector financial`)가 결정되면 Countrywide Financial과 Bank of America를 매수한다.
2. **`R22-short-Countrywide-Financial`**과 **`R23-short-BankofAmerica`**: 금융 업종 공매도(`short sector financial`)가 결정되면 두 종목을 공매도한다.

금융 업종 매수나 공매도 사실은 이 군집에서 만들지 않는다. 군집 I의 R1(시장 상승이고 업종 강함)과 R2(시장 하락이고 업종 약함)가 만든다. 따라서 금리가 낮아 금융 업종이 강해도 시장이 상승일 때만 금융주 매수 권고가 나온다.

---

## 7. 규칙 간 연결 정리

부록 전체를 하나의 흐름으로 보면 다음과 같다.

1. 사용자가 두 지수의 추세를 입력한다(입력 규칙).
2. 군집 II가 시장 방향을 결론짓는다.
3. 시장이 up 또는 down이면 유가와 금리를 추가로 묻는다.
4. 군집 III과 IV가 수치를 분류하고 업종 강약을 판단한다.
5. 군집 I이 시장 방향과 업종 강약을 결합해 업종 매수·공매도를 결정한다.
6. 종목 규칙들이 업종 결정을 개별 종목 권고로 구체화해 화면에 출력한다.

시장이 sideways이면 R3이 시장에서 빠지라는 권고만 내고, 유가와 금리를 묻지 않으므로 충돌이 생기지 않는다.

<br>
<br>
<br>

[Diagrammatic Reasoning in AI](../)
