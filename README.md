# Spark 템플릿

로컬 개발에서 사용할 수 있는 Apache Spark 클러스터 템플릿입니다. Spark master 1개와 worker 1개로 구성하고, 간단한 PySpark 예제를 포함합니다.

공식 `apache/spark` 이미지를 사용합니다. (Bitnami 공개 카탈로그는 2025년 8월
종료되어 `bitnami/spark` 태그는 더 이상 갱신되지 않습니다.)

## 구성

```text
docker-compose.yml   Spark master/worker 실행 구성
.env.example         Worker 환경 변수 예시 (.env로 복사해 사용)
.gitignore           .env 제외 규칙
jobs/example.py      PySpark 예제 작업
README.md            사용 가이드
```

## 환경 변수

worker 리소스는 `.env`로 조정합니다. master는 환경 변수가 필요 없습니다.

```text
SPARK_WORKER_MEMORY   worker 메모리 (예: 1G)
SPARK_WORKER_CORES    worker 코어 수 (예: 1)
```

## 실행

```bash
cp .env.example .env
docker compose up -d
```

Spark master UI:

```text
http://localhost:8080
```

Spark master:

```text
spark://localhost:7077
```

master가 healthy 상태가 된 뒤 worker가 시작되고 자동으로 등록됩니다.
master UI의 Workers 목록에서 확인할 수 있습니다.

## 예제 작업 실행

```bash
docker compose exec spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 /opt/spark/jobs/example.py
```

## Worker 확장

worker는 `container_name`을 고정하지 않으므로 scale 옵션으로 늘릴 수 있습니다.

```bash
docker compose up -d --scale spark-worker=2
```

## 종료

```bash
docker compose down
```
