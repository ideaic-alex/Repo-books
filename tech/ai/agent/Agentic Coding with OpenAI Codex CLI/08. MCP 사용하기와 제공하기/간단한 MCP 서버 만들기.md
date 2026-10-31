# 간단한 MCP 서버 만들기

MCP 서버는 생각보다 만들기 쉽다. Python SDK의 FastMCP 데코레이터 API를 쓰면 함수 몇 개로 서버가 된다. 이 문서는 최소 서버 예제, Codex CLI에 연결하는 두 가지 설정 방식, 연결 전에 MCP Inspector로 따로 테스트하는 방법을 정리한다.

---

## 1. 최소 서버 작성

SDK는 `pip install "mcp[cli]"`로 설치한다. 단어 수를 세는 도구 하나를 가진 서버는 다음과 같다.

```python
# server.py: a minimal MCP server using FastMCP
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("example-server")

@mcp.tool()
def word_count(text: str) -> int:
    """Count words in the given text."""
    return len(text.split())

if __name__ == "__main__":
    mcp.run()
```

FastMCP는 함수 시그니처를 도구 스키마로 자동 변환한다.

- `text: str`는 필수 문자열 입력이 된다.
- 독스트링(docstring)은 도구 설명이 된다.
- 반환 타입은 도구의 출력 타입으로 대응된다.

내부에서는 저수준 Server API가 쓰는 것과 같은 JSON-RPC 프로토콜로 통신한다. FastMCP는 새 서버를 만들 때 권장되는 진입점이다. 도구 설명은 컨텍스트 비용으로 이어지므로, 독스트링도 짧게 쓰는 편이 좋다는 점은 앞 문서에서 다룬 그대로다.

## 2. Codex CLI에 연결하기

~/.codex/config.toml에 `[mcp_servers.<name>]` 블록을 추가한다. 특정 프로필에서만 쓰고 싶다면 프로필 파일 `~/.codex/<name>.config.toml` 안에 같은 블록을 둔다.

```toml
[mcp_servers.wordcount]
enabled = true
command = "python"
args = ["/absolute/path/to/server.py"]
```

args에는 절대 경로를 쓴다. 그래야 Codex를 어느 디렉터리에서 시작해도 서버가 뜬다. 대안은 cwd를 지정하고 args를 상대 경로로 두는 방식이다.

```toml
[mcp_servers.wordcount]
enabled = true
command = "python"
args = ["server.py"]
cwd = "/path/to/server/directory"
```

더 큰 서버도 같은 패턴으로 키운다. `@mcp.tool()`을 붙인 함수를 더 추가하고, 각 도구의 입력과 반환 타입을 명시해 두면 된다. 도구 발견, 호출, 결과 변환은 MCP 프로토콜이 알아서 처리한다.

## 3. 서버를 따로 테스트하기

Codex CLI에 붙이기 전에 서버를 단독으로 먼저 테스트한다.

```bash
# If you installed the SDK into the current environment with pip
mcp dev server.py
# Or, if you run Python tools through uv
uv run mcp dev server.py
```

이 명령은 MCP Inspector를 띄운다. Inspector는 시각적인 디버깅 도구로, FastMCP 서버를 시작하고 프로토콜 핸드셰이크를 수행한 뒤 도구 목록을 보고 직접 호출해 볼 수 있게 해 준다. word_count가 필수 text 인자와 함께 목록에 나타나는지 확인하고, 예시 문장으로 호출해 본 다음 Codex CLI에 연결한다.

## 4. 만들 때의 체크 포인트

- 도구마다 입력 타입과 반환 타입을 명시한다.
- 도구 설명(description)은 짧게 쓴다.
- 쓰기가 가능한 도구에는 정직한 어노테이션을 단다. 의심스러우면 파괴적이라고 표시하는 쪽이 안전하다.
- 서버를 실행하는 command와 args가 PATH와 경로 기준으로 어디서든 동작하는지 확인한다.

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
