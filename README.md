# Flink 템플릿

로컬 개발에서 사용할 수 있는 Apache Flink 클러스터 템플릿입니다. JobManager 1개와 TaskManager 1개로 구성합니다.

## 구성

```text
docker-compose.yml   Flink 클러스터 실행 구성 (FLINK_PROPERTIES 포함)
jobs/                사용자 job jar를 두는 디렉터리 (JobManager에 마운트됨)
README.md            사용 가이드
```

## Flink 설정

Flink 설정은 `docker-compose.yml`의 `FLINK_PROPERTIES` 환경 변수로 주입합니다.

```yaml
environment:
  - |
    FLINK_PROPERTIES=
    jobmanager.rpc.address: jobmanager
    taskmanager.numberOfTaskSlots: 2
    parallelism.default: 1
```

설정을 바꾸려면 이 블록에 `키: 값` 줄을 추가합니다.

`FLINK_PROPERTIES`는 줄바꿈이 필요한 값이라 `env_file`로는 전달할 수 없습니다.
(`env_file`은 `\n`을 이스케이프가 아닌 리터럴 문자로 취급합니다.) 이 때문에 이
템플릿은 예외적으로 compose의 `environment:` 멀티라인 방식을 사용합니다. 이는
Flink 공식 문서의 권장 방식이기도 합니다.

참고: Flink 1.20부터는 새 설정 파일 형식인 `config.yaml`이 표준이고 기존
`flink-conf.yaml`은 deprecated입니다(2.0에서 제거). 설정 파일을 직접 마운트하는
방식으로 바꾸려면 `config.yaml`을 `/opt/flink/conf`에 마운트합니다.

## 실행

```bash
docker compose up -d
```

Flink UI:

```text
http://localhost:8081
```

JobManager가 준비되면 healthcheck가 `healthy`로 바뀝니다.

```bash
docker compose ps
```

## Job 제출

동작 확인은 이미지에 포함된 예제 job으로 바로 할 수 있습니다.

```bash
docker compose exec jobmanager flink run /opt/flink/examples/streaming/WordCount.jar
```

실제 작업 jar는 `jobs/` 디렉터리에 두면 JobManager의 `/opt/flink/jobs`로
마운트됩니다.

```bash
docker compose exec jobmanager flink run /opt/flink/jobs/my-job.jar
```

## TaskManager 확장

TaskManager는 `container_name`을 고정하지 않으므로 scale 옵션으로 늘릴 수 있습니다.

```bash
docker compose up -d --scale taskmanager=2
```

## 종료

```bash
docker compose down
```
