# Airflow 템플릿

로컬 DAG 개발을 위한 Apache Airflow 템플릿입니다. PostgreSQL metadata DB, webserver, scheduler, 초기화 컨테이너로 구성합니다.

## 구성

```text
docker-compose.yml       Airflow 실행 구성
.env.airflow.example     Airflow 환경 변수 예시 (.env.airflow로 복사해 사용)
.env.postgres.example    PostgreSQL 환경 변수 예시 (.env.postgres로 복사해 사용)
.gitignore               실제 env 파일과 로그 제외 규칙
dags/                DAG 파일 위치
logs/                Airflow 로그 위치
plugins/             Airflow plugin 위치
README.md            사용 가이드
```

## 환경 변수

Compose의 `environment:` 블록은 사용하지 않고 `env_file`로 환경 변수를 주입합니다.

주요 값:

```text
AIRFLOW_UID
AIRFLOW__CORE__EXECUTOR
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN
AIRFLOW__CORE__LOAD_EXAMPLES
_AIRFLOW_WWW_USER_USERNAME
_AIRFLOW_WWW_USER_PASSWORD
```

PostgreSQL:

```text
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB
```

compose는 `.env.airflow`, `.env.postgres`를 로드합니다. example 파일을 복사해
만들고, 실제 env 파일은 커밋하지 않습니다 (`.gitignore`에 포함).

## 실행

```bash
cp .env.airflow.example .env.airflow
cp .env.postgres.example .env.postgres
docker compose up -d
```

`airflow-init`이 DB migration과 관리자 계정 생성을 마친 뒤에 webserver와
scheduler가 시작됩니다 (`service_completed_successfully` 의존성). 별도의
init 선실행 단계는 필요 없습니다.

Linux 호스트에서는 bind mount 권한 문제를 막기 위해 호스트 사용자 UID를
`.env`에 설정합니다. (`user:` 값의 `${AIRFLOW_UID}` 보간은 compose가 `.env`
에서 읽습니다. `env_file`은 컨테이너 내부 환경 변수 전용이라 여기에 넣어도
적용되지 않습니다.)

```bash
echo "AIRFLOW_UID=$(id -u)" > .env
```

설정하지 않으면 기본값 `50000`(공식 이미지의 airflow 사용자)을 사용합니다.

Airflow UI:

```text
http://localhost:8080
```

기본 계정은 `.env.airflow`의 `_AIRFLOW_WWW_USER_USERNAME/PASSWORD`입니다.
예시값 `airflow / airflow`는 로컬 개발 전용이며, 외부에 노출되는 환경에서는
반드시 교체합니다.

## DAG 추가

`dags/` 디렉터리에 DAG 파일을 추가하면 Airflow가 주기적으로 감지합니다.

```text
dags/example_dag.py
```

## 종료

```bash
docker compose down
```

metadata DB 볼륨까지 삭제하려면 다음 명령을 사용합니다.

```bash
docker compose down -v
```
