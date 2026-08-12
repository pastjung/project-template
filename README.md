# Prometheus Grafana Template

Prometheus 3 + Grafana 12 + node-exporter로 구성한 로컬 모니터링 스택입니다.
데이터소스/대시보드 프로비저닝과 알림 규칙 예시를 포함합니다.

## 구성

```text
docker-compose.yml                          스택 실행 구성
.env.example                                Grafana 관리자 계정 (.env로 복사)
prometheus/prometheus.yml                   scrape 대상 (prometheus, node-exporter)
prometheus/rules/alerts.yml                 알림 규칙 예시 (InstanceDown, CPU, Memory)
grafana/provisioning/datasources/           Prometheus 데이터소스 자동 등록
grafana/provisioning/dashboards/            대시보드 provider 설정
grafana/dashboards/node-exporter-overview.json  기본 대시보드
```

## Run

```bash
cp .env.example .env
docker compose up -d
```

| Service | URL |
| --- | --- |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |
| node-exporter | 내부 전용 (prometheus가 수집) |

Grafana 계정은 `.env`의 `GRAFANA_ADMIN_USER/PASSWORD`입니다. 예시값
`admin/admin`은 로컬 전용이며 외부 노출 환경에서는 반드시 교체합니다.

로그인하면 `Local` 폴더에 **Node Exporter Overview** 대시보드가 자동으로
로드되어 있습니다.

## Alerts

`prometheus/rules/alerts.yml`에 예시 알림 3개(InstanceDown,
HostHighCpuUsage, HostLowMemory)가 정의되어 있습니다. Prometheus UI의
`Alerts` 탭에서 상태를 확인할 수 있습니다.

알림을 Slack/메일로 발송하려면 Alertmanager를 추가하고 `alerting` 설정을
연결합니다 (이 템플릿에는 규칙까지만 포함).

## 애플리케이션 메트릭 수집

`prometheus/prometheus.yml`의 주석 처리된 `api` job을 참고해 scrape 대상을
추가합니다. Spring Boot는 actuator의 `/actuator/prometheus`, FastAPI는
`prometheus-fastapi-instrumentator` 등을 사용합니다.

## node-exporter 주의

기본 구성은 데모용으로 컨테이너 자신의 메트릭을 수집합니다. Linux 호스트
메트릭을 정확히 수집하려면 `--path.rootfs=/host` 인자와 호스트 루트
마운트(`/:/host:ro,rslave`)를 추가하세요.

## 종료

```bash
docker compose down        # 데이터 유지
docker compose down -v     # 볼륨까지 삭제
```
