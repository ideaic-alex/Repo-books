# 설치 위치와 WSL 도구

배포판이 디스크 어디에 어떻게 저장되는지, Windows 쪽에 어떤 WSL 설정 파일이 있는지 정리한다. 내부 구조를 알면 문제 해결과 관리에 도움이 된다.

---

## 1. 설치 형태와 위치

- 모든 배포판은 rootfs 이미지로 설치된다. 스토어나 `.appx`로 설치하면 rootfs에 부가 구성(WSL API 등록, 시작 메뉴 아이콘, 실행 별칭 `ubuntu.exe`, sudo 권한의 기본 사용자 생성)이 함께 들어 있다. 이 부가 구성은 배포판마다 조금씩 다르며, Microsoft의 공식 템플릿은 WSL-DistroLauncher다.
- 스토어와 `.appx` 설치본은 다른 UWP 패키지와 같이 `C:\Users\<사용자>\AppData\Local\Packages\` 아래에 놓인다.
- **WSL 1**: 첫 실행 때 `<패키지명>\LocalState`에 파일 시스템으로 풀린다.
- **WSL 2**: 같은 위치의 `LocalState\ext4.vhdx`라는 Hyper-V 가상 디스크(VHDX)로 풀린다.
- `wsl.exe --import`는 WSL 등록 외의 부가 구성이 없고, 지정한 위치에 풀린다(WSL 2는 VHDX).

---

## 2. 접근 시 주의

- 위 경로로 WSL 파일 시스템에 직접 접근해 수정하면 데이터가 복구 불가능하게 손상될 수 있다.
- 파일은 `\\wsl$\<배포판 이름>` 경로나 Windows 10 2010 이후 파일 탐색기의 빠른 실행 메뉴로만 접근한다.

---

## 3. %SystemRoot%\system32\lxss\

- `LxssManager.dll`: WSL 환경 관리 서비스.
- `LxssManagerProxyStub.dll`: 부팅 후반에 `LxssManager.dll`을 로드하는 초기 스텁.
- `wslclient.dll`: 빌드 19555 이상에서 `wsl.exe`, `bash.exe`, `wslhost.exe`, `wslconfig.exe`, `LxssManager.dll`의 기능을 하나로 통합한 라이브러리.
- `wslhost.exe`: WSL 1에서 백그라운드 작업의 Windows 상호운용성을 유지하는 도구.
- `tools/`와 `lib/` 폴더.

---

## 4. tools 폴더 (WSL 2 핵심 구성)

- **bsdtar**: WSL 설치본을 tar.gz로 변환(내보내기·가져오기)하는 도구.
- **ext4.vhdx.gz**: 미리 포맷된 빈 ext4 파일 시스템.
- **init**: WSL 2 컨테이너에서 PID 1로 동작하는 init 프로세스.
- **initrd.img**: 부팅 과정에서 WSL 2 커널이 로드하는 초기 RAM 디스크.
- **kernel**: WSL 2 리눅스 커널.
- **license**: 커널에 적용되는 GPL 2 사본.

---

## 5. lib 폴더 (GPU용, 빌드 20150 이상)

- Nvidia 쪽: `libcuda.so`, `libnvidia-ml.so.1`, `libnvwgf2umx.so` 등. CUDA와 머신러닝 등 GPU 연산 지원.
- DirectX 쪽: `libdxcore.so`, `libd3d12.so`, `libd3d12core.so`, `libdirectml.so` 등. Direct3D 가속과 DirectML 지원.
- 이 폴더는 배포판 안의 `/usr/lib/wsl/lib/`에 연결(미러링)된다.

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
