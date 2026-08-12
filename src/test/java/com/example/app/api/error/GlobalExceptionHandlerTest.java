package com.example.app.api.error;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.example.app.domain.error.AlreadyExistsException;
import com.example.app.domain.error.NotFoundException;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@Import(GlobalExceptionHandlerTest.FailingController.class)
class GlobalExceptionHandlerTest {
    @Autowired
    private MockMvc mockMvc;

    @RestController
    static class FailingController {
        record CreateUserRequest(@NotBlank(message = "name must not be blank") String name) {
        }

        @GetMapping("/test-errors/not-found")
        void notFound() {
            throw new NotFoundException("USER_NOT_FOUND", "User not found");
        }

        @GetMapping("/test-errors/conflict")
        void conflict() {
            throw new AlreadyExistsException("USER_ALREADY_EXISTS", "User already exists");
        }

        @GetMapping("/test-errors/boom")
        void boom() {
            throw new IllegalStateException("internal detail that must not leak");
        }

        @PostMapping("/test-errors/users")
        void createUser(@Valid @RequestBody CreateUserRequest request) {
        }
    }

    @Test
    void domainNotFoundMapsTo404() throws Exception {
        mockMvc.perform(get("/test-errors/not-found"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.error.code").value("USER_NOT_FOUND"))
                .andExpect(jsonPath("$.error.details").isEmpty());
    }

    @Test
    void domainConflictMapsTo409() throws Exception {
        mockMvc.perform(get("/test-errors/conflict"))
                .andExpect(status().isConflict())
                .andExpect(jsonPath("$.error.code").value("USER_ALREADY_EXISTS"));
    }

    @Test
    void validationFailureReturnsFieldDetails() throws Exception {
        mockMvc.perform(post("/test-errors/users")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"name\":\"\"}"))
                .andExpect(status().isUnprocessableEntity())
                .andExpect(jsonPath("$.error.code").value("VALIDATION_FAILED"))
                .andExpect(jsonPath("$.error.details[0].field").value("name"));
    }

    @Test
    void unexpectedErrorHidesInternals() throws Exception {
        mockMvc.perform(get("/test-errors/boom"))
                .andExpect(status().isInternalServerError())
                .andExpect(jsonPath("$.error.code").value("INTERNAL_SERVER_ERROR"))
                .andExpect(jsonPath("$.error.message").value("Unexpected server error"));
    }

    @Test
    void unknownRouteReturnsErrorEnvelope() throws Exception {
        mockMvc.perform(get("/does-not-exist"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.error.code").value("NOT_FOUND"));
    }
}
