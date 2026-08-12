---
branch: github/pr-template
description: 기본 PR 템플릿 + 브랜치 타입별 PR 템플릿 6종
provides:
  - .github/pull_request_template.md
  - .github/PULL_REQUEST_TEMPLATE/feat.md
  - .github/PULL_REQUEST_TEMPLATE/bugfix.md
  - .github/PULL_REQUEST_TEMPLATE/hotfix.md
  - .github/PULL_REQUEST_TEMPLATE/refactor.md
  - .github/PULL_REQUEST_TEMPLATE/docs.md
  - .github/PULL_REQUEST_TEMPLATE/release.md
  - docs/github-pr-template.md
requires: []
works-with:
  - branch: github/semantic-pr
    reason: 템플릿의 권장 제목 prefix가 semantic-pr 검사 type과 정합
  - branch: standards/branch-strategy
    reason: 브랜치 타입 명칭과 target 브랜치 매핑을 공유
  - branch: github/labels
    reason: 템플릿 metadata의 권장 라벨이 라벨 정의와 정합
conflicts: []
placeholders: []
secrets: []
after-import:
  - 템플릿 질문과 체크리스트를 프로젝트에 맞게 조정
verify:
  - test -f .github/pull_request_template.md
---

# Pull Request Template Guide

이 문서는 PR 생성 시 브랜치 타입에 맞는 Pull Request 템플릿을 선택하는 기준을 정리합니다.

## Template Files

기본 템플릿 1개와 브랜치 타입별 템플릿 6개를 함께 관리합니다.

```text
.github/
  pull_request_template.md   기본 템플릿 (PR 생성 시 자동 적용)
  PULL_REQUEST_TEMPLATE/
    feat.md
    bugfix.md
    hotfix.md
    refactor.md
    docs.md
    release.md
```

`.github/PULL_REQUEST_TEMPLATE/` 하위 템플릿만 있으면 GitHub는 PR 생성 시
아무 템플릿도 자동 적용하지 않고, URL `template` 파라미터를 붙였을 때만
적용합니다. 대부분의 PR이 빈 본문으로 열리는 것을 막기 위해 범용 기본
템플릿을 자동 적용하고, 특수한 경우(release, hotfix 등)에만 타입별 템플릿을
URL로 여는 하이브리드 구성을 사용합니다.

## Branch And Template Mapping

| Branch Type | Target Branch | Template |
| --- | --- | --- |
| `feat/*` | `dev` | `feat.md` |
| `bugfix/*` | `dev` | `bugfix.md` |
| `refactor/*` | `dev` | `refactor.md` |
| `docs/*` | `dev` | `docs.md` |
| `release/*` | `main` | `release.md` |
| `hotfix/*` | `main` | `hotfix.md` |

## Usage

GitHub는 브랜치 이름만 보고 PR 템플릿을 자동 선택하지 않습니다.
PR 작성자는 브랜치 타입에 맞는 템플릿을 선택해야 합니다.

PR 템플릿 상단의 metadata comment는 사람이 템플릿 목적, 권장 PR 제목 prefix, 기본 라벨, target branch를 확인하기 위한 정보입니다.
GitHub는 Issue Template과 달리 PR Template의 YAML front matter를 자동 라벨이나 제목으로 처리하지 않습니다.

metadata comment의 `title` 값은 `github/semantic-pr`의 Conventional Commits 검사와 맞춘 참고용 prefix입니다.
예를 들어 기능 PR은 `feat: ...`, 버그 수정과 긴급 수정 PR은 `fix: ...`, 릴리즈 PR은 `release: ...` 형식으로 작성합니다.

예시:

```text
feat/login        -> feat.md
bugfix/login-form -> bugfix.md
hotfix/payment    -> hotfix.md
refactor/auth     -> refactor.md
docs/api-guide    -> docs.md
release/1.0.0     -> release.md
```

## URL Parameter

GitHub PR 생성 URL에 `template` 파라미터를 추가하면 특정 템플릿을 직접 열 수 있습니다.

```text
?template=feat.md
?template=bugfix.md
?template=hotfix.md
?template=refactor.md
?template=docs.md
?template=release.md
```

예시:

```text
https://github.com/<owner>/<repo>/compare/dev...feat/login?quick_pull=1&template=feat.md
```

## Review Rules

- PR 제목은 변경 내용을 명확히 설명합니다.
- PR 본문에는 변경사항, 테스트 결과, 리뷰어가 확인해야 할 내용을 작성합니다.
- PR은 브랜치 전략의 병합 흐름에 맞는 target branch로 생성합니다.
- 리뷰 승인 후 병합하고, 병합이 끝난 작업 브랜치는 삭제합니다.

## Standalone Usage

이 브랜치만 가져와도 기본 템플릿이 PR 생성 시 자동 적용됩니다. 타입별
템플릿은 URL `template` 파라미터로 엽니다.

## Works With

`github/semantic-pr`과 함께 쓰면 템플릿이 권장하는 제목 prefix가 자동
검사됩니다. `standards/branch-strategy`의 브랜치 타입 명칭과 템플릿 매핑이
일치합니다.
