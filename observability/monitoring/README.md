# Monitoring Stack Import Guide

이 문서는 monitoring stack 관련 브랜치를 `dev` 브랜치로 가져오는 명령어를 정리합니다.

## Available Branches

| Branch | Description | Result Path |
| --- | --- | --- |
| `observability/prometheus-grafana` | Prometheus, Grafana 통합 실행 템플릿 | `observability/prometheus-grafana/` |

## Before Import

```bash
git switch dev
git fetch origin
```

## Prometheus Grafana

Single Commit Mode:

```bash
git read-tree --prefix=observability/prometheus-grafana/ -u origin/observability/prometheus-grafana
git commit -m "init: add Prometheus Grafana"
```

Full History Mode:

```bash
git subtree add --prefix=observability/prometheus-grafana origin/observability/prometheus-grafana
```
