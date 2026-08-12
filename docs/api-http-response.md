---
branch: api/http-response
description: HTTP 응답 규칙 (상태 코드, data/error envelope, traceId, 에러 코드 네이밍)
provides:
  - docs/api-http-response.md
requires: []
works-with:
  - branch: backend/spring-boot
    reason: GlobalExceptionHandler가 이 문서의 error envelope를 구현
  - branch: backend/fastapi
    reason: app/core/error_handlers.py가 이 문서의 error envelope를 구현
  - branch: backend/django
    reason: config/exception_handler.py가 이 문서의 error envelope를 구현
conflicts: []
placeholders: []
secrets: []
after-import:
  - 에러 코드 체계(<DOMAIN>_* 네이밍)를 프로젝트 도메인에 맞게 확장
verify:
  - test -f docs/api-http-response.md
---

# HTTP Response Guide

이 문서는 API에서 발생할 수 있는 상황별 HTTP 응답 기준을 정의합니다.

- 클라이언트가 응답만 보고 성공, 실패, 재시도 가능 여부를 판단할 수 있게 합니다.
- 서버는 같은 상황에 대해 일관된 status code와 response body를 반환합니다.
- 프레임워크별 구현 방식은 달라도 응답 정책은 프로젝트 전체에서 동일하게 유지합니다.

## Basic Rules

- HTTP status code는 요청 처리 결과를 표현합니다.
- response body는 클라이언트가 화면 처리, 에러 메시지 표시, 재시도 여부 판단에 필요한 정보를 제공합니다.
- 성공 응답과 실패 응답의 구조를 프로젝트 전체에서 통일합니다.
- 같은 에러 상황은 같은 error code를 사용합니다.
- 서버 내부 예외 메시지, stack trace, DB 쿼리, 외부 API secret은 응답에 포함하지 않습니다.

## Response Body Format

프로젝트 상황에 맞게 응답 포맷을 선택하되, 한 프로젝트 안에서는 일관되게 사용합니다.

### Success Response

```json
{
  "data": {
    "id": 1,
    "name": "user"
  }
}
```

목록 응답:

```json
{
  "data": [
    {
      "id": 1,
      "name": "user"
    }
  ],
  "page": {
    "number": 1,
    "size": 20,
    "totalElements": 100,
    "totalPages": 5
  }
}
```

### Error Response

```json
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "User not found",
    "details": []
  }
}
```

