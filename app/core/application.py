import logging

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.api.v1.routes.health import health
from app.core.config import get_settings
from app.core.error_handlers import register_error_handlers
from app.schemas.health import HealthResponse


def create_app() -> FastAPI:
    settings = get_settings()

    logging.basicConfig(level=settings.log_level.upper())

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        docs_url="/docs" if settings.docs_enabled else None,
        redoc_url="/redoc" if settings.docs_enabled else None,
        openapi_url="/openapi.json" if settings.docs_enabled else None,
    )

    register_error_handlers(app)

    app.include_router(api_router)
    app.add_api_route("/health", health, response_model=HealthResponse, tags=["health"])

    return app
