# GitHub Import Guide

이 문서는 GitHub 템플릿, 라벨, Actions workflow 관련 브랜치를 `dev` 브랜치로
가져오는 명령어를 정리합니다.

## Available Branches

| Branch | Description | Result Path |
| --- | --- | --- |
| `github/pr-template` | 브랜치 타입별 Pull Request 템플릿 | `.github/PULL_REQUEST_TEMPLATE/`, `docs/pr-template-guide.md` |
| `github/issue-template` | 용도별 Issue 템플릿 | `.github/ISSUE_TEMPLATE/`, `docs/issue-template-guide.md` |
| `github/labels` | GitHub 라벨 운영 기준과 라벨 정의 | `.github/labels.json`, `docs/label-strategy.md` |
| `github/semantic-pr` | PR 제목을 Conventional Commits 형식으로 검사하는 workflow | `.github/workflows/semantic-pr.yml`, `docs/semantic-pr.md` |
| `github/stale-issues` | 오래된 issue와 PR을 표시하고 정리하는 workflow | `.github/workflows/stale-issues.yml`, `docs/stale-issues.md` |
| `github/slack-notification` | GitHub 이벤트 Slack 알림 workflow | `.github/workflows/slack-notification.yml`, `docs/slack-notification.md` |
| `github/codeowners` | 경로별 code owner와 리뷰 담당 기준 | `.github/CODEOWNERS`, `docs/codeowners-guide.md` |

## Before Import

```bash
git switch dev
git fetch origin
```

## Pull Request Template

Single Commit Mode:

```bash
git merge --squash origin/github/pr-template
git commit -m "init: add PR templates"
```

Full History Mode:

```bash
git merge --no-ff -m "init: merge PR templates" origin/github/pr-template
```

## Issue Template

Single Commit Mode:

```bash
git merge --squash origin/github/issue-template
git commit -m "init: add issue templates"
```

Full History Mode:

```bash
git merge --no-ff -m "init: merge issue templates" origin/github/issue-template
```

## Labels

Single Commit Mode:

```bash
git merge --squash origin/github/labels
git commit -m "init: add GitHub labels"
```

Full History Mode:

```bash
git merge --no-ff -m "init: merge GitHub labels" origin/github/labels
```

## Semantic PR

Single Commit Mode:

```bash
git merge --squash origin/github/semantic-pr
git commit -m "init: add semantic PR workflow"
```

Full History Mode:

```bash
git merge --no-ff -m "init: merge semantic PR workflow" origin/github/semantic-pr
```

## Stale Issues

Single Commit Mode:

```bash
git merge --squash origin/github/stale-issues
git commit -m "init: add stale issues workflow"
```

Full History Mode:

```bash
git merge --no-ff -m "init: merge stale issues workflow" origin/github/stale-issues
```

## Slack Notification

Single Commit Mode:

```bash
git merge --squash origin/github/slack-notification
git commit -m "init: add Slack notifications"
```

Full History Mode:

```bash
git merge --no-ff -m "init: merge Slack notifications" origin/github/slack-notification
```

## CODEOWNERS

Single Commit Mode:

```bash
git merge --squash origin/github/codeowners
git commit -m "init: add CODEOWNERS"
```

Full History Mode:

```bash
git merge --no-ff -m "init: merge CODEOWNERS" origin/github/codeowners
```

## Notes

- Issue Template의 front matter는 GitHub가 자동으로 인식합니다.
- Issue Template에서 사용하는 라벨은 `github/labels`의 `.github/labels.json`과 맞춰 관리합니다.
- `github/semantic-pr`는 `docs/commit-strategy`의 commit type과 같은 기준을 사용합니다.
- `github/stale-issues`를 적용하기 전 `status/stale` 라벨이 있는지 확인합니다.
- Slack 알림은 Slack App에서 Incoming Webhook을 만든 뒤 `SLACK_WEBHOOK_URL` secret을 등록해야 합니다.
- CODEOWNERS를 적용한 뒤 branch protection rule에서 `Require review from Code Owners`를 켜면 owner 승인을 병합 조건으로 사용할 수 있습니다.
