from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.domain.exceptions import (
    AlreadyExistsError,
    DomainError,
    InvalidStateError,
    NotFoundError,
)

_STATUS_CODES: dict[int, str] = {
    status.HTTP_400_BAD_REQUEST: "BAD_REQUEST",
    status.HTTP_401_UNAUTHORIZED: "UNAUTHORIZED",
    status.HTTP_403_FORBIDDEN: "FORBIDDEN",
    status.HTTP_404_NOT_FOUND: "NOT_FOUND",
    status.HTTP_405_METHOD_NOT_ALLOWED: "METHOD_NOT_ALLOWED",
    status.HTTP_409_CONFLICT: "CONFLICT",
    status.HTTP_429_TOO_MANY_REQUESTS: "TOO_MANY_REQUESTS",
}

_DOMAIN_STATUS: dict[type[DomainError], int] = {
    NotFoundError: status.HTTP_404_NOT_FOUND,
    AlreadyExistsError: status.HTTP_409_CONFLICT,
    InvalidStateError: status.HTTP_409_CONFLICT,
}


def _error_response(
    status_code: int, code: str, message: str, details: list[dict] | None = None
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error": {"code": code, "message": message, "details": details or []}},
    )


async def _handle_validation_error(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    details = [
        {"field": ".".join(str(part) for part in error["loc"][1:]), "reason": error["msg"]}
        for error in exc.errors()
    ]
    return _error_response(
        status.HTTP_422_UNPROCESSABLE_ENTITY, "VALIDATION_FAILED", "Validation failed", details
    )


async def _handle_domain_error(request: Request, exc: DomainError) -> JSONResponse:
    status_code = status.HTTP_400_BAD_REQUEST
    for error_type, mapped_status in _DOMAIN_STATUS.items():
        if isinstance(exc, error_type):
            status_code = mapped_status
            break
    return _error_response(status_code, exc.code, exc.message, exc.details)


async def _handle_http_exception(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    code = _STATUS_CODES.get(exc.status_code, "INTERNAL_SERVER_ERROR")
    return _error_response(exc.status_code, code, str(exc.detail))


async def _handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
    return _error_response(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "INTERNAL_SERVER_ERROR",
        "Unexpected server error",
    )


def register_error_handlers(app: FastAPI) -> None:
    """Register handlers that produce the docs/http-response.md error envelope."""
    app.add_exception_handler(RequestValidationError, _handle_validation_error)
    app.add_exception_handler(DomainError, _handle_domain_error)
    app.add_exception_handler(StarletteHTTPException, _handle_http_exception)
    app.add_exception_handler(Exception, _handle_unexpected_error)
