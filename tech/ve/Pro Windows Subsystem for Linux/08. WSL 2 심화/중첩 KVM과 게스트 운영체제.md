# 중첩 KVM과 게스트 운영체제

직접 만든 커널에 KVM을 모듈로 넣었다면, 이제 모듈을 로드하고 설정해서 중첩 가상화를 켠다. 그러면 KVM이 필요한 minikube(Kubernetes)를 쓸 수 있다. QEMU로는 리눅스뿐 아니라 macOS, Arca Noae, OpenIndiana, Haiku 같은 다른 운영체제도 직접 실행할 수 있다.

---

## 1. kvm_intel 모듈 설정과 로드

- **모듈 옵션 파일**: `/etc/modprobe.d/kvm-nested.conf`에 `kvm-intel` 옵션을 적는다. 중첩 가상화(`nested`)와 속도를 높이는 옵션(`enable_shadow_vmcs`, `enable_apicv`, `ept`)을 켠다.
- **로드**: `sudo modprobe kvm_intel`을 실행한다. 로드하기 전에 `kvm-ok`(cpu-checker 패키지)를 실행하면 `/dev/kvm`이 없다고 알려 준다.
- **오류 힌트**: "Module kvm_intel not found" 오류가 나면 `sudo make modules_install`을 빠뜨린 것이다.
- **확인**: 로드한 뒤에는 `kvm-ok`가 가속을 쓸 수 있다고 알려 준다. 중첩 가상화 지원 여부는 `/sys/module/kvm_intel/parameters/nested` 값으로 확인한다.
- **권한**: 일반 사용자가 쓸 수 있도록 `/dev/kvm`의 접근 권한을 `chmod 666`으로 연다.

```bash
sudo modprobe kvm_intel
cat /sys/module/kvm_intel/parameters/nested
sudo chmod 666 /dev/kvm
```

---

## 2. 모듈 사용 팁

- KVM을 모듈로 빌드했기 때문에, KVM을 쓰려는 WSL을 시작할 때마다 직접 로드해야 한다.
- 설정을 바꿀 때는 `modprobe -r kvm_intel`로 언로드하고, 파일을 수정한 뒤 다시 로드한다.
- 설정이 확정되면 KVM을 커널에 내장해서 다시 빌드할 수 있다. Windows 10 빌드 21286 이상에서는 `modprobe kvm_intel`을 `[boot]` 명령에 넣는 방법도 있다.
- 모듈 이름을 `.wslconfig`의 커널 명령줄에 추가하는 방법도 있다고 언급된다.

---

## 3. QEMU로 Kubuntu 설치하기

QEMU 창은 X로 표시되므로 7장에서 설정한 X 서버나 공식 GUI 지원이 필요하다.

1. `qemu-kvm`과 대용량 다운로드 도구 `aria2`를 설치한다.
2. 설치 ISO의 torrent 파일을 `aria2c`로 받는다. 멀티스레드로 받을 수 있어서 `wget`이나 `curl`보다 빠르다.
3. `qemu-img create`로 qcow2 형식(QEMU 기본 가상 디스크) 20G 디스크를 만든다. `qemu-img`로 QCOW, Hyper-V의 VHDX, VirtualBox의 VMDK 사이의 변환도 할 수 있다.
4. `qemu-system-x86_64`로 부팅한다.

```bash
qemu-system-x86_64 -drive file=kubuntu.qcow2,format=qcow2 \
  -drive file=kubuntu-20.04.2-desktop-amd64.iso,media=cdrom,readonly \
  -net nic -net user -m 5172 -vga qxl --enable-kvm -smp 4 \
  -cpu kvm64,+vmx,+vme,+msr,+x2apic,+hypervisor
```

- 위 명령의 옵션은 순서대로 설치 디스크, 읽기 전용 CD-ROM(ISO), 가상 NIC, RAM, 가상 VGA(X 창으로 전달), KVM 가속, 가상 CPU 코어 4개, 중첩 가상화용 CPU 옵션을 지정한다.

---

## 4. 설치 후 사용

- 설치가 끝나면 명령에서 ISO 항목을 빼고, `start_kubuntu.sh` 같은 스크립트로 저장해 `chmod +x`로 실행 권한을 준 뒤 사용한다. ISO 파일은 지워도 된다.
- RAM과 코어 수를 조정해 성능을 맞춘다.
- 다른 운영체제도 같은 방식으로 설치 ISO를 지정해 부팅할 수 있다.

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
