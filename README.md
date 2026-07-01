# MongoDB Docker Template

이 브랜치는 MongoDB를 Dockerfile과 Docker Compose로 실행하기 위한 초기 설정을
제공합니다.

## Files

```text
Dockerfile
docker-compose.yml
.env.example
initdb/001-init.js
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
| `MONGO_CONTAINER_NAME` | 컨테이너 이름 |
| `MONGO_PORT` | 호스트에서 노출할 MongoDB 포트 |
| `MONGO_INITDB_ROOT_USERNAME` | root 계정 이름 |
| `MONGO_INITDB_ROOT_PASSWORD` | root 계정 비밀번호 |
| `MONGO_INITDB_DATABASE` | 기본 앱 데이터베이스 |
| `MONGO_APP_USER` | 앱 전용 사용자 |
| `MONGO_APP_PASSWORD` | 앱 전용 사용자 비밀번호 |
| `MONGO_TIMEZONE` | 컨테이너 timezone |

## Run

```bash
docker compose up -d --build
```

상태 확인:

```bash
docker compose ps
docker compose logs -f mongodb
```

root 계정으로 접속:

```bash
docker compose exec mongodb mongosh \
  -u "$MONGO_INITDB_ROOT_USERNAME" \
  -p "$MONGO_INITDB_ROOT_PASSWORD" \
  --authenticationDatabase admin
```

앱 계정 접속 URI:

```text
mongodb://app:app-password@localhost:27017/app?authSource=app
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

## Initial Script

초기화 스크립트는 `initdb/` 아래에 둡니다.

```text
initdb/001-init.js
```

MongoDB 공식 이미지의 entrypoint는 최초 데이터 디렉터리 생성 시
`/docker-entrypoint-initdb.d/` 아래의 JavaScript 파일을 실행합니다.

현재 스크립트는 다음 작업을 수행합니다.

- 앱 데이터베이스 선택
- 앱 사용자 생성
- `health_check` 컬렉션 생성
- 초기 health check document 삽입

이미 volume이 생성된 뒤 스크립트를 다시 실행하려면 volume을 삭제하고 다시
시작합니다.

```bash
docker compose down -v
docker compose up -d --build
```

## Import To Dev

`dev` 브랜치에서 MongoDB 템플릿을 가져옵니다.

Single Commit Mode:

```bash
git read-tree --prefix=data/mongodb/ -u origin/data/mongodb
git commit -m "init: add MongoDB"
```

Full History Mode:

```bash
git subtree add --prefix=data/mongodb origin/data/mongodb
```
