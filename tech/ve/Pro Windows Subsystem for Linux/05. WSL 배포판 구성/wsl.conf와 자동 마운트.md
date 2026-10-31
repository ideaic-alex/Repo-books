# wsl.conf와 자동 마운트

WSL에는 일반 리눅스에 없는 고유 설정이 있다. 이 설정은 배포판마다 따로 적용하는 per-distro 설정과 PC 전체에 적용하는 전역(global) 설정으로 나뉜다. 배포판별 설정은 각 배포판 안의 `/etc/wsl.conf`에 적는다. 이 문서에서는 이 파일이 어떤 파일인지 살펴보고, `[automount]` 섹션 중 마운트 위치, fstab, 배포판 간 공유, 라이브러리 캐시와 관련된 항목을 정리한다.

---

## 1. wsl.conf란

- **`/etc/wsl.conf`**: WSL이 배포판을 시작할 때 읽는 INI 형식의 설정 파일이다. `[automount]`, `[network]`, `[interop]`, `[user]`, `[boot]` 섹션별로 키를 나눠 적는다.
- **기본값**: 일부 배포판은 기본 설정이 들어 있는 파일을 함께 배포한다. 파일이 없으면 직접 만들어서 기본값을 덮어쓰면 된다.
- **적용 범위**: 해당 배포판 하나에만 적용된다. PC 전체에 적용하는 설정은 6장에서 다루는 `.wslconfig`로 한다.

---

## 2. Windows 드라이브 자동 마운트

- **활성화(enabled)**: 기본값은 `true`다. C 드라이브 같은 Windows 드라이브가 `/mnt/c` 등의 경로에 자동으로 마운트되어, 리눅스에서 Windows 파일에 바로 접근할 수 있다. WSL을 Windows 파일 시스템과 분리하고 싶으면 `false`로 둔다.
- **마운트 루트(root)**: 드라이브를 마운트할 기준 폴더이며 기본값은 `/mnt/`이다. `/windrives/`처럼 다른 위치를 지정할 수도 있다. 이 폴더는 미리 있어야 하므로 `sudo mkdir`로 만들어 둔다.

```ini
[automount]
enabled = true
root = /windrives/
```

---

## 3. fstab 처리

- **`mountFsTab`**: 리눅스의 전통적인 마운트 설정 파일인 `/etc/fstab`을 시작할 때 읽을지 정한다. 기본값은 `true`다.
- **쓰임새**: fstab을 읽으면 가상 디스크나 네트워크 파일 공유 같은 고급 마운트를 시작할 때 자동으로 수행할 수 있다.
- **끄는 경우**: WSL을 더 확실하게 분리하고 싶거나 고급 마운트에서 생긴 문제를 점검할 때 `false`로 둔다. 이때도 루트 파일 시스템은 자동으로 마운트된다. fstab 없이 WSL의 기본 설정대로 마운트되는 것이다.
- **세부 설정**: `mount` 명령의 다른 플래그에 해당하는 값은 `wsl.conf`의 options에 넣을 수 없다. 이런 값은 `/etc/fstab`을 직접 편집해서 지정한다.

---

## 4. 배포판 간 마운트 공유

- **`crossDistro`**: 켜면(기본값 `true`) `/mnt/wsl` 경로가 열리고, 한 배포판이 이 아래에 마운트한 폴더를 다른 모든 배포판에서도 볼 수 있다.
- **용도**: 배포판끼리 파일을 주고받을 때 쓴다. 예를 들어 Ubuntu에서 폴더를 bind 마운트하면 Fedora Remix에서도 같은 내용이 보인다.
- **끄는 경우**: 기업 환경 등에서 보안을 위해 배포판끼리 분리하고 싶을 때 `false`로 둔다.

```bash
sudo mount --bind ~/ubuntufolder /mnt/wsl/sharedfolder
```

---

## 5. ldconfig와 GPU 라이브러리

- **ldconfig란(library path cache)**: 라이브러리는 여러 애플리케이션이 함께 쓰는 함수 모음이다. 시스템은 `/etc/ld.so.conf`와 `/etc/ld.so.conf.d/*.conf`에 적힌 경로로 캐시를 만들고, 라이브러리를 이 캐시에서 찾는다. `/etc/ld.so.conf.d/` 아래 설정 파일은 알파벳순으로 읽힌다.
- **`ld.wsl.conf`**: Windows 10 빌드 20150부터 WSL이 이 파일을 자동으로 추가해 `/usr/lib/wsl/lib`을 캐시 경로에 넣는다. CUDA, DirectML 같은 GPU 연산용 WSL 전용 라이브러리가 이 경로에 있다.
- **`ldconfig` 키**: 기본값은 `true`이며, GPU 연산을 쓰려면 켜 두는 것이 일반적이다. GPU 사용 여부에 따른 성능을 비교하거나 다른 드라이버로 대체하려는 경우에는 `false`로 끈다.
- **끈 뒤에 할 일**: 캐시를 다시 만들도록 `sudo ldconfig`를 실행한다.

---

## 6. 정리

| 키 | 기본값 | 의미 |
|---|---|---|
| `enabled` | true | Windows 드라이브 자동 마운트 |
| `root` | /mnt/ | 마운트 기준 폴더 |
| `mountFsTab` | true | `/etc/fstab` 처리 |
| `crossDistro` | true | `/mnt/wsl` 배포판 간 공유 |
| `ldconfig` | true | GPU 라이브러리 경로 추가 |

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
