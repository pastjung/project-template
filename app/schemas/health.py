from pydantic import BaseModel

from app.domain.entities.health_status import HealthStatus


class HealthResponse(BaseModel):
    status: str
    service: str
    environment: str

    @classmethod
    def from_domain(cls, health_status: HealthStatus) -> "HealthResponse":
        return cls(
            status=health_status.status,
            service=health_status.service,
            environment=health_status.environment,
        )
