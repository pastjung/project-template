package com.example.app.application.health;

import static org.assertj.core.api.Assertions.assertThat;

import com.example.app.core.config.AppProperties;
import com.example.app.domain.health.HealthStatus;
import org.junit.jupiter.api.Test;

class GetHealthStatusUseCaseTest {
    @Test
    void executeReturnsConfiguredServiceMetadata() {
        GetHealthStatusUseCase useCase = new GetHealthStatusUseCase(
                new AppProperties("spring-boot-app", "0.1.0", "test")
        );

        HealthStatus healthStatus = useCase.execute();

        assertThat(healthStatus.status()).isEqualTo("ok");
        assertThat(healthStatus.service()).isEqualTo("spring-boot-app");
        assertThat(healthStatus.environment()).isEqualTo("test");
    }
}

