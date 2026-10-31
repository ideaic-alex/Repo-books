# 네트워크 공유와 FUSE 파일 시스템

WSL 2를 쓰면 Windows가 직접 다루지 못하는 파일 시스템과 원격 저장소까지 Windows 쪽에서 접근할 수 있다. 이 문서는 Windows 파일 공유와 FUSE 기반 파일 시스템(SSHFS 등)을 다룬다. 결과물은 Windows 탐색기의 Linux 노드와 `\\wsl$` 경로로 노출된다.

---

## 1. WSL 파일을 Windows에 노출하는 통로

- WSL 2 배포판은 Windows 탐색기 사이드바의 **Linux 노드**에 나타난다.
- 특수 UNC 경로 `\\wsl$`로도 접근한다. 마운트한 파일 시스템도 같은 경로 체계로 보인다.

---

## 2. Windows 파일 공유 (drvfs)

- **drvfs**: Windows가 알고 있는 위치를 WSL 환경으로 전달하는 파일 시스템 유형이다.

### 드라이브 문자로 매핑하는 방법

1. Windows 탐색기에서 네트워크의 서버를 열고 공유를 우클릭해 "네트워크 드라이브 연결"로 `Z:` 등을 지정한다. 필요하면 자격 증명을 입력한다.
2. WSL에서 마운트 지점을 만들고 `drvfs`로 마운트한다.
3. 재시작 후에도 유지하려면 `/etc/fstab`에 항목을 추가한다.

```bash
sudo mkdir /mnt/z; sudo mount -t drvfs Z: /mnt/z
# /etc/fstab
Z: /mnt/z drvfs defaults 0 0
```

### UNC 경로로 직접 마운트하는 방법

- 드라이브 매핑 없이 `\\server\share-name` 형태의 UNC 경로를 바로 `mount`에 줄 수 있다.
- 단점은 Windows의 기본 자격 증명이 사용되고 바꿀 수 없다는 점이다. 다른 자격 증명이 필요하면 드라이브 문자 방식을 써야 한다.
- 이 경우도 `/etc/fstab`에 같은 형식으로 등록하면 재마운트된다.

---

## 3. FUSE 기반 파일 시스템

- **FUSE(Filesystem in User space)**: 파일 시스템 드라이버를 커널이 아니라 일반 프로그램으로 실행하는 방식이다. 커널을 직접 재빌드하지 않고도 FUSE 드라이버가 있는 파일 시스템을 쓸 수 있다.
- **SSHFS**: SSH 연결로 원격 PC의 파일 시스템을 로컬처럼 마운트한다. 대표적인 FUSE 활용 예다.

### SSHFS 마운트 절차

1. `sshfs`를 설치하고 SSH 키를 준비한다.
2. `/etc/fuse.conf`에 `user_allow_other`를 추가해 `allow_root` 옵션을 허용한다.
3. 마운트할 폴더를 실행 사용자 소유로 만든 뒤 `sshfs`로 마운트한다.

```bash
sshfs -o idmap=user,uid=1000,gid=1000,allow_root server:/root/test /mnt/test
```

---

## 4. 효과

- 마운트 시 `allow_root`를 주면 Windows 탐색기의 Linux 노드와 `\\wsl$\<배포판>\<경로>`에서 그 파일이 보인다.
- 그래서 Windows가 기본 지원하지 않는 SSHFS 같은 파일 시스템도 UNC 경로를 열 수 있는 모든 Windows 앱에서 사용 가능하다. 예: 원격 서버의 파일을 `notepad.exe`로 연다.

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
