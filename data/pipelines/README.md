# Data Streaming And Batch Import Guide

이 문서는 data streaming과 batch 처리 관련 브랜치를 `dev` 브랜치로 가져오는 명령어를
정리합니다.

## Available Branches

| Branch | Description | Result Path |
| --- | --- | --- |
| `data/kafka` | Kafka 실행 템플릿 | `data/kafka/` |
| `data/flink` | Flink 실행 템플릿 | `data/flink/` |
| `data/spark` | Spark 실행 템플릿 | `data/spark/` |
| `data/airflow` | Airflow 실행 템플릿 | `data/airflow/` |

## Before Import

```bash
git switch dev
git fetch origin
```

## Kafka

Single Commit Mode:

```bash
git read-tree --prefix=data/kafka/ -u origin/data/kafka
git commit -m "init: add Kafka"
```

Full History Mode:

```bash
git subtree add --prefix=data/kafka origin/data/kafka
```

## Flink

Single Commit Mode:

```bash
git read-tree --prefix=data/flink/ -u origin/data/flink
git commit -m "init: add Flink"
```

Full History Mode:

```bash
git subtree add --prefix=data/flink origin/data/flink
```

## Spark

Single Commit Mode:

```bash
git read-tree --prefix=data/spark/ -u origin/data/spark
git commit -m "init: add Spark"
```

Full History Mode:

```bash
git subtree add --prefix=data/spark origin/data/spark
```

## Airflow

Single Commit Mode:

```bash
git read-tree --prefix=data/airflow/ -u origin/data/airflow
git commit -m "init: add Airflow"
```

Full History Mode:

```bash
git subtree add --prefix=data/airflow origin/data/airflow
```
