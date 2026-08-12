from apps.health.application.use_cases import GetHealthStatusUseCase


def test_get_health_status_returns_service_metadata():
    use_case = GetHealthStatusUseCase(
        service_name="django-app",
        environment="test",
    )

    health_status = use_case.execute()

    assert health_status.status == "ok"
    assert health_status.service == "django-app"
    assert health_status.environment == "test"

