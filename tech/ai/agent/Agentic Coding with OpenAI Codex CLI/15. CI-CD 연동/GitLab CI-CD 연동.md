# GitLab CI/CD 연동

앞에서 본 패턴은 GitHub Actions 기준이었다. Codex CLI는 GitLab에서도 똑같이 잘 동작한다. 이 문서는 GitLab의 Duo Agent Platform으로 붙이는 방법과, `.gitlab-ci.yml`에 `codex exec`를 직접 넣어 코드 품질 리포트를 만드는 방법을 다룬다.

---

## 1. Duo Agent Platform

GitLab의 Duo Agent Platform은 2026년 1월에 정식 출시(GA)되었고, GitLab 18.8 이상에서 Codex CLI를 외부 에이전트로 지원한다. 개발자가 이슈 댓글이나 머지 리퀘스트(MR) 토론에서 `@codex`를 멘션하면 에이전트가 저장소 맥락을 읽고 그 자리에서 답한다. 인증은 GitLab의 AI Gateway를 거친다. 그래서 별도의 `OPENAI_API_KEY`가 필요 없다.

## 2. .gitlab-ci.yml에서의 코드 품질 분석

MR마다 체계적으로 분석하고 싶다면 `codex exec`를 파이프라인에 직접 넣는다. 핵심은 마커 기반 추출이다. Codex CLI에게 출력을 구분선 사이에 감싸 달라고 지시하고, 그 구간만 `awk`로 뽑아낸다.

잡 구성은 이렇다.

- `stage: codex`, `image: node:24`
- 규칙: `$CI_PIPELINE_SOURCE == "merge_request_event"`일 때만 실행
- 설치: `npm -g i @openai/codex@latest`
- 파일 목록: `git ls-files`를 `FILE_LIST`로 만들어 프롬프트에 넣는다

```yaml
codex_review:
  stage: codex
  image: node:24
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
  script:
    - npm -g i @openai/codex@latest
    - FILE_LIST="$(git ls-files | sed 's/^/- /')"
```

그다음 `codex exec -s workspace-write -c approval_policy=never`에 프롬프트를 준다. 프롬프트는 저장소를 리뷰해서 CodeClimate JSON 형식의 GitLab Code Quality 리포트를 내라는 것이다. 출력은 `=== BEGIN_CODE_QUALITY_JSON ===`과 `=== END_CODE_QUALITY_JSON ===` 마커 사이의 JSON 배열 하나여야 한다. 이슈마다 `description`, `check_name`, `fingerprint`, `severity`, 그리고 `path`와 `lines.begin`을 가진 `location`이 있어야 하고, 이슈는 `${FILE_LIST}`에 있는 파일만 보고하게 한다. 출력은 `tee artifacts/codex-raw.log`로 로그에 저장한다.

### 마커 사이만 잘라 내기

로그에서 ANSI 이스케이프 코드를 `sed -E 's/\x1B\[[0-9;]*[A-Za-z]//g'`로 지우고, `awk`로 시작 마커와 끝 마커 사이만 골라 `gl-code-quality-report.json`에 쓴다.

```bash
sed -E 's/\x1B\[[0-9;]*[A-Za-z]//g' artifacts/codex-raw.log \
 | awk '/BEGIN_CODE_QUALITY_JSON/{g=1;next}
 /END_CODE_QUALITY_JSON/{g=0}g' \
 > gl-code-quality-report.json
```

### 아티팩트 설정

```yaml
artifacts:
  reports:
    codequality: gl-code-quality-report.json
  expire_in: 14 days
```

`codequality` 타입의 아티팩트로 올리면 결과가 MR 위젯에 GitLab 기본 스캐너 결과와 나란히 표시된다.

> 주의: 파싱 전에 원본 로그의 ANSI 코드를 반드시 지운다. `codex exec`가 터미널 색상 시퀀스를 섞어 내보내면 JSON 추출이 깨진다.

## 3. 확장: 보안 수정과 MCP

같은 `codex exec` 방식은 보안 수정(SAST 스캔 결과에 Codex가 만든 패치를 짝지우는 것)이나 LLM 분석이 도움이 되는 어떤 파이프라인 단계에도 이어 쓸 수 있다. GitLab API 접근이 필요한 대화형 세션이라면 GitLab의 기본 MCP 서버를 `codex mcp add --url`로 설정한다.

## 4. GitHub과 GitLab 비교

GitLab 연동은 `openai/codex-action`보다 손으로 설정할 것이 많지만 할 수 있는 일은 같다. `codex exec`의 옵션, 승인 모드, 구조화된 출력은 두 플랫폼에서 똑같이 동작한다. 다른 것은 파이프라인 문법과 아티팩트 형식뿐이다.

| 항목 | GitHub | GitLab |
| --- | --- | --- |
| 연동 방식 | `openai/codex-action` | Duo Agent Platform, `codex exec` 직접 호출 |
| 인증 | `OPENAI_API_KEY` 시크릿 | Duo는 AI Gateway가 처리(키 불필요) |
| 결과 노출 | 댓글, PR | `codequality`, SAST 아티팩트 |
| 출력 추출 | `final-message` 출력 | 마커 + `awk` 추출 |

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
