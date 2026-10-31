# WSL 활성화 방법

WSL은 Windows에서 기본으로 켜져 있지 않으므로 GUI나 명령줄로 직접 켜야 한다. Home, Professional, Enterprise, Server 등 모든 에디션(SKU)에서 켤 수 있고, 숙련도와 환경에 맞는 방법을 고르면 된다.

---

## 1. 방법 선택 기준

- 입문자는 GUI, 숙련자는 PowerShell, 많은 PC를 관리하는 시스템 관리자는 DISM이 알맞다.
- WSL 1은 "Windows Subsystem for Linux" 기능만 켜면 된다. WSL 2는 여기에 "Virtual Machine Platform"까지 켜야 한다.
- 기능을 켠 뒤에는 PC를 재시작해야 한다.

---

## 2. GUI (프로그램 및 기능)

- 시작 메뉴에서 "Windows 기능 켜기/끄기"를 열고 "Windows Subsystem for Linux"를 체크한다. WSL 2를 쓰려면 "Virtual Machine Platform"도 체크한다.
- **단점**: Windows 10 1909 이후 버전에서 이 방법으로 WSL 2를 켜도 기본 버전은 WSL 1로 남는다. 관리자 권한 PowerShell에서 기본 버전을 따로 지정해야 한다.

```powershell
wsl.exe --set-default-version 2
```

---

## 3. PowerShell

- 관리자 권한 PowerShell에서 `Enable-WindowsOptionalFeature`를 실행한다.
- WSL 1은 `Microsoft-Windows-Subsystem-Linux` 기능을, WSL 2는 `VirtualMachinePlatform` 기능을 켠다(둘 다 `-Online -NoRestart` 옵션을 쓴다).
- 그런 다음 `Restart-Computer`로 재시작한다. WSL 2를 기본 버전으로 쓰려면 위에서 본 `--set-default-version 2`를 실행한다.

```powershell
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux -NoRestart
Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -NoRestart
```

---

## 4. DISM

- **DISM(Deployment Image Servicing and Management)**: 시스템 관리자에게 익숙한 배포 이미지 관리 도구다.
- 같은 두 기능을 `/online /enable-feature /featurename:<기능> /all /norestart` 형식으로 켠다.
- 재시작과 기본 버전 지정 단계는 PowerShell 방식과 같다.

```powershell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

---

## 5. wsl.exe --install

- Build 2020 행사에서 발표된 방식으로, 대상이 되는 Windows 10 버전 전반에서 WSL을 한 번에 켜 준다.
- 기본으로 WSL 2를 켜고, WSL 2 커널을 업데이트하며, 대상 버전에서는 GUI 지원도 함께 설치한다. 이 방식은 현재 지원 중인 기존 Windows 버전(서비스 채널)에도 적용(백포트)될 예정이다.
- 빌드 20211 이상에서는 스토어 앱 없이도 배포판을 바로 설치할 수 있다(다음 문서 참고).

```powershell
wsl.exe --install
```

---

## 6. 이미지와 Hyper-V 게스트

- **이미지에 포함**: DISM으로 Windows 이미지에 WSL을 켜고, `.appx`로 배포판을 사이드로드한다. 그 뒤 이미지를 일반화(generalize)하면, 설치할 수 있는 파생 이미지를 만들 수 있다.
- **Hyper-V 게스트**: Windows 10 게스트(Hyper-V 안에서 돌리는 가상 머신)에서도 WSL을 쓸 수 있다. 그래서 Dev와 Beta 채널의 새 기능을 실제 환경에 배포하기 전에 시험해 보기에 좋다.
- Hyper-V를 쓰려면 Windows 10 Pro, Enterprise, Education과 VT-x를 지원하는 인텔 프로세서가 필요하고, BIOS/EFI에서 가상화 확장을 먼저 켜야 한다. AMD의 중첩 가상화(nested virtualization)는 집필 당시 지원을 막 발표한 단계였다.
- 게스트에서 가상화 확장을 쓰게 하려면 호스트의 관리자 PowerShell에서 다음 명령을 실행한다. 게스트가 시작되지 않거나 기능이 꺼져 있으면 BIOS 설정과 가상 머신 이름을 다시 확인한다.

```powershell
Set-VMProcessor -VMName "VM이름" -ExposeVirtualizationExtensions $true
```

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
