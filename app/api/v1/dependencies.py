from typing import Annotated

from fastapi import Depends

from app.application.use_cases.get_health_status import GetHealthStatusUseCase
from app.core.config import Settings, get_settings


def get_health_status_use_case(
    settings: Annotated[Settings, Depends(get_settings)],
) -> GetHealthStatusUseCase:
    return GetHealthStatusUseCase(
        service_name=settings.app_name,
        environment=settings.app_env,
    )
