# Observability Import Guide

이 문서는 Observability 계열 브랜치 전체 목록과 공통 import 규칙을 정리합니다.

Observability 템플릿은 `observability/<name>/` 아래로 가져옵니다. 실제로 가져오는
명령어는 하위 README에서 관리합니다.

## Groups

| Group | Guide | Description |
| --- | --- | --- |
| Logging stack | [logging/README.md](logging/README.md) | Elasticsearch, Kibana, Logstash, Beats |
| Monitoring stack | [monitoring/README.md](monitoring/README.md) | Prometheus, Grafana |

## Available Branches

| Branch | Result Path |
| --- | --- |
| `observability/elastic-stack` | `observability/elastic-stack/` |
| `observability/prometheus-grafana` | `observability/prometheus-grafana/` |

## Before Import

```bash
git switch dev
git fetch origin
```

## Import Modes

Single Commit Mode:

```bash
git read-tree --prefix=observability/<name>/ -u origin/observability/<branch-name>
git commit -m "init: add <name>"
```

Full History Mode:

```bash
git subtree add --prefix=observability/<name> origin/observability/<branch-name>
```
