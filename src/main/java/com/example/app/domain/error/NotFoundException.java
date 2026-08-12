package com.example.app.domain.error;

public class NotFoundException extends DomainException {
    public NotFoundException(String code, String message) {
        super(code, message);
    }
}
