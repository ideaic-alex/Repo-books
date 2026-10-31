# 6장. WSL 2 구성 (Configuring WSL 2)

WSL 2는 가벼운 가상 머신으로 동작하기 때문에 메모리나 프로세서 수 같은 자원을 지정하는 설정이 따로 있다. 이런 설정은 Windows 사용자 홈의 `.wslconfig`에 적으며, 모든 WSL 2 배포판에 전역으로 적용된다. 이 장은 커널, 자원, 네트워크, 가상화, 디버깅 설정과 레지스트리 설정을 살펴본다.

---

## 1. 핵심 요점

- `.wslconfig`의 `[wsl2]` 섹션은 전역 설정이며, 파일이 없으면 기본값이 적용된다.
- 공식 WSL 2 커널을 `kernel=`로 교체할 수 있고, `kernelCommandLine=`으로 커널 매개변수를 더할 수 있다.
- `processors`, `memory`, `swap`, `swapfile`로 CPU, RAM, 스왑을 조절하며 기본 메모리 상한은 RAM의 50%와 8GB 중 작은 값이다.
- `pageReporting`은 사용하지 않는 메모리를 Windows에 돌려주는 기능이다.
- `localhostforwarding`, `nestedVirtualization`, `debugConsole`로 네트워크, 중첩 가상화, 커널 로그 확인을 설정한다.
- 변경 사항은 `wsl.exe --shutdown` 후에 반영되며, 파일은 CRLF 줄바꿈이어야 한다.
- 레지스트리의 `Lxss` 키에서 일부 설정을 볼 수 있지만 마지막 수단으로만 쓴다.

---

## 2. 섹션 문서

- [.wslconfig와 커널 설정](.wslconfig%EC%99%80%20%EC%BB%A4%EB%84%90%20%EC%84%A4%EC%A0%95.md)
- [프로세서 메모리 스왑 설정](%ED%94%84%EB%A1%9C%EC%84%B8%EC%84%9C%20%EB%A9%94%EB%AA%A8%EB%A6%AC%20%EC%8A%A4%EC%99%91%20%EC%84%A4%EC%A0%95.md)
- [네트워크 가상화 디버그와 레지스트리](%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%EA%B0%80%EC%83%81%ED%99%94%20%EB%94%94%EB%B2%84%EA%B7%B8%EC%99%80%20%EB%A0%88%EC%A7%80%EC%8A%A4%ED%8A%B8%EB%A6%AC.md)

<br>
<br>
<br>

[Pro Windows Subsystem for Linux](../)
