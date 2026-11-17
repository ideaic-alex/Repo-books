# 스킬 해부: 디렉터리 구조와 YAML frontmatter

스킬을 잘 쓰려면 먼저 뼈대를 알아야 한다. 책은 소를 힘이 아니라 구조에 대한 이해로 발라냈다는 포정(庖丁)의 고사를 꺼내, 지식이 어디에 어떻게 놓이는지를 보고 나서야 능숙하게 쓸 수 있다고 말한다. 이 문서는 스킬 폴더의 구성, 이름 규칙, 그리고 SKILL.md 맨 위에 있는 YAML frontmatter(파일 맨 앞 `---` 사이에 적는 설정 영역)의 필드를 다룬다.

frontmatter는 스킬의 "신분증"이다. 필드는 많지만 책은 이를 세 묶음으로 나누어 트리거 방식, 권한 통제, 실행 환경이라는 설계의 세 축에 대응시킨다.

---

## 1. 디렉터리 구조

대표적인 스킬 폴더(책의 예는 api-doc-generator)는 다음과 같다.

```
api-doc-generator/
├── SKILL.md          # 필수. 핵심 뼈대
├── scripts/          # 선택. 실행 스크립트 (예: detect-routes.py)
├── reference/        # 선택. 필요할 때만 읽는 참고 문서
│   ├── openapi-patterns.md
│   └── error-codes.md
└── templates/        # 선택. 출력 서식 (예: endpoint-doc.md)
```

| 구성 요소 | 책의 비유 | 역할 |
|---|---|---|
| SKILL.md | 핵심 뼈대 | 필수 주 파일. 유일한 "방아쇠" |
| scripts/ | 손발 | 스킬이 직접 "행동"하게 하는 실행 스크립트. 예를 들어 코드베이스를 훑어 라우트를 찾는다 |
| reference/ | 기억 은행 | 필요할 때만 읽는 참고 문서. 상주 메모리를 차지하지 않는다 |
| templates/ | 틀 | 출력 형식을 일정하게 만드는 서식 |

## 2. 반드시 지켜야 할 이름 규칙

책은 이 규칙들을 "번거로운 규정처럼 보이지만 경험으로 얻은 오류 방지 장치"라고 부르며 네 가지를 강조한다.

### 2-1. 파일명은 SKILL.md

대문자 그대로여야 한다. skill.md, Skill.md, SKILL.MD는 모두 무효다. Claude의 로더가 파일을 훑을 때 퍼지 검색이 아니라 문자열 정확 일치를 하기 때문이다.

### 2-2. 디렉터리명은 kebab-case

소문자와 하이픈만 쓴다(예: api-doc-generator).

- 최대 64자, 허용 문자는 `[a-z0-9-]`다.
- 공백, 밑줄, 대문자, 앞뒤 하이픈, 연속 하이픈은 허용되지 않는다.
- 이유는 운영체제 차이를 없애기 위해서다. Windows는 대소문자를 구분하지 않고 Linux는 구분한다. 책은 kebab-case를 인터넷 시대의 에스페란토라고 부른다.

### 2-3. 스킬 폴더 안에는 README.md를 두지 않는 것이 좋다

Anthropic은 스킬 디렉터리에 README.md를 두지 말라고 권하며, 사람용 문서는 상위 디렉터리에 두라고 한다. 책은 이것이 엄격한 규칙이 아니라 위생 문제라고 선을 긋는다. 스킬이 활성화되면 SKILL.md 본문만 컨텍스트 윈도에 들어가고, 보조 파일은 SKILL.md가 명시적으로 가리킬 때만 로드된다. 따라서 가리키지 않은 README.md는 컨텍스트를 전혀 쓰지 않는다. 다만 사람용 문서가 없으면 그 문서를 참조하고 싶은 유혹이 사라져 지침 영역이 깔끔하게 유지된다.

### 2-4. 이름에 claude와 anthropic을 피하기

이것도 강제 검증이 아니라 관례다. Claude Code가 실제로 강제하는 것은 식별자가 소문자, 숫자, 하이픈이고, 길이 제한 안이며, 폴더 이름과 일치한다는 점이다. 스킬은 하니스(harness, 모델을 감싸 도구 호출과 실행 환경을 제공하는 실행 틀)가 달라도 옮겨 쓸 수 있는 범용 지식 캡슐 형식이므로, 브랜드 중립적인 이름이 이식성에 유리하다는 취지다.

## 3. YAML frontmatter 필드

책이 보여 주는 전체 예시의 필드를 정리하면 다음과 같다.

