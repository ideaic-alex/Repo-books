# openai.yaml과 스킬 만들어 배포하기

SKILL.md만으로는 Codex 전용 설정, 즉 호출 정책과 MCP 의존성을 표현할 수 없다. 이 문서는 그 역할을 맡는 `agents/openai.yaml`을 먼저 설명하고, 이어서 스킬을 검증하고 시험하고 공개하는 과정을 따라간다. 그다음 스킬을 얼마나 크게 만들지 정하는 5단계 기준, 그리고 먼저 손으로 해 보고 나중에 스킬로 옮기는 작성 순서를 다룬다.

---

## 1. agents/openai.yaml

이 파일은 선택 사항이며, UI 표시, 호출 정책, MCP 서버 의존성을 설정한다. 원서의 예시는 대략 이렇게 생겼다.

```yaml
interface:
  display_name: "Staging Deploy"
  short_description: "Deploy containerised services to the staging environment"
  brand_color: "#FF9900"
  default_prompt: "Deploy the current service to staging"
policy:
  allow_implicit_invocation: false
dependencies:
  tools:
    - type: "mcp"
      value: "awsInfrastructure"
      description: "AWS infrastructure MCP server for ECS and ECR access"
      transport: "streamable_http"
      url: "https://mcp.internal.example.com/aws"
```

`allow_implicit_invocation`의 기본값은 `true`다. 프로덕션 인프라를 건드리거나, 상태를 바꾸는 테스트를 돌리거나, 파일을 지우거나, 과금에 영향을 주는 API를 부르는 스킬에는 `false`로 둔다. 어쩌다 프롬프트에 'deploy'라는 단어가 들어갔다고 배포 워크플로가 조용히 시작되는 일은 없어야 한다. 영향이 큰 스킬에는 항상 `allow_implicit_invocation: false`를 건다.

`dependencies.tools` 배열은 스킬과 MCP를 잇는 다리다. 스킬은 워크플로를 어떻게 실행하는지를 담고, MCP 서버는 외부 시스템에 대한 실시간 접근을 제공한다. Codex CLI가 MCP 의존성이 있는 스킬을 불러올 때 설치되지 않은 서버가 있으면 사용자에게 설치할지 묻는다.

## 2. 로컬 검증

Codex에서 시험하기 전에 참조 검증기를 돌린다. `skills-ref`는 사양 저장소에 들어 있는 Python 도구이며 소스에서 설치한다.

```
git clone https://github.com/agentskills/agentskills.git
cd agentskills/skills-ref
pip install -e .
skills-ref validate ~/code/your-repo/.agents/skills/deploy-to-staging/
```

uv를 쓴다면 `pip install -e .` 대신 `uv sync`를 써도 된다. 검증기는 frontmatter 제약을 확인하고, name이 디렉터리 이름과 일치하는지 보고, 줄 단위로 오류를 알려 준다.

## 3. Codex에서 시험

스킬이 들어 있는 저장소에서 Codex CLI 세션을 연다. description에 쓴 동의어를 넣은 프롬프트를 입력해 스킬이 활성화되는지 확인한다. 그다음 `allow_implicit_invocation: false`가 암묵적 활성화를 실제로 막는지도 확인한다.

## 4. 공개와 공유

agentskills.io는 사양 문서와 클라이언트 디렉터리일 뿐 관리형 레지스트리가 아니다. 눌러서 스킬을 이름 하나로 설치되게 만들어 주는 "게시" 버튼은 없다. 다른 오픈소스 산출물과 똑같이, 공개 Git 저장소에 올리고 URL을 알리는 방식으로 배포한다.

1. 스킬 디렉터리를 공개 GitHub 저장소에 올린다. 관례적인 경로는 저장소 루트의 `skills/<skill-name>/`이다.
2. 스킬 디렉터리에 README.md를 넣는다. 짧은 설명, 전제 조건, 호출 예시 하나를 적는다.
3. 원하면 agentskills.io나 skills.sh 같은 커뮤니티 카탈로그에 등록한다. 둘 다 공개 저장소의 스킬을 색인해 준다.

독자가 설치하는 방법은 세 가지이고, 배포 채널에 맞는 것을 고르면 된다.

```
# Git URL에서 직접: 어떤 호스트든 가능
$skill-installer install https://github.com/<owner>/<repo>/tree/main/skills/<skill-name>

# 여러 에이전트를 지원하는 커뮤니티 CLI
npx skills add <owner>/<repo> --skill <skill-name> -a codex

# 팀이 등록해 둔 마켓플레이스 경유
codex plugin marketplace add <owner>/<repo>
```

이름만 쓰는 조회(예: `$skill-installer gh-fix-ci`)는 OpenAI 선별 카탈로그(github.com/openai/skills)에 있는 스킬에만 허용된다. 커뮤니티 스킬은 항상 URL이나 owner/repo 네임스페이스가 필요하다.

## 5. 스킬 크기 정하기: 5단계 스펙트럼

