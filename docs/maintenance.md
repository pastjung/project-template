# Template Maintenance Guide

이 템플릿 저장소를 최신 상태로 유지하기 위한 정기 점검 절차입니다.
분기(3개월)에 한 번 수행하는 것을 권장합니다.

## 1. 카탈로그 정합성 검사

```bash
git fetch origin
uv run scripts/validate_composition.py catalog
```

uv가 없으면 Docker로 실행합니다.

```bash
docker run --rm -v "$(pwd):/repo" -w /repo python:3.12-slim sh -c "apt-get update -qq > /dev/null && apt-get install -y -qq git > /dev/null; pip install -q pyyaml; git config --global --add safe.directory /repo; python scripts/validate_composition.py catalog"
```

"카탈로그 정합성 OK"가 나와야 합니다. 오류가 있으면 해당 브랜치의 front
matter나 파일 구조가 깨진 것입니다.

## 2. 버전 노후 점검

| 점검 대상 | 위치 | 확인 방법 |
| --- | --- | --- |
| AI 리뷰 기본 모델 | `ai/review-*` 브랜치의 workflow (`*_REVIEW_MODEL` 기본값) | 각 provider의 현행 모델명과 비교 |
| Docker 이미지 태그 | `data/*`, `observability/*` 브랜치의 docker-compose.yml | 각 프로젝트의 최신 안정 버전과 비교 |
| GitHub Actions SHA | 각 workflow 브랜치의 `uses:` 라인 | `git ls-remote --tags https://github.com/<owner>/<action>.git`으로 최신 태그 SHA 확인 |
| 프레임워크 버전 | `backend/*`의 build.gradle/pyproject.toml, `frontend/*`의 package.json | EOL 일정과 최신 LTS 확인 |

전 브랜치의 액션 버전을 한 번에 보려면:

```bash
for b in $(git branch -r --format='%(refname:short)' | grep -v HEAD); do git grep -h "uses:" "$b" -- '.github/workflows/' 2>/dev/null; done | sort -u
```

## 3. 브랜치 수정 절차

버전을 올릴 브랜치가 있으면 이 저장소의 커밋 규칙을 따릅니다.

```bash
git switch <branch>
# ... 수정 후 검증 (해당 브랜치 docs의 verify 명령) ...
git add -A && git commit -m "wip"          # 작업 커밋은 자유롭게
git reset --soft d48d8ad                    # 공통 루트 커밋
git commit -m "✨ feat: add <X> template"   # 클린 커밋으로 재작성
git push --force-with-lease origin <branch>
```

수정 후 1번의 카탈로그 검사를 다시 실행합니다.

## 4. 보류된 업그레이드 과제

다음 항목은 2026-08-12 점검에서 의도적으로 보류했습니다. 점검 시 재평가하세요.

- **Airflow 2.10 → 3.x**: 3.x는 아키텍처 변경이 커서 compose 재작성 필요
- **Kafka 3.8 → 4.x**: 클라이언트 라이브러리 호환성 확인 후
- **Elasticsearch 8.19 → 9.x**: breaking changes 확인 후 `.env`의 버전만 교체
- **Grafana alerting provisioning**: Alertmanager 도입과 함께 확장

## Agent에게 위임하기

Claude Code에서 이 저장소를 열고 다음과 같이 요청하면 됩니다.

> docs/maintenance.md 절차대로 템플릿 정기 점검을 수행해줘.
> 카탈로그 검사를 돌리고, 버전 노후 항목을 조사해서 표로 보고해줘.
> 수정은 내가 승인한 항목만 진행해.
