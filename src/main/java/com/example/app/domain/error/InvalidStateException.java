package com.example.app.domain.error;

public class InvalidStateException extends DomainException {
    public InvalidStateException(String code, String message) {
        super(code, message);
    }
}
