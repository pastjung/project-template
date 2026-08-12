package com.example.app.application.health;

import com.example.app.core.config.AppProperties;
import com.example.app.domain.health.HealthStatus;
import org.springframework.stereotype.Service;

@Service
public class GetHealthStatusUseCase {
    private final AppProperties appProperties;

    public GetHealthStatusUseCase(AppProperties appProperties) {
        this.appProperties = appProperties;
    }

    public HealthStatus execute() {
        return new HealthStatus(
                "ok",
                appProperties.name(),
                appProperties.environment()
        );
    }
}

