# Docs Import Guide

이 문서는 문서형 운영 기준 브랜치를 `dev` 브랜치로 가져오는 명령어를 정리합니다.

`docs/*` 브랜치는 최종 프로젝트에 들어갈 문서 파일을 그대로 관리합니다.

## Available Branches

| Branch | Description | Result Path |
| --- | --- | --- |
| `docs/branch-strategy` | 프로젝트 브랜치 전략 | `docs/branch-strategy.md` |
| `docs/commit-strategy` | 커밋 단위, 메시지, gitmoji 전략 | `docs/commit-strategy.md` |
| `docs/code-convention` | 공통 코드 컨벤션 | `docs/code-convention.md` |

## Before Import

```bash
git switch dev
git fetch origin
```

## Branch Strategy

Single Commit Mode:

```bash
git merge --squash origin/docs/branch-strategy
git commit -m "init: add branch strategy"
```

Full History Mode:

```bash
git merge --no-ff -m "init: merge branch strategy" origin/docs/branch-strategy
```

## Commit Strategy

Single Commit Mode:

```bash
git merge --squash origin/docs/commit-strategy
git commit -m "init: add commit strategy"
```

Full History Mode:

```bash
git merge --no-ff -m "init: merge commit strategy" origin/docs/commit-strategy
```

## Code Convention

Single Commit Mode:

```bash
git merge --squash origin/docs/code-convention
git commit -m "init: add code convention"
```

Full History Mode:

```bash
git merge --no-ff -m "init: merge code convention" origin/docs/code-convention
```

