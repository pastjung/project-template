import pytest
from django.test import Client
from django.urls import path
from rest_framework import serializers
from rest_framework.views import APIView

from apps.common.exceptions import AlreadyExistsError, NotFoundError
from config.urls import urlpatterns as project_urlpatterns


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()


class NotFoundView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, _request):
        raise NotFoundError("User not found")


class ConflictView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, _request):
        raise AlreadyExistsError("User already exists")


class ValidationView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)


class BoomView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, _request):
        raise RuntimeError("internal detail that must not leak")


urlpatterns = project_urlpatterns + [
    path("test-errors/not-found/", NotFoundView.as_view()),
    path("test-errors/conflict/", ConflictView.as_view()),
    path("test-errors/users/", ValidationView.as_view()),
    path("test-errors/boom/", BoomView.as_view()),
]

handler404 = "config.exception_handler.handler404"
handler500 = "config.exception_handler.handler500"

pytestmark = [pytest.mark.django_db, pytest.mark.urls(__name__)]


def test_domain_not_found_maps_to_404(client):
    response = client.get("/test-errors/not-found/")

    assert response.status_code == 404
    body = response.json()
    assert body["error"]["code"] == "NOT_FOUND"
    assert body["error"]["details"] == []


def test_domain_conflict_maps_to_409(client):
    response = client.get("/test-errors/conflict/")

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "ALREADY_EXISTS"


def test_validation_failure_returns_field_details(client):
    response = client.post(
        "/test-errors/users/", data={"email": "not-an-email"}, content_type="application/json"
    )

    assert response.status_code == 400
    body = response.json()
    assert body["error"]["code"] == "VALIDATION_FAILED"
    assert body["error"]["details"][0]["field"] == "email"


def test_unexpected_error_hides_internals():
    client = Client(raise_request_exception=False)

    response = client.get("/test-errors/boom/")

    assert response.status_code == 500
    body = response.json()
    assert body["error"]["code"] == "INTERNAL_SERVER_ERROR"
    assert "internal detail" not in body["error"]["message"]


def test_unknown_route_returns_error_envelope(client):
    response = client.get("/does-not-exist/")

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"
