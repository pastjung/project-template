---
branch: git/hooks
description: 의존성 없는 커밋 메시지 검사 hook (Conventional Commits 강제)
provides:
  - .githooks/commit-msg
  - .githooks/.gitattributes
  - docs/git-hooks.md
requires: []
works-with:
  - branch: standards/commit-strategy
    reason: 이 hook이 강제하는 type 목록의 기준 문서
  - branch: github/semantic-pr
    reason: 로컬(hook)과 PR(workflow) 양쪽에서 같은 규칙을 검사
conflicts: []
placeholders: []
secrets: []
after-import:
  - 각 팀원이 git config core.hooksPath .githooks 실행 (또는 setup 스크립트에 포함)
verify:
  - sh -n .githooks/commit-msg
---

# Git Hooks Guide

이 문서는 커밋 메시지 규칙을 로컬에서 강제하는 git hook의 운영 기준을
정의합니다.

## Purpose

`standards/commit-strategy`의 커밋 규칙은 문서만으로는 강제되지 않습니다.
이 브랜치는 **의존성 없는 POSIX sh 스크립트**로 commit 시점에 형식을
검사합니다. Node 프로젝트가 아니어도 동작합니다.

## Setup

hook은 자동으로 활성화되지 않습니다. clone 후 한 번 실행합니다.

```bash
git config core.hooksPath .githooks
```

팀 전체에 강제하려면 프로젝트 setup 스크립트나 README 온보딩 절차에 위
명령을 포함합니다.

## Rules

- 첫 줄이 `<type>(<scope>): <subject>` 형식이어야 합니다 (scope 선택).
- gitmoji 병용 형식(`✨ feat: ...`)도 허용합니다.
- merge, revert, fixup!, squash! 커밋은 검사하지 않습니다.
- 허용 type: `init feat fix build chore ci docs style refactor test perf
  revert release` (`standards/commit-strategy`와 동일)

## commitlint Alternative

Node 기반 프로젝트에서 더 정교한 검사(빈 subject, 대문자, 길이 제한)가
필요하면 husky + commitlint로 대체할 수 있습니다.

```bash
npm install -D husky @commitlint/cli @commitlint/config-conventional
npx husky init
echo 'npx --no -- commitlint --edit "$1"' > .husky/commit-msg
```

```js
// commitlint.config.js — 비표준 type(init, release)을 등록해야 합니다.
export default {
  extends: ["@commitlint/config-conventional"],
  rules: {
    "type-enum": [
      2,
      "always",
      ["init", "feat", "fix", "build", "chore", "ci", "docs", "style",
       "refactor", "test", "perf", "revert", "release"],
    ],
  },
};
```

단, commitlint는 이모지 접두 형식을 인식하지 못하므로 gitmoji를 쓰는 팀은
이 브랜치의 sh hook을 유지하는 것을 권장합니다.

## Standalone Usage

이 브랜치만 가져와도 `core.hooksPath` 설정 후 즉시 동작합니다. 어떤 언어
스택에도 의존하지 않습니다.

## Works With

`standards/commit-strategy`(규칙 정의), `github/semantic-pr`(PR 제목 검사)과
함께 쓰면 로컬 커밋과 PR 제목이 같은 기준으로 검사됩니다.
