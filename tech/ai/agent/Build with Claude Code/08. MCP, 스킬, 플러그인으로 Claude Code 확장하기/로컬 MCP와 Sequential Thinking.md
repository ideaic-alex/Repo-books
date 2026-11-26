# 로컬 MCP와 Sequential Thinking

앞 문서에서는 이미 인터넷에 준비된 MCP 서버(Notion)에 접속했다. 이번에는 내 컴퓨터에서 직접 MCP 서버 프로그램을 돌리는 방법을 배운다. 대상은 Anthropic이 만들어 배포하는 공식 MCP인 Sequential Thinking이다. 문제를 작은 단위로 쪼개 차례대로 추론하게 돕는 도구다.

비유하면 원격 MCP는 이미 차려진 식당에 가서 먹는 것이고, 로컬 MCP는 내 부엌에서 직접 요리하는 것이다. 식당은 빠르게 시작할 수 있고 부엌은 준비가 더 필요하지만 인터넷 없이도 되고 남에게 보이지 않는다.

---

## 1. 원격 MCP와 로컬 MCP

MCP 서버는 연결 방식에 따라 두 종류다. 로컬 MCP는 MCP 서버 프로그램을 내 컴퓨터에서 직접 실행한다. 원격 MCP는 인터넷 너머의 외부 서버에서 그 프로그램이 돈다. 두 방식 모두 Claude Code를 외부 시스템과 잇지만 연결 위치와 설정 과정이 다르다.

| 구분 | 원격 MCP | 로컬 MCP |
|---|---|---|
| 접속 대상 | 인터넷의 외부 서버 주소(URL) | 내 컴퓨터에서 실행하는 명령 |
| 설정 난이도 | 쉽다. 명령 한 줄이면 바로 연결 | 실행 명령을 직접 지정해야 해서 조금 더 번거롭다 |
| 장점과 단점 | 여러 사람과 공유하기 편하다. 인터넷이 필요하다 | 인터넷 없이 되고 응답이 빠르며 사생활 보호에 좋다 |

원격 MCP는 대개 로그인이나 인증으로 내 계정과 연결한다. Notion을 설치한 명령이 원격 방식이었다.

```bash
claude mcp add --transport http [사용할 이름] [서버 URL]
```

로컬 MCP는 URL 대신 실행할 명령을 적는다. 이때 `--` 기호가 Claude Code 옵션과 MCP 실행 명령을 갈라 준다.

```bash
claude mcp add [사용할 이름] [옵션] -- [MCP 실행 명령]
```

어느 쪽을 고를지는 상황에 따른다. 빠르게 시작하고 다른 사람과 협업해야 하면 원격이 낫다. 네트워크가 불안하거나 개인 환경에서 안전하게 작업하려면 로컬이 맞다. 모든 MCP가 두 방식을 다 지원하는 것은 아니다. 하나만 있으면 환경에 맞춰 그것을 쓴다.

## 2. 로컬 설치 명령 뜯어보기

설치할 MCP는 Sequential Thinking이다. 명령 한 줄에 필요한 정보가 다 들어 있다.

```bash
claude mcp add sequential-thinking -s local -- npx -y @modelcontextprotocol/server-sequential-thinking@latest
```

부분별 뜻은 다음과 같다.

- `sequential-thinking`: Claude Code 안에서 이 MCP를 부르는 이름이다.
- `-s local`: MCP가 적용되는 범위(scope)다. `-s`는 `--scope`의 줄임이다. `local`은 현재 프로젝트에만 적용한다. `project`로 하면 프로젝트 팀원과 공유되고, `user`로 하면 내 계정의 모든 프로젝트에서 쓴다. 기본값이 `local`이라 `-s`를 생략해도 같다.
- `--`: 구분 기호다. 앞에는 Claude Code용 옵션, 뒤에는 MCP 서버 실행 명령이 온다.
- `npx -y`: Node.js 패키지를 실행한다. `-y`는 패키지가 없으면 설치를 자동 승인해서 'Ok to proceed? (y)' 물음을 건너뛴다.
- `@modelcontextprotocol/server-sequential-thinking@latest`: 불러올 MCP 패키지 이름이다. `@조직/패키지@버전` 구조이고, 여기서는 공식 MCP 팀이 배포한 패키지의 최신 버전(latest)을 뜻한다. 개인이 만든 서버는 `@조직` 부분을 빼도 된다. `@버전`도 생략할 수 있고, `@2.0`처럼 특정 버전을 지정할 수도 있다.

