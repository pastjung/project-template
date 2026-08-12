# Settings Import Guide

이 문서는 개발 환경 기본값 브랜치를 `dev` 브랜치로 가져오는 명령어를 정리합니다.

## Available Branches

| Branch | Description | Result Path |
| --- | --- | --- |
| `settings/editor-config` | 에디터와 IDE의 기본 파일 포맷 규칙 | `.editorconfig`, `docs/settings-editor-config.md` |

## Before Import

```bash
git switch dev
git fetch origin
```

## EditorConfig

Single Commit Mode:

```bash
git merge --squash origin/settings/editor-config
git commit -m "init: add editor config"
```

Full History Mode:

```bash
git merge --no-ff -m "init: merge editor config" origin/settings/editor-config
```
