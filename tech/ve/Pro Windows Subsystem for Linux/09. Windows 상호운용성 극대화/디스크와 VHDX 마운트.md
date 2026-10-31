# 디스크와 VHDX 마운트

WSL 2에서는 `wsl.exe --mount`로 물리 디스크, 파티션, 가상 디스크 이미지를 배포판에 붙일 수 있다. 이 기능으로 Windows가 원래 인식하지 못하는 네이티브 Linux 파일 시스템도 Windows에서 쓸 수 있다. 다만 책은 강력한 기능이므로 익숙하지 않다면 시도하지 말라고 경고한다.

---

## 1. 지원 파일 시스템 확인

- Linux는 다양한 파일 시스템을 다룬다. 흔한 것으로는 ext2/3/4, XFS, btrfs가 있다.
- 지금 커널이 지원하는 목록은 WSL 2 안에서 `cat /proc/filesystems`로 확인한다.

---

## 2. 물리 디스크/파티션 마운트

- 네이티브 Linux 파티션이 있는 디스크를 `--mount`로 WSL에 붙인다.
- 제약: Windows가 그 디스크를 사용 중이면 안 된다. 예를 들어 Windows 부팅 장치에 있는 보조 파티션은 대상이 아니다.
- 먼저 디스크의 Windows 내부 경로(DeviceID)를 알아야 한다. 명령 프롬프트나 PowerShell에서 `wmic diskdrive list brief`로 확인한다. 형식은 `\\.\PHYSICALDRIVEn`(n은 0부터 시작)이다.

```powershell
wsl.exe --mount \\.\PHYSICALDRIVE1 --partition 2
```

---

## 3. 가상 디스크 이미지(VHDX) 마운트

- `.vhdx`는 Windows의 Hyper-V 가상화에서 쓰는 가상 디스크 이미지다. WSL 2도 이를 WSL용으로 변형해서 쓴다.
- 절차는 물리 디스크와 거의 같다. 다른 점은, 디스크를 물리적으로 연결하는 대신 PowerShell로 `.vhdx`를 먼저 Windows에 마운트한다는 것이다.
- `Mount-VHD`와 `Get-Disk`를 함께 쓰면 마운트하면서 `\\.\PhysicalDrive<번호>` 이름을 출력해 준다. 이 이름을 `wsl.exe --mount`에 쓴다.

```powershell
Write-Output \\.\PhysicalDrive$((Mount-VHD -Path <pathToVHDX> -PassThru | Get-Disk).Number)
```

---

## 4. 마운트 옵션

- **`-t <파일 시스템>`**: 파일 시스템이 자동으로 감지되지 않을 때 지정한다(예: `-t ext4`).
- **`-o <옵션>`**: Linux 마운트 옵션을 넘긴다(예: `noatime,uid=1000,gid=1000`).
- **`--bare`**: 파티션이 아니라 장치 전체를 그대로 붙인다. 이때는 `--partition`, `-t`, `-o`를 함께 쓸 수 없다.

```powershell
wsl.exe --mount \\.\PHYSICALDRIVE1 --partition 2 -t ext4 -o noatime
wsl.exe --mount \\.\PHYSICALDRIVE1 --bare
```

---

## 5. 접근과 해제

- 마운트한 파일 시스템은 탐색기의 Linux 노드와 `\\wsl$` UNC 경로로 Windows에서 접근한다.
- 다 쓰고 나면 `--unmount`로 분리한다. 디스크 경로를 생략하면 모든 디스크와 이미지가 한꺼번에 해제된다.

```powershell
wsl.exe --unmount \\.\PHYSICALDRIVE1
wsl.exe --unmount
```

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
