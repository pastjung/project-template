# Documentation Standards

이 문서는 모든 서브 브랜치의 `docs/` 문서가 따라야 하는 표준을 정의합니다.
사람이 읽는 가이드이면서, Claude Code나 Codex 같은 Agent가 브랜치를 자동
조립할 때 파싱하는 기준이기도 합니다.

## File Naming Rule

루트 병합 브랜치의 문서 파일명은 브랜치명에서 `/`를 `-`로 치환해 결정합니다.

```
docs/<브랜치명의 '/'를 '-'로 치환>.md
```

- 브랜치명만 알면 문서 경로가 결정되고, 문서명만 알면 브랜치를 역산할 수 있습니다.
- 예: `github/labels` → `docs/github-labels.md`, `standards/commit-strategy` → `docs/standards-commit-strategy.md`

전체 브랜치의 표준 문서 경로는 다음과 같습니다.

| Branch | Document |
| --- | --- |
| `settings/editor-config` | `docs/settings-editor-config.md` |
| `git/attributes` | `docs/git-attributes.md` |
| `git/ignore` | `docs/git-ignore.md` |
| `git/hooks` | `docs/git-hooks.md` |
| `standards/branch-strategy` | `docs/standards-branch-strategy.md` |
| `standards/commit-strategy` | `docs/standards-commit-strategy.md` |
| `standards/code-convention` | `docs/standards-code-convention.md` |
| `github/pr-template` | `docs/github-pr-template.md` |
| `github/issue-template` | `docs/github-issue-template.md` |
| `github/labels` | `docs/github-labels.md` |
| `github/codeowners` | `docs/github-codeowners.md` |
| `github/semantic-pr` | `docs/github-semantic-pr.md` |
| `github/stale-issues` | `docs/github-stale-issues.md` |
| `github/slack-notification` | `docs/github-slack-notification.md` |
| `github/ci` | `docs/github-ci.md` |
| `github/dependabot` | `docs/github-dependabot.md` |
| `github/release` | `docs/github-release.md` |
| `github/community` | `docs/github-community.md` |
| `ai/review-guide` | `docs/ai-review-guide.md` |
| `ai/review-openai` | `docs/ai-review-openai.md` |
| `ai/review-gemini` | `docs/ai-review-gemini.md` |
| `ai/review-claude` | `docs/ai-review-claude.md` |
| `ai/review-copilot` | `docs/ai-review-copilot.md` |
| `api/http-response` | `docs/api-http-response.md` |
| `modules/main` | `docs/modules-main.md` |
| `modules/sub` | `docs/modules-sub.md` |
| `modules/sync` | `docs/modules-sync.md` |

`backend/*`, `frontend/*`, `data/*`, `observability/*`처럼 `read-tree --prefix`로
하위 폴더에 들어가는 브랜치는 이 규칙의 대상이 아니며, 자체 README를 사용합니다.

## Front Matter Standard

모든 `docs/*.md` 문서는 상단에 다음 스키마의 YAML front matter를 포함합니다.
Agent는 이 블록만 파싱해서 의존성 그래프, 후속 작업, 검증 명령을 얻습니다.

```yaml
---
branch: github/stale-issues            # 이 문서를 제공하는 브랜치 (필수)
description: 오래된 issue/PR을 stale 처리하는 workflow   # 한 줄 요약 (필수)
provides:                              # 이 브랜치가 추가하는 파일 (필수)
  - .github/workflows/stale-issues.yml
requires: []                           # 없으면 동작 불가한 선행 브랜치 (필수, 없으면 빈 배열)
works-with:                            # 함께 쓰면 좋은 브랜치 + 이유 (필수, 없으면 빈 배열)
  - branch: github/labels
    reason: status/stale, pinned, security, blocked 라벨을 자동 생성
conflicts: []                          # 함께 가져올 때 충돌·모순되는 브랜치 (필수, 없으면 빈 배열)
placeholders: []                       # 병합 후 치환할 값. 예: {file: .github/CODEOWNERS, token: "{{OWNER}}/{{TEAM}}"}
secrets: []                            # 등록 필요한 GitHub secrets. 예: SLACK_WEBHOOK_URL
after-import:                          # 병합 후 수동 작업 목록 (필수, 없으면 빈 배열)
  - 저장소에 status/stale 라벨 존재 확인
verify:                                # 적용 확인 명령 (필수, 없으면 빈 배열)
  - actionlint .github/workflows/stale-issues.yml
---
```

규칙:

- `branch`, `description`, `provides`, `requires`, `works-with`, `conflicts`,
  `after-import`, `verify`는 필수 키입니다. 해당 없으면 빈 배열로 명시합니다.
- `requires`는 "없으면 동작 자체가 불가"일 때만 사용하고, 권장 조합은
  `works-with`에 이유와 함께 적습니다.
- `verify`는 병합 후 성공 여부를 판정할 수 있는 실행 가능한 명령이어야 합니다.

## Placeholder Rule

병합 후 사용자가 치환해야 하는 값은 `{{NAME}}` 형식으로 통일합니다.

| Placeholder | 의미 |
| --- | --- |
| `{{OWNER}}` | GitHub organization 또는 사용자명 |
| `{{TEAM}}` | GitHub team slug |
| `{{REPOSITORY}}` | 저장소 이름 |

- `<owner>`, `<repository>` 같은 꺾쇠 표기는 사용하지 않습니다.
- 새 placeholder가 필요하면 이 표에 먼저 추가한 뒤 사용합니다.
- 각 브랜치는 자신이 사용하는 placeholder를 front matter의 `placeholders`에
  파일 경로와 함께 선언합니다.

## Document Body Structure

front matter 아래 본문은 다음 절을 포함하는 것을 권장합니다.

1. 개요 — 브랜치가 제공하는 것과 목적
2. Standalone Usage — 이 브랜치만 단독으로 가져왔을 때의 동작 조건과 절차
3. Works With — 다른 브랜치와 함께 쓸 때의 연결 시나리오
4. Customization — 프로젝트에 맞게 수정할 지점
5. Limitations — 알려진 한계와 주의사항
