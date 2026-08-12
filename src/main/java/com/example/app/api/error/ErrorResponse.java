package com.example.app.api.error;

import java.util.List;

/**
 * Error envelope defined in docs/http-response.md (api/http-response branch).
 */
public record ErrorResponse(ErrorBody error) {

    public record ErrorBody(String code, String message, List<FieldErrorDetail> details) {
    }

    public record FieldErrorDetail(String field, String reason) {
    }

    public static ErrorResponse of(String code, String message) {
        return new ErrorResponse(new ErrorBody(code, message, List.of()));
    }

    public static ErrorResponse of(String code, String message, List<FieldErrorDetail> details) {
        return new ErrorResponse(new ErrorBody(code, message, details));
    }
}
