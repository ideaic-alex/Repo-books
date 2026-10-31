# 모델 개발과 EON Tuner

데이터를 올린 뒤에는 Edge Impulse의 impulse 설계로 신호 처리(DSP)와 학습을 구성한다. 기본 설정만으로 76.3% 정확도를 얻고, 자동 머신러닝 도구인 EON Tuner로 약 89%까지 올리는 과정을 정리한다.

---

## 1. Impulse 설계

- **impulse design**: DSP와 ML 학습을 묶은 Edge Impulse의 워크플로 이름으로, 전체 파이프라인을 블록 그림으로 보여 준다.
- **원시 데이터 블록**: 이미지를 같은 크기로 정규화하고, 정사각형이 아니면 지정한 방식으로 자르거나 맞춘다.
- **DSP 블록**: 이미지의 핵심 특징을 오픈 소스 신호 처리 스크립트로 추출한다.
- **학습 블록**: 설정한 구조로 신경망을 학습한다.
- **출력**: 분류할 클래스가 배포 출력으로 표시된다.

| 항목 | 설정 |
|---|---|
| 이미지 너비/높이 | 160 / 160 |
| Resize mode | Fit shortest axis |
| Processing block | Image |
| Learning block | Transfer Learning (Images) |

---

## 2. DSP 블록

- **Image 블록**: 기본 제공되며 무료로 쓰고 배포할 수 있다. 코드는 Edge Impulse GitHub의 `processing-blocks` 저장소에 공개되어 있다.
- **색 깊이**: RGB로 두고 파라미터를 저장한 뒤 Generate features를 실행하면 feature explorer로 특징 분포를 볼 수 있다.
- **커스텀 DSP 블록**: 원하는 언어로 만들 수 있지만, 배포가 동작하려면 같은 로직을 C++로 구현해 SDK에 통합해야 한다.
- **기본 블록의 장점**: 자체 C++ 코드를 쓰지 않아도 배포 라이브러리에 모두 포함되어 개발 시간이 줄어든다.

---

## 3. 전이 학습 기본 설정

- **Visual 모드**: 웹 GUI로 가장 쉽게 설정하며, 기본값이 자동 적용된다.
- **학습 위치**: 학습 작업은 Edge Impulse 서버에서 실행되므로 로컬 자원을 쓰지 않는다. 오래 걸리면 알림 벨로 완료 메일을 받을 수 있다.
- **Expert 모드**: TensorFlow/Keras에 익숙하면 Keras 모드로 전환하거나 블록을 로컬에서 편집할 수 있다.

```
Number of training cycles: 100
Learning rate: 0.0005
Validation set size: 20%
Auto-balance dataset / Data augmentation: unchecked
Architecture: MobileNetV2 96x96 0.35 (16 neurons, 0.1 dropout)
```

- **초기 결과**: 코드 없이 기본값만으로 정확도 76.3%를 얻었고, 맞춤 설정 없이는 꽤 괜찮은 출발점으로 평가된다. Model의 Last training performance 화면에서 확인한다.

---

## 4. EON Tuner

- **개념**: 대상 기기와 지연 시간 요구에 맞춰 여러 후보 모델 구조와 DSP 블록을 동시에 평가하는 자동 머신러닝 도구이다.
- **설정**: Dataset category는 Vision, Target device는 Cortex-M7(비지원 기기면 하드웨어가 가장 비슷한 것), Time per inference는 100 ms로 두고 Start EON tuner를 누른다.
- **결과 해석**: 기본 블록은 76.3%였고 튜너 후보는 89.5%대까지 나왔다. 최고 후보는 약 90%였지만 RAM과 ROM이 대상 하드웨어 사양을 넘어 제외하고, 사양 안의 차선책 89%를 선택했다.
- **적용**: 선택한 구성의 Select 버튼으로 primary model을 갱신하면 Impulse design 블록이 바뀌고, Transfer learning 화면에서 새 정확도와 지연 시간 계산을 확인할 수 있다.
- **교훈**: 정확도만 보지 말고 대상 기기의 RAM, ROM, 지연 시간 제약 안에서 고르는 것이 임베디드 모델 선택의 핵심이다.

<br>
<br>
<br>

[AI at the Edge](../)
