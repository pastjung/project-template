# Redis Docker Template

이 브랜치는 Redis를 Dockerfile과 Docker Compose로 실행하기 위한 초기 설정을 제공합니다.

## Files

```text
Dockerfile
docker-compose.yml
.env.example
redis.conf
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
| `REDIS_CONTAINER_NAME` | 컨테이너 이름 |
| `REDIS_PORT` | 호스트에서 노출할 Redis 포트 |
| `REDIS_PASSWORD` | Redis 접속 비밀번호 |
| `REDIS_TIMEZONE` | 컨테이너 timezone |

`REDIS_PASSWORD`는 로컬 개발용 예시값 그대로 사용하지 말고 프로젝트별 값으로 변경합니다.

## Run

```bash
docker compose up -d --build
```

상태 확인:

```bash
docker compose ps
docker compose logs -f redis
```

접속:

```bash
docker compose exec redis redis-cli -a "$REDIS_PASSWORD"
```

간단한 확인:

```bash
docker compose exec redis redis-cli -a "$REDIS_PASSWORD" ping
```

## Stop

```bash
docker compose down
```

volume까지 삭제하려면 다음 명령을 사용합니다.

```bash
docker compose down -v
```

## Configuration

Redis 설정은 `redis.conf`에서 관리합니다.

기본 설정:

- 컨테이너 내부의 모든 인터페이스에서 접속 허용
- protected mode 활성화
- AOF persistence 활성화
- 기본 snapshot save 정책 유지
- `noeviction` maxmemory policy 사용

비밀번호는 `docker-compose.yml`의 command에서 `.env`의 `REDIS_PASSWORD`를 사용해 주입합니다.

## Network And Security

이 템플릿은 로컬 개발에서 바로 접속하기 쉽도록 호스트 포트를 열어 둡니다.

```yaml
ports:
  - "${REDIS_PORT:-6379}:6379"
```

`redis.conf`의 `bind 0.0.0.0`도 컨테이너 네트워크 안에서 Redis가 요청을 받을 수 있게 하기 위한 개발용 기본값입니다.
운영 환경에서는 이 설정을 그대로 공개 네트워크에 노출하지 않습니다.

운영 또는 공유 개발 환경에서는 다음 기준을 적용합니다.

- Redis 포트를 인터넷에 직접 노출하지 않습니다.
- 애플리케이션 컨테이너와 같은 private network 안에서만 접근하게 합니다.
- 외부 접속이 꼭 필요하면 방화벽, 보안 그룹, VPN, private subnet으로 접근 대상을 제한합니다.
- `REDIS_PASSWORD`는 충분히 긴 값으로 바꾸고 secret manager 또는 배포 환경 변수로 관리합니다.
- 로그, README, issue, PR에 실제 Redis 비밀번호를 남기지 않습니다.

Docker Compose 내부 서비스에서만 Redis를 사용할 프로젝트라면 `ports` 항목을 제거하고 Compose network를 통해 `redis:6379`로 접근하는 방식을 우선 고려합니다.

## Import To Dev

`dev` 브랜치에서 Redis 템플릿을 가져옵니다.

Single Commit Mode:

```bash
git read-tree --prefix=data/redis/ -u origin/data/redis
git commit -m "init: add Redis"
```

Full History Mode:

```bash
git subtree add --prefix=data/redis origin/data/redis
```
