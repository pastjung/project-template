---
branch: github/community
description: 커뮤니티 헬스 파일 (CONTRIBUTING.md, SECURITY.md)
provides:
  - CONTRIBUTING.md
  - SECURITY.md
  - docs/github-community.md
requires: []
works-with:
  - branch: standards/branch-strategy
    reason: CONTRIBUTING의 브랜치 규칙이 이 전략을 요약
  - branch: standards/commit-strategy
    reason: CONTRIBUTING의 커밋 규칙이 이 전략을 요약
  - branch: git/hooks
    reason: CONTRIBUTING이 안내하는 커밋 검사 hook
conflicts: []
placeholders:
  - file: CONTRIBUTING.md
    token: "{{FEATURE_NAME}}"
  - file: SECURITY.md
    token: "{{SECURITY_CONTACT}}"
secrets: []
after-import:
  - SECURITY.md의 연락처 placeholder 치환
  - GitHub Settings에서 Private vulnerability reporting 활성화
verify:
  - test -f CONTRIBUTING.md
  - test -f SECURITY.md
---

# Community Health Files Guide

이 문서는 CONTRIBUTING.md와 SECURITY.md의 운영 기준을 정의합니다.

## CONTRIBUTING.md

새 기여자의 온보딩 문서입니다. 브랜치 전략과 커밋 전략 문서의 핵심만
요약하고, 상세 규칙은 해당 문서로 위임합니다. GitHub은 PR/이슈 생성 화면에서
이 파일 링크를 자동으로 노출합니다.

## SECURITY.md

취약점 신고 채널을 정의합니다. 저장소의 Security 탭에 자동으로 연결됩니다.

- `{{SECURITY_CONTACT}}`를 실제 연락처(이메일 등)로 치환합니다.
- GitHub Private vulnerability reporting을 활성화하면 신고가 비공개
  advisory로 접수됩니다.

## Standalone Usage

이 브랜치만 가져와도 GitHub이 두 파일을 자동 인식합니다. placeholder 치환만
필요합니다.

## Works With

CONTRIBUTING이 요약하는 상세 규칙은 `standards/branch-strategy`,
`standards/commit-strategy`에 있습니다. `git/hooks`를 함께 적용하면
CONTRIBUTING이 안내하는 커밋 검사가 실제로 동작합니다.
