# Spring Boot 앱 템플릿

Java 21, Spring Boot, Gradle 기반의 백엔드 API 템플릿입니다. 현업에서 자주 쓰는 DDD-lite 계층 구조, profile별 설정, 테스트, 개발용/배포용 Docker 실행 방식을 포함합니다.

## 기술 스택

- Java 21
- Spring Boot
- Gradle
- Spring Web
- Spring Boot Actuator
- Spring Boot Validation
- Spring Boot DevTools
- JUnit 5

## 프로젝트 구조

```text
src/
  main/
    java/com/example/app/
      api/                 REST Controller, 요청/응답 DTO
        health/
      application/         Use case, 애플리케이션 서비스
        health/
      domain/              도메인 모델, 값 객체, 도메인 규칙
        health/
      infrastructure/      DB, 외부 API, 메시징 등 기술 어댑터
      core/                설정, 공통 예외, 보안 등 공통 부트스트랩
        config/
      Application.java     Spring Boot 진입점
    resources/
      application.properties
      application-dev.properties
      application-prod.properties
      application-test.properties
  test/
    java/com/example/app/  단위 테스트와 Spring 통합 테스트
```

## 설계 방향

이 템플릿은 full DDD보다 가볍고, 일반적인 `controller/service/repository` 구조보다 확장에 유리한 DDD-lite 구조를 기준으로 합니다.

의존 방향:

```text
api -> application -> domain
api -> core
application -> core
infrastructure -> domain
```

계층별 책임:

- `api`: HTTP 어댑터 계층입니다. Controller, request/response DTO, 라우팅과 HTTP 관련 처리를 둡니다.
- `application`: Use case 계층입니다. 도메인 로직을 호출하고 트랜잭션 경계를 두는 위치입니다.
- `domain`: 비즈니스 핵심 계층입니다. Spring MVC, JPA, HTTP, 외부 시스템에 의존하지 않도록 유지합니다.
- `infrastructure`: 기술 구현 계층입니다. JPA entity, repository 구현체, 외부 API client, queue, storage adapter 등을 둡니다.
- `core`: 애플리케이션 설정, properties 바인딩, 보안, 공통 예외 처리 같은 공통 구성을 둡니다.

단순 CRUD 서비스에서는 `controller/service/repository` 구조도 충분히 흔합니다. 이 템플릿은 주문, 결제, 정산, 예약처럼 비즈니스 규칙이 늘어나는 서비스에서도 구조가 무너지지 않도록 DDD-lite를 기본으로 둡니다.

## 설정 파일

설정은 YAML 대신 `.properties` 파일로 분리합니다.

```text
application.properties       공통 기본값
application-dev.properties   로컬 개발 환경
application-prod.properties  배포 환경
application-test.properties  테스트 환경
```

기본 profile은 `dev`입니다.

```properties
spring.profiles.default=dev
```

실행 환경에서 profile을 바꾸려면 다음 환경 변수를 사용합니다.

```bash
SPRING_PROFILES_ACTIVE=prod
```

## 로컬 실행

Gradle Wrapper가 포함되어 있어 별도의 Gradle 설치 없이 실행할 수 있습니다.

```bash
./gradlew bootRun
```

Windows(cmd)에서는 `gradlew.bat bootRun`을 사용합니다.

상태 확인:

```bash
curl http://127.0.0.1:8080/health
curl http://127.0.0.1:8080/api/v1/health
curl http://127.0.0.1:8080/actuator/health
```

## 테스트

```bash
./gradlew test
```

## Docker 실행

개발용과 배포용 Docker 구성을 분리합니다.

```text
Dockerfile.dev            개발용 이미지
Dockerfile                배포용 이미지
docker-compose.yml        개발용 Compose
docker-compose.prod.yml   배포용 Compose
```

### 개발용 Docker

개발용은 코드 변경이 빠르게 반영되도록 구성합니다.

```bash
docker compose up --build
```

개발용 구성의 핵심:

- `./src`를 컨테이너의 `/workspace/src`에 bind mount 합니다.
- 로컬에서 Java 코드를 수정하면 컨테이너 내부 소스도 즉시 바뀝니다.
- 컨테이너는 `gradle bootRun --continuous --no-daemon`으로 실행됩니다.
- `spring-boot-devtools`가 포함되어 있어 클래스 변경 시 애플리케이션 컨텍스트가 빠르게 재시작됩니다.
- LiveReload 포트 `35729`도 열어둡니다.
- Gradle 캐시는 `gradle-cache` 볼륨에 저장해 재실행 속도를 줄입니다.

주의할 점:

- Spring Boot 개발 반영은 프론트엔드 HMR처럼 완전 무중단 교체가 아닙니다.
- 일반적으로 DevTools가 변경을 감지한 뒤 애플리케이션을 빠르게 재시작하는 방식입니다.
- `build.gradle`이나 `settings.gradle`을 바꾼 경우에는 컨테이너를 다시 빌드하는 편이 안전합니다.

### 배포용 Docker

배포용은 jar를 빌드한 뒤 slim JRE 이미지에서 실행합니다.

```bash
docker compose -f docker-compose.prod.yml up --build
```

배포용 구성의 핵심:

- `Dockerfile`은 multi-stage build를 사용합니다.
- Gradle builder 이미지에서 `bootJar`를 만들고, layered jar를 추출해 의존성/애플리케이션 레이어를 분리합니다. 실행 이미지는 JRE만 포함합니다.
- 기본 profile은 `prod`입니다.
- `JAVA_OPTS`로 JVM 옵션을 주입할 수 있습니다.

## 기본 엔드포인트

```text
GET /health
GET /api/v1/health
GET /actuator/health
```

`/health`는 로드밸런서나 컨테이너 healthcheck에서 쓰기 좋은 간단한 상태 확인용이고, `/api/v1/health`는 versioned API 라우팅 예시입니다.
