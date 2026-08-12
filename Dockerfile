FROM gradle:8.14-jdk21 AS builder
WORKDIR /workspace

# 의존성 레이어 캐시: 빌드 스크립트만 먼저 복사해 의존성 해석을 캐시합니다.
# 소스만 바뀐 빌드에서는 의존성 다운로드를 건너뜁니다.
COPY build.gradle settings.gradle ./
RUN gradle dependencies --no-daemon --quiet > /dev/null 2>&1 || true

COPY src ./src
RUN gradle bootJar --no-daemon

# Spring Boot layered jar 추출: 의존성과 애플리케이션 코드를 별도 레이어로
# 분리해 재배포 시 이미지 push/pull 크기를 줄입니다.
RUN java -Djarmode=tools -jar build/libs/app.jar extract --layers --launcher --destination extracted

FROM eclipse-temurin:21-jre-alpine
WORKDIR /app

RUN addgroup -S app && adduser -S app -G app

COPY --from=builder /workspace/extracted/dependencies/ ./
COPY --from=builder /workspace/extracted/spring-boot-loader/ ./
COPY --from=builder /workspace/extracted/snapshot-dependencies/ ./
COPY --from=builder /workspace/extracted/application/ ./

USER app

ENV SPRING_PROFILES_ACTIVE=prod \
    JAVA_OPTS=""

EXPOSE 8080

ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS org.springframework.boot.loader.launch.JarLauncher"]
