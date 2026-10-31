# GPU 연산 패스스루

AI/ML 작업은 연산량이 많아서 CPU만으로는 느리고, TensorFlow 같은 프레임워크는 GPU 가속을 권장한다. 이 문서에서는 WSL 2에서 GPU를 쓰는 방식과, NVIDIA CUDA 및 DirectML 환경을 설정하는 절차를 정리한다.

---

## 1. WSL 2의 GPU 접근 방식

- Windows가 화면 출력에 GPU를 쓰고 있어서, PCI 패스스루(GPU 패스스루)로 GPU를 떼어내 WSL 2 가상 머신에 전용으로 할당할 수 없다.
- 대신 WSL 2가 GPU에 접근하는 API를 제공한다. 덕분에 Windows에서 GPU를 분리하지 않고도 GPU 연산을 쓸 수 있다.
- 책에 따르면 이 기능은 Windows Insider 빌드 20150부터 쓸 수 있고, 일반 사용자에게는 21H1 정식 릴리스부터 제공된다.

---

## 2. NVIDIA CUDA

- 사전 조건: NVIDIA GPU가 있어야 하고, NVIDIA 사이트에서 WSL용 개발자 드라이버를 설치해야 한다.
- TensorFlow는 WSL 안에 Docker를 직접 설치해서 쓰는 방식이 가장 좋다고 한다. Docker Desktop을 쓰고 있다면 해당 배포판의 WSL 통합은 꺼야 한다.

### 설정 절차

1. WSL 배포판(Debian/Ubuntu 기준)에 `docker.io`를 설치하고, 사용자를 `docker` 그룹에 추가한다.
2. NVIDIA의 APT 저장소(nvidia-docker, libnvidia-container 실험 버전)를 등록한다.
3. `apt update`를 실행한 뒤 `nvidia-docker2`를 설치한다. 컨테이너가 GPU에 접근할 수 있게 하는 패키지다.
4. `wsl.exe --terminate <배포판>`으로 인스턴스를 종료해, 변경 사항이 적용되도록 다시 시작한다.
5. CUDA 벤치마크 컨테이너를 실행해 GPU 장치 이름이 출력되는지 확인한다.
6. TensorFlow GPU 이미지로 Jupyter Notebook 컨테이너를 실행한다.
7. 출력 마지막 줄의 URL을 브라우저에 붙여 넣는다. 이때 `127.0.0.1`을 `localhost`로 바꿔서 접속한다.

```bash
sudo apt -y install docker.io
sudo apt install -y nvidia-docker2
docker run --gpus all nvcr.io/nvidia/k8s/cuda-sample:nbody nbody -gpu -benchmark
```

---

## 3. DirectML (NVIDIA 외 GPU)

- **DirectML**: AMD GPU(또는 그래픽 기능이 내장된 AMD CPU), Intel GPU(또는 그래픽 기능이 내장된 Intel CPU)에서 GPU 가속을 쓰는 방법이다.
- 먼저 각 제조사가 제공하는 WSL용 개발자 드라이버를 설치해야 한다.
- TensorFlow의 DirectML 지원 버전을 Miniconda 환경에 설치한다.

### 설정 절차

1. Miniconda 설치 스크립트를 내려받아 실행한다.
2. `conda`로 새 Python 환경(예: `directml`)을 만들고 활성화한다.
3. `pip install tensorflow-directml`로 패키지를 설치한다.
4. 파이썬 대화형 세션에서 간단한 텐서 연산 예제를 실행해, 가속이 동작하는지 확인한다.

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