필드 검증 실패 응답:

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "reason": "Invalid email format"
      }
    ]
  }
}
```

### Trace ID

요청 추적용 `traceId`는 항상 **최상위 필드**에 둡니다. `error` 객체 내부에
넣지 않습니다. 최상위에 두면 성공 응답과 에러 응답에서 같은 위치를 사용할 수
있어 클라이언트와 로깅 파이프라인이 하나의 규칙으로 처리할 수 있습니다.

```json
{
  "data": { "id": 1 },
  "traceId": "01HZX..."
}
```

```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "Unexpected server error",
    "details": []
  },
  "traceId": "01HZX..."
}
```

- 서버 오류(5xx) 응답에는 `traceId`를 포함하는 것을 권장합니다. 사용자 문의를
  서버 로그와 연결하는 핵심 수단입니다.
- 성공 응답과 4xx 응답에서는 선택 사항입니다.
- 값은 요청 단위로 고유해야 하며, 서버 로그에 같은 값이 남아야 합니다.

## Status Code Rules

| Status | Meaning | Usage |
| --- | --- | --- |
| `200 OK` | 요청 성공 | 조회, 수정, 삭제 성공 후 응답 body가 필요한 경우 |
| `201 Created` | 리소스 생성 성공 | `POST`로 새 리소스를 생성한 경우 |
| `202 Accepted` | 요청 접수 | 비동기 작업이 접수되었지만 아직 완료되지 않은 경우 |
| `204 No Content` | 응답 body 없는 성공 | 삭제 성공, 응답 데이터가 필요 없는 수정 성공 |
| `400 Bad Request` | 잘못된 요청 | 요청 형식, 타입, 파라미터가 잘못된 경우 |
| `401 Unauthorized` | 인증 실패 | 로그인 필요, 토큰 누락, 토큰 만료 |
| `403 Forbidden` | 권한 없음 | 인증은 되었지만 해당 리소스 접근 권한이 없는 경우 |
| `404 Not Found` | 리소스 없음 | 요청한 리소스를 찾을 수 없는 경우 |
| `409 Conflict` | 상태 충돌 | 중복 생성, 이미 처리된 요청, 현재 상태에서 처리 불가 |
| `422 Unprocessable Entity` | 의미상 처리 불가 | 문법은 맞지만 비즈니스 검증에 실패한 경우 |
| `429 Too Many Requests` | 요청 횟수 초과 | rate limit을 초과한 경우 |
| `500 Internal Server Error` | 서버 내부 오류 | 예상하지 못한 서버 오류 |
| `502 Bad Gateway` | 외부 연동 오류 | upstream 서버가 잘못된 응답을 반환한 경우 |
| `503 Service Unavailable` | 서비스 일시 불가 | 점검, 과부하, 외부 의존성 장애 |
| `504 Gateway Timeout` | 외부 연동 timeout | upstream 서버 응답 시간이 초과된 경우 |

## Success Cases

### 단건 조회 성공

```text
GET /api/v1/users/{userId}
```

응답:

```text
200 OK
```

```json
{
  "data": {
    "id": 1,
    "name": "user"
  }
}
```

### 목록 조회 성공

```text
GET /api/v1/users?page=1&size=20
```

응답:

```text
200 OK
```

```json
{
  "data": [],
  "page": {
    "number": 1,
    "size": 20,
    "totalElements": 0,
    "totalPages": 0
  }
}
```

목록 조회 결과가 비어 있어도 `404 Not Found`가 아니라 `200 OK`와 빈 배열을 반환합니다.

### 생성 성공

```text
POST /api/v1/users
```

응답:

```text
201 Created
```

```json
{
  "data": {
    "id": 1
  }
}
```

필요하다면 `Location` header에 생성된 리소스 URL을 포함합니다.

```text
Location: /api/v1/users/1
```

### 수정 성공

응답 body가 필요한 경우:

```text
200 OK
```

응답 body가 필요 없는 경우:

```text
204 No Content
```

### 삭제 성공

삭제 후 반환할 데이터가 없다면 `204 No Content`를 사용합니다.

```text
204 No Content
```

## Client Error Cases

### 요청 형식 오류

요청 JSON이 깨져 있거나 타입이 맞지 않는 경우 `400 Bad Request`를 사용합니다.

```json
{
  "error": {
    "code": "BAD_REQUEST",
    "message": "Invalid request format",
    "details": []
  }
}
```

### 필드 검증 실패

필수값 누락, 길이 제한 초과, 형식 오류는 `400 Bad Request` 또는 `422 Unprocessable Entity` 중 하나로 통일합니다.

권장 기준:

- 요청 형식 자체가 잘못되었으면 `400 Bad Request`
- 요청 형식은 맞지만 비즈니스 규칙을 만족하지 못하면 `422 Unprocessable Entity`

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Validation failed",
    "details": [
      {
        "field": "password",
        "reason": "Password must be at least 8 characters"
      }
    ]
  }
}
```

### 인증 실패

