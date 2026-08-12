package com.example.app.api.health;

import com.example.app.application.health.GetHealthStatusUseCase;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HealthController {
    private final GetHealthStatusUseCase getHealthStatusUseCase;

    public HealthController(GetHealthStatusUseCase getHealthStatusUseCase) {
        this.getHealthStatusUseCase = getHealthStatusUseCase;
    }

    @GetMapping({"/health", "/api/v1/health"})
    public HealthResponse health() {
        return HealthResponse.from(getHealthStatusUseCase.execute());
    }
}

