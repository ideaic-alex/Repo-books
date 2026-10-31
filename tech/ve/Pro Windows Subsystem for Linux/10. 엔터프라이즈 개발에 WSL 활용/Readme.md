# 10장. 엔터프라이즈 개발에 WSL 활용 (Using WSL for Enterprise Development)

WSL은 Windows와 연동되므로, 익숙한 Windows IDE와 편집기를 그대로 쓰면서 프로젝트는 실제 Linux 환경에서 실행할 수 있다. WSL 2는 Linux 커널을 쓰기 때문에 쿠버네티스로 마이크로서비스를 개발하거나, 워크스테이션의 GPU로 머신러닝 연산을 가속하는 일도 된다. 이 장에서는 이런 작업을 위한 실제 설정 방법을 다룬다.

---

## 1. 핵심 요점

- `microk8s`는 Snap으로 설치하는 올인원 쿠버네티스다. systemd가 켜진 WSL 2에서 애드온(dns, helm3, ingress)과 Helm으로 개발용 클러스터를 만든다.
- Docker Desktop에서 WSL 2 기반 엔진과 WSL 통합을 켜면, Windows와 각 배포판이 같은 Docker 엔진을 함께 쓴다.
- Visual Studio는 .NET Core Debugging with WSL 2로, VS Code는 Remote - WSL 확장으로, JetBrains는 `\\wsl$` 경로와 WSL 도구 지정으로 WSL과 연동한다.
- WSL 2에서는 GPU를 패스스루로 넘기지 않고 WSL 2가 제공하는 API로 쓴다. NVIDIA GPU는 CUDA(Docker와 nvidia-docker2)를, 그 외 GPU는 DirectML(Miniconda와 tensorflow-directml)을 쓴다.

---

## 2. 섹션 문서

- [Microk8s 쿠버네티스 워크스테이션](Microk8s%20쿠버네티스%20워크스테이션.md)
- [Docker Desktop 연동](Docker%20Desktop%20연동.md)
- [편집기와 IDE 연동](편집기와%20IDE%20연동.md)
- [GPU 연산 패스스루](GPU%20연산%20패스스루.md)

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
