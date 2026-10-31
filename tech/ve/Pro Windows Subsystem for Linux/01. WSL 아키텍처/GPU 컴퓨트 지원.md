# GPU 컴퓨트 지원

2020년에 발표된 WSL 2의 큰 구조 변화는 GPU 연산 지원이다. 이 문서는 준가상화(para-virtualized) GPU의 구성 요소와 DirectX, CUDA, OpenGL 계열 지원 방식을 정리한다. 내용은 집필 시점(2020년) 기준의 계획과 현황이다.

---

## 1. 개요와 요건

- **GPU 컴퓨트(GPU compute)**: WSL 2 안에 준가상화 GPU(para-virtualized GPU)를 두고 AI, 머신러닝, 통계 분석 같은 GPU 연산을 가능하게 하는 기능이다.
- 2020년 6월 Insider Dev 채널 빌드로 먼저 공개됐고, 2021년 Windows 10 정식 릴리스에 포함될 것으로 예상됐다.
- 최소 Windows 10 빌드 20150과, GPU 칩셋 제조사의 WSL 대응 Windows 드라이버가 필요하다. Nvidia 베타 드라이버는 개발자 프로그램으로 제공되고, 추후 Windows Update로 배포될 예정이다.
- 가속 개발 환경 설정은 책의 10장에서 다룬다.

---

## 2. /dev/dxgkrnl 드라이버

- **`/dev/dxgkrnl`**: 새로 추가된 리눅스 커널 장치 드라이버. NT 커널에서 DirectX가 WDDM(Windows Display Driver Model)을 통해 제공하는 것과 비슷한 장치 호출을 제공한다. 덕분에 WDDM용으로 작성된 API와 드라이버가 WSL에서 동작할 수 있다.
- **통신 경로**: Hyper-V VM Bus를 거쳐 WDDM Paravirtualization Protocol로 NT 커널의 dxgkrnl과 직접 통신하고, 요청은 GPU 커널 모드 드라이버를 거쳐 GPU에 전달된다.
- NT 커널은 WSL과 Windows의 GPU 프로세스를 동등하게 취급하며 자원을 동적으로 배분한다.
- 성격은 VirtualBox 같은 가상화 플랫폼의 패스스루 그래픽 드라이버와 비슷하다.
- 현재는 GPU 연산과 화면 밖 렌더링(off-screen rendering)만 되고, 화면 출력 기능은 없다.
- DirectX 자체는 포함하지 않으며, 소스는 공개돼 있고 Microsoft가 메인라인 커널로의 업스트림 절차를 시작했다.

---

## 3. 각 API 지원 방식

- **Direct3D 12**: WDDM이 리눅스로 확장된 덕에 Direct3D 12 API를 포팅했다. Windows 라이브러리 소스에서 리눅스용 전체 라이브러리를 컴파일한다. 지금은 화면 밖 렌더링만 가능하다.
- **DirectML**: DirectX의 저수준 머신러닝 API. DirectX 호환 하드웨어면 어디서나 동작하므로, Nvidia GPU가 필요한 CUDA와 달리 Intel과 AMD GPU에서도 쓸 수 있다. DirectML 백엔드를 붙인 TensorFlow 프리뷰도 공개됐고 업스트림을 협의 중이다.
- **OpenGL / OpenCL**: Collabora와 협력해 오픈소스 Mesa 라이브러리 위에 DirectX 매핑 계층을 만든다. 작업은 미완성이며, Ubuntu 같은 배포판이 새 Mesa를 채택하면 3D 가속이 자동으로 적용된다. Vulkan은 지원 방식을 계속 검토 중이다.
- **Nvidia CUDA**: Nvidia와 협력해 `/dev/dxgkrnl`을 통해 WDDM 계층을 겨냥한 리눅스용 CUDA를 만들었다. WSL의 TensorFlow와 Nvidia 런타임으로 실행하는 Docker 컨테이너에 CUDA 가속을 제공한다.

---

## 4. 라이브러리 배치

- GPU 기능용 라이브러리는 glibc 기반 배포판의 `/usr/lib/wsl/lib`에 덧씌워진다(Windows 쪽 `%SystemRoot%\system32\lxss\lib`에서 연결). 리눅스 전용 드라이버는 따로 필요 없다.
- musl libc를 쓰는 Alpine 같은 배포판은 아직 지원되지 않는다.
- `libd3d12`, `libdirectml`, `libcuda`, `libdxcore`는 오픈소스가 아니다.

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
