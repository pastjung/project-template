---
branch: github/semantic-pr
description: PR 제목을 Conventional Commits 형식으로 검사하는 workflow
provides:
  - .github/workflows/semantic-pr.yml
  - docs/github-semantic-pr.md
requires: []
works-with:
  - branch: standards/commit-strategy
    reason: 허용 type 목록을 공유 (한쪽 변경 시 함께 갱신)
  - branch: github/pr-template
    reason: 템플릿의 권장 제목 prefix가 이 검사를 통과하도록 정합
conflicts: []
placeholders: []
secrets: []
after-import:
  - 허용 type과 requireScope를 팀 커밋 전략과 일치시키기
  - branch protection의 required status check로 등록 검토
verify:
  - actionlint .github/workflows/semantic-pr.yml
---

# Semantic PR Guide

이 문서는 Pull Request 제목을 Conventional Commits 형식으로 검사하는 GitHub Actions workflow의 운영 기준을 정의합니다.

## Purpose

`github/semantic-pr`는 PR 제목을 일정한 형식으로 맞춰 squash merge, changelog 작성, 릴리스 노트 정리를 쉽게 만들기 위한 설정입니다.

주요 목적은 다음과 같습니다.

- PR 제목을 Conventional Commits 형식으로 통일합니다.
- squash merge 시 최종 커밋 메시지를 예측 가능하게 만듭니다.
- changelog와 release note 자동화의 기반을 마련합니다.
- 개별 커밋보다 PR 제목을 우선 검사해 팀 운영 부담을 낮춥니다.

## Files

이 브랜치는 다음 파일을 추가합니다.

| File | Purpose |
| --- | --- |
| `.github/workflows/semantic-pr.yml` | PR 제목을 검사하는 GitHub Actions workflow |
| `docs/semantic-pr.md` | semantic PR 운영 기준과 수정 가이드 |

## Title Format

PR 제목은 다음 형식을 사용합니다.

```text
<type>: <subject>
<type>(<scope>): <subject>
```

`scope`는 선택 사항입니다.

예시:

```text
feat: add login page
feat(auth): add login API
fix(auth): handle expired token
docs: update API guide
ci: add test workflow
```

## Allowed Types

허용하는 type은 `standards/commit-strategy`의 commit type과 맞춥니다.

| Type | Usage |
| --- | --- |
| `init` | 프로젝트 초기 설정 |
| `feat` | 새로운 기능 추가 |
| `fix` | 버그 수정 |
| `build` | 빌드 시스템 또는 외부 의존성 변경 |
| `chore` | 기능 변화 없는 기타 작업과 설정 변경 |
| `ci` | CI/CD 설정 변경 |
| `docs` | 문서 수정 |
| `style` | 코드 포맷팅, 세미콜론, 들여쓰기 등 |
| `refactor` | 기능 변경 없는 코드 구조 개선 |
| `test` | 테스트 추가 또는 수정 |
| `perf` | 성능 개선 |
| `revert` | 이전 변경 되돌리기 |
| `release` | 버전 릴리스 |

workflow 설정은 다음과 같습니다.

```yaml
types: |
  init
  feat
  fix
  build
  chore
  ci
  docs
  style
  refactor
  test
  perf
  revert
  release
```

`init`과 `release`는 Conventional Commits 명세의 표준 type이 아닌 커스텀
type입니다. 이 workflow는 위 `types` 목록으로 직접 허용하므로 동작에 문제가
없지만, 이후 commitlint나 semantic-release를 도입하면 별도의 커스텀 type
등록이 필요합니다. 자세한 내용은 `standards/commit-strategy` 문서의
"비표준 type 주의" 절을 참고합니다.

## Scope Policy

기본 설정은 scope를 필수로 요구하지 않습니다.

```yaml
requireScope: false
```

따라서 다음 두 형식 모두 허용됩니다.

```text
docs: update README
feat(auth): add login API
```

팀에서 항상 scope를 요구하고 싶다면 다음처럼 바꿉니다.

```yaml
requireScope: true
```

## Workflow Trigger

workflow는 PR 제목이 생성되거나 변경될 수 있는 이벤트에서 실행됩니다.

```yaml
on:
  pull_request_target:
    types:
      - opened
      - edited
      - reopened
      - synchronize
```

`pull_request_target`은 fork PR에서도 기본 토큰을 사용할 수 있지만, 보안상 주의가 필요합니다.
이 workflow는 checkout이나 외부 코드를 실행하지 않고 PR metadata만 검사하도록 유지합니다.

## Permissions

PR 제목만 읽으면 되므로 최소 권한을 사용합니다.

```yaml
permissions:
  pull-requests: read
```

## Gitmoji

이 workflow는 기본적으로 PR 제목 앞의 gitmoji를 허용하지 않습니다.

권장 PR 제목:

```text
feat(auth): add login API
```

권장하지 않는 PR 제목:

```text
✨ feat(auth): add login API
```

커밋 메시지에서는 gitmoji를 선택적으로 사용할 수 있지만, PR 제목은 자동화와 changelog 연동을 위해 Conventional Commits 형식만 사용하는 것을 권장합니다.

## Good Examples

```text
init: initialize project
feat(auth): add login API
fix(auth): handle expired token
build: add Dockerfile
chore: update env example
ci: add test workflow
docs: update branch strategy
style: format user service
refactor(auth): split token service
test(auth): add login test
perf(post): optimize list query
revert: revert login API change
release: v1.0.0
```

## Bad Examples

```text
add login API
login bug fix
Feat: add login API
feature: add login API
feat add login API
feat(auth) add login API
```

## Usage Rules

- 이 브랜치는 PR 기반 협업을 사용하는 프로젝트에 적용합니다.
- squash merge를 사용할 때 특히 유용합니다.
- 개별 커밋 메시지 검사는 강제하지 않고 PR 제목만 검사합니다.
- type 목록은 `standards/commit-strategy`와 함께 관리합니다.
- PR 제목에 issue 번호를 넣어야 한다면 subject 뒤에 자연스럽게 포함합니다.

예시:

```text
fix(auth): handle expired token (#123)
```

## Recommended Import

이 설정은 `standards/commit-strategy`를 적용한 뒤 사용하는 것을 권장합니다.

```bash
git merge --squash origin/github/semantic-pr
git commit -m "init: add semantic PR workflow"
```

## Standalone Usage

이 브랜치만 가져와도 PR 제목 검사가 즉시 동작합니다. 검사 결과를 병합
조건으로 만들려면 branch protection의 required status check에 등록합니다.

## Works With

type 목록은 `standards/commit-strategy`와 단일 기준으로 관리합니다. 한쪽을
수정하면 다른 쪽도 함께 갱신해야 합니다.
