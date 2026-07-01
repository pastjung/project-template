# Project Template Repository

이 저장소는 새 프로젝트를 시작할 때 필요한 초기 세팅을 빠르게 조립하기 위한
브랜치 기반 프로젝트 템플릿 저장소입니다.

각 기술 스택과 공통 설정은 독립 브랜치에서 관리하고, 실제 프로젝트를 만들 때
필요한 브랜치만 선택해서 `dev` 브랜치에 조립한 뒤 새 원격 저장소의 `main`
브랜치로 연결하는 방식으로 사용합니다.

## Branch Roles

| Branch | Role |
| --- | --- |
| `main` | 이 템플릿 저장소의 사용법과 브랜치 카탈로그를 관리합니다. |
| `dev` | 새 프로젝트를 만들기 위한 조립용 브랜치입니다. |
| `settings/*` | 에디터, IDE, 개발 환경 기본값을 관리합니다. |
| `git/*` | `.gitignore`, `.gitattributes`처럼 Git 동작에 직접 영향을 주는 설정을 관리합니다. |
| `docs/*` | 브랜치 전략, 커밋 전략, 코드 컨벤션 같은 문서형 운영 기준을 관리합니다. |
| `github/*` | GitHub 템플릿, 라벨, CODEOWNERS, Actions workflow를 관리합니다. |
| `ai/*` | AI 코드 리뷰와 AI 협업 가이드를 관리합니다. |
| `api/*` | API 설계와 응답 규칙을 관리합니다. |
| `modules/*` | 메인 모듈, 서브 모듈, 모듈 동기화 운영 기준을 관리합니다. |
| `frontend/*` | Frontend 애플리케이션 초기 세팅을 관리합니다. |
| `backend/*` | Backend 애플리케이션 초기 세팅을 관리합니다. |
| `data/*` | Database, cache, streaming, batch 처리 초기 세팅을 관리합니다. |
| `observability/*` | Logging, monitoring 초기 세팅을 관리합니다. |

## Import Guides

각 브랜치를 `dev`로 가져오는 구체적인 명령어는 역할별 README에서 관리합니다.

| Area | Guide | Description |
| --- | --- | --- |
| Settings | [settings/README.md](settings/README.md) | EditorConfig 같은 개발 환경 기본값 |
| Git | [git/README.md](git/README.md) | Git attributes, Git ignore |
| Docs | [docs/README.md](docs/README.md) | 브랜치 전략, 커밋 전략, 코드 컨벤션 |
| GitHub | [github/README.md](github/README.md) | PR/Issue 템플릿, 라벨, CODEOWNERS, semantic PR, stale issue, Slack 알림 |
| AI | [ai/README.md](ai/README.md) | AI 리뷰 가이드와 AI 리뷰 workflow |
| API | [api/README.md](api/README.md) | HTTP 응답 규칙 |
| Modules | [modules/README.md](modules/README.md) | 메인 모듈, 서브 모듈, 모듈 동기화 |
| Backend | [backend/README.md](backend/README.md) | Spring Boot, FastAPI, Django 초기 세팅 |
| Frontend | [frontend/README.md](frontend/README.md) | React + Vite, Vue + Vite 초기 세팅 |
| Data | [data/README.md](data/README.md) | MySQL, PostgreSQL, MongoDB, Redis, Kafka, Flink, Spark, Airflow |
| Observability | [observability/README.md](observability/README.md) | Elasticsearch, Kibana, Logstash, Beats, Prometheus, Grafana |

## Branch Catalog