로컬 MCP와 앞으로 쓸 여러 도구를 편하게 설치하려면 먼저 Node.js를 깔아 두는 것이 좋다. Node.js는 여러 프로그램을 설치하고 실행하게 돕는 기본 도구이며, 공식 사이트(https://nodejs.org)에서 운영체제에 맞는 설치 파일을 받는다.

## 3. 인증이란 무엇인가

외부 서비스를 MCP에 연결하면 인증(Authentication)이 필요하다. 연결하려는 사람이 정말 권한 있는 사용자인지 확인하는 절차다.

MCP 서버는 여러 사용자의 데이터를 관리한다. 누가 요청하는지 모르면 다른 사람의 정보나 파일에 잘못 접근할 수 있다. 그래서 요청자가 진짜 그 사용자임을 증명하게 한다. 특히 원격 MCP는 인터넷으로 통신하므로 중간에 데이터가 새어 나갈 위험이 있다. 인증을 거치면 서버와 클라이언트가 암호화된 연결로 안전하게 데이터를 주고받는다.

## 4. Sequential Thinking MCP 설치와 사용

설치 순서는 간단하다.

1. 위의 설치 명령을 실행한다.
2. 설치가 끝나면 `claude mcp list`로 설치된 MCP 목록을 확인한다. 방금 넣은 MCP가 `sequential-thinking`이라는 이름으로 보이면 성공이다.

## 5. 성능 비교 실습

설치한 MCP가 일반 추론과 얼마나 다른지 비교해 본다. 목표는 '웹 포트폴리오 사이트의 방문자 체류 시간을 두 배로 늘리는 전략 세우기'다.

방법은 같은 주제를 두 번 시키는 것이다. 먼저 일반 방식으로 체류 시간을 늘리는 방법을 묻고 Notion에 `Increase Dwell Time`이라는 제목으로 저장한다. 다음에 Sequential Thinking MCP로 같은 주제를 더 체계적이고 단계적으로 시키고, 비교를 위해 `Increase Dwell Time – Systematic Structure`라는 제목으로 저장한다. 프롬프트는 두 문서를 한 번에 요청한다.

```text
I want to double the time visitors spend on my web portfolio. Please create two documents:
1. Devise a way to achieve this goal and use the Notion MCP to save it as "Increase Dwell Time".
2. Use the Sequential Thinking MCP to systematically devise a way to achieve this goal, and then use the Notion MCP to save it as "Increase Dwell Time – Systematic Structure".
```

잠시 기다리면 완료 메시지와 함께 두 Notion 문서의 URL이 나온다. 파란 밑줄 링크를 Ctrl 키와 함께 누르거나 Notion을 직접 열어 확인한다. 이 실습에는 Notion MCP와 Sequential Thinking MCP가 함께 쓰인다는 점도 눈여겨보자. MCP는 이렇게 여러 개를 조합할 수 있다.

## 6. 결과 해석

두 문서의 분량을 비교하면 차이가 뚜렷하다. 일반 추론 문서는 85줄이었고, 순차 추론 문서는 222줄이었다. 순차 추론 문서는 목차도 더 자세해서 목표, 구현 방법, 실행 로드맵, 지표, 위험 대응 같은 절을 담았다.

원서의 결론은 이렇다. Sequential Thinking MCP는 프로젝트를 단계별로 계획해 체계적인 프롬프트나 PRD(제품 요구사항 문서)를 만들 때 쓸모가 있다. 여러 요인이 얽힌 복잡한 문제를 구조적으로 분석하고 정리해야 할 때 특히 강하다.

참고(노트 작성자): 줄 수는 한 번의 실행 결과이므로 매번 같지는 않다. 이 비교는 '단계적으로 쪼개 생각하면 결과물이 더 구조적이다'는 경향을 보여 주는 예로 읽으면 된다.

## 7. 핵심 정리와 복습 문제

책은 이 부분을 여섯 개 키워드로 요약한다.

- MCP는 AI 모델이 외부 데이터, 도구, 서비스와 연결할 때 쓰는 표준 통신 규약이다.
- 클라이언트-서버 모델은 클라이언트가 요청하고 서버가 응답하는 네트워크 구조다.
- 로컬 MCP는 MCP 중개 프로그램을 내 컴퓨터에서 직접 돌리는 방식이다.
- 원격 MCP는 중개 프로그램까지 인터넷의 외부 서버에서 도는 방식이다.
- 인증은 연결하려는 사람이 정말 권한 있는 사용자인지 확인하는 과정이다.
- 이중 하이픈(`--`)은 두 글자 이상 옵션 이름을 나타내거나 명령과 옵션을 가르는 기호다. 위치와 띄어쓰기에 따라 뜻이 달라지니 헷갈리지 않도록 주의한다.

복습 문제는 세 개다. 정답은 부록 장에 있다.

1. MCP와 API의 차이를 가장 알맞게 설명한 것을 고르시오. 보기는 (1) API는 특정 기능을 요청하는 방법이고 MCP는 AI가 외부 시스템과 직접 소통하게 하는 규약이다, (2) MCP가 API보다 빠르다, (3) API는 유료이고 MCP는 무료다, (4) MCP는 Claude Code에서만 쓸 수 있다.
2. 로컬 MCP 서버 설치 명령에서 `--` 구분 기호의 역할로 옳은 것을 고르시오. 보기는 (1) 주석 표시 기호, (2) Claude Code 옵션과 MCP 서버 실행 명령을 가르는 기호, (3) 버전 정보 표시, (4) 오류 처리 구분자다.
3. Sequential Thinking MCP를 쓸 때와 일반 추론의 차이를 서술하시오.

<br>
<br>
<br>

[Build with Claude Code](../)
