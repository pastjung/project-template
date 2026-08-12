# FastAPI App Template

Production-lean FastAPI starter with a Clean Architecture / DDD-lite layout, versioned API routes, health checks, environment configuration, tests, and Docker support.

## Stack

- FastAPI
- Uvicorn
- Pydantic Settings
- Pytest

## Project Layout

```text
app/
  api/
    v1/
      routes/          FastAPI route handlers
      dependencies.py  Dependency wiring for API adapters
      router.py        Versioned API router
  application/
    use_cases/         Application workflows and orchestration
  domain/
    entities/          Business entities and value objects
    repositories/      Repository interfaces owned by the domain
    services/          Domain services for business rules
    exceptions.py      Domain-level exceptions
  infrastructure/
    database/          Database engine/session setup
    repositories/      Concrete repository implementations
  core/                Application factory and runtime settings
  schemas/             Pydantic request/response DTOs
  main.py              ASGI entrypoint
tests/             Pytest test suite
```

## Architecture

This template uses a pragmatic Clean Architecture / DDD-lite structure rather than full DDD.

Dependency direction:

```text
api -> application -> domain
api -> infrastructure
infrastructure -> domain
```

Layer responsibilities:

- `api`: FastAPI-specific adapters. Keep routing, request parsing, response mapping, and dependency injection here.
- `application`: Use cases. Coordinate domain logic and infrastructure ports without depending on FastAPI.
- `domain`: Business concepts. Keep this layer framework-agnostic and avoid importing FastAPI, SQLAlchemy, or settings.
- `infrastructure`: External systems. Put database sessions, repository implementations, clients, queues, and storage adapters here.
- `schemas`: Transport DTOs. Convert domain objects to API responses and request payloads.
- `core`: Runtime configuration and application bootstrap.

For small CRUD services, this layout can feel heavier than a simple `services/` and `repositories/` split. It pays off once the service has non-trivial business rules, multiple storage adapters, background workers, or tests that should run without FastAPI and a database.

## Run Locally

의존성은 [uv](https://docs.astral.sh/uv/)로 관리합니다 (`uv.lock` 커밋됨).

```bash
cp .env.example .env
uv sync --extra dev
uv run uvicorn app.main:app --reload
```

uv 없이 pip만 쓰는 경우 (requirements 파일은 `uv export`로 생성된 산출물입니다):

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Health check:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/api/v1/health
```

## Test

```bash
uv run pytest
uv run ruff check .
```

## Settings

설정은 `app/core/config.py`의 `Settings`(pydantic-settings)가 담당하고,
라우트/의존성에서는 `Depends(get_settings)`로 주입받습니다. 테스트에서는
`app.dependency_overrides[get_settings]`로 교체할 수 있습니다
(`tests/test_settings_override.py` 참고).

의존성을 변경하면 lock과 requirements를 함께 갱신합니다.

```bash
uv lock
uv export --format requirements-txt --no-hashes --no-dev --no-emit-project -o requirements.txt
uv export --format requirements-txt --no-hashes --extra dev --no-emit-project -o requirements-dev.txt
```

## Docker

개발용:

```bash
cp .env.example .env
docker compose up --build
```

The Compose file is optimized for local development:

- mounts `./app` read-only into the container
- runs Uvicorn with `--reload`
- exposes a Docker healthcheck against `/health`
- loads settings from `.env` (copy of `.env.example`)

배포용:

```bash
docker compose -f docker-compose.prod.yml up --build
```

- bind mount와 `--reload` 없이 실행합니다.
- `APP_ENV=prod`, `DOCS_ENABLED=false`로 API 문서를 비활성화합니다.
