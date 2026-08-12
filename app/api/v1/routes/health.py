from fastapi import APIRouter, Depends

from app.api.v1.dependencies import get_health_status_use_case
from app.application.use_cases.get_health_status import GetHealthStatusUseCase
from app.schemas.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health(
    use_case: GetHealthStatusUseCase = Depends(get_health_status_use_case),
) -> HealthResponse:
    return HealthResponse.from_domain(use_case.execute())
