class DomainError(Exception):
    """Base class for domain-level errors.

    code and message follow the error response rules in docs/http-response.md.
    Subclasses override code/message and are mapped to HTTP statuses in
    app/core/error_handlers.py so the domain layer stays HTTP-agnostic.
    """

    code = "DOMAIN_ERROR"
    message = "Domain rule violation"

    def __init__(self, message: str | None = None, details: list[dict] | None = None) -> None:
        self.message = message or self.__class__.message
        self.details = details or []
        super().__init__(self.message)


class NotFoundError(DomainError):
    code = "NOT_FOUND"
    message = "Resource not found"


class AlreadyExistsError(DomainError):
    code = "ALREADY_EXISTS"
    message = "Resource already exists"


class InvalidStateError(DomainError):
    code = "INVALID_STATE"
    message = "Resource state does not allow this operation"
