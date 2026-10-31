# GPU 연산 패스스루

AI/ML 작업은 대량의 연산이 필요해서 CPU만으로는 느리고, TensorFlow 같은 프레임워크는 GPU 가속을 권장한다. WSL 2에서 GPU를 쓰는 방법과, NVIDIA CUDA 및 DirectML 환경 구성 절차를 정리한다.

---

## 1. WSL 2의 GPU 접근 방식

- GPU는 Windows가 화면 출력에 쓰고 있어서, PCI 패스스루(GPU 패스스루)로 떼어내 WSL 2 가상 머신에 전용 할당할 수 없다.
- 대신 WSL 2가 GPU에 접근하는 API를 노출하므로, Windows에서 GPU를 분리하지 않고도 연산을 쓸 수 있다.
- 책은 이 기능을 Windows Insider 빌드 20150부터 가능하고 21H1 공개 릴리스에서 사용할 수 있다고 설명한다.

---

## 2. NVIDIA CUDA

- 전제: NVIDIA GPU와, NVIDIA 사이트의 WSL용 개발자 드라이버 설치.
- TensorFlow는 WSL 안에 Docker를 직접 설치해 쓰는 방식이 가장 좋다고 한다. Docker Desktop을 쓰고 있다면 해당 배포판의 WSL 통합은 꺼야 한다.

### 구성 절차

1. WSL 배포판(Debian/Ubuntu 가정)에 `docker.io`를 설치하고 사용자를 `docker` 그룹에 추가한다.
2. NVIDIA의 APT 저장소(nvidia-docker, libnvidia-container 실험 버전)를 등록한다.
3. `apt update` 후 `nvidia-docker2`를 설치해 컨테이너가 GPU에 접근하도록 한다.
4. `wsl.exe --terminate <배포판>`으로 인스턴스를 종료해 재시작을 반영한다.
5. CUDA 벤치마크 컨테이너를 실행해 GPU 장치명이 출력되는지 검증한다.
6. TensorFlow GPU 이미지로 Jupyter Notebook 컨테이너를 실행한다.
7. 출력 마지막 줄의 URL을 브라우저에 붙여 넣되 `127.0.0.1`을 `localhost`로 바꿔 접속한다.

```bash
sudo apt -y install docker.io
sudo apt install -y nvidia-docker2
docker run --gpus all nvcr.io/nvidia/k8s/cuda-sample:nbody nbody -gpu -benchmark
```

---

## 3. DirectML (NVIDIA 외 GPU)

- **DirectML**: AMD GPU(또는 그래픽 내장 AMD CPU), Intel GPU(또는 그래픽 내장 Intel CPU)에서 가속을 쓰는 경로다.
- 각 제조사의 WSL용 개발자 드라이버를 먼저 설치해야 한다.
- TensorFlow의 DirectML 지원판을 Miniconda 환경에 설치한다.

### 구성 절차

1. Miniconda 설치 스크립트를 내려받아 실행한다.
2. `conda`로 새 Python 환경(예: `directml`)을 만들고 활성화한다.
3. `pip install tensorflow-directml`로 패키지를 설치한다.
4. 파이썬 대화형 세션에서 간단한 텐서 연산 예제로 가속 동작을 검증한다.

```bash
conda create --name directml python=3.6
conda activate directml
pip install tensorflow-directml
```

- 더 많은 예제는 Microsoft의 DirectML GitHub 저장소를 참고하라고 안내한다.

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
