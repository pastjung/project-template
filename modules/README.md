# Module Import Guide

이 문서는 메인 모듈, 서브 모듈, 모듈 동기화 관련 브랜치를 `dev` 브랜치로 가져오는
명령어를 정리합니다.

## Available Branches

| Branch | Description | Result Path |
| --- | --- | --- |
| `modules/main` | 멀티모듈 구조에서 메인 모듈 역할과 운영 기준 | `docs/main-module.md` |
| `modules/sub` | 멀티모듈 구조에서 서브 모듈 역할과 운영 기준 | `docs/sub-module.md` |
| `modules/sync` | 서브 모듈 변경을 메인 모듈 `dev`로 반영하는 자동화 | `.github/workflows/main-module-sync.yml`, `.github/workflows/sub-module-dispatch.yml`, `docs/module-sync.md` |

## Before Import

```bash
git switch dev
git fetch origin
```

## Main Module

Single Commit Mode:

```bash
git merge --squash origin/modules/main
git commit -m "init: add main module guide"
```

Full History Mode:

```bash
git merge --no-ff -m "init: merge main module guide" origin/modules/main
```

## Sub Module

Single Commit Mode:

```bash
git merge --squash origin/modules/sub
git commit -m "init: add sub module guide"
```

Full History Mode:

```bash
git merge --no-ff -m "init: merge sub module guide" origin/modules/sub
```

## Module Sync

Single Commit Mode:

```bash
git merge --squash origin/modules/sync
git commit -m "init: add module sync workflow"
```

Full History Mode:

```bash
git merge --no-ff -m "init: merge module sync workflow" origin/modules/sync
```

## Notes

- `modules/main`과 `modules/sub`은 개념과 운영 기준을 설명합니다.
- `modules/sync`는 서브 모듈 변경을 메인 모듈 `dev`에 PR로 반영하는 실제 자동화입니다.
- module sync는 `submodule` mode와 `subtree` mode를 지원합니다.
