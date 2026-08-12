import logging

from django.http import JsonResponse
from rest_framework import exceptions as drf_exceptions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

from apps.common.exceptions import (
    AlreadyExistsError,
    DomainError,
    InvalidStateError,
    NotFoundError,
)

logger = logging.getLogger(__name__)

_STATUS_CODES = {
    status.HTTP_400_BAD_REQUEST: "BAD_REQUEST",
    status.HTTP_401_UNAUTHORIZED: "UNAUTHORIZED",
    status.HTTP_403_FORBIDDEN: "FORBIDDEN",
    status.HTTP_404_NOT_FOUND: "NOT_FOUND",
    status.HTTP_405_METHOD_NOT_ALLOWED: "METHOD_NOT_ALLOWED",
    status.HTTP_409_CONFLICT: "CONFLICT",
    status.HTTP_429_TOO_MANY_REQUESTS: "TOO_MANY_REQUESTS",
}

_DOMAIN_STATUS = (
    (NotFoundError, status.HTTP_404_NOT_FOUND),
    (AlreadyExistsError, status.HTTP_409_CONFLICT),
    (InvalidStateError, status.HTTP_409_CONFLICT),
)


def _envelope(code: str, message: str, details: list[dict] | None = None) -> dict:
    return {"error": {"code": code, "message": message, "details": details or []}}


def _validation_details(data) -> list[dict]:
    details = []
    if isinstance(data, dict):
        for field, reasons in data.items():
            if isinstance(reasons, (list, tuple)):
                details.extend({"field": str(field), "reason": str(reason)} for reason in reasons)
            else:
                details.append({"field": str(field), "reason": str(reasons)})
    elif isinstance(data, (list, tuple)):
        details.extend({"field": "", "reason": str(reason)} for reason in data)
    return details


def exception_handler(exc, context):
    """DRF EXCEPTION_HANDLER producing the docs/http-response.md error envelope."""
    if isinstance(exc, DomainError):
        status_code = status.HTTP_400_BAD_REQUEST
        for error_type, mapped_status in _DOMAIN_STATUS:
            if isinstance(exc, error_type):
                status_code = mapped_status
                break
        return Response(_envelope(exc.code, exc.message, exc.details), status=status_code)

    response = drf_exception_handler(exc, context)
    if response is not None:
        if isinstance(exc, drf_exceptions.ValidationError):
            body = _envelope(
                "VALIDATION_FAILED", "Validation failed", _validation_details(response.data)
            )
        else:
            code = _STATUS_CODES.get(response.status_code, "INTERNAL_SERVER_ERROR")
            detail = response.data.get("detail") if isinstance(response.data, dict) else None
            body = _envelope(code, str(detail) if detail else "Request failed")
        response.data = body
        return response

    logger.exception("Unhandled exception in API view", exc_info=exc)
    return Response(
        _envelope("INTERNAL_SERVER_ERROR", "Unexpected server error"),
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def handler404(request, exception=None):
    return JsonResponse(_envelope("NOT_FOUND", "Resource not found"), status=404)


def handler500(request):
    return JsonResponse(_envelope("INTERNAL_SERVER_ERROR", "Unexpected server error"), status=500)
