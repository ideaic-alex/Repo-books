# 환경 변수 공유 WSLENV

Windows와 WSL의 환경 변수는 기본적으로 서로 분리되어 있다. `WSLENV`라는 특수 변수를 설정하면 원하는 변수만 두 환경 사이로 넘길 수 있다.

---

## 1. WSLENV의 동작 방식

- **환경 변수(environment variable)**: 실행하는 프로그램에 전달되는 작은 메모리 상 텍스트 항목이다.
- **WSLENV**: 어떤 변수를 경계 너머로 전달할지 지정하는 변수다. Windows와 WSL 사이 경계를 넘을 때마다 참조되므로 언제든 바꿔도 된다.
- 변수 이름을 나열하되 여러 개는 콜론(`:`)으로 구분한다.
- 예: `JAVA_HOME`과 `OneDrive`를 함께 전달하도록 지정할 수 있다.

---

## 2. 경로 변환 플래그

- 변수 이름 뒤에 `/p`를 붙이면 값을 경로로 보고 Windows와 WSL 표기를 자동 변환한다.
- 예를 들어 `JAVA_HOME/p`로 설정하면 Windows에서 `C:\Program Files\...` 형태인 값이 WSL에서는 `/mnt/c/Program Files/...`로 보인다.
- 그래서 Windows에 설치된 도구의 위치를 가리키는 변수를 WSL 스크립트에서 그대로 활용할 수 있다.

```text
WSLENV=JAVA_HOME/p:OneDrive/p
```

---

## 3. 사용 가능한 접미사

| 접미사 | 의미 |
|---|---|
| `/p` | 값을 경로로 취급해 Windows/WSL 표기 간 변환 |
| `/l` | 경로 목록으로 취급(WSL은 콜론, Windows는 세미콜론 구분), 각 경로를 변환 |
| `/u` | Windows에서 WSL로만 전달(반대 방향 전달 안 함) |
| `/w` | WSL에서 Windows로만 전달(반대 방향 전달 안 함) |

- `/u`, `/w`는 `/p`나 `/l`과 조합할 수 있다.
- **/pu**: 경로 변환 대상이며 Windows에서 WSL 방향으로만 전파된다.
- **/lw**: 경로 목록 변환 대상이며 WSL에서 Windows 방향으로만 전파된다.
- 위 조합은 예시이며 가능한 경우의 전부는 아니다.

---

## 4. 활용 포인트

- `wslpath`가 명령 단위의 경로 변환이라면, `WSLENV`의 `/p`는 변수 값 단위의 자동 변환이다.
- 방향을 제한(`/u`, `/w`)하면 한쪽 환경의 값을 다른 쪽이 덮어쓰는 일을 막을 수 있다.

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
