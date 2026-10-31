# WSL 활성화 방법

WSL은 Windows에 기본으로 켜져 있지 않으므로 GUI나 명령줄로 직접 켜야 한다. Home, Professional, Enterprise, Server 등 모든 에디션(SKU)에서 가능하며, 숙련도와 환경에 맞춰 방법을 고르면 된다.

---

## 1. 방법 선택 기준

- 입문자는 GUI, 숙련자는 PowerShell, 다수의 PC를 관리하는 시스템 관리자는 DISM이 어울린다.
- WSL 1은 "Windows Subsystem for Linux" 기능만, WSL 2는 여기에 "Virtual Machine Platform"까지 켜야 한다.
- 기능을 켠 뒤에는 재시작이 필요하다.

---

## 2. GUI (프로그램 및 기능)

- 시작 메뉴에서 "Windows 기능 켜기/끄기"를 열어 "Windows Subsystem for Linux"를 체크하고, WSL 2를 쓰려면 "Virtual Machine Platform"도 체크한다.
- **단점**: Windows 10 1909 이후에서 WSL 2를 켜도 기본 버전은 WSL 1로 남는다. 관리자 PowerShell에서 따로 지정해야 한다.

```powershell
wsl.exe --set-default-version 2
```

---

## 3. PowerShell

- 관리자 권한 PowerShell에서 `Enable-WindowsOptionalFeature`를 사용한다.
- WSL 1은 `Microsoft-Windows-Subsystem-Linux`, WSL 2는 `VirtualMachinePlatform` 기능을 켠다(둘 다 `-Online -NoRestart`).
- 이후 `Restart-Computer`로 재시작하고, WSL 2를 기본으로 하려면 위의 `--set-default-version 2`를 실행한다.

```powershell
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux -NoRestart
Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -NoRestart
```

---

## 4. DISM

- **DISM(Deployment Image Servicing and Management)**: 관리자에게 익숙한 배포 이미지 관리 도구.
- 같은 두 기능을 `/online /enable-feature /featurename:<기능> /all /norestart` 형식으로 켠다.
- 재시작과 기본 버전 지정 단계는 PowerShell 방식과 같다.

```powershell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

---

## 5. wsl.exe --install

- Build 2020에서 발표된 방식으로, 대상 Windows 10 버전 전반에서 WSL을 한 번에 켜 준다.
- 기본으로 WSL 2를 활성화하고, WSL 2 커널을 업데이트하며, 대상 버전에서는 GUI 지원도 설치한다. 지원 중인 기존 서비스 채널로 백포트될 예정이다.
- 빌드 20211 이상에서는 스토어 앱 없이 배포판을 바로 설치할 수 있다(다음 문서 참고).

```powershell
wsl.exe --install
```

---

## 6. 이미지와 Hyper-V 게스트

- **이미지에 포함**: DISM으로 Windows 이미지에 WSL을 켜고, `.appx`로 배포판을 사이드로드한 뒤 이미지를 일반화(generalize)해 설치 가능한 파생 이미지를 만든다.
- **Hyper-V 게스트**: Windows 10 게스트에서도 WSL을 쓸 수 있어, Dev와 Beta 채널의 새 기능을 운영 배포 전에 시험하기 좋다.
- Hyper-V에는 Windows 10 Pro, Enterprise, Education과 VT-x가 있는 인텔 프로세서가 필요하고, BIOS/EFI에서 가상화 확장을 먼저 켜야 한다. AMD의 중첩 가상화(nested virtualization)는 초기 지원 발표 단계였다.
- 게스트에 가상화 확장을 노출하려면 호스트의 관리자 PowerShell에서 다음을 실행한다. 게스트가 시작되지 않거나 기능이 비활성이면 BIOS 설정과 VM 이름을 다시 확인한다.

```powershell
Set-VMProcessor -VMName "VM이름" -ExposeVirtualizationExtensions $true
```

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
