# Claude Code와 GitHub로 개발 워크플로 자동화

5장은 Claude Code를 GitHub에 연결하는 방법과 그 쓰임을 다룬다. GitHub CLI와 Claude GitHub 앱을 설치하고, GitHub Actions 워크플로로 이슈와 PR에서 Claude를 부르는 구조를 만든다. 이어 실제 이슈를 맡겨 보며 맥락이 없을 때의 실패와 CLAUDE.md를 더한 뒤의 개선을 확인한다.

---

## 1. 핵심 요점

- 연동은 GitHub CLI 설치와 인증, `/install-github-app`, Claude GitHub 앱 설치, 워크플로 추가 순서로 이뤄진다.
- 자동화는 GitHub Actions가 돌리며 Claude Code CLI와 SDK를 쓴다. 워크플로는 `.github/workflows`의 YAML 파일이다.
- 설치 옵션은 Tag Claude(댓글에서 호출)와 Claude Code Review(새 PR 자동 검토)이고, 비용은 구독 장기 토큰이나 API 키로 낸다.
- 토큰은 Actions 시크릿에 저장되고 워크플로 파일에서 이름으로만 참조한다. 저장소 접근 권한이 있는 사용자만 실행할 수 있다.
- Claude는 `claude/issue/<번호>` 같은 새 브랜치에서 일하므로 main을 직접 바꾸지 않고, 병합 결정은 사람이 한다.
- 맥락 없이 맡긴 변수 이름 변경은 외부 API 계약을 깨뜨렸다. PR 설명이 그럴듯해도 diff를 반드시 검토해야 한다.
- `/init`으로 만든 CLAUDE.md를 커밋하고 힌트를 더해 재요청하자 올바른 PR이 나왔고 자동 리뷰가 승인했다.

---

## 2. 문서 목록

- [GitHub 연동 설치와 설정](GitHub 연동 설치와 설정.md): 연동 구조, 사전 준비, 앱과 워크플로 설치, 인증 방법, 설치 PR과 YAML
- [이슈 해결 실습과 컨텍스트의 효과](이슈 해결 실습과 컨텍스트의 효과.md): 이슈 태그, 틀린 PR, 작업 브랜치, CLAUDE.md 추가, 재시도와 자동 검토
- [요약과 핵심 개념](요약과 핵심 개념.md): 장 전체 흐름, 핵심 개념 표, 자주 놓치는 점

<br>
<br>
<br>

[Agentic Coding with Claude Code](../)
