# Microk8s 쿠버네티스 워크스테이션

WSL 2는 실제 Linux 커널을 쓰기 때문에 쿠버네티스(Kubernetes) 배포판을 올려 마이크로서비스 개발 환경으로 쓸 수 있다. 여기서는 Canonical이 Ubuntu 계열로 패키징한 `microk8s`를 WSL 2에 설치하고 애드온과 Helm으로 워크로드를 배포하는 흐름을 정리한다.

---

## 1. microk8s와 사전 조건

- **microk8s**: 자체 완결형 쿠버네티스 배포판으로, 한 줄 명령으로 설치된다.
- **Snap**: microk8s는 모든 의존성을 묶은 Snap 패키지로 배포된다.
- Snap은 systemd가 필요하므로, systemd가 동작하는 WSL 2 배포판이 전제다(원문은 7장 "Customizing WSL"을 가리키지만, 이 노트에서는 8장 "systemd 실행하기" 문서에 정리되어 있다).
- `snap version`으로 snapd가 응답하는지 확인하고, `hello-world` Snap을 설치해 실행해 보면 동작 여부를 검증할 수 있다.

---

## 2. 설치

- `--classic` 옵션으로 설치한 뒤 현재 사용자를 `microk8s` 그룹에 추가하고, `~/.kube` 소유권을 정리한다.
- 설치 후 `microk8s status`로 상태를 확인한다.
- 이후 `kubectl`로 제어 평면(control plane)에 접근하며, 운영 클러스터를 다루듯 서비스와 파드를 배포, 관리한다.

```bash
sudo snap install microk8s --classic
sudo usermod -a -G microk8s $USER
newgrp microk8s
microk8s status
```

---

## 3. 애드온(add-on) 관리

- `microk8s enable`과 `microk8s disable`로 기능을 켜고 끈다.
- **DNS(CoreDNS)**: 클러스터 내부 서비스를 이름으로 찾기 위한 기능이다. microk8s는 최소 구성이라 기본으로 꺼져 있으므로 `microk8s enable dns`로 켠다. 필요 없어지면 `microk8s disable dns`.
- **Helm**: `microk8s enable helm3`로 활성화한다.
- **ingress**: 외부에서 서비스에 접근하려면 `microk8s enable ingress`로 인그레스 컨트롤러를 켠다.

---

## 4. Helm으로 배포

- **Helm**: 쿠버네티스 워크로드를 차트(chart) 단위로 배포하는 일반적인 방법이다.
- microk8s에서는 `microk8s.helm`(Helm 2)과 `microk8s.helm3`(Helm 3)로 접근한다. 운영 환경과 같은 버전을 고르되, 선호가 없으면 Helm 3로 시작한다.
- 예로 Ghost 블로그를 저장소 추가, 갱신, 설치 순서로 배포한다.
- 이후 운영 환경에서 Helm을 쓰듯 개발에 활용한다.

```bash
microk8s.helm3 repo add groundhog2k https://groundhog2k.github.io/helm-charts/
microk8s.helm3 repo update
microk8s.helm3 install ghost groundhog2k/ghost
```

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
