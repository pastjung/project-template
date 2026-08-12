# Elastic Stack Template

로그 수집/검색용 로컬 Elastic Stack입니다. Filebeat → Logstash →
Elasticsearch(data stream + ILM) → Kibana 파이프라인을 포함합니다.

**로컬 개발 전용 구성입니다.** `xpack.security.enabled: false`로 보안이 꺼져
있으므로 외부에 노출되는 환경에서는 security 활성화, TLS, 인증 설정이
필요합니다.

## 구성

```text
docker-compose.yml            5개 서비스 (ES, setup, Kibana, Logstash, Filebeat)
.env.example                  ELASTIC_VERSION (.env로 복사)
filebeat/filebeat.yml         JSON 라인 로그를 구조화하는 filestream 입력
logstash/pipeline/logstash.conf  data stream 출력 파이프라인
logs/app.log                  JSON 라인 샘플 로그
```

## 파이프라인

```text
logs/*.log (JSON lines)
  → Filebeat (ndjson parser: level, message가 필드로 구조화됨)
  → Logstash (ingested_by 필드 추가)
  → Elasticsearch data stream: logs-app-default
  → Kibana Discover
```

`setup` 일회성 컨테이너가 ILM 정책(`logs-app-7d`: 1일 rollover, 7일 삭제)과
index template을 생성해 로그 인덱스가 무한히 쌓이지 않습니다.

## Run

```bash
cp .env.example .env
docker compose up -d
```

| Service | URL |
| --- | --- |
| Kibana | http://localhost:5601 |
| Elasticsearch | http://localhost:9200 |

모든 서비스가 healthy가 될 때까지 1~2분 걸립니다.

```bash
docker compose ps
```

## 로그 확인

색인 확인:

```bash
curl -s "http://localhost:9200/logs-app-default/_search?q=level:INFO" | head -c 500
```

Kibana Discover에서 `logs-app-default` data view를 만들면 `level`,
`message`, `ingested_by`가 구조화된 필드로 조회됩니다.

## 애플리케이션 로그 연결

`logs/` 디렉터리에 JSON 라인(`{"level":"...","message":"..."}`) 형식으로
로그 파일을 쓰면 자동으로 수집됩니다. 평문 로그를 쓴다면
`filebeat/filebeat.yml`의 `parsers` 블록을 제거하세요.

## 버전

`ELASTIC_VERSION`(.env)으로 스택 전체 버전을 관리합니다. 기본값은 8.19
라인입니다. Elasticsearch 9.x로 올릴 때는 breaking changes 문서를 확인한 뒤
`.env`에서 버전만 교체하면 됩니다.

## 종료

```bash
docker compose down        # 데이터 유지
docker compose down -v     # 볼륨까지 삭제
```
