# Logging Stack Import Guide

이 문서는 logging stack 관련 브랜치를 `dev` 브랜치로 가져오는 명령어를 정리합니다.

## Available Branches

| Branch | Description | Result Path |
| --- | --- | --- |
| `observability/elastic-stack` | Elasticsearch, Kibana, Logstash, Beats 통합 실행 템플릿 | `observability/elastic-stack/` |

## Before Import

```bash
git switch dev
git fetch origin
```

## Elastic Stack

Single Commit Mode:

```bash
git read-tree --prefix=observability/elastic-stack/ -u origin/observability/elastic-stack
git commit -m "init: add Elastic Stack"
```

Full History Mode:

```bash
git subtree add --prefix=observability/elastic-stack origin/observability/elastic-stack
```
