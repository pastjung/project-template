import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_health_endpoint_returns_service_metadata(client, settings):
    settings.APP_NAME = "django-app"
    settings.APP_ENV = "test"

    response = client.get(reverse("health"))

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "django-app",
        "environment": "test",
    }


@pytest.mark.django_db
def test_versioned_health_endpoint_returns_service_metadata(client, settings):
    settings.APP_NAME = "django-app"
    settings.APP_ENV = "test"

    response = client.get("/api/v1/health/")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"