| Group | Guide | Branches |
| --- | --- | --- |
| Settings | [settings/README.md](settings/README.md) | `settings/editor-config` |
| Git | [git/README.md](git/README.md) | `git/attributes`, `git/ignore` |
| Docs | [docs/README.md](docs/README.md) | `docs/branch-strategy`, `docs/commit-strategy`, `docs/code-convention` |
| GitHub | [github/README.md](github/README.md) | `github/pr-template`, `github/issue-template`, `github/labels`, `github/codeowners`, `github/semantic-pr`, `github/stale-issues`, `github/slack-notification` |
| AI | [ai/README.md](ai/README.md) | `ai/review-guide`, `ai/review-openai`, `ai/review-gemini`, `ai/review-claude`, `ai/review-copilot` |
| API | [api/README.md](api/README.md) | `api/http-response` |
| Modules | [modules/README.md](modules/README.md) | `modules/main`, `modules/sub`, `modules/sync` |
| Backend apps | [backend/apps/README.md](backend/apps/README.md) | `backend/spring-boot`, `backend/fastapi`, `backend/django` |
| Frontend apps | [frontend/apps/README.md](frontend/apps/README.md) | `frontend/react-vite`, `frontend/vue-vite` |
| Databases and cache | [data/databases/README.md](data/databases/README.md) | `data/mysql`, `data/postgresql`, `data/mongodb`, `data/redis` |
| Data streaming and batch | [data/pipelines/README.md](data/pipelines/README.md) | `data/kafka`, `data/flink`, `data/spark`, `data/airflow` |
| Logging stack | [observability/logging/README.md](observability/logging/README.md) | `observability/elastic-stack` |
| Monitoring stack | [observability/monitoring/README.md](observability/monitoring/README.md) | `observability/prometheus-grafana` |

## Recommended Project Setup Order

새 프로젝트를 만들 때는 모든 브랜치를 한 번에 가져오기보다, 충돌 가능성이 낮고
팀 전체에 영향을 주는 기본 설정부터 적용하는 것을 권장합니다.

| Order | Branch | Priority | When to Import | After Import |
| --- | --- | --- | --- | --- |
| 1 | [`settings/editor-config`](settings/README.md) | 필수 | 프로젝트 파일을 본격적으로 추가하기 전 | 언어별 들여쓰기 규칙이 팀 기준과 맞는지 확인합니다. |
| 2 | [`git/attributes`](git/README.md) | 필수 | `.editorconfig` 다음 | Windows, macOS, Linux 혼합 사용 여부에 맞춰 줄 끝 정책과 binary 확장자를 확인합니다. |
| 3 | [`git/ignore`](git/README.md) | 필수 | 기술 스택 브랜치를 가져오기 전 | 실제 사용하는 언어, IDE, 빌드 도구에 맞춰 ignore 규칙을 보강합니다. |
| 4 | [`docs/branch-strategy`](docs/README.md) | 추천 | 협업 브랜치 흐름을 정하기 전 | Git Flow, GitHub Flow, trunk-based 등 팀 운영 방식에 맞춰 수정합니다. |
| 5 | [`docs/commit-strategy`](docs/README.md) | 추천 | PR 제목, changelog, release note 규칙을 정하기 전 | commit type, scope 사용 여부, squash merge 정책을 팀 기준에 맞춥니다. |
| 6 | [`github/labels`](github/README.md) | 추천 | issue, PR, stale 정책을 운영하기 전 | 실제 사용할 라벨만 남기고 `status/stale` 같은 자동화 라벨을 확인합니다. |
| 7 | [`github/semantic-pr`](github/README.md) | 추천 | [`docs/commit-strategy`](docs/README.md) 적용 후 | 허용 type과 scope 필수 여부를 commit 전략과 일치시킵니다. |
| 8 | [`github/pr-template`](github/README.md), [`github/issue-template`](github/README.md) | 추천 | GitHub에서 PR과 issue를 운영하기 전 | 템플릿 질문, 체크리스트, 담당자 흐름을 프로젝트에 맞게 줄이거나 추가합니다. |
| 9 | [`github/codeowners`](github/README.md) | 추천 | PR 리뷰 담당 영역을 자동 요청하고 싶을 때 | 실제 GitHub organization, team 이름으로 owner placeholder를 교체합니다. |
| 10 | [`github/stale-issues`](github/README.md) | 선택 | issue를 꾸준히 관리해야 할 때 | stale 기간, 자동 close 여부, 예외 라벨을 팀 합의에 맞게 수정합니다. |
| 11 | [`github/slack-notification`](github/README.md) | 선택 | GitHub Actions 알림을 Slack으로 받을 때 | webhook, 알림 대상 workflow, 채널 정책을 확인합니다. |
| 12 | [`docs/code-convention`](docs/README.md) | 추천 | 본격적인 코드 작성 전 | 사용하는 언어와 formatter, linter 기준에 맞춰 구체화합니다. |
| 13 | [`api/http-response`](api/README.md) | 선택 | API 서버를 만드는 프로젝트에서 | 응답 포맷과 에러 코드 체계를 백엔드 스택에 맞게 조정합니다. |
| 14 | [`modules/main`](modules/README.md), [`modules/sub`](modules/README.md), [`modules/sync`](modules/README.md) | 선택 | 멀티 모듈이나 저장소 간 동기화가 필요할 때 | 모듈 이름, 동기화 대상, GitHub secret을 실제 구조에 맞게 수정합니다. |
| 15 | [`ai/review-*`](ai/README.md) | 선택 | AI 코드 리뷰 workflow를 쓸 때 | API key, 실행 조건, 비용 정책을 확인합니다. |

