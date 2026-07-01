# Git Import Guide

이 문서는 Git 동작에 직접 영향을 주는 설정 브랜치를 `dev` 브랜치로 가져오는
명령어를 정리합니다.

## Available Branches

| Branch | Description | Result Path |
| --- | --- | --- |
| `git/attributes` | 줄 끝 정규화와 binary 파일 처리 기준 | `.gitattributes`, `docs/git-attributes.md` |
| `git/ignore` | 공통 ignore 규칙 | `.gitignore`, `docs/gitignore-guide.md` |

## Before Import

```bash
git switch dev
git fetch origin
```

## Git Attributes

Single Commit Mode:

```bash
git merge --squash origin/git/attributes
git commit -m "init: add git attributes"
```

Full History Mode:

```bash
git merge --no-ff -m "init: merge git attributes" origin/git/attributes
```

## Git Ignore

Single Commit Mode:

```bash
git merge --squash origin/git/ignore
git commit -m "init: add gitignore"
```

Full History Mode:

```bash
git merge --no-ff -m "init: merge gitignore" origin/git/ignore
```
