package com.example.app.domain.error;

/**
 * Base class for domain-level errors.
 *
 * Error codes follow docs/http-response.md (api/http-response branch).
 * The domain layer stays HTTP-agnostic; status mapping lives in
 * GlobalExceptionHandler.
 */
public class DomainException extends RuntimeException {
    private final String code;

    public DomainException(String code, String message) {
        super(message);
        this.code = code;
    }

    public String getCode() {
        return code;
    }
}
