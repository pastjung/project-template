
# PostgreSQL Docker Template

이 브랜치는 PostgreSQL을 Dockerfile과 Docker Compose로 실행하기 위한 초기 설정을
제공합니다.

## Files

```text
Dockerfile
docker-compose.yml
.env.example
conf.d/postgresql.conf
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
| `POSTGRES_CONTAINER_NAME` | 컨테이너 이름 |
| `POSTGRES_PORT` | 호스트에서 노출할 PostgreSQL 포트 |
| `POSTGRES_DB` | 기본 생성 데이터베이스 |
| `POSTGRES_USER` | 기본 생성 사용자 |
| `POSTGRES_PASSWORD` | 기본 생성 사용자 비밀번호 |
| `POSTGRES_TIMEZONE` | 컨테이너 timezone |

`POSTGRES_PASSWORD`는 로컬 개발용 예시값 그대로 사용하지 말고 프로젝트별 값으로
변경합니다.

## Run

```bash
docker compose up -d --build
```

상태 확인:

```bash
docker compose ps
docker compose logs -f postgresql
```

접속:

```bash
docker compose exec postgresql psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"
```

호스트에서 접속할 때는 `.env`의 포트와 계정 정보를 사용합니다.

```bash
psql "postgresql://app:app-password@localhost:5432/app"
```

실제 값은 `.env`에 맞게 변경합니다.

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

PostgreSQL 공식 이미지의 entrypoint는 최초 데이터 디렉터리 생성 시
`/docker-entrypoint-initdb.d/` 아래의 SQL 또는 shell 파일을 실행합니다.

현재 SQL은 다음 작업을 수행하는 용도로 사용합니다.

- 앱 schema 생성
- health check table 생성
- 초기 health check row 삽입
- 필요한 extension 활성화

이미 volume이 생성된 뒤 SQL을 다시 실행하려면 volume을 삭제하고 다시 시작합니다.

```bash
docker compose down -v
docker compose up -d --build
```

## Configuration

PostgreSQL 설정은 `conf.d/postgresql.conf`에서 관리합니다.

기본 설정:

- 컨테이너 내부의 모든 인터페이스에서 접속 허용
- 개발 환경 기준 connection, logging, timezone 설정
- SQL query와 slow query 확인을 위한 기본 로그 설정
- 데이터는 Docker volume에 저장

운영 환경에서는 shared buffers, work mem, checkpoint, WAL, connection 수를 실제
서버 사양과 트래픽에 맞게 조정합니다.

## Network And Security

이 템플릿은 로컬 개발에서 바로 접속하기 쉽도록 호스트 포트를 열어 둡니다.

```yaml
ports:
  - "${POSTGRES_PORT:-5432}:5432"
```

운영 또는 공유 개발 환경에서는 다음 기준을 적용합니다.

- PostgreSQL 포트를 인터넷에 직접 노출하지 않습니다.
- 애플리케이션 컨테이너와 같은 private network 안에서만 접근하게 합니다.
- 외부 접속이 꼭 필요하면 방화벽, 보안 그룹, VPN, private subnet으로 접근 대상을 제한합니다.
- `POSTGRES_PASSWORD`는 충분히 긴 값으로 바꾸고 secret manager 또는 배포 환경 변수로 관리합니다.
- 로그, README, issue, PR에 실제 PostgreSQL 비밀번호를 남기지 않습니다.
- 앱 계정에는 필요한 schema와 table 권한만 부여합니다.

Docker Compose 내부 서비스에서만 PostgreSQL을 사용할 프로젝트라면 `ports` 항목을
제거하고 Compose network를 통해 `postgresql:5432`로 접근하는 방식을 우선 고려합니다.

## Import To Dev

`dev` 브랜치에서 PostgreSQL 템플릿을 가져옵니다.

Single Commit Mode:

```bash
git read-tree --prefix=data/postgresql/ -u origin/data/postgresql
git commit -m "init: add PostgreSQL"
```

Full History Mode:

```bash
git subtree add --prefix=data/postgresql origin/data/postgresql
```
