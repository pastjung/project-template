from fastapi.testclient import TestClient

from app.core.application import create_app
from app.core.config import Settings, get_settings


def test_settings_can_be_overridden_per_test() -> None:
    app = create_app()
    app.dependency_overrides[get_settings] = lambda: Settings(
        app_name="overridden-service", app_env="test"
    )

    response = TestClient(app).get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["service"] == "overridden-service"
    assert response.json()["environment"] == "test"