로그인이 필요하거나 토큰이 없거나 만료된 경우 `401 Unauthorized`를 사용합니다.

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication is required",
    "details": []
  }
}
```

### 권한 없음

인증은 되었지만 권한이 부족한 경우 `403 Forbidden`을 사용합니다.

```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "You do not have permission to access this resource",
    "details": []
  }
}
```

### 리소스 없음

단건 조회, 수정, 삭제 대상 리소스가 없는 경우 `404 Not Found`를 사용합니다.

```json
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "User not found",
    "details": []
  }
}
```

### 중복 또는 상태 충돌

이미 존재하는 이메일로 가입하거나, 이미 취소된 주문을 다시 취소하는 경우 `409 Conflict`를 사용합니다.

```json
{
  "error": {
    "code": "USER_EMAIL_ALREADY_EXISTS",
    "message": "Email already exists",
    "details": []
  }
}
```

### 요청 횟수 초과

rate limit을 초과한 경우 `429 Too Many Requests`를 사용합니다.

```json
{
  "error": {
    "code": "TOO_MANY_REQUESTS",
    "message": "Too many requests",
    "details": []
  }
}
```

가능하면 `Retry-After` header를 함께 반환합니다.

```text
Retry-After: 60
```

## Server Error Cases

### 예상하지 못한 서버 오류

서버 내부에서 처리하지 못한 예외가 발생한 경우 `500 Internal Server Error`를 사용합니다.

```json
{
  "error": {
    "code": "INTERNAL_SERVER_ERROR",
    "message": "Internal server error",
    "details": []
  }
}
```

주의:

- 사용자에게 내부 예외 메시지를 그대로 노출하지 않습니다.
- 자세한 원인은 서버 로그에 남깁니다.
- request id 또는 trace id를 응답에 포함하면 장애 추적에 도움이 됩니다.

예시:

```json
{
  "error": {
    "code": "INTERNAL_SERVER_ERROR",
    "message": "Internal server error",
    "details": []
  },
  "traceId": "01HZX..."
}
```

### 외부 API 오류

외부 API, 메시지 브로커, DB proxy 등 upstream 시스템이 잘못된 응답을 반환한 경우 `502 Bad Gateway`를 사용할 수 있습니다.

```json
{
  "error": {
    "code": "UPSTREAM_BAD_RESPONSE",
    "message": "External service returned an invalid response",
    "details": []
  }
}
```

### 서비스 일시 불가

점검, 과부하, 필수 외부 시스템 장애로 요청을 처리할 수 없는 경우 `503 Service Unavailable`을 사용합니다.

```json
{
  "error": {
    "code": "SERVICE_UNAVAILABLE",
    "message": "Service is temporarily unavailable",
    "details": []
  }
}
```

### 외부 API timeout

upstream 시스템 응답 시간이 초과된 경우 `504 Gateway Timeout`을 사용할 수 있습니다.

```json
{
  "error": {
    "code": "UPSTREAM_TIMEOUT",
    "message": "External service timeout",
    "details": []
  }
}
```

## Async Request Cases

요청 처리가 오래 걸리는 작업은 즉시 완료 응답을 반환하지 않고 작업 접수 응답을 사용할 수 있습니다.

예시:

```text
POST /api/v1/reports
```

응답:

```text
202 Accepted
```

```json
{
  "data": {
    "jobId": "report-20260611-001",
    "status": "PENDING"
  }
}
```

작업 상태 조회 API를 함께 제공합니다.

```text
GET /api/v1/reports/jobs/{jobId}
```

## Idempotency Cases

결제, 주문, 포인트 적립처럼 중복 요청이 문제가 되는 API는 idempotency key 사용을 고려합니다.

예시 header:

```text
Idempotency-Key: 9f3d3f3a-52af-4b2f-8a4a-4e3f1d2f0a10
```

권장 기준:

- 같은 key로 같은 요청이 반복되면 같은 결과를 반환합니다.
- 같은 key로 다른 요청 body가 들어오면 `409 Conflict`를 반환할 수 있습니다.
- key 저장 만료 시간을 정합니다.

## Error Code Naming Rules

에러 코드는 클라이언트와 서버가 공통으로 이해할 수 있는 안정적인 식별자입니다.

규칙:

- 대문자 snake case를 사용합니다.
- 도메인과 원인을 함께 표현합니다.
- 화면 표시 문구와 error code를 분리합니다.
- error code는 자주 바꾸지 않습니다.

예시:

```text
VALIDATION_FAILED
UNAUTHORIZED
FORBIDDEN
USER_NOT_FOUND
USER_EMAIL_ALREADY_EXISTS
ORDER_ALREADY_CANCELLED
PAYMENT_APPROVAL_FAILED
UPSTREAM_TIMEOUT
```

## Header Rules

응답 상황에 따라 필요한 header를 함께 사용합니다.

| Header | Usage |
| --- | --- |
| `Location` | 생성된 리소스 위치 |
| `Retry-After` | 재시도 가능 시점 또는 대기 시간 |
| `WWW-Authenticate` | 인증 실패 원인 또는 인증 방식 |
| `X-Request-Id` | 요청 추적 ID |
| `X-RateLimit-Limit` | 허용 요청 수 |
| `X-RateLimit-Remaining` | 남은 요청 수 |
| `X-RateLimit-Reset` | 제한 초기화 시점 |

## Situation Summary

| Situation | Status | Error Code |
| --- | --- | --- |
| 단건 조회 성공 | `200 OK` | - |
| 목록 조회 성공, 결과 없음 | `200 OK` | - |
| 리소스 생성 성공 | `201 Created` | - |
| 비동기 작업 접수 | `202 Accepted` | - |
| 응답 body 없는 성공 | `204 No Content` | - |
| 요청 형식 오류 | `400 Bad Request` | `BAD_REQUEST` |
| 필드 검증 실패 | `400 Bad Request` 또는 `422 Unprocessable Entity` | `VALIDATION_FAILED` |
| 인증 실패 | `401 Unauthorized` | `UNAUTHORIZED` |
| 권한 없음 | `403 Forbidden` | `FORBIDDEN` |
| 리소스 없음 | `404 Not Found` | `<DOMAIN>_NOT_FOUND` |
| 중복 생성 | `409 Conflict` | `<DOMAIN>_ALREADY_EXISTS` |
| 현재 상태에서 처리 불가 | `409 Conflict` | `<DOMAIN>_INVALID_STATE` |
| 요청 횟수 초과 | `429 Too Many Requests` | `TOO_MANY_REQUESTS` |
| 서버 내부 오류 | `500 Internal Server Error` | `INTERNAL_SERVER_ERROR` |
| 외부 시스템 응답 오류 | `502 Bad Gateway` | `UPSTREAM_BAD_RESPONSE` |
| 서비스 일시 불가 | `503 Service Unavailable` | `SERVICE_UNAVAILABLE` |
| 외부 시스템 timeout | `504 Gateway Timeout` | `UPSTREAM_TIMEOUT` |

## Reference Implementations

이 응답 규칙을 구현한 전역 예외 처리기가 각 백엔드 템플릿에 포함되어 있습니다.
백엔드 브랜치와 함께 사용하면 문서와 실제 응답이 일치합니다.

| Branch | Implementation |
| --- | --- |
| `backend/spring-boot` | `GlobalExceptionHandler` (`@RestControllerAdvice`) |
| `backend/fastapi` | `app/core/error_handlers.py` (`add_exception_handler`) |
| `backend/django` | `config/exception_handler.py` (DRF `EXCEPTION_HANDLER`) |

## Standalone Usage

이 브랜치는 문서 전용입니다. 단독으로 가져오면 API 설계 기준 문서로
기능하며, 실제 응답 포맷 강제는 각 백엔드의 전역 예외 처리기가 담당합니다.

## Works With

백엔드 3종(spring-boot, fastapi, django) 템플릿에 이 규칙을 구현한 전역
예외 처리기가 포함되어 있어, 함께 사용하면 문서와 실제 응답이 일치합니다
(Reference Implementations 절 참고).
