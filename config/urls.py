from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", include("apps.health.api.urls")),
    path("api/v1/health/", include("apps.health.api.urls")),
]

# API 우선 템플릿이므로 매칭되지 않는 경로와 서버 오류도
# docs/http-response.md의 error envelope(JSON)으로 응답합니다.
handler404 = "config.exception_handler.handler404"
handler500 = "config.exception_handler.handler500"

