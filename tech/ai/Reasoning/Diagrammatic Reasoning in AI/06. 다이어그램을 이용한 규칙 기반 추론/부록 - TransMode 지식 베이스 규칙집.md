# 부록 A: TransMode 지식 베이스 규칙 해설

이 문서는 6장 부록 A에 실린 TransMode 지식 베이스의 52개 규칙(R1~R52)을 범주별로 풀어 설명한다. 앞 절들에서 순서도와 규칙 추적 다이어그램이 가리키던 규칙 번호의 실제 내용이 여기에 있다. 규칙은 크게 입력을 범주로 변환하는 규칙(R1~R32), 특수 요구와 적재 유형으로 대안을 좁히는 규칙(R33~R40), 두 대안 사이의 동점을 깨는 규칙(R41~R52)으로 나뉜다. 부록은 규칙 목록이라 원문에 해설이 없으므로, 아래 설명은 규칙의 내용을 정리하고 본문의 전략 설명과 대응시킨 것이다.

---

## 1. 입력을 범주로 바꾸는 규칙 (R1~R32)

이 규칙들은 숫자나 원시 입력을 `small`, `high` 같은 이산적 범주로 변환한다. 계층 모델의 잎 노드에서 중간 노드로 올라가는 부분에 해당한다.

### 1.1 적재 유형 (입력: `Shipment-Weight`)

| 규칙 | 조건 | 결론 `Load-Type` |
|---|---|---|
| R1 | 100파운드 이하 | `small-shipment` |
| R2 | 100 초과 5000 이하 | `average-shipment` |
| R3 | 5000 초과 15000 이하 | `large-shipment` |
| R4 | 15000 초과 | `very-large-shipment` |

### 1.2 거리 범위 (입력: `Distance`)

| 규칙 | 조건 | 결론 `Distance-Range` |
|---|---|---|
| R5 | 50마일 이하 | `local` |
| R6 | 50 초과 400 이하 | `short` |
| R7 | 400 초과 1000 이하 | `medium` |
| R8 | 1000 초과 | `long` |

### 1.3 속도 등급 (입력: `Transit-Time`)

| 규칙 | 조건 | 결론 `Speed-Rating` |
|---|---|---|
| R9 | 2일 이하 | `express` |
| R10 | 2일 초과 5일 이하 | `quick` |
| R11 | 5일 초과 10일 이하 | `average` |
| R12 | 10일 초과 | `slow` |

### 1.4 운송 거리 유형 (입력: `Distance-Range`, `Speed-Rating`)

`Haul-Type`은 거리와 속도를 합친 복합 범주다.

- `R13`: 거리 `long` 이고 속도가 `express` 또는 `quick`이면 `long-fast`.
- `R14`: 거리 `long` 이고 속도가 `average` 또는 `slow`이면 `long-slow`.
- `R15`: 거리 `medium` 이고 속도 `express`이면 `medium-fast`.
- `R16`: 거리가 `medium` 또는 `short`이고 속도가 `quick`, `average`, `slow` 중 하나이면 `medium-slow`.
- `R17`: 거리 `local`이면 속도와 무관하게 `local`.

이 규칙들 때문에 짧은 거리(short)에 `express`가 붙으면 R13~R17 어디에도 맞지 않아 `Haul-Type`이 정해지지 않는다. 이 점은 원문이 언급하지 않으므로 규칙 목록을 읽어서 확인되는 사실로만 적어 둔다.

### 1.5 수송 가능 수단 (입력: `Special-Products`, `Perishable`)

- `R18`: 특수 제품이 위험 광물 또는 위험 화학물질이면 `Modes-Capable = rail-only`.
- `R19`: 특수 제품이 농산물이고 `Perishable = yes`이면 `Modes-Capable = rail-or-trucking`.

이 두 규칙이 전략의 1단계, 즉 특수 요구 파악을 구현한다.

### 1.6 유연성 등급 (입력: `Frequency-of-Service`, `Door-to-Door-Service`)

| 규칙 | 서비스 빈도 | 문전 서비스 | `Flexibility-Rating` |
|---|---|---|---|
| R20 | 매일 | 예 | `high` |
| R21 | 매일 | 아니오 | `medium` |
| R22 | 매일 아님 | 예 | `medium` |
| R23 | 매일 아님 | 아니오 | `low` |

### 1.7 가치:무게 비율과 귀중도

- `R24`: 품목 하나의 무게와 가치가 둘 다 비어 있지 않으면 `Value-Weight-Ratio`를 가치 나누기 무게로 계산한다. 계산이 필요한 유일한 규칙이다.
- 귀중도는 이 비율의 구간으로 정한다.

| 규칙 | 비율 | `Valuable-Rating` |
|---|---|---|
| R25 | 100달러 이상 | `very-high` |
| R26 | 20 이상 100 미만 | `high` |
| R27 | 1 이상 20 미만 | `average` |
| R28 | 1 미만 | `low` |

앞 절의 사례에서 가치 500을 무게 10.0으로 나눈 비율 50.0은 R26에 해당하여 `high`가 된다.

### 1.8 손실·파손 등급 (입력: `Valuable-Rating`, `Fragility-Rating`)

