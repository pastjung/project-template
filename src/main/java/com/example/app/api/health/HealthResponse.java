package com.example.app.api.health;

import com.example.app.domain.health.HealthStatus;

public record HealthResponse(String status, String service, String environment) {
    public static HealthResponse from(HealthStatus healthStatus) {
        return new HealthResponse(
                healthStatus.status(),
                healthStatus.service(),
                healthStatus.environment()
        );
    }
}

