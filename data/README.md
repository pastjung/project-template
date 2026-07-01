# Data Import Guide

이 문서는 Data 계열 브랜치 전체 목록과 공통 import 규칙을 정리합니다.

Data 템플릿은 `data/<name>/` 아래로 가져옵니다. 실제로 가져오는 명령어는 하위
README에서 관리합니다.

## Groups

| Group | Guide | Description |
| --- | --- | --- |
| Databases and cache | [databases/README.md](databases/README.md) | MySQL, PostgreSQL, MongoDB, Redis |
| Data streaming and batch | [pipelines/README.md](pipelines/README.md) | Kafka, Flink, Spark, Airflow |

## Available Branches

| Branch | Result Path |
| --- | --- |
| `data/mysql` | `data/mysql/` |
| `data/postgresql` | `data/postgresql/` |
| `data/mongodb` | `data/mongodb/` |
| `data/redis` | `data/redis/` |
| `data/kafka` | `data/kafka/` |
| `data/flink` | `data/flink/` |
| `data/spark` | `data/spark/` |
| `data/airflow` | `data/airflow/` |

## Before Import

```bash
git switch dev
git fetch origin
```

## Import Modes

Single Commit Mode:

```bash
git read-tree --prefix=data/<name>/ -u origin/data/<branch-name>
git commit -m "init: add <name>"
```

Full History Mode:

```bash
git subtree add --prefix=data/<name> origin/data/<branch-name>
```
