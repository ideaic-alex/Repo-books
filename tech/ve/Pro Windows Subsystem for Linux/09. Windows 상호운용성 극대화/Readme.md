# 9장. Windows 상호운용성 극대화 (Maximizing Windows Interoperability)

WSL을 쓰다 보면 Windows의 도구와 파일을 Linux 작업에 쓰거나, 반대로 Linux 도구를 Windows 작업에 써야 할 때가 많다. 이 장은 WSL 배포판과 Windows 사이의 벽을 낮춰, 한쪽만 쓸 때보다 작업하기 편한 환경을 만드는 방법을 정리한다. 경로 변환, 명령 연결, 환경 변수 공유, 파일 시스템 마운트를 차례로 다룬다.

---

## 1. 핵심 요점

- `wslpath`로 Windows 경로와 WSL 경로를 서로 변환한다. `wslutilities`(`wslusc`, `wslsys`, `wslfetch`, `wslvar`, `wslview`)로는 바로가기 만들기, 시스템 정보 확인, Windows 변수 읽기, 기본 앱으로 열기를 할 수 있다.
- 파이프와 리다이렉션은 Windows와 WSL의 경계를 넘나든다. `clip.exe`, `powershell.exe`, `wsl.exe`를 서로 연결할 수 있고, 히어독으로 여러 줄 입력도 넘길 수 있다.
- `WSLENV`와 접미사(`/p`, `/l`, `/u`, `/w`)로 환경 변수를 어느 방향으로 넘길지, 경로로 변환할지를 정한다.
- `drvfs`로 Windows 파일 공유를 WSL에서 쓴다. FUSE(SSHFS 등)로는 Windows가 모르는 파일 시스템을 WSL에서 쓰고, `\\wsl$`를 통해 다시 Windows에서 열 수 있다.
- `wsl.exe --mount`로 물리 디스크, 파티션, VHDX를 붙이면 Windows에서도 네이티브 Linux 파일 시스템을 쓸 수 있다. 쓰고 나면 `--unmount`로 해제한다.

---

## 2. 섹션 문서

- [경로 변환과 wslutilities](경로%20변환과%20wslutilities.md)
- [Windows와 Linux 간 파이프와 리다이렉션](Windows와%20Linux%20간%20파이프와%20리다이렉션.md)
- [환경 변수 공유 WSLENV](환경%20변수%20공유%20WSLENV.md)
- [네트워크 공유와 FUSE 파일 시스템](네트워크%20공유와%20FUSE%20파일%20시스템.md)
- [디스크와 VHDX 마운트](디스크와%20VHDX%20마운트.md)

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
