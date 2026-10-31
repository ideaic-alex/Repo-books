# GPU 컴퓨트 지원

2020년에 발표된 WSL 2의 큰 구조 변화 하나는 GPU 연산 지원이다. 이 문서는 준가상화(para-virtualized) GPU의 구성 요소와 DirectX, CUDA, OpenGL 계열의 지원 방식을 정리한다. 내용은 책을 쓸 당시(2020년)의 계획과 현황이다.

---

## 1. 개요와 요건

- **GPU 컴퓨트(GPU compute)**: WSL 2 안에 준가상화 GPU(para-virtualized GPU)를 두어서 AI, 머신러닝, 통계 분석 같은 GPU 연산을 할 수 있게 하는 기능이다.
- 2020년 6월 Insider Dev 채널 빌드로 먼저 공개되었고, 2021년 Windows 10 정식 릴리스에 포함될 것으로 예상되었다.
- Windows 10 빌드 20150 이상과, GPU 제조사가 WSL용으로 내놓은 Windows 드라이버가 필요하다. Nvidia 베타 드라이버는 개발자 프로그램으로 받을 수 있고, 나중에 Windows Update로 배포될 예정이다.
- GPU 가속 개발 환경을 설정하는 방법은 책의 10장에서 다룬다.

---

## 2. /dev/dxgkrnl 드라이버

- **`/dev/dxgkrnl`**: 새로 추가된 리눅스 커널 장치 드라이버다. NT 커널에서 DirectX가 WDDM(Windows Display Driver Model)을 통해 제공하는 것과 비슷한 장치 호출을 제공한다. 덕분에 WDDM용으로 작성된 API와 드라이버가 WSL에서도 동작한다.
- **통신 경로**: Hyper-V VM Bus를 거쳐 WDDM Paravirtualization Protocol로 NT 커널의 dxgkrnl과 직접 통신한다. 요청은 GPU 커널 모드 드라이버를 거쳐 GPU에 전달된다.
- NT 커널은 WSL의 GPU 프로세스와 Windows의 GPU 프로세스를 똑같이 대하며 자원을 상황에 맞게 나누어 준다.
- 성격은 VirtualBox 같은 가상화 플랫폼의 패스스루 그래픽 드라이버와 비슷하다.
- 현재는 GPU 연산과 화면 밖 렌더링(off-screen rendering)만 되고, 화면에 출력하는 기능은 없다.
- DirectX 자체는 포함하지 않는다. 소스는 공개되어 있고, Microsoft가 메인라인 커널에 반영하는 업스트림 절차를 시작했다.

---

## 3. 각 API 지원 방식

- **Direct3D 12**: WDDM이 리눅스까지 확장되어 Direct3D 12 API를 포팅했다. Windows 라이브러리 소스로 리눅스용 라이브러리 전체를 컴파일한다. 지금은 화면 밖 렌더링만 가능하다.
- **DirectML**: DirectX의 저수준 머신러닝 API다. DirectX와 호환되는 하드웨어면 어디서나 동작한다. 그래서 Nvidia GPU가 필요한 CUDA와 달리 Intel과 AMD GPU에서도 쓸 수 있다. DirectML 백엔드를 붙인 TensorFlow 프리뷰도 공개되었고, 업스트림 반영을 협의 중이다.
- **OpenGL / OpenCL**: Collabora와 협력해서 오픈소스 Mesa 라이브러리 위에 DirectX 매핑 계층을 만들고 있다. 작업은 아직 끝나지 않았다. Ubuntu 같은 배포판이 새 Mesa를 채택하면 3D 가속이 자동으로 적용된다. Vulkan은 지원 방식을 계속 검토 중이다.
- **Nvidia CUDA**: Nvidia와 협력해서 `/dev/dxgkrnl`을 통해 WDDM 계층에 맞춘 리눅스용 CUDA를 만들었다. WSL의 TensorFlow와, Nvidia 런타임으로 실행하는 Docker 컨테이너에서 CUDA 가속을 쓸 수 있다.

---

## 4. 라이브러리 배치

- GPU 기능에 쓰는 라이브러리는 glibc 기반 배포판의 `/usr/lib/wsl/lib`에 겹쳐서 마운트된다(Windows 쪽 `%SystemRoot%\system32\lxss\lib`에서 연결). 리눅스 전용 드라이버는 따로 설치하지 않아도 된다.
- musl libc를 쓰는 Alpine 같은 배포판은 아직 지원하지 않는다.
- `libd3d12`, `libdirectml`, `libcuda`, `libdxcore`는 오픈소스가 아니다.

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
