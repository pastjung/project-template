# Databases And Cache Import Guide

이 문서는 database와 cache 브랜치를 `dev` 브랜치로 가져오는 명령어를 정리합니다.

## Available Branches

| Branch | Description | Result Path |
| --- | --- | --- |
| `data/mysql` | MySQL 실행 템플릿 | `data/mysql/` |
| `data/postgresql` | PostgreSQL 실행 템플릿 | `data/postgresql/` |
| `data/mongodb` | MongoDB 실행 템플릿 | `data/mongodb/` |
| `data/redis` | Redis 실행 템플릿 | `data/redis/` |

## Before Import

```bash
git switch dev
git fetch origin
```

## MySQL

Single Commit Mode:

```bash
git read-tree --prefix=data/mysql/ -u origin/data/mysql
git commit -m "init: add MySQL"
```

Full History Mode:

```bash
git subtree add --prefix=data/mysql origin/data/mysql
```

## PostgreSQL

Single Commit Mode:

```bash
git read-tree --prefix=data/postgresql/ -u origin/data/postgresql
git commit -m "init: add PostgreSQL"
```

Full History Mode:

```bash
git subtree add --prefix=data/postgresql origin/data/postgresql
```

## MongoDB

Single Commit Mode:

```bash
git read-tree --prefix=data/mongodb/ -u origin/data/mongodb
git commit -m "init: add MongoDB"
```

Full History Mode:

```bash
git subtree add --prefix=data/mongodb origin/data/mongodb
```

## Redis

Single Commit Mode:

```bash
git read-tree --prefix=data/redis/ -u origin/data/redis
git commit -m "init: add Redis"
```

Full History Mode:

```bash
git subtree add --prefix=data/redis origin/data/redis
```
