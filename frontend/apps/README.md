# Frontend Apps Import Guide

이 문서는 Frontend 애플리케이션 브랜치를 `dev` 브랜치로 가져오는 명령어를 정리합니다.

## Available Branches

| Branch | Description | Result Path |
| --- | --- | --- |
| `frontend/react-vite` | React + Vite 초기 프로젝트 템플릿 | `frontend/react-vite-app/` |
| `frontend/vue-vite` | Vue + Vite 초기 프로젝트 템플릿 | `frontend/vue-vite-app/` |

## Before Import

```bash
git switch dev
git fetch origin
```

## React + Vite

Single Commit Mode:

```bash
git read-tree --prefix=frontend/react-vite-app/ -u origin/frontend/react-vite
git commit -m "init: add React Vite app"
```

Full History Mode:

```bash
git subtree add --prefix=frontend/react-vite-app origin/frontend/react-vite
```

## Vue + Vite

Single Commit Mode:

```bash
git read-tree --prefix=frontend/vue-vite-app/ -u origin/frontend/vue-vite
git commit -m "init: add Vue Vite app"
```

Full History Mode:

```bash
git subtree add --prefix=frontend/vue-vite-app origin/frontend/vue-vite
```