최소 세팅만 빠르게 시작하려면 [`settings/editor-config`](settings/README.md), [`git/attributes`](git/README.md),
[`git/ignore`](git/README.md)를 먼저 적용합니다. PR 기반 협업까지 바로 시작하려면
[`docs/commit-strategy`](docs/README.md), [`github/labels`](github/README.md), [`github/semantic-pr`](github/README.md), [`github/pr-template`](github/README.md)을
이어서 적용하는 흐름이 가장 무난합니다.

## Composition Rules

브랜치를 `dev`로 가져오는 방식은 세 가지입니다.

### Folder Bundle Mode

설정 계열을 폴더 단위로 한 번에 가져오고 싶을 때 사용합니다. `backend`, `frontend`,
`data`, `observability`는 보통 필요한 기술 스택만 선택해서 가져오므로 폴더 단위
병합 예시에서 제외합니다.

Single Commit Mode로 폴더 전체를 하나의 커밋에 모으려면 필요한 브랜치를 모두
`merge --squash`한 뒤 한 번만 커밋합니다.

```bash
git merge --squash origin/settings/editor-config
git commit -m "init: add settings"
```

```bash
git merge --squash origin/git/attributes origin/git/ignore
git commit -m "init: add Git settings"
```

```bash
git merge --squash origin/docs/branch-strategy origin/docs/commit-strategy origin/docs/code-convention
git commit -m "init: add documentation standards"
```

```bash
git merge --squash origin/github/pr-template origin/github/issue-template origin/github/labels origin/github/codeowners origin/github/semantic-pr origin/github/stale-issues origin/github/slack-notification
git commit -m "init: add GitHub templates and automation"
```

```bash
git merge --squash origin/ai/review-guide origin/ai/review-openai origin/ai/review-gemini origin/ai/review-claude origin/ai/review-copilot
git commit -m "init: add AI review guides"
```

```bash
git merge --squash origin/api/http-response
git commit -m "init: add API response standard"
```

```bash
git merge --squash origin/modules/main origin/modules/sub origin/modules/sync
git commit -m "init: add module standards"
```

### Single Commit Mode

초기 세팅 내용을 하나의 커밋으로만 남기고 싶을 때 사용합니다. 새 프로젝트의
히스토리를 단순하게 유지하고 싶다면 이 방식을 기본으로 사용합니다.

루트에 그대로 들어가는 설정 브랜치는 `merge --squash`로 가져온 뒤 직접 커밋합니다.

```bash
git merge --squash origin/settings/editor-config
git commit -m "init: add editor config"
```

애플리케이션이나 인프라 템플릿 브랜치는 독립 프로젝트처럼 루트에 파일을 두고
관리하므로 `read-tree --prefix`로 원하는 프로젝트 폴더 아래에 가져온 뒤 직접
커밋합니다.

```bash
git read-tree --prefix=backend/fastapi-app/ -u origin/backend/fastapi
git commit -m "init: add FastAPI app"
```