모든 워크플로가 스크립트, 참고 자료, CI 검증까지 갖춘 본격 스킬일 필요는 없다. 스킬의 복잡도는 5단계로 나뉘며, 대부분의 팀은 처음부터 윗단계로 뛰어올라 과투자한다.

| 단계 | 이름 | 모양 | 적합한 경우 |
| --- | --- | --- | --- |
| 1 | 10단어 프롬프트 | AGENTS.md의 한 문장이나 직접 입력. 파일도 YAML도 없다. | 한두 번 하고 말 일회성 워크플로. 예: "변경된 모든 파일에 ESLint를 돌리고 자동 수정 가능한 문제를 고쳐라." |
| 2 | 재사용 프롬프트 | 텍스트 파일에 담은 한 문단, 또는 보조 파일 없는 짧은 SKILL.md | 매주 반복하는 워크플로. 예: 설명과 지시 다섯 줄로 변경 이력(changelog)을 만드는 SKILL.md |
| 3 | 팀 관례 | 설명, 트리거 동의어, 제외 조건을 갖춘 SKILL.md와 도우미 스크립트 한두 개가 든 scripts/ | 팀이 공유하는 워크플로. 프로젝트 고유 스킬 대부분이 여기에 해당한다. |
| 4 | 라이브러리 스킬 | references/, scripts/, assets/, agents/openai.yaml, MCP 의존성, CI 검증을 모두 갖춘 SKILL.md | 팀이나 조직을 넘나드는 스킬, 커뮤니티 카탈로그에 올리는 스킬 |
| 5 | 프로덕션 산출물 | 버전 고정, 자동 벤치마크, 회귀 테스트, 공식 검토 절차를 갖춘 스킬 | 프로덕션 배포를 통제하거나 컴플라이언스 정책을 강제하는 스킬 |

함정은 2단계나 3단계로 충분한데 4단계나 5단계를 찾는 것이다. 오늘의 문제를 푸는 10단어 프롬프트가, 내일 생길지도 모르는 가상의 문제를 푸는 사흘짜리 프로덕션 스킬보다 낫다. SKILL.md를 쓰는 데 자동화하려는 작업보다 시간이 더 들었다면 과설계하고 있는 것이다. 프롬프트부터 쓰고, 세 번 쓰게 되면 2단계 스킬로 뽑아내고, 팀이 채택하면 3단계로 올린다. 사용량이 복잡도를 이끌게 한다.

## 6. 작성 순서: 먼저 손으로, 그다음 인코딩

Nate Herk의 Codex CLI 강의로 널리 알려진 커뮤니티 관행이 있다. 스킬을 처음부터 설계해 놓고 나중에 빈틈을 발견하기보다, 워크플로를 먼저 손으로 해 보고 그 뒤에 스킬로 옮기는 것이다. 다섯 단계로 진행한다.

1. 일반 세션에서 직접 해 본다. 작업을 처음부터 끝까지 완주하며 단계, 에러 처리 로직, 출력 형식, API 엔드포인트를 파악한다.
2. SKILL.md를 쓴다. 분명한 description(라우팅 규칙)과 단계별 지시문으로 절차를 옮긴다.
3. 활성화를 확인한다. TUI 선택 창에 스킬이 나타나고 `$` 호출에 반응하는지 본다.
4. AGENTS.md와 연결한다. 스킬이 프로젝트 고유의 경로, 인프라, 관례에 기대고 있다면 세션 시작 때 프로젝트의 AGENTS.md가 그 컨텍스트를 제공하도록 한다.
5. 반복해서 다듬는다. 실제 입력으로 돌려 보고, 실패 유형이 드러나면 지시문을 더 조인다.

이 방식은 4단계로 성급히 뛰어들지 않고 자연스럽게 2~3단계 스킬을 만들어 낸다. 같은 흐름 주변에는 관행이 세 가지 더 있다.

- 전역 대 프로젝트 로컬: 스킬이 특정 파일 경로, 인프라 엔드포인트, 프로젝트 고유 설정을 참조하면 프로젝트 로컬로 만들어 `$REPO_ROOT/.agents/skills/`에 커밋한다. 변경 이력 생성기나 PR 요약 스킬처럼 일반적으로 동작하면 `$HOME/.agents/skills/`에 전역으로 설치한다.
- 스킬 단계로서의 품질 게이트: 배포 스킬에 browser-use 검증 단계를 넣어, 치명적인 버그가 없을 때까지 푸시를 막을 수 있다. 별도의 CI 검사에 기대지 않고 스킬 절차 안에 품질 게이트를 심는 방식이며, 19장의 소스에서 품질을 챙기는 원칙과 맞닿는다.
- 작성용 추론 강도: 반복해서 다듬을 때는 Medium이나 High가 적당하다. 빠르게 돌릴 수 있고 절차를 정확히 옮길 만큼 정확하다. Extra High는 복잡한 실패를 디버깅할 때를 위해 아껴 둔다.

SKILL.md를 맨 처음부터 쓰기보다 `$skill-creator`로 뼈대를 만드는 편이 좋다.

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
