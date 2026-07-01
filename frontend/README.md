# Frontend Import Guide

이 문서는 Frontend 계열 브랜치 전체 목록과 공통 import 규칙을 정리합니다.

Frontend 템플릿은 `frontend/<name>-app/` 아래로 가져옵니다. 실제로 가져오는 명령어는
하위 README에서 관리합니다.

## Groups

| Group | Guide | Description |
| --- | --- | --- |
| Frontend apps | [apps/README.md](apps/README.md) | React + Vite, Vue + Vite |

## Available Branches

| Branch | Result Path |
| --- | --- |
| `frontend/react-vite` | `frontend/react-vite-app/` |
| `frontend/vue-vite` | `frontend/vue-vite-app/` |

## Before Import

```bash
git switch dev
git fetch origin
```

## Import Modes

Single Commit Mode:

```bash
git read-tree --prefix=frontend/<name>-app/ -u origin/frontend/<branch-name>
git commit -m "init: add <name> app"
```

Full History Mode:

```bash
git subtree add --prefix=frontend/<name>-app origin/frontend/<branch-name>
```
