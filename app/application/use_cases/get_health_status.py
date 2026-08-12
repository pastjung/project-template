from app.domain.entities.health_status import HealthStatus


class GetHealthStatusUseCase:
    def __init__(self, service_name: str, environment: str) -> None:
        self._service_name = service_name
        self._environment = environment

    def execute(self) -> HealthStatus:
        return HealthStatus(
            status="ok",
            service=self._service_name,
            environment=self._environment,
        )

