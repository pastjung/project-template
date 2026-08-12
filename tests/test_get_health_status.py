from app.application.use_cases.get_health_status import GetHealthStatusUseCase


def test_get_health_status_returns_service_metadata() -> None:
    use_case = GetHealthStatusUseCase(service_name="fastapi-app", environment="local")

    health = use_case.execute()

    assert health.status == "ok"
    assert health.service == "fastapi-app"
    assert health.environment == "local"
