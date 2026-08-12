package com.example.app.domain.error;

public class AlreadyExistsException extends DomainException {
    public AlreadyExistsException(String code, String message) {
        super(code, message);
    }
}
