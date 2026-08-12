from rest_framework import serializers

from apps.health.domain.entities import HealthStatus


class HealthStatusSerializer(serializers.Serializer):
    status = serializers.CharField()
    service = serializers.CharField()
    environment = serializers.CharField()

    @classmethod
    def from_domain(cls, health_status: HealthStatus) -> "HealthStatusSerializer":
        return cls(
            {
                "status": health_status.status,
                "service": health_status.service,
                "environment": health_status.environment,
            }
        )

