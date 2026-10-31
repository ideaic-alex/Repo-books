# wsl.conf와 자동 마운트

WSL에는 일반 리눅스에 없는 고유 설정이 있고, 배포판마다 따로 적용하는 설정(per-distro)과 기기 전체에 적용하는 전역 설정(global)으로 나뉜다. 배포판별 설정은 각 배포판 안의 `/etc/wsl.conf`에 적으며, 이 문서에서는 이 파일의 성격과 `[automount]` 섹션 중 마운트 위치·fstab·배포판 간 공유·라이브러리 캐시 관련 항목을 정리한다.

---

## 1. wsl.conf의 성격

- **`/etc/wsl.conf`**: WSL이 배포판을 "부팅"할 때 읽는 INI 형식 설정 파일이다. 섹션(`[automount]`, `[network]`, `[interop]`, `[user]`, `[boot]`)별로 키를 나눠 적는다.
- **기본값 제공 여부**: 일부 배포판 게시자는 기본 설정이 든 파일을 함께 배포한다. 없다면 직접 만들어 기본값을 덮어쓰면 된다.
- **적용 범위**: 해당 배포판 하나에만 영향을 준다. 기기 전체 설정은 6장의 `.wslconfig` 몫이다.

---

## 2. Windows 드라이브 자동 마운트

- **활성화(enabled)**: 기본값은 `true`로, C 드라이브 등이 `/mnt/c` 같은 경로에 자동으로 붙어 파일 시스템 상호운용을 제공한다. WSL을 Windows 파일 시스템으로부터 격리하려면 `false`로 둔다.
- **마운트 루트(root)**: 드라이브가 붙는 기준 폴더이며 기본은 `/mnt/`이다. 다른 위치(예: `/windrives/`)를 지정할 수 있으나 해당 폴더가 미리 존재해야 하므로 `sudo mkdir`로 만들어 둔다.

```ini
[automount]
enabled = true
root = /windrives/
```

---

## 3. fstab 처리

- **`mountFsTab`**: 전통적인 리눅스 마운트 설정 파일 `/etc/fstab`을 부팅 때 해석할지 정한다. 기본은 `true`다.
- **활용**: fstab을 쓰면 가상 디스크나 네트워크 파일 공유 같은 고급 마운트를 부팅 시 수행할 수 있다.
- **끄는 경우**: 격리를 강화하거나 고급 마운트 문제를 점검할 때 `false`로 둘 수 있다. 이때도 루트 파일 시스템은 자동으로 마운트되며, fstab 없이 WSL 기본 설정으로 붙는다.
- **세밀한 제어**: `mount` 명령의 다른 플래그에 해당하는 값은 `wsl.conf`의 options에 넣을 수 없고, `/etc/fstab`을 편집해야 한다.

---

## 4. 배포판 간 마운트 공유

- **`crossDistro`**: 켜면(기본 `true`) `/mnt/wsl` 공간이 열리고, 한 배포판이 이 아래에 마운트한 폴더를 다른 모든 배포판이 볼 수 있다.
- **용도**: 배포판끼리 파일을 주고받을 때 유용하다. 예를 들어 Ubuntu에서 폴더를 bind 마운트하면 Fedora Remix에서도 같은 내용이 보인다.
- **끄는 경우**: 기업 환경에서 보안상 배포판을 서로 격리하고 싶을 때 `false`로 둔다.

```bash
sudo mount --bind ~/ubuntufolder /mnt/wsl/sharedfolder
```

---

## 5. ldconfig와 GPU 라이브러리

- **ldconfig 개념(library path cache)**: 라이브러리는 애플리케이션이 공통으로 쓰는 함수 모음이며, 그 위치는 `/etc/ld.so.conf`와 `/etc/ld.so.conf.d/*.conf`에 적힌 경로로 만든 캐시에서 찾는다. 하위 설정 파일은 알파벳순으로 읽힌다.
- **`ld.wsl.conf`**: Windows 10 빌드 20150부터 WSL이 이 파일을 자동 추가해 `/usr/lib/wsl/lib`을 캐시 경로에 넣는다. CUDA, DirectML 등 GPU 연산용 WSL 전용 라이브러리가 여기에 있다.
- **`ldconfig` 키**: 기본 `true`이며 GPU 연산을 쓰려면 켜 두는 것이 일반적이다. 성능 비교(GPU 사용 여부)나 다른 드라이버 대체 목적이면 `false`로 끈다.
- **끈 뒤 후속 작업**: 캐시를 다시 만들도록 `sudo ldconfig`를 실행한다.

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