이 방식은 브랜치 하나를 가져올 때 `dev`에 `init: ...` 커밋 하나만 남기는 것을
목표로 합니다.

### Full History Mode

초기 세팅 브랜치 안에 의미 있는 단계별 커밋이 있을 때 사용합니다. 예를 들어
Spring Boot 템플릿에서 에러 코드, CORS 설정, 공통 응답 포맷, 인증 설정 등을
각 커밋으로 나누어 관리했다면 이 방식을 사용해 해당 커밋 기록을 보존할 수
있습니다.

루트에 그대로 들어가는 설정 브랜치의 커밋 기록을 보존하려면 일반 merge를 사용합니다.

```bash
git merge --no-ff -m "init: merge editor config" origin/settings/editor-config
```

애플리케이션이나 인프라 템플릿 브랜치의 커밋 기록을 보존하면서 특정 폴더 아래로
가져오려면 `git subtree add`를 `--squash` 없이 사용합니다.

```bash
git subtree add --prefix=backend/spring-boot-app origin/backend/spring-boot
```

정리하면, 히스토리를 깔끔하게 하나의 `init: ...` 커밋으로 남기고 싶으면
Single Commit Mode를 사용하고, 템플릿 브랜치의 세부 커밋 기록까지 새 프로젝트에
남기고 싶으면 Full History Mode를 사용합니다.

## New Project Workflow

1. 템플릿 저장소를 복제하고 `dev` 브랜치로 이동합니다.

   ```bash
   git clone https://github.com/pastjung/project-template.git <생성할 폴더명>
   ```
   ```bash
   cd <생성한 폴더명>
   ```
   ```bash
   git fetch origin
   git branch -r
   git switch --track origin/dev
   ```

   - `git fetch origin`: 템플릿 저장소의 모든 원격 브랜치 정보를 최신 상태로 가져옵니다.
   - `git branch -r`: `origin/settings/*`, `origin/git/*`, `origin/frontend/*` 같은 브랜치가 보이는지 확인합니다.
   - `git switch --track origin/dev`: `origin/dev`를 기준으로 로컬 `dev` 브랜치를 만듭니다.

2. 필요한 설정과 기술 스택을 `dev` 브랜치로 가져옵니다.

   각 영역별 README를 참고해 필요한 브랜치를 조립합니다.

3. 조립이 끝나면 기존 템플릿 원격 저장소 연결을 제거합니다.

   ```bash
   git remote remove origin
   ```

4. 현재 작업 중인 `dev` 브랜치를 새 프로젝트의 `main` 브랜치로 변경합니다.

   clone 직후에는 로컬에 템플릿 저장소의 `main` 브랜치가 이미 존재합니다. 기존
   `main`을 삭제해도 된다면 아래 명령을 사용합니다.

   ```bash
   git branch -D main
   git branch -m main
   ```

   기존 `main`을 삭제하지 않고 남겨두고 싶다면 백업 이름으로 변경한 뒤 진행합니다.

   ```bash
   git branch -m main template-main
   git branch -m main
   ```

5. 새 프로젝트 원격 저장소를 연결하고 push합니다.

   ```bash
   git remote add origin <new-project-repository-url>
   git push -u origin main
   ```

## Clean History Option

템플릿 저장소의 조립 히스토리를 새 프로젝트에 남기고 싶지 않다면, 조립을 마친
뒤 현재 파일 상태를 새 루트 커밋으로 만들 수 있습니다.

### PowerShell

```powershell
$rootCommit = git commit-tree "HEAD^{tree}" -m "🎉 init: initialize project"
git branch -f main $rootCommit
git switch main
git remote remove origin
git remote add origin <new-project-repository-url>
git push -u origin main
```

### Bash / Git Bash

```bash
rootCommit=$(git commit-tree HEAD^{tree} -m "🎉 init: initialize project")
git branch -f main "$rootCommit"
git switch main
git remote remove origin
git remote add origin <new-project-repository-url>
git push -u origin main
```
