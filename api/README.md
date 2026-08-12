# API Import Guide

이 문서는 API 규칙 관련 브랜치를 `dev` 브랜치로 가져오는 명령어를 정리합니다.

## Available Branches

| Branch | Description | Result Path |
| --- | --- | --- |
| `api/http-response` | 성공, 실패, 인증, 권한, validation, 외부 API 오류 등 상황별 HTTP 응답 기준 | `docs/api-http-response.md` |

## Before Import

```bash
git switch dev
git fetch origin
```

## HTTP Response

Single Commit Mode:

```bash
git merge --squash origin/api/http-response
git commit -m "init: add HTTP response guide"
```

Full History Mode:

```bash
git merge --no-ff -m "init: merge HTTP response guide" origin/api/http-response
```
