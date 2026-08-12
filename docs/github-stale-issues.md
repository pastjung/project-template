---
branch: github/stale-issues
description: 오래된 issue/PR을 stale 처리하는 workflow (이슈만 자동 close)
provides:
  - .github/workflows/stale-issues.yml
  - docs/github-stale-issues.md
requires: []
works-with:
  - branch: github/labels
    reason: status/stale, pinned, security, blocked 라벨을 자동 생성
conflicts: []
placeholders: []
secrets: []
after-import:
  - 저장소에 status/stale, pinned, security, blocked 라벨 존재 확인
  - stale 기간과 자동 close 여부를 팀 합의에 맞게 조정
verify:
  - actionlint .github/workflows/stale-issues.yml
---

# Stale Issues Guide

이 문서는 오래된 issue와 pull request를 자동으로 표시하고 정리하는 GitHub Actions workflow의 운영 기준을 정의합니다.

## Purpose

`github/stale-issues`는 일정 기간 활동이 없는 issue와 pull request에 stale 라벨을 붙여 관리자가 오래된 항목을 쉽게 정리할 수 있게 합니다.

주요 목적은 다음과 같습니다.

- 활동이 없는 issue를 자동으로 표시합니다.
- stale 상태가 오래 유지된 issue를 자동으로 닫습니다.
- pull request는 stale 표시만 하고 자동 close하지 않습니다.
- 보안, 차단, 고정 항목은 자동 처리 대상에서 제외합니다.

## Files

이 브랜치는 다음 파일을 추가합니다.

| File | Purpose |
| --- | --- |
| `.github/workflows/stale-issues.yml` | stale issue와 PR을 처리하는 GitHub Actions workflow |
| `docs/stale-issues.md` | stale workflow 운영 기준과 수정 가이드 |

## Default Policy

기본 정책은 issue는 정리하고, pull request는 자동 close하지 않는 보수적인 방식입니다.

| Target | Stale After | Close After | Auto Close |
| --- | --- | --- | --- |
| Issue | 30 days inactive | 14 days after stale | Yes |
| Pull request | 14 days inactive | Disabled | No |

Pull request는 작업 맥락이 남아 있을 수 있으므로 자동 close하지 않습니다.

## Workflow Trigger

workflow는 매일 한 번 실행되며, 필요하면 수동 실행할 수 있습니다.

```yaml
on:
  schedule:
    - cron: "0 0 * * *"
  workflow_dispatch:
```

`cron` 시간은 UTC 기준입니다.

## Permissions

stale workflow는 issue와 pull request에 라벨을 붙이고 comment를 작성해야 하므로 다음 권한을 사용합니다.

```yaml
permissions:
  issues: write
  pull-requests: write
```

## Labels

기본 stale 라벨은 다음과 같습니다.

```yaml
stale-issue-label: status/stale
stale-pr-label: status/stale
```

이 라벨은 저장소에 미리 존재해야 합니다. `github/labels`를 사용하는 프로젝트라면 라벨 정의에 `status/stale`을 추가합니다.

## Exempt Labels

다음 라벨이 붙은 issue와 pull request는 stale 처리에서 제외합니다.

```yaml
exempt-issue-labels: pinned,security,blocked
exempt-pr-labels: pinned,security,blocked
```

각 라벨의 의미는 다음과 같습니다.

| Label | Reason |
| --- | --- |
| `pinned` | 의도적으로 남겨두는 항목 |
| `security` | 보안 이슈로 자동 close하면 안 되는 항목 |
| `blocked` | 외부 의존성이나 의사결정을 기다리는 항목 |

프로젝트 라벨 전략에 맞춰 `priority/high`, `needs/discussion`, `epic` 같은 예외 라벨을 추가할 수 있습니다.

`github/labels`의 기본 라벨 정의만으로는 이 workflow가 사용하는 모든 라벨이 준비되지 않을 수 있습니다.
이 브랜치를 적용하기 전에 다음 라벨을 GitHub UI에서 직접 만들거나 `github/labels`의 `.github/labels.json`에 추가합니다.

| Label | Used By | Required |
| --- | --- | --- |
| `status/stale` | stale issue와 PR 표시 | Yes |
| `pinned` | stale 처리 예외 | Optional |
| `security` | stale 처리 예외 | Optional |
| `blocked` | stale 처리 예외 | Optional |

## Pull Request Policy

기본 설정은 PR을 자동 close하지 않습니다.

```yaml
days-before-pr-close: -1
```

PR 자동 close를 사용하려면 팀의 리뷰/배포 흐름에 맞춰 값을 정합니다.

예시:

```yaml
days-before-pr-close: 14
```

참고사항:

| Policy | Setting | Usage |
| --- | --- | --- |
| PR 자동 close 비활성화 | `days-before-pr-close: -1` | 장기 작업 PR이나 draft PR이 많은 프로젝트 |
| PR stale 이후 14일 뒤 close | `days-before-pr-close: 14` | PR을 짧은 주기로 정리하는 팀 프로젝트 |
| PR stale 이후 30일 뒤 close | `days-before-pr-close: 30` | 리뷰 주기가 길지만 오래된 PR은 정리하고 싶은 프로젝트 |

PR 자동 close를 켜면 stale 라벨이 붙은 뒤 지정한 기간 동안 활동이 없는 PR이 닫힙니다.
다시 열 수는 있지만, 작업자가 놓칠 수 있으므로 팀 합의 후 적용하는 것을 권장합니다.

단, 장기 작업 브랜치나 릴리즈 브랜치를 사용하는 프로젝트에서는 PR 자동 close가 혼란을 만들 수 있으므로 신중하게 적용합니다.

## Issue Close Policy

issue는 30일 동안 활동이 없으면 stale 라벨을 붙이고, stale 이후 14일 동안 활동이 없으면 자동으로 닫습니다.

```yaml
days-before-issue-stale: 30
days-before-issue-close: 14
```

자동 close가 부담스럽다면 다음처럼 close를 비활성화하고 라벨링만 사용할 수 있습니다.

```yaml
days-before-issue-close: -1
```

## Recommended Customization

프로젝트 성격에 따라 다음 값을 조정합니다.

| Project Type | Suggested Policy |
| --- | --- |
| Short-term project | stale label only, no auto close |
| Team product | issue auto close, PR label only |
| Open source project | issue and PR auto close with clear messages |
| Security-heavy project | add more exempt labels |

## Usage Rules

- 이 브랜치는 선택 적용을 권장합니다.
- 프로젝트에서 issue를 적극적으로 운영할 때 적용합니다.
- 적용 전 `status/stale` 라벨이 있는지 확인합니다.
- 자동 close가 부담스럽다면 `days-before-issue-close: -1`로 바꿉니다.
- 보안, 차단, 고정 항목에는 예외 라벨을 붙입니다.

## Recommended Import

이 설정은 GitHub issue 운영 방식이 정해진 뒤 적용하는 것을 권장합니다.

```bash
git merge --squash origin/github/stale-issues
git commit -m "init: add stale issues workflow"
```

## Standalone Usage

이 브랜치만 가져올 때는 workflow가 사용하는 라벨(status/stale, pinned,
security, blocked)을 GitHub에서 직접 생성해야 합니다. 라벨이 없으면 stale
처리 시 라벨 부여가 실패합니다.

## Works With

`github/labels`를 함께 적용하면 필요한 라벨이 labels.json에 이미 정의되어
있어 동기화만으로 준비가 끝납니다.
