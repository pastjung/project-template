# MySQL Docker Template

이 브랜치는 MySQL을 Dockerfile과 Docker Compose로 실행하기 위한 초기 설정을
제공합니다.

## Files

```text
Dockerfile
docker-compose.yml
.env.example
conf.d/my.cnf
initdb/001-init.sql
```

## Requirements

- Docker
- Docker Compose

## Environment

`.env.example`을 복사해 `.env`를 생성합니다.

```bash
cp .env.example .env
```

환경 변수:

| Name | Description |
| --- | --- |
| `MYSQL_CONTAINER_NAME` | 컨테이너 이름 |
| `MYSQL_PORT` | 호스트에서 노출할 MySQL 포트 |
| `MYSQL_ROOT_PASSWORD` | root 계정 비밀번호 |
| `MYSQL_DATABASE` | 기본 생성 데이터베이스 |
| `MYSQL_USER` | 기본 생성 사용자 |
| `MYSQL_PASSWORD` | 기본 생성 사용자 비밀번호 |
| `MYSQL_TIMEZONE` | 컨테이너 timezone |

## Run

```bash
docker compose up -d --build
```

상태 확인:

```bash
docker compose ps
docker compose logs -f mysql
```

접속:

```bash
docker compose exec mysql mysql -u root -p
```

## Stop

```bash
docker compose down
```

volume까지 삭제하려면 다음 명령을 사용합니다.

```bash
docker compose down -v
```

## Initial SQL

초기 SQL은 `initdb/` 아래에 둡니다.

```text
initdb/001-init.sql
```

MySQL 공식 이미지의 entrypoint는 최초 데이터 디렉터리 생성 시
`/docker-entrypoint-initdb.d/` 아래의 SQL 파일을 실행합니다.

이미 volume이 생성된 뒤 SQL을 다시 실행하려면 volume을 삭제하고 다시 시작합니다.

```bash
docker compose down -v
docker compose up -d --build
```

## Import To Dev

`dev` 브랜치에서 MySQL 템플릿을 가져옵니다.

Single Commit Mode:

```bash
git read-tree --prefix=data/mysql/ -u origin/data/mysql
git commit -m "init: add MySQL"
```

Full History Mode:

```bash
git subtree add --prefix=data/mysql origin/data/mysql
```
