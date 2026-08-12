---
branch: github/codeowners
description: 경로별 코드 오너 자동 리뷰 요청 (.github/CODEOWNERS)
provides:
  - .github/CODEOWNERS
  - docs/github-codeowners.md
requires: []
works-with:
  - branch: github/pr-template
    reason: PR 리뷰 흐름(오너 자동 지정 + 템플릿 체크리스트)을 함께 구성
conflicts: []
placeholders:
  - file: .github/CODEOWNERS
    token: "{{OWNER}}"
secrets: []
after-import:
  - "{{OWNER}}와 팀 slug를 실제 organization/team으로 치환 (치환 전에는 unknown owner 오류)"
  - branch protection에서 Require review from Code Owners 활성화 검토
verify:
  - "! grep -q '{{OWNER}}' .github/CODEOWNERS"
---

# CODEOWNERS Guide

이 문서는 GitHub CODEOWNERS 파일의 역할과 관리 기준을 정의합니다.

## Files

```text
.github/CODEOWNERS
docs/codeowners-guide.md
```

## Purpose

`CODEOWNERS`는 특정 경로나 파일을 담당하는 GitHub 사용자 또는 팀을 정의합니다.

PR이 생성되면 GitHub는 변경된 파일과 `CODEOWNERS` 규칙을 비교해 해당 owner에게 리뷰를 자동 요청할 수 있습니다.
브랜치 보호 규칙에서 code owner review를 필수로 설정하면, 담당 owner의 승인이 있어야 병합할 수 있습니다.

## Location

GitHub는 다음 위치의 CODEOWNERS 파일을 인식합니다.

```text
.github/CODEOWNERS
CODEOWNERS
docs/CODEOWNERS
```

이 저장소는 GitHub 설정 파일을 한곳에 모으기 위해 `.github/CODEOWNERS`를 사용합니다.

## Owner Format

owner는 GitHub 사용자 또는 팀으로 지정합니다.

```text
* @{{OWNER}}/repo-admins
/backend/ @{{OWNER}}/backend
/frontend/ @{{OWNER}}/frontend
```

각 placeholder는 실제 저장소 owner와 팀 이름으로 바꿔야 합니다.

| Placeholder | Replace With |
| --- | --- |
| `{{OWNER}}` | GitHub organization 또는 user 이름 |
| `repo-admins` | 저장소 전체를 관리하는 팀 |
| `<team>` | 해당 영역을 담당하는 팀 |

예시:

```text
* @acme/repo-admins
/backend/ @acme/backend
/frontend/ @acme/frontend
```

## Matching Rules

- 마지막으로 매칭된 규칙이 우선합니다.
- `*`는 기본 owner를 지정합니다.
- `/backend/`처럼 `/`로 시작하면 저장소 루트 기준 경로를 의미합니다.
- 디렉터리 뒤에 `/`를 붙이면 해당 디렉터리 아래 전체 파일에 적용됩니다.
- owner는 한 줄에 여러 명 또는 여러 팀을 지정할 수 있습니다.

예시:

```text
/backend/ @acme/backend @acme/platform
```

## Current Ownership Map

| Path | Owner |
| --- | --- |
| `*` | `@{{OWNER}}/repo-admins` |
| `.github/` | `@{{OWNER}}/repo-admins` |
| `backend/` | `@{{OWNER}}/backend` |
| `frontend/` | `@{{OWNER}}/frontend` |
| `api/` | `@{{OWNER}}/backend` |
| `data/` | `@{{OWNER}}/data` |
| `observability/` | `@{{OWNER}}/infra` |
| `settings/` | `@{{OWNER}}/infra` |
| `docs/` | `@{{OWNER}}/docs` |
| `git/` | `@{{OWNER}}/repo-maintainers` |
| `modules/` | `@{{OWNER}}/repo-maintainers` |
| `ai/` | `@{{OWNER}}/ai` |

## Branch Protection

CODEOWNERS 파일만 추가해도 GitHub는 PR 화면에서 owner를 표시할 수 있습니다.
하지만 owner 승인을 병합 조건으로 강제하려면 branch protection rule이 필요합니다.

권장 설정:

1. GitHub 저장소의 `Settings`로 이동합니다.
2. `Branches`를 선택합니다.
3. 보호할 branch rule을 생성하거나 수정합니다.
4. `Require a pull request before merging`을 켭니다.
5. `Require review from Code Owners`를 켭니다.

## Maintenance Rules

- 새 최상위 디렉터리를 추가하면 CODEOWNERS에 담당 owner를 함께 추가합니다.
- 팀 이름이 바뀌면 CODEOWNERS와 이 문서를 함께 수정합니다.
- owner가 없는 파일은 기본 규칙 `*`에 의해 저장소 관리자에게 할당됩니다.
- 민감한 설정, 배포, 보안 관련 파일은 단일 개인보다 팀 owner를 지정합니다.
- CODEOWNERS 변경 PR은 저장소 관리자 또는 해당 영역 owner의 리뷰를 받습니다.

## Standalone Usage

placeholder({{OWNER}}, 팀 slug)를 실제 값으로 치환해야 동작합니다. 치환
전에는 GitHub CODEOWNERS 화면에 unknown owner 오류가 표시되고 자동 리뷰
요청이 동작하지 않습니다.

## Works With

`github/pr-template`과 함께 쓰면 오너 자동 지정과 PR 체크리스트가 하나의
리뷰 흐름을 구성합니다. branch protection의 Require review from Code Owners와
결합하면 오너 승인을 병합 조건으로 강제할 수 있습니다.
