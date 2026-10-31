# CI/CD와 헤드리스 자동화

사람이 지켜보는 터미널에서 쓰는 Claude Code와, CI 파이프라인에서 새벽에 티켓을 처리하고 깨진 빌드를 고치는 Claude Code는 사실상 다른 범주의 도구다. 인터랙티브에서 헤드리스로 바뀌면 권한 모델, 출력 형식, 실패 복구 전략, 자동화의 경제성이 모두 달라진다.

이 장은 Claude Code를 화면 없이 돌리는 헤드리스 모드와 그 주변 기술을 다룬다. 비대화형 플래그와 출력 형식, 안전하게 무인으로 돌리는 컨테이너 전략, 실제 CI/CD 시스템과의 연동 패턴, 훅으로 만드는 품질 관문, 파일 단위 일괄 처리(팬아웃)를 설명하고, 아직 되지 않는 부분과 그 전망도 짚는다.

---

## 1. 핵심 요점

- **`-p` 플래그**: Claude Code를 대화형에서 비대화형 명령 처리기로 바꾼다. `--output-format`(text, json, stream-json), `--max-turns`, `--budget`, `--model`로 동작을 조절한다.
- **유닉스 조합성**: stdin으로 입력을 받고 stdout으로 출력하므로 파이프, jq, 빌드 스크립트와 그대로 연결된다. 별도의 통합 계층이 필요 없다.
- **무인 실행의 안전**: 격리된 devcontainer, 기본 차단 방화벽, `--dangerously-skip-permissions`의 세 겹이 표준이다. 컨테이너를 못 쓰면 `--permission-prompt-tool`로 권한 정책을 코드로 만든다. 주입된 시크릿은 컨테이너로 막을 수 없으므로 수명이 짧은 토큰을 쓴다.
- **재현성**: CI에서는 파일 기반 시스템 프롬프트 플래그(`--append-system-prompt-file` 등)를 쓰고, CLAUDE.md와 함께 두 겹의 맥락으로 쓴다.
- **CI 연동 패턴**: PR 자동 수정, 이슈 자동 처리, 자동 코드 리뷰가 검증되었다. 모두 이벤트, 맥락 모으기, 헤드리스 실행, 결과 게시의 구조이며, 범위가 분명한 작업에 맞는다.
- **팬아웃과 파이프라인 생성**: 파일마다 `--allowedTools`로 권한을 좁혀 호출하면 안전한 일괄 분석이 된다. CI 설정 생성은 결과를 바로 검증할 수 있어 ROI가 높다.
- **훅이 품질 관문**: 비동기 PostToolUse 테스트 러너, TaskCompleted 훅, 에이전트형 Stop 훅, CLAUDE_ENV_FILE, 프리커밋 훅으로 Claude가 스스로 실패를 보고 고치게 한다.
- **남은 공백**: CI 실패 자동 수정은 아직 제품화되지 않았다. 33일 장기 운영 사례는 컨텍스트 압축과 기억의 외부화 문제를 보여 준다.
- **도입 순서**: 인터랙티브, 스크립트, 빌드 스크립트, CI, 피드백 고리의 다섯 단계로 넓혀 가며, 단계마다 독립된 가치가 있다.

---

## 2. 문서 목록

- [헤드리스 모드 기본](%ED%97%A4%EB%93%9C%EB%A6%AC%EC%8A%A4%20%EB%AA%A8%EB%93%9C%20%EA%B8%B0%EB%B3%B8.md): -p 플래그, 출력 형식, 파이프 사용법, 빌드 스크립트 통합
- [무인 실행의 안전장치](%EB%AC%B4%EC%9D%B8%20%EC%8B%A4%ED%96%89%EC%9D%98%20%EC%95%88%EC%A0%84%EC%9E%A5%EC%B9%98.md): devcontainer 세 겹 구조, permission-prompt-tool, 시스템 프롬프트 플래그, 참조 devcontainer
- [CI 플랫폼 연동 패턴](CI%20%ED%94%8C%EB%9E%AB%ED%8F%BC%20%EC%97%B0%EB%8F%99%20%ED%8C%A8%ED%84%B4.md): PR 자동 수정, 이슈 자동 처리, 자동 리뷰, /commit-push-pr, --from-pr, 메신저 연동
- [팬아웃과 CI 파이프라인 생성](%ED%8C%AC%EC%95%84%EC%9B%83%EA%B3%BC%20CI%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%20%EC%83%9D%EC%84%B1.md): 파일 단위 일괄 처리, CI 설정 생성과 반복 개선, 보안 스캔 분담
- [훅으로 만드는 품질 관문](%ED%9B%85%EC%9C%BC%EB%A1%9C%20%EB%A7%8C%EB%93%9C%EB%8A%94%20%ED%92%88%EC%A7%88%20%EA%B4%80%EB%AC%B8.md): 비동기 훅, TaskCompleted, 에이전트 Stop 훅, CLAUDE_ENV_FILE, 프리커밋 훅, attribution
- [아직 안 되는 것과 장기 실행](%EC%95%84%EC%A7%81%20%EC%95%88%20%EB%90%98%EB%8A%94%20%EA%B2%83%EA%B3%BC%20%EC%9E%A5%EA%B8%B0%20%EC%8B%A4%ED%96%89.md): CI 자동 수정의 공백과 33일 장기 헤드리스 운영 사례
- [핵심 정리](%ED%95%B5%EC%8B%AC%20%EC%A0%95%EB%A6%AC.md): 6장 요점 여덟 가지를 이유와 함께 복습

<br>
<br>
<br>

[Claude Code The Definitive Guide to Agentic Development-2](../)
