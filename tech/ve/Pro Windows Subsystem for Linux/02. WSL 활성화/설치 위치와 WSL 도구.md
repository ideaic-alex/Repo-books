# 설치 위치와 WSL 도구

배포판이 디스크의 어디에 어떤 형태로 저장되는지, Windows 쪽에 어떤 WSL 관련 파일이 있는지 정리한다. 내부 구조를 알아 두면 문제를 해결하거나 관리할 때 도움이 된다.

---

## 1. 설치 형태와 위치

- 모든 배포판은 rootfs 이미지로 설치된다. 스토어나 `.appx`로 설치하면 rootfs에 부가 설정이 함께 들어 있다. 부가 설정은 WSL API 등록, 시작 메뉴 아이콘, 실행 별칭(`ubuntu.exe`), sudo 권한이 있는 기본 사용자 생성이다. 이 부가 설정은 배포판마다 조금씩 다르며, Microsoft가 공식으로 제공하는 템플릿은 WSL-DistroLauncher다.
- 스토어와 `.appx`로 설치한 배포판은 다른 UWP 패키지와 마찬가지로 `C:\Users\<사용자>\AppData\Local\Packages\` 아래에 놓인다.
- **WSL 1**: 처음 실행할 때 `<패키지명>\LocalState` 폴더에 파일 시스템 형태로 풀린다.
- **WSL 2**: 같은 위치의 `LocalState\ext4.vhdx`라는 Hyper-V 가상 디스크(VHDX) 파일로 풀린다.
- `wsl.exe --import`로 설치하면 WSL에 등록하는 것 외의 부가 설정은 없고, 지정한 위치에 풀린다(WSL 2는 VHDX 파일).

---

## 2. 접근 시 주의

- 위 경로로 WSL 파일 시스템에 직접 접근해 수정하면 데이터가 복구할 수 없을 만큼 손상될 수 있다.
- 파일은 `\\wsl$\<배포판 이름>` 경로로 접근하거나, Windows 10 2010 이후 버전의 파일 탐색기 빠른 실행 메뉴로만 접근한다.

---

## 3. %SystemRoot%\system32\lxss\

- `LxssManager.dll`: WSL 환경을 관리하는 서비스.
- `LxssManagerProxyStub.dll`: 부팅 후반에 `LxssManager.dll`을 불러오는(로드하는) 초기 스텁.
- `wslclient.dll`: 빌드 19555 이상에서 `wsl.exe`, `bash.exe`, `wslhost.exe`, `wslconfig.exe`, `LxssManager.dll`의 기능을 하나로 합친 라이브러리.
- `wslhost.exe`: WSL 1에서 백그라운드 작업이 Windows와 계속 연동되도록(상호운용성) 유지해 주는 도구.
- `tools/`와 `lib/` 폴더.

---

## 4. tools 폴더 (WSL 2 핵심 구성)

- **bsdtar**: WSL에 설치된 배포판을 tar.gz로 변환(내보내기·가져오기)하는 도구.
- **ext4.vhdx.gz**: 미리 포맷해 둔 빈 ext4 파일 시스템.
- **init**: WSL 2 컨테이너에서 PID 1로 동작하는 init 프로세스.
- **initrd.img**: 부팅 과정에서 WSL 2 커널이 불러오는(로드하는) 초기 RAM 디스크.
- **kernel**: WSL 2 리눅스 커널.
- **license**: 커널에 적용되는 GPL 2 사본.

---

## 5. lib 폴더 (GPU용, 빌드 20150 이상)

- Nvidia 쪽: `libcuda.so`, `libnvidia-ml.so.1`, `libnvwgf2umx.so` 등이 있고, CUDA와 머신러닝 등 GPU 연산을 지원한다.
- DirectX 쪽: `libdxcore.so`, `libd3d12.so`, `libd3d12core.so`, `libdirectml.so` 등이 있고, Direct3D 가속과 DirectML을 지원한다.
- 이 폴더는 배포판 안의 `/usr/lib/wsl/lib/`에 연결(미러링)된다.

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
