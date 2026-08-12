# Standards Import Guide

이 문서는 문서형 운영 기준 브랜치를 `dev` 브랜치로 가져오는 명령어를 정리합니다.

`standards/*` 브랜치는 최종 프로젝트에 들어갈 문서 파일을 그대로 관리합니다.

## Available Branches

| Branch | Description | Result Path |
| --- | --- | --- |
| `standards/branch-strategy` | 프로젝트 브랜치 전략 | `docs/standards-branch-strategy.md` |
| `standards/commit-strategy` | 커밋 단위, 메시지, gitmoji 전략 | `docs/standards-commit-strategy.md` |
| `standards/code-convention` | 공통 코드 컨벤션 | `docs/standards-code-convention.md` |

## Before Import

```bash
git switch dev
git fetch origin
```

## Branch Strategy

Single Commit Mode:

```bash
git merge --squash origin/standards/branch-strategy
git commit -m "init: add branch strategy"
```

Full History Mode:

```bash
git merge --no-ff -m "init: merge branch strategy" origin/standards/branch-strategy
```

## Commit Strategy

Single Commit Mode:

```bash
git merge --squash origin/standards/commit-strategy
git commit -m "init: add commit strategy"
```

Full History Mode:

```bash
git merge --no-ff -m "init: merge commit strategy" origin/standards/commit-strategy
```

## Code Convention

Single Commit Mode:

```bash
git merge --squash origin/standards/code-convention
git commit -m "init: add code convention"
```

Full History Mode:

```bash
git merge --no-ff -m "init: merge code convention" origin/standards/code-convention
```

