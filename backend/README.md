# Backend Import Guide

이 문서는 Backend 계열 브랜치 전체 목록과 공통 import 규칙을 정리합니다.

Backend 템플릿은 `backend/<name>-app/` 아래로 가져옵니다. 실제로 가져오는 명령어는
하위 README에서 관리합니다.

## Groups

| Group | Guide | Description |
| --- | --- | --- |
| Backend apps | [apps/README.md](apps/README.md) | Spring Boot, FastAPI, Django |

## Available Branches

| Branch | Result Path |
| --- | --- |
| `backend/spring-boot` | `backend/spring-boot-app/` |
| `backend/fastapi` | `backend/fastapi-app/` |
| `backend/django` | `backend/django-app/` |

## Before Import

```bash
git switch dev
git fetch origin
```

## Import Modes

Single Commit Mode:

```bash
git read-tree --prefix=backend/<name>-app/ -u origin/backend/<branch-name>
git commit -m "init: add <name> app"
```

Full History Mode:

```bash
git subtree add --prefix=backend/<name>-app origin/backend/<branch-name>
```