| 필드 | 한 줄 설명 | 비고 |
|---|---|---|
| name | 고유 식별자 | 최대 64자. 생략하면 디렉터리 이름 사용 |
| description | 트리거 설명 | 최대 1024자. 생략하면 본문 첫 문단 사용 |
| argument-hint | `/` 메뉴에 보이는 인자 힌트 | 예: "[source directory] [output format]" |
| disable-model-invocation | true면 Claude의 자동 호출 금지 | 기본값 false. 사용자가 `/스킬이름`으로 직접 실행 |
| user-invocable | false면 `/` 메뉴에서 숨김 | 기본값 true. Claude는 여전히 자동 호출 가능 |
| allowed-tools | 도구 허용 목록 | 예: Read, Grep, Glob, Write, Bash(python:*) |
| model | 이 스킬에서 쓸 모델 | 단순 작업은 haiku를 권함 |
| context | 실행 맥락 | fork면 격리된 서브에이전트에서 실행 |
| agent | 서브에이전트 종류 | context가 fork일 때 유효. Explore, Plan, general-purpose, 사용자 정의 에이전트 |
| hooks | 스킬 활성 중에만 유효한 수명 주기 훅(Hooks, 특정 시점에 자동 실행되는 처리 로직) | 예: PreToolUse에서 Bash 입력을 audit.log에 기록 |

참고(노트 작성자): 책의 예시 코드에는 `disallowed-tools` 필드의 예가 없고, 본문에서 이름만 언급된다.

### 3-1. 세 가지 묶음

- 신원 필드(트리거 메커니즘): name, description, argument-hint. 스킬이 무엇인지, 어떻게 부르는지를 Claude와 사용자 양쪽에 알린다. 트리거 논리의 토대다.
- 호출과 도구 필드: disable-model-invocation, user-invocable, allowed-tools, disallowed-tools, model.
- 실행 필드(런타임 환경): context, agent, hooks. 어디에서 실행되고 실행 중에 무슨 일이 일어나는지를 정한다. 격리 환경, 서브에이전트 종류, 수명 주기 훅을 설정한다.

### 3-2. 이름이 약속하는 것보다 적게 해 주는 필드들

호출과 도구 필드에 대해 책은 "이름이 실제보다 많은 것을 약속한다"며 정확히 읽으라고 경고한다.

- disable-model-invocation: true는 Claude의 자동 호출을 막아 사용자 트리거만 남긴다.
- user-invocable: false는 슬래시 명령 메뉴에서 숨길 뿐이다. 가시성 스위치이지 보안 경계가 아니다.
- allowed-tools는 스킬이 활성인 동안 도구를 허용하고 자동 승인한다. 제한하는 것이 아니다. Claude의 손에서 도구를 빼앗는 필드는 disallowed-tools다.
- model은 현재 턴의 나머지 동안 모델을 바꾼다. 권한 통제가 아니라 라우팅 결정이다.

진짜 경계는 권한 설정과 훅(5장에서 다룬다)에서 나온다.

참고(노트 작성자): 5장 뒤쪽에서 allowed-tools를 "최소 권한" 도구로 설명하는 대목이 있다. 이는 이 경고와 긴장 관계에 있으므로, 두 서술을 함께 읽고 실제 동작은 사용하는 Claude Code 버전에서 확인하는 편이 안전하다.

### 3-3. 두 호출 스위치의 구분

Kage의 메모는 disable-model-invocation과 user-invocable을 서로 직교하는 두 방향의 통제로 설명한다.

| 설정 | 의미 | 어울리는 스킬 |
|---|---|---|
| disable-model-invocation: true | Claude는 자동 실행 불가, 사용자가 `/스킬이름`으로만 실행 | 부작용이 크거나 위험한 작업. 예: `/commit`, `/deploy` |
| user-invocable: false | `/` 메뉴에서 안 보임, 사용자 수동 실행 불가, Claude는 자동 호출 가능 | 순수 정보성, 보조 참조 스킬 |
| 둘 다 기본값 | Claude와 사용자 모두 호출 가능 | 일반적인 스킬 |

## 4. 핵심 정리

- 필수 파일은 SKILL.md뿐이고, scripts/, reference/, templates/는 선택이다.
- 디렉터리 이름은 `[a-z0-9-]`, 64자 이하의 kebab-case이며 폴더 이름과 name이 일치해야 한다.
- README.md와 브랜드명 회피는 강제가 아닌 권장 관례다.
- frontmatter는 신원, 호출과 도구, 실행의 세 묶음으로 읽는다.
- user-invocable: false는 숨기기일 뿐이며, 보안 경계는 권한 설정과 훅이 맡는다.

<br>
<br>
<br>

[The Claude Code Operating Model](../)
