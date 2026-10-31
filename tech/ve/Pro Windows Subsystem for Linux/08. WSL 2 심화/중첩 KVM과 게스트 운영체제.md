# 중첩 KVM과 게스트 운영체제

커스텀 커널에 KVM을 모듈로 넣었다면 이제 모듈을 로드하고 설정해 중첩 가상화를 활성화한다. 이를 바탕으로 KVM에 의존하는 minikube(Kubernetes)를 쓰거나, QEMU로 리눅스뿐 아니라 macOS, Arca Noae, OpenIndiana, Haiku 같은 다른 운영체제를 직접 실행할 수 있다.

---

## 1. kvm_intel 모듈 설정과 로드

- **모듈 옵션 파일**: `/etc/modprobe.d/kvm-nested.conf`에 `kvm-intel` 옵션을 적는다. 중첩 가상화(`nested`)와 속도 최적화 옵션(`enable_shadow_vmcs`, `enable_apicv`, `ept`)을 켠다.
- **로드**: `sudo modprobe kvm_intel`. 로드 전 `kvm-ok`(cpu-checker 패키지)는 `/dev/kvm`이 없다고 알린다.
- **오류 힌트**: "Module kvm_intel not found" 오류는 `sudo make modules_install`을 빠뜨렸다는 뜻이다.
- **확인**: 로드 후 `kvm-ok`가 가속 사용 가능을 알리고, `/sys/module/kvm_intel/parameters/nested` 값으로 중첩 지원을 확인한다.
- **권한**: `/dev/kvm`의 접근 권한을 `chmod 666`으로 열어 사용자가 쓸 수 있게 한다.

```bash
sudo modprobe kvm_intel
cat /sys/module/kvm_intel/parameters/nested
sudo chmod 666 /dev/kvm
```

---

## 2. 모듈 운용 팁

- 모듈로 빌드했으므로 KVM을 쓸 WSL을 실행할 때마다 직접 로드해야 한다.
- 설정을 바꿀 때는 `modprobe -r kvm_intel`로 언로드하고, 파일을 수정한 뒤 다시 로드한다.
- 설정이 굳어지면 커널에 내장해 재빌드하거나, Windows 10 빌드 21286 이상에서는 `modprobe kvm_intel`을 `[boot]` 명령에 넣는다.
- 모듈 이름을 `.wslconfig`의 커널 명령줄에 추가하는 방법도 언급된다.

---

## 3. QEMU로 Kubuntu 설치 예시

QEMU 창은 X로 표시되므로 7장의 X 서버 설정이나 공식 GUI 지원이 필요하다.

1. `qemu-kvm`과 대용량 다운로더 `aria2`를 설치한다.
2. 설치 ISO의 torrent 파일을 `aria2c`로 받는다. 멀티스레드 다운로드가 `wget`이나 `curl`보다 유리하다.
3. `qemu-img create`로 qcow2 형식(QEMU 기본 가상 디스크) 20G 디스크를 만든다. `qemu-img`는 QCOW, Hyper-V의 VHDX, VirtualBox의 VMDK 사이를 변환할 수 있다.
4. `qemu-system-x86_64`로 부팅한다.

```bash
qemu-system-x86_64 -drive file=kubuntu.qcow2,format=qcow2 \
  -drive file=kubuntu-20.04.2-desktop-amd64.iso,media=cdrom,readonly \
  -net nic -net user -m 5172 -vga qxl --enable-kvm -smp 4 \
  -cpu kvm64,+vmx,+vme,+msr,+x2apic,+hypervisor
```

- 옵션 구성은 설치 디스크, 읽기 전용 CD-ROM(ISO), 가상 NIC, RAM, 가상 VGA(X 창으로 전달), KVM 가속, 가상 CPU 코어 4개, 중첩 가상화용 CPU 옵션이다.

---

## 4. 이후 운용

- 설치 후에는 ISO 항목을 빼고 `start_kubuntu.sh` 같은 스크립트로 저장해 `chmod +x` 후 쓴다. ISO는 지워도 된다.
- RAM과 코어 수를 조정해 성능을 맞춘다.
- 같은 방식으로 다른 운영체제의 설치 ISO로도 부팅할 수 있다.

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
