# CI/CD 연동

이 장은 Codex CLI를 사람이 지켜보는 대화형 환경에서 파이프라인으로 옮긴다. 에이전트가 사람 없이 혼자 도는 헤드리스 `codex exec`, GitHub Action `openai/codex-action`, GitLab Duo Agent Platform, 그리고 PR 리뷰·테스트 생성·의존성 업데이트·보안 수정 같은 실전 자동화 패턴을 다룬다.

에이전트 기반 파이프라인에서는 어떤 모델을 쓰느냐보다 파이프라인을 어떻게 설계했느냐가 더 중요하다. 그래서 권한, 격리, 구조화된 출력, 사람 관문, 관측 같은 설계 주제가 장의 중심이다.

---

## 1. 핵심 요점

- 모든 CI 패턴은 `codex exec`를 바탕으로 한다. `--json`, `--output-schema`, `codex exec resume`, stdin 파이프가 파이프라인 연결 표면이다.
- `--ignore-user-config`와 `--ignore-rules`로 실행을 격리하고, `requirements.toml`의 호스트 이름 패턴으로 환경별 샌드박스 상한을 둔다. AGENTS.md는 여전히 읽힌다.
- GitHub에서는 PR 리뷰, 머지 때 테스트 생성, 주간 의존성 업데이트를 읽기 전용·쓰기 제한 샌드박스와 PR 관문으로 구성한다.
- GitLab에서는 Duo Agent Platform과 `.gitlab-ci.yml`의 마커 기반 출력 추출로 같은 기능을 구현한다.
- 자가 치유 성숙도 모델은 Observer, Gatekeeper, Healer 세 단계이며, 대부분의 팀은 Gatekeeper에서 오래 머물러야 한다.
- CI 에이전트는 신뢰하지 않는 대상으로 다룬다. PR 내용은 파일로 넘기고, 토큰 범위를 줄이고, 네트워크를 제한하고, 포크 PR에서는 `--yolo`를 쓰지 않는다.
- 토큰 사용량, 조향 메타데이터, 스레드 맥락으로 비용과 감사를 관리하고, keepalive와 원격 연결로 긴 세션을 안정적으로 운영한다.
- 에이전트 PR 933,000건 이상을 분석한 연구는 실패 원인이 코드 품질보다 리뷰어 이탈과 중복 같은 워크플로 문제임을 보여 준다.

---

## 2. 문서 목록

- [헤드리스 실행 codex exec](%ED%97%A4%EB%93%9C%EB%A6%AC%EC%8A%A4%20%EC%8B%A4%ED%96%89%20codex%20exec.md): `codex exec`의 CI용 옵션, JSONL 출력, 스키마 출력, 세션 이어가기, 비TTY 제한
- [재현 가능한 실행과 샌드박스 제한](%EC%9E%AC%ED%98%84%20%EA%B0%80%EB%8A%A5%ED%95%9C%20%EC%8B%A4%ED%96%89%EA%B3%BC%20%EC%83%8C%EB%93%9C%EB%B0%95%EC%8A%A4%20%EC%A0%9C%ED%95%9C.md): 격리 옵션 세 가지와 호스트 이름 패턴 샌드박스 정책
- [GitHub Actions 기본 패턴](GitHub%20Actions%20%EA%B8%B0%EB%B3%B8%20%ED%8C%A8%ED%84%B4.md): `openai/codex-action`, PR 요약·리뷰, 테스트 생성, 의존성 업데이트
- [프로젝트 스킬과 스택 PR](%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%20%EC%8A%A4%ED%82%AC%EA%B3%BC%20%EC%8A%A4%ED%83%9D%20PR.md): `codex-pr-body` 스킬과 스택 PR 설명 자동 갱신
- [GitLab CI-CD 연동](GitLab%20CI-CD%20%EC%97%B0%EB%8F%99.md): Duo Agent Platform과 `.gitlab-ci.yml` 코드 품질 리포트
- [자가 치유 파이프라인과 AutoLoop](%EC%9E%90%EA%B0%80%20%EC%B9%98%EC%9C%A0%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%EA%B3%BC%20AutoLoop.md): 3단계 성숙도 모델, Pipeline Doctor(그림 15.1), AutoLoop
- [CI 에이전트 안전 전략과 관측](CI%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EC%95%88%EC%A0%84%20%EC%A0%84%EB%9E%B5%EA%B3%BC%20%EA%B4%80%EC%B8%A1.md): 안전 원칙, 토큰·감사 관측, keepalive, 원격 승인
- [빌드 시스템과 실증 연구 그리고 패턴 표](%EB%B9%8C%EB%93%9C%20%EC%8B%9C%EC%8A%A4%ED%85%9C%EA%B3%BC%20%EC%8B%A4%EC%A6%9D%20%EC%97%B0%EA%B5%AC%20%EA%B7%B8%EB%A6%AC%EA%B3%A0%20%ED%8C%A8%ED%84%B4%20%ED%91%9C.md): Bazel·Dagger, 에이전트 PR 연구, Microsoft 플레이북, 패턴 카탈로그
- [요약](%EC%9A%94%EC%95%BD.md): 장 전체 열 가지 결론
- [연습 문제](%EC%97%B0%EC%8A%B5%20%EB%AC%B8%EC%A0%9C.md): 여섯 개 실습 문제와 풀이 방향

<br>
<br>
<br>

[Agentic Coding with OpenAI Codex CLI](../)
