# Django 앱 템플릿

Django, Django REST Framework 기반의 백엔드 API 템플릿입니다. 현업에서 자주 쓰는 settings 분리, 앱 단위 모듈화, DDD-lite 구조, 테스트, 개발용/배포용 Docker 실행 방식을 포함합니다.

## 기술 스택

- Python 3.12
- Django
- Django REST Framework
- Gunicorn
- Pytest
- Pytest Django
- Ruff

## 프로젝트 구조

```text
apps/
  health/
    api/              DRF View, serializer, URL
    application/      Use case, 애플리케이션 서비스
    domain/           도메인 모델, 값 객체, 도메인 예외
    infrastructure/   DB, 외부 API, 메시징 등 기술 어댑터
config/
  settings/
    base.py           공통 설정
    dev.py            로컬 개발 설정
    prod.py           배포 설정
    test.py           테스트 설정
  urls.py             프로젝트 URL 라우팅
  asgi.py
  wsgi.py
tests/                단위 테스트와 Django 통합 테스트
manage.py
```

## 설계 방향

Django는 앱 단위 모듈화를 많이 사용합니다. 이 템플릿은 Django app 내부를 다시 `api / application / domain / infrastructure`로 나누는 DDD-lite 구조를 사용합니다.

의존 방향:

```text
api -> application -> domain
api -> Django/DRF
application -> domain
infrastructure -> domain
```

계층별 책임:

- `api`: HTTP 어댑터 계층입니다. DRF View, serializer, URL 라우팅을 둡니다.
- `application`: Use case 계층입니다. 도메인 객체를 조합하고 유스케이스 흐름을 담당합니다.
- `domain`: 비즈니스 핵심 계층입니다. Django ORM, DRF, HTTP에 의존하지 않는 순수 Python 객체를 둡니다.
- `infrastructure`: 기술 구현 계층입니다. ORM repository, 외부 API client, queue, storage adapter 등을 둡니다.
- `config`: Django 프로젝트 설정, URL, ASGI/WSGI 진입점을 둡니다.

단순 CRUD 프로젝트라면 `views.py`, `models.py`, `serializers.py` 중심의 기본 Django 앱 구조도 충분합니다. 이 템플릿은 서비스가 커졌을 때 도메인 규칙과 프레임워크 코드를 분리하기 쉽도록 DDD-lite를 기본으로 둡니다.

## 설정 파일

settings는 하나의 `settings.py`가 아니라 환경별 모듈로 나눕니다.

```text
config/settings/base.py   공통 설정
config/settings/dev.py    로컬 개발 설정
config/settings/prod.py   배포 설정
config/settings/test.py   테스트 설정
```

기본 로컬 실행은 `config.settings.dev`를 사용합니다.

```bash
DJANGO_SETTINGS_MODULE=config.settings.dev
```

배포 실행은 `config.settings.prod`를 사용합니다.

```bash
DJANGO_SETTINGS_MODULE=config.settings.prod
```

## 로컬 실행

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux
pip install -r requirements-dev.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

`.env`는 `config/settings/base.py`의 `load_dotenv`가 자동으로 읽습니다.

상태 확인:

```bash
curl http://127.0.0.1:8000/health/
curl http://127.0.0.1:8000/api/v1/health/
```

## 테스트

```bash
pytest
ruff check .
```

## Docker 실행

개발용과 배포용 Docker 구성을 분리합니다.

```text
Dockerfile.dev            개발용 이미지
Dockerfile                배포용 이미지
docker-compose.yml        개발용 Compose
docker-compose.prod.yml   배포용 Compose
```

### 개발용 Docker

개발용은 코드 변경이 빠르게 반영되도록 구성합니다.

```bash
docker compose up --build
```

개발용 구성의 핵심:

- `./apps`를 컨테이너의 `/app/apps`에 bind mount 합니다.
- `./config`를 컨테이너의 `/app/config`에 bind mount 합니다.
- 로컬에서 Python 코드를 수정하면 컨테이너 내부 파일도 즉시 바뀝니다.
- 컨테이너는 Django 개발 서버 `python manage.py runserver 0.0.0.0:8000`로 실행됩니다.
- Django 개발 서버의 autoreload가 파일 변경을 감지해 프로세스를 자동 재시작합니다.

주의할 점:

- Django 개발 반영은 프론트엔드 HMR처럼 무중단 교체가 아닙니다.
- 일반적으로 코드 변경을 감지한 뒤 개발 서버가 빠르게 재시작하는 방식입니다.
- `requirements*.txt`나 Dockerfile을 바꾼 경우에는 이미지를 다시 빌드해야 합니다.

### 배포용 Docker

배포용은 Gunicorn으로 WSGI 애플리케이션을 실행합니다.

```bash
cp .env.example .env
# .env의 DJANGO_SECRET_KEY를 실제 비밀 값으로 교체합니다.
docker compose -f docker-compose.prod.yml up --build
```

배포용 구성의 핵심:

- `Dockerfile`은 런타임 의존성만 설치합니다.
- 기본 settings는 `config.settings.prod`입니다.
- `config.settings.prod`는 `DJANGO_SECRET_KEY`가 없거나 `change-me`이면 기동을 거부합니다.
- 이미지 빌드 시 `collectstatic`으로 정적 파일을 수집하고 whitenoise로 서빙합니다.
- `gunicorn config.wsgi:application`으로 실행합니다.
- 개발용 bind mount를 사용하지 않습니다.

## 기본 엔드포인트

```text
GET /health/
GET /api/v1/health/
```

`/health/`는 로드밸런서나 컨테이너 healthcheck에서 쓰기 좋은 간단한 상태 확인용이고, `/api/v1/health/`는 versioned API 라우팅 예시입니다.
