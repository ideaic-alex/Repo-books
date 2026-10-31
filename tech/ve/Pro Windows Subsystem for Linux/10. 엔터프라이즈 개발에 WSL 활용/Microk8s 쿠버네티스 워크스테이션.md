# Microk8s 쿠버네티스 워크스테이션

WSL 2는 실제 Linux 커널을 쓰기 때문에 쿠버네티스(Kubernetes) 배포판을 설치해 마이크로서비스 개발 환경으로 쓸 수 있다. 여기서는 Canonical이 Ubuntu 계열용으로 패키징한 `microk8s`를 WSL 2에 설치하고, 애드온과 Helm으로 워크로드를 배포하는 과정을 정리한다.

---

## 1. microk8s와 사전 조건

- **microk8s**: 필요한 것을 모두 담은 쿠버네티스 배포판으로, 명령 한 줄로 설치된다.
- **Snap**: microk8s는 의존성을 모두 묶은 Snap 패키지로 배포된다.
- Snap은 systemd가 있어야 동작한다. 따라서 systemd가 실행 중인 WSL 2 배포판이 먼저 있어야 한다. 원문은 7장 "Customizing WSL"을 참고하라고 하지만, 이 노트에서는 8장 "systemd 실행하기" 문서에 정리되어 있다.
- `snap version`으로 snapd가 응답하는지 확인한다. `hello-world` Snap을 설치해 실행해 보면 Snap이 제대로 동작하는지 검증할 수 있다.

---

## 2. 설치

- `--classic` 옵션으로 설치한 뒤, 현재 사용자를 `microk8s` 그룹에 추가하고 `~/.kube` 소유권을 정리한다.
- 설치가 끝나면 `microk8s status`로 상태를 확인한다.
- 그다음에는 `kubectl`로 제어 평면(control plane)에 접속한다. 운영 클러스터를 다룰 때처럼 서비스와 파드를 배포하고 관리하면 된다.

```bash
sudo snap install microk8s --classic
sudo usermod -a -G microk8s $USER
newgrp microk8s
microk8s status
```

---

## 3. 애드온(add-on) 관리

- `microk8s enable`과 `microk8s disable`로 기능을 켜고 끈다.
- **DNS(CoreDNS)**: 클러스터 안의 서비스를 이름으로 찾게 해 주는 기능이다. microk8s는 최소한의 기능만 갖추고 있어 기본으로는 꺼져 있다. `microk8s enable dns`로 켜고, 필요 없어지면 `microk8s disable dns`로 끈다.
- **Helm**: `microk8s enable helm3`로 켠다.
- **ingress**: 클러스터 밖에서 서비스에 접속하려면 `microk8s enable ingress`로 인그레스 컨트롤러를 켠다.

---

## 4. Helm으로 배포

- **Helm**: 쿠버네티스 워크로드를 차트(chart) 단위로 배포할 때 가장 널리 쓰는 도구다.
- microk8s에서는 `microk8s.helm`(Helm 2)과 `microk8s.helm3`(Helm 3)로 Helm을 실행한다. 운영 환경과 같은 버전을 고르는 것이 좋고, 특별히 정해진 것이 없으면 Helm 3로 시작한다.
- 예제에서는 Ghost 블로그를 배포한다. 차트 저장소를 추가하고, 갱신한 뒤, 설치하는 순서다.
- 이렇게 하면 운영 환경에서 Helm을 쓰는 방식 그대로 개발에도 쓸 수 있다.

```bash
microk8s.helm3 repo add groundhog2k https://groundhog2k.github.io/helm-charts/
microk8s.helm3 repo update
microk8s.helm3 install ghost groundhog2k/ghost
```

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
