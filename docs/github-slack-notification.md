---
branch: github/slack-notification
description: PR/이슈/push/workflow_run 이벤트의 Slack 알림 workflow
provides:
  - .github/workflows/slack-notification.yml
  - docs/github-slack-notification.md
requires: []
works-with: []
conflicts: []
placeholders: []
secrets:
  - SLACK_WEBHOOK_URL
after-import:
  - Slack Incoming Webhook 생성 후 SLACK_WEBHOOK_URL secret 등록
  - workflow_run 대상(CI, CD, Deploy)을 실제 workflow 이름으로 교체
verify:
  - actionlint .github/workflows/slack-notification.yml
---

# Slack Notification Guide

이 문서는 GitHub 저장소 이벤트를 Slack으로 알림 보내는 설정 방법을 정의합니다.

## Files

```text
.github/workflows/slack-notification.yml
docs/slack-notification.md
```

## Workflow Events

기본 workflow는 다음 이벤트를 Slack으로 전송합니다.

| Event | Trigger |
| --- | --- |
| Pull Request | opened, reopened, ready_for_review, closed |
| Issue | opened, closed, reopened |
| Push | `main`, `dev` branch push |
| Workflow Run | `CI`, `CD`, `Deploy` workflow completed |

## Required Settings

Slack Incoming Webhook URL을 GitHub Actions secret으로 등록합니다.

```text
Settings
-> Secrets and variables
-> Actions
-> Repository secrets
-> New repository secret
```

필수 secret:

| Name | Description |
| --- | --- |
| `SLACK_WEBHOOK_URL` | Slack Incoming Webhook URL |

## Slack Incoming Webhook

Slack에서 Incoming Webhook을 생성한 뒤, 알림을 받을 채널을 선택합니다.

### Slack App Setup

Slack workspace에서 다음 순서로 설정합니다.

1. [Slack API](https://api.slack.com/apps) 페이지에서 `Create New App`을 선택합니다.
2. `From scratch`를 선택합니다.
3. App 이름을 입력하고 알림을 보낼 workspace를 선택합니다.
4. App 설정 화면에서 `Incoming Webhooks` 메뉴로 이동합니다.
5. `Activate Incoming Webhooks`를 `On`으로 변경합니다.
6. `Add New Webhook to Workspace`를 선택합니다.
7. GitHub 알림을 받을 Slack channel을 선택합니다.
8. 생성된 webhook URL을 복사합니다.
9. GitHub repository secret에 `SLACK_WEBHOOK_URL` 이름으로 등록합니다.

생성된 webhook URL은 다음과 같은 형태입니다.

```text
https://hooks.slack.com/services/...
```

이 URL은 secret이므로 저장소에 직접 커밋하지 않습니다.

### Slack Permission Notes

- workspace 설정에 따라 App 생성 또는 설치 권한이 필요할 수 있습니다.
- 권한이 없다면 workspace admin에게 App 설치 또는 Incoming Webhook 생성을 요청합니다.
- 알림을 보낼 channel이 private channel이면 App이 해당 channel에 초대되어 있어야 합니다.
- 알림 channel을 바꾸려면 Slack App에서 webhook을 새로 만들거나 기존 webhook 설정을 변경합니다.

## Notification Rules

- `main` push는 배포 또는 릴리즈와 가까운 이벤트로 간주합니다.
- `dev` push는 개발 통합 이벤트로 간주합니다.
- PR close 이벤트는 merge 여부에 따라 성공 또는 종료 알림으로 구분합니다.
- workflow 실패는 Slack에서 빠르게 확인할 수 있게 빨간색 알림으로 표시합니다.
- 너무 많은 알림이 발생하면 이벤트 범위를 줄입니다.

## Customization

알림 범위를 줄이고 싶다면 workflow의 `on` 섹션을 수정합니다.

PR 알림만 사용:

```yaml
on:
  pull_request:
    types:
      - opened
      - ready_for_review
      - closed
```

workflow 실패만 사용:

```yaml
on:
  workflow_run:
    workflows:
      - CI
    types:
      - completed
```

이 경우 workflow 내부에서 `workflow.conclusion`이 `success`가 아닐 때만 전송하도록 조건을 추가할 수 있습니다.

주의: `workflow_run.workflows`의 값은 대상 workflow 파일의 `name:` 값과
**정확히 일치**해야 합니다. 이 템플릿의 기본값(`CI`, `CD`, `Deploy`)은
예시이며, 해당 이름의 workflow가 저장소에 없으면 workflow_run 알림은
발생하지 않습니다. 실제 사용하는 workflow 이름으로 교체하세요.

## Security Rules

- `SLACK_WEBHOOK_URL`은 반드시 GitHub Secret으로 관리합니다.
- webhook URL을 README, issue, PR, log에 노출하지 않습니다.
- webhook URL이 노출되었다면 Slack에서 기존 webhook을 폐기하고 새로 발급합니다.
- 조직에서 Slack App 권한 정책이 있다면 Incoming Webhook 사용 가능 여부를 먼저 확인합니다.

## Branch Strategy Integration

브랜치 전략과 함께 사용할 때 권장 알림 기준은 다음과 같습니다.

| Branch/Event | Notification Purpose |
| --- | --- |
| `feat/*` PR opened | 기능 개발 리뷰 시작 알림 |
| `bugfix/*` PR opened | 버그 수정 리뷰 시작 알림 |
| `release/*` PR opened | 릴리즈 검증 시작 알림 |
| `hotfix/*` PR opened | 긴급 수정 리뷰 시작 알림 |
| `main` push | 릴리즈 또는 운영 반영 알림 |
| CI/CD failure | 빠른 장애 확인 |

## Import Command

`dev` 브랜치에서 이 설정을 가져올 때는 다음 명령을 사용합니다.

```bash
git merge --squash origin/github/slack-notification
git commit -m "init: add Slack notifications"
```

## References

이 브랜치는 GitHub Actions에서 Slack Incoming Webhook으로 알림을 보내는 템플릿입니다.

Slack 채널에서 GitHub App을 설치하고 `/github subscribe` 명령으로 저장소를 구독하는 방식도 사용할 수 있습니다.
이 방식은 workflow 파일 없이 Slack과 GitHub를 직접 연결할 때 적합합니다.

- [Slack Incoming Webhooks 공식 문서](https://api.slack.com/messaging/webhooks)
- [GitHub Slack integration 공식 문서](https://github.com/integrations/slack)
- [Slack과 GitHub 연동 방법 정리](https://velog.io/@chwogus/Github-Slack%EA%B3%BC-Github-%EC%97%B0%EB%8F%99-%EB%B0%A9%EB%B2%95)

## Standalone Usage

`SLACK_WEBHOOK_URL` secret만 등록하면 PR/이슈/push 알림이 즉시 동작합니다.
secret이 없으면 workflow는 조용히 skip합니다. workflow_run 알림은 해당
이름의 workflow가 실제로 존재해야 발생합니다.

## Works With

CI workflow 브랜치를 도입하면 workflow_run 대상에 그 이름을 등록해 빌드
실패 알림을 받을 수 있습니다.
