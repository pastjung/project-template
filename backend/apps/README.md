# Backend Apps Import Guide

이 문서는 Backend 애플리케이션 브랜치를 `dev` 브랜치로 가져오는 명령어를 정리합니다.

## Available Branches

| Branch | Description | Result Path |
| --- | --- | --- |
| `backend/spring-boot` | Spring Boot 초기 프로젝트 템플릿 | `backend/spring-boot-app/` |
| `backend/fastapi` | FastAPI 초기 프로젝트 템플릿 | `backend/fastapi-app/` |
| `backend/django` | Django 초기 프로젝트 템플릿 | `backend/django-app/` |

## Before Import

```bash
git switch dev
git fetch origin
```

## Spring Boot

Single Commit Mode:

```bash
git read-tree --prefix=backend/spring-boot-app/ -u origin/backend/spring-boot
git commit -m "init: add Spring Boot app"
```

Full History Mode:

```bash
git subtree add --prefix=backend/spring-boot-app origin/backend/spring-boot
```

## FastAPI

Single Commit Mode:

```bash
git read-tree --prefix=backend/fastapi-app/ -u origin/backend/fastapi
git commit -m "init: add FastAPI app"
```

Full History Mode:

```bash
git subtree add --prefix=backend/fastapi-app origin/backend/fastapi
```

## Django

Single Commit Mode:

```bash
git read-tree --prefix=backend/django-app/ -u origin/backend/django
git commit -m "init: add Django app"
```

Full History Mode:

```bash
git subtree add --prefix=backend/django-app origin/backend/django
```
