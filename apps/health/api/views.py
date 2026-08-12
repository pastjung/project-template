from rest_framework.response import Response
from rest_framework.views import APIView

from apps.health.api.serializers import HealthStatusSerializer
from apps.health.application.use_cases import GetHealthStatusUseCase


class HealthView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, _request):
        health_status = GetHealthStatusUseCase.from_settings().execute()
        serializer = HealthStatusSerializer.from_domain(health_status)
        return Response(serializer.data)