- `R29`: 귀중도 `very-high`이면 파손 용이도와 무관하게 `important`.
- `R30`: 귀중도 `high`이고 파손 용이도 `high`이면 `important`.
- `R31`: 귀중도 `high`이고 파손 용이도가 high가 아니면 `somewhat-important`.
- `R32`: 귀중도 `average`이고 파손 용이도 `high`이면 `somewhat-important`.
- 부록의 주석에 따르면 위에 해당하지 않는 나머지 모든 경우는 `unimportant`다.

---

## 2. 특수 요구와 적재 유형으로 대안을 좁히는 규칙 (R33~R40)

### 2.1 수송 가능 수단을 쓰는 규칙

- `R33`: `Modes-Capable = rail-only`이면 권고는 RAIL이다. 이 경우 더 따질 것이 없이 곧바로 결정된다.
- `R34`: `Modes-Capable = rail-or-trucking`이면 `Alternatives = rail-or-trucking`으로 둔다. 권고는 아직 없고 후보만 줄어든 상태다.

### 2.2 적재 유형을 쓰는 규칙

- `R35`: 소량이면 권고는 소포 배송 서비스(SMALL-PACKAGE-SERVICE).
- `R36`: 보통이면 `Alternatives = trucking-or-air`.
- `R37`: 대량이면 `Alternatives = rail-or-trucking`이고 `Preference = trucking`.
- `R38`: 초대량이면 `Alternatives = rail-or-trucking`이고 `Preference = rail`.

R37과 R38의 `Preference`는 본문에서 대량은 트럭이 약간 유리하고 초대량은 철도가 약간 유리하다고 한 설명을 규칙으로 옮긴 것이다.

### 2.3 나머지 값이 모두 비었을 때의 규칙

- `R39`: 대안이 `rail-or-trucking`이고 선호가 트럭이며 다른 값이 모두 비어 있으면 권고는 TRUCKING.
- `R40`: 같은 조건에서 선호가 철도이면 권고는 RAIL.

이 두 규칙이 순서도에서 말한 제한된 데이터로의 권고, 곧 불완전한 정보에서도 최선의 판단을 내리는 동작을 만든다.

---

## 3. 트럭 대 항공의 동점 해소 (R41~R46)

모든 규칙은 `Alternatives = trucking-or-air`가 전제 조건이다. 세 변수를 중요도 순서대로 쓴다.

| 단계 | 규칙 | 조건 | 권고 |
|---|---|---|---|
| 운송 거리 유형 | R41 | `long-fast` 또는 `medium-fast` | AIR |
| 운송 거리 유형 | R42 | `long-slow`, `medium-slow`, `local` | Trucking |
| 유연성 | R43 | `Flexibility-Rating = high` | Trucking |
| 유연성 | R44 | `medium` 또는 `low` | AIR |
| 손실·파손 | R45 | `important` 또는 `somewhat-important` | AIR |
| 손실·파손 | R46 | `unimportant` | TRUCKING |

규칙 자체에는 우선순위 표시가 없다. 본문의 전략 설명처럼 앞 변수로 결정되면 뒤 변수는 쓰이지 않는다는 순서는 전략적 지식이 부여하는 것이며, 이것이 전략 다이어그램이 필요한 이유 중 하나다.

---

## 4. 철도 대 트럭의 동점 해소 (R47~R52)

모든 규칙은 `Alternatives = rail-or-trucking`이 전제다.

| 단계 | 규칙 | 조건 | 결과 |
|---|---|---|---|
| 운송 거리 유형 | R47 | `medium-fast` | TRUCKING |
| 운송 거리 유형 | R48 | `long-fast` | 어떤 수단으로도 보낼 수 없다는 메시지를 표시하고 다른 매개변수를 시도해 보라고 안내 |
| 운송 거리 유형 | R49 | `local` | TRUCKING |
| 유연성 | R50 | `Flexibility-Rating = high` | Trucking |
| 손실·파손 | R51 | `important` 또는 `somewhat-important` | TRUCKING |
| 손실·파손 | R52 | `unimportant` | RAIL |

---

## 5. 앞 사례를 규칙 번호로 다시 읽기

그림 6.8의 규칙 추적에 나온 규칙 번호를 이 부록과 맞춰 보면 한 번의 추론이 다음처럼 재구성된다.

1. `R3`: 선적 중량 10000이 5000 초과 15000 이하이므로 `large-shipment`.
2. `R37`: 대량이므로 대안 `rail-or-trucking`, 선호는 트럭.
3. `R24`: 가치 500을 무게 10.0으로 나누어 비율 50.0.
4. `R26`: 비율 50.0은 20 이상 100 미만이므로 귀중도 `high`.
5. `R30`: 귀중도 `high`와 파손 용이도 `high`가 합쳐져 손실·파손 등급이 `important`.
6. `R51`: 대안이 철도와 트럭이고 등급이 중요이므로 권고는 TRUCKING.

이 순서는 다이어그램의 화살표 방향과 일치한다. 다이어그램의 각 노드는 규칙 하나의 결론이고, 화살표는 그 결론을 조건으로 쓰는 다음 규칙으로 이어진다.

<br>
<br>
<br>

[Diagrammatic Reasoning in AI](../)
