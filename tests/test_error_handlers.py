from fastapi import Query
from fastapi.testclient import TestClient

from app.core.application import create_app
from app.domain.exceptions import AlreadyExistsError, NotFoundError


def build_client() -> TestClient:
    app = create_app()

    @app.get("/boom")
    def boom() -> None:
        raise RuntimeError("unexpected")

    @app.get("/users/{user_id}")
    def get_user(user_id: int) -> None:
        raise NotFoundError("User not found")

    @app.post("/users")
    def create_user(name: str = Query(min_length=1)) -> None:
        raise AlreadyExistsError("User already exists")

    return TestClient(app, raise_server_exceptions=False)


def test_unknown_route_returns_error_envelope() -> None:
    response = build_client().get("/does-not-exist")

    assert response.status_code == 404
    body = response.json()
    assert body["error"]["code"] == "NOT_FOUND"
    assert body["error"]["details"] == []


def test_validation_failure_returns_field_details() -> None:
    response = build_client().get("/users/not-a-number")

    assert response.status_code == 422
    body = response.json()
    assert body["error"]["code"] == "VALIDATION_FAILED"
    assert body["error"]["details"][0]["field"] == "user_id"
    assert body["error"]["details"][0]["reason"]


def test_domain_not_found_maps_to_404() -> None:
    response = build_client().get("/users/1")

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"


def test_domain_conflict_maps_to_409() -> None:
    response = build_client().post("/users", params={"name": "kim"})

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "ALREADY_EXISTS"


def test_unexpected_error_hides_internals() -> None:
    response = build_client().get("/boom")

    assert response.status_code == 500
    body = response.json()
    assert body["error"]["code"] == "INTERNAL_SERVER_ERROR"
    assert "unexpected" not in body["error"]["message"]
