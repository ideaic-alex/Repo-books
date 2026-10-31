# WSL 2 커널 직접 빌드

Microsoft는 WSL 2용 리눅스 커널을 제공한다. 이 커널에는 장치 지원과 메모리 관리 등 WSL 2에 맞춘 패치가 들어 있다. 기본으로 꺼져 있는 커널 기능이 필요하면 커널을 직접 빌드할 수 있다. 책에서는 KVM 가속을 켜는 예제로 설정 파일 편집과 메뉴 도구 사용법을 함께 익힌다.

---

## 1. 접근 방식 선택

- 서드파티 커널이나 upstream 소스로 직접 만든 커널도 쓸 수 있지만, WSL 2 전용 패치가 빠진다.
- **선택지 1**: Microsoft의 패치를 내가 고른 커널에 옮겨 넣는다.
- **선택지 2**: Microsoft 커널을 필요한 설정으로 다시 빌드한다. 패치를 조정하는 일이 익숙하지 않다면 저자는 이쪽을 권한다.
- 예제 기능인 KVM 게스트 가속을 쓰려면 Windows 10 빌드 20175 이상과 Intel CPU가 필요하다.

---

## 2. 소스 준비

- 소스는 GitHub의 `microsoft/WSL2-Linux-Kernel` 저장소에 있다.
- 전체 커밋 이력은 필요 없으므로 얕은 복제(`--depth 1`)를 쓴다.
- 빌드에 필요한 패키지를 설치하고, Microsoft 기본 설정 파일을 `.config`로 복사해 출발점으로 삼는다. ARM64 기기는 `config-wsl-arm64`를 쓴다.

```bash
git clone --depth 1 https://github.com/microsoft/WSL2-Linux-Kernel
sudo apt -y install build-essential libncurses-dev bison flex libssl-dev libelf-dev
cd WSL2-Linux-Kernel && cp Microsoft/config-wsl .config
```

---

## 3. 설정 변경

설정을 바꾸는 방법은 두 가지다.

- **직접 편집**: `.config`를 nano, VS Code, 메모장 등으로 열어 다음 키를 설정한다.
  - `KVM_GUEST=y`, `CONFIG_KVM=y`, `CONFIG_KVM_INTEL=m`, `CONFIG_VHOST=y`
- **메뉴 도구**: `make menuconfig`를 실행하면 터미널에 메뉴가 열린다. 방향키로 이동하고, 스페이스로 항목 상태를 차례로 바꾸고, 엔터로 하위 메뉴(`--->`)에 들어간다. 하단의 Exit를 고르면 상위 메뉴로 나가며, 최상위에서 나갈 때 저장 여부를 묻는다.
  - "Processor type and features"의 "Linux guest support"에서 "KVM Guest support"를 켠다.
  - "Virtualization"에서 "Kernel-based Virtual Machine (KVM) support"는 내장으로, "KVM for Intel processors support"는 모듈로 켠다.
- **내장(`*`)과 모듈(`M`)**: `*`로 표시한 기능은 커널 본체에 포함된다. `M`으로 표시한 기능은 필요할 때 로드하고 언로드한다. 모듈로 두면 설정을 바꾼 뒤 모듈만 다시 올려 빠르게 시험할 수 있다.

---

## 4. 빌드와 설치

1. `make -j <코어 수>`로 빌드한다. 코어 수를 지정하면 빌드 시간이 크게 줄어든다. `.wslconfig`에 지정한 코어 수를 기준으로 삼아도 된다.
2. 빌드가 끝나면 `arch/x86/boot/bzImage`가 만들어진다.
3. 모듈로 표시한 기능은 `sudo make modules_install`로 빌드하고, 배포판의 `/lib/modules`에 설치한다.
4. `bzImage`를 Windows 파일 시스템으로 복사한다. 사용자 홈 폴더를 권장한다. 경로는 `wslvar USERPROFILE`과 `wslpath`로 만든다.

---

## 5. 직접 만든 커널 지정과 확인

- Windows 사용자 홈 폴더의 `.wslconfig`에서 `[wsl2]` 아래에 `kernel` 경로를 지정한다. 경로는 절대 경로여야 하고, 변수는 쓸 수 없으며, 백슬래시는 두 번씩 써야 한다.
- 중첩 가상화 옵션 `nestedVirtualization=true`도 함께 적는다. 빌드 20175부터는 기본으로 켜져 있으므로 최신 빌드에서는 생략해도 된다.
- `wsl.exe --shutdown`으로 WSL을 종료하고 새 터미널을 열면 새 커널로 "재부팅"된다. `uname -ar`에 나온 빌드 시각으로 적용 여부를 확인한다.

```
[wsl2]
kernel=C:\\Users\\Hayden\\bzImage
nestedVirtualization=true
```

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
