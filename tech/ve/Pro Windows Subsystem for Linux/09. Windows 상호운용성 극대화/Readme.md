# 9장. Windows 상호운용성 극대화 (Maximizing Windows Interoperability)

WSL을 쓰다 보면 Windows의 도구와 파일을 Linux 작업에 쓰거나 그 반대가 필요할 때가 많다. 이 장은 WSL 배포판과 Windows 사이의 벽을 낮춰, 어느 한쪽만 쓸 때보다 생산적인 환경을 만드는 방법을 정리한다. 경로 변환, 명령 연결, 환경 변수 공유, 파일 시스템 마운트가 중심이다.

---

## 1. 핵심 요점

- `wslpath`로 Windows와 WSL 경로를 상호 변환하고, `wslutilities`(`wslusc`, `wslsys`, `wslfetch`, `wslvar`, `wslview`)로 바로가기, 시스템 정보, Windows 변수, 기본 앱 열기를 처리한다.
- 파이프와 리다이렉션이 Windows와 WSL 경계를 넘나든다. `clip.exe`, `powershell.exe`, `wsl.exe`를 연결하고 히어독으로 여러 줄 입력을 넘길 수 있다.
- `WSLENV`와 접미사(`/p`, `/l`, `/u`, `/w`)로 환경 변수의 전달 방향과 경로 변환을 제어한다.
- `drvfs`로 Windows 파일 공유를, FUSE(SSHFS 등)로 Windows가 모르는 파일 시스템을 WSL에서 쓰고 `\\wsl$`로 다시 Windows에 노출한다.
- `wsl.exe --mount`로 물리 디스크, 파티션, VHDX를 붙여 네이티브 Linux 파일 시스템을 Windows에서 활용하고 `--unmount`로 해제한다.

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
