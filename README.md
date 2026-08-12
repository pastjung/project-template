# Kafka 템플릿

로컬 개발에서 바로 사용할 수 있는 Apache Kafka 단일 브로커 템플릿입니다. ZooKeeper 없이 KRaft 모드로 실행합니다.

## 구성

```text
docker-compose.yml   Kafka 실행 구성
.env.example         Kafka 컨테이너 환경 변수 예시
.gitignore           .env 제외 규칙
README.md            사용 가이드
```

## 실행

`.env.example`을 복사해 `.env`를 만든 뒤 실행합니다. `.env`는 커밋하지 않습니다.

```bash
cp .env.example .env
docker compose up -d
```

브로커가 준비되면 healthcheck가 `healthy`로 바뀝니다.

```bash
docker compose ps
```

## 리스너 구조

같은 Docker 네트워크의 컨테이너와 호스트 클라이언트가 서로 다른 주소로 접속하도록
리스너를 분리합니다.

| Listener | 주소 | 용도 |
| --- | --- | --- |
| INTERNAL | `kafka:19092` | 같은 compose 네트워크의 앱 컨테이너 |
| EXTERNAL | `localhost:9092` | 호스트에서 실행하는 클라이언트, CLI |
| CONTROLLER | `kafka:9093` | KRaft controller (내부 전용) |

앱 컨테이너에서 접속할 때는 bootstrap server를 `kafka:19092`로 설정합니다.

## 토픽 생성

`apache/kafka` 이미지의 CLI는 `.sh` 확장자를 사용하며 `/opt/kafka/bin/`에 있습니다.

```bash
docker compose exec kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic events --partitions 3 --replication-factor 1
```

## 토픽 목록 확인

```bash
docker compose exec kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
```

## 콘솔 프로듀서 / 컨슈머

```bash
docker compose exec kafka /opt/kafka/bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic events
```

```bash
docker compose exec kafka /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic events --from-beginning
```

## 환경 변수

주요 변수는 `.env.example`의 주석을 참고합니다. 새 클러스터를 만들 때는
`KAFKA_CLUSTER_ID`를 고유 값으로 교체합니다.

```bash
docker run --rm apache/kafka:3.8.0 /opt/kafka/bin/kafka-storage.sh random-uuid
```

## 종료

```bash
docker compose down
```

볼륨(토픽 데이터)까지 삭제하려면 다음 명령을 사용합니다.

```bash
docker compose down -v
```
