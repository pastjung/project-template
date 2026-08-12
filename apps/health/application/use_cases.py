from dataclasses import dataclass

from django.conf import settings

from apps.health.domain.entities import HealthStatus


@dataclass(frozen=True)
class GetHealthStatusUseCase:
    service_name: str
    environment: str

    @classmethod
    def from_settings(cls) -> "GetHealthStatusUseCase":
        return cls(
            service_name=settings.APP_NAME,
            environment=settings.APP_ENV,
        )

    def execute(self) -> HealthStatus:
        return HealthStatus(
            status="ok",
            service=self.service_name,
            environment=self.environment,
        )

