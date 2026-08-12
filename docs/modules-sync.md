---
branch: modules/sync
description: 서브 모듈 변경을 메인 모듈 dev에 sync PR로 반영하는 자동화
provides:
  - .github/workflows/sub-module-dispatch.yml
  - .github/workflows/main-module-sync.yml
  - Dockerfile
  - docker-compose.yml
  - .env.example
  - scripts/module-sync-local.sh
  - scripts/.gitattributes
  - docs/modules-sync.md
requires: []
works-with:
  - branch: modules/main
    reason: 메인 모듈 운영 기준을 정의
  - branch: modules/sub
    reason: 서브 모듈 운영 기준을 정의
conflicts: []
placeholders: []
secrets:
  - MAIN_MODULE_DISPATCH_TOKEN
  - MODULE_SYNC_TOKEN
after-import:
  - 서브 모듈 저장소에 MAIN_MODULE_DISPATCH_TOKEN secret과 variable 등록
  - 메인 모듈 저장소에 MODULE_SYNC_TOKEN 등록 (sync PR에서 CI를 실행하려면 필수)
verify:
  - actionlint .github/workflows/main-module-sync.yml .github/workflows/sub-module-dispatch.yml
  - shellcheck scripts/module-sync-local.sh
---

# Module Sync Guide

이 문서는 서브 모듈 변경사항을 메인 모듈의 `dev` 브랜치로 반영하는 자동화 방법을 정의합니다.

- `modules/main`과 `modules/sub`은 메인/서브 모듈의 개념과 운영 기준을 설명합니다.
- `modules/sync`는 서브 모듈의 변경을 메인 모듈에 반영하는 실제 GitHub Actions workflow를 제공합니다.
- 기본 전략은 서브 모듈 `main` 또는 `release/*` 변경을 감지한 뒤, 메인 모듈 `dev` 브랜치 대상으로 sync PR을 생성하는 것입니다.

## Files

```text
.env.example
Dockerfile
docker-compose.yml
.github/workflows/sub-module-dispatch.yml
.github/workflows/main-module-sync.yml
scripts/module-sync-local.sh
docs/modules-sync.md
```

## Sync Flow

```text
sub module main/release push
        ↓
sub-module-dispatch.yml
        ↓
repository_dispatch
        ↓
main-module-sync.yml
        ↓
main module dev 대상 sync PR 생성
```

자동으로 `dev`에 직접 push하지 않고 PR을 만드는 방식을 기본으로 사용합니다.
서브 모듈 변경이 메인 모듈의 빌드나 테스트를 깨뜨릴 수 있으므로, CI 검증과 리뷰를 거친 뒤 병합하는 것이 안전합니다.

## Workflow Roles

| Workflow | Repository | Role |
| --- | --- | --- |
| `sub-module-dispatch.yml` | Sub module repository | 서브 모듈 변경을 메인 모듈 저장소에 알림 |
| `main-module-sync.yml` | Main module repository | 알림을 받아 `dev` 대상 sync PR 생성 |

## Sync Modes

서브 모듈을 메인 모듈에 반영하는 방식은 프로젝트 구조에 따라 선택합니다.

| Mode | Description | Use Case |
| --- | --- | --- |
| `submodule` | 기존 Git submodule commit pointer를 갱신 | 서브 모듈이 이미 Git submodule로 등록되어 있고 commit hash로 고정해야 할 때 |
| `subtree` | 서브 모듈 저장소 내용을 특정 폴더로 가져옴 | 메인 모듈 저장소 안에 서브 모듈 코드를 복사해 함께 관리하고 싶을 때 |

## Sub Module Repository Settings

서브 모듈 저장소에는 `.github/workflows/sub-module-dispatch.yml`을 둡니다.

필수 secret:

| Name | Description |
| --- | --- |
| `MAIN_MODULE_DISPATCH_TOKEN` | 메인 모듈 저장소에 `repository_dispatch`를 보낼 수 있는 token |

필수 variable:

| Name | Description | Example |
| --- | --- | --- |
| `MAIN_MODULE_REPOSITORY` | 메인 모듈 저장소 | `owner/main-module-repo` |
| `MODULE_NAME` | 서브 모듈 이름 | `auth-module` |
| `MODULE_PATH` | 메인 모듈 저장소 안의 서브 모듈 경로 | `backend/auth-module` |

token 권한:

- 대상 메인 모듈 저장소에 접근 가능해야 합니다.
- `repository_dispatch` 이벤트를 보낼 수 있어야 합니다.
- private repository라면 fine-grained token 또는 classic PAT 권한을 확인합니다.

## Main Module Repository Settings

메인 모듈 저장소에는 `.github/workflows/main-module-sync.yml`을 둡니다.

선택 variable:

| Name | Description | Default |
| --- | --- | --- |
| `MODULE_SYNC_MODE` | `submodule` 또는 `subtree` | `submodule` |

권장 secret:

| Name | Description |
| --- | --- |
| `MODULE_SYNC_TOKEN` | sync branch push와 PR 생성에 사용할 PAT 또는 GitHub App token |

workflow 권한:

```yaml
permissions:
  contents: write
  pull-requests: write
```

이 권한은 sync branch push와 PR 생성을 위해 필요합니다.

### MODULE_SYNC_TOKEN이 필요한 이유

GitHub 정책상 기본 `GITHUB_TOKEN`으로 생성한 PR은 다른 workflow를 트리거하지
않습니다. 즉 `MODULE_SYNC_TOKEN` 없이 만들어진 sync PR에서는 `pull_request`
이벤트 기반 CI가 실행되지 않습니다. 이 문서의 Branch Strategy Integration
규칙("sync PR에서는 메인 모듈 CI를 반드시 실행")을 지키려면 다음 중 하나가
필요합니다.

1. `MODULE_SYNC_TOKEN`에 fine-grained PAT(contents: write, pull-requests: write)
   또는 GitHub App token을 등록합니다. 이 template의 workflow는 secret이 있으면
   자동으로 사용합니다.
2. token을 등록하지 않는 경우, sync PR에 대해 수동으로 CI를 실행하거나
   `workflow_dispatch` 기반 검증 절차를 사용합니다.

`MODULE_SYNC_TOKEN`은 private 서브 모듈 접근에도 사용됩니다. checkout 단계에서
등록한 token은 같은 GitHub 호스트의 fetch에 재사용되므로, token이 서브 모듈
저장소 읽기 권한을 가지고 있으면 private 저장소의 subtree fetch와 submodule
update가 함께 동작합니다.

## Local Docker Setup

GitHub Actions에 적용하기 전에 로컬에서 module sync 흐름을 확인할 수 있도록 Docker Compose 설정을 제공합니다.

```text
Dockerfile
docker-compose.yml
.env.example
scripts/module-sync-local.sh
```

`.env.example`을 복사해 `.env`를 생성합니다.

```bash
cp .env.example .env
```

주요 환경 변수:

| Name | Description |
| --- | --- |
| `MAIN_MODULE_REPOSITORY` | 메인 모듈 GitHub 저장소 |
| `MAIN_MODULE_DISPATCH_TOKEN` | repository dispatch 전송용 token |
| `MODULE_NAME` | 서브 모듈 이름 |
| `MODULE_PATH` | 메인 모듈 저장소 안의 서브 모듈 경로 |
| `MODULE_REPOSITORY` | 서브 모듈 GitHub 저장소 |
| `MODULE_REF` | 가져올 branch 또는 tag |
| `MODULE_SHA` | 동기화할 commit SHA. submodule mode에서는 필수, subtree mode에서는 재현 가능한 동기화를 위해 권장 |
| `MODULE_SYNC_MODE` | `submodule` 또는 `subtree` |
| `MAIN_MODULE_LOCAL_PATH` | 로컬 메인 모듈 저장소 경로 |
| `SYNC_BRANCH_PREFIX` | 로컬 sync branch prefix |

로컬 실행:

```bash
docker compose run --rm module-sync
```

이 명령은 `MAIN_MODULE_LOCAL_PATH`에 지정한 로컬 메인 모듈 저장소를 컨테이너에 마운트한 뒤, `dev` 기준 sync branch를 생성합니다.

주의사항:

- 로컬 메인 모듈 저장소에는 `dev` 브랜치가 있어야 합니다.
- subtree mode에서는 `git subtree` 명령을 사용합니다.
- subtree mode에서 `MODULE_SHA`가 있으면 `MODULE_REF`의 최신 상태가 아니라 해당 commit SHA를 우선 반영합니다.
- submodule mode에서는 `MODULE_SHA` 값이 필요합니다.
- submodule mode는 이미 등록된 submodule path의 commit pointer를 갱신하는 용도입니다.
- 로컬 실행은 PR을 자동 생성하지 않고 sync branch까지만 만듭니다.

## Submodule Mode

`submodule` mode는 메인 모듈 저장소가 서브 모듈 저장소를 Git submodule로 이미 가지고 있을 때 사용합니다.
이 workflow는 최초 submodule 추가가 아니라 기존 submodule path의 commit pointer를 갱신하는 흐름을 기본으로 합니다.
최초 추가가 필요하면 메인 모듈 저장소에서 먼저 `git submodule add`로 `.gitmodules`와 submodule path를 구성한 뒤 사용합니다.

메인 모듈 저장소 예시:

```text
backend/auth-module  # Git submodule path
```

동작:

1. 서브 모듈 저장소의 `main` 또는 `release/*`에 push됩니다.
2. 서브 모듈 workflow가 메인 모듈 저장소로 dispatch를 보냅니다.
3. 메인 모듈 workflow가 `dev`에서 sync branch를 생성합니다.
4. 기존 submodule path를 전달받은 commit SHA로 checkout합니다.
5. 변경된 submodule pointer를 커밋합니다.
6. `dev` 대상으로 PR을 생성합니다.

## Subtree Mode

`subtree` mode는 서브 모듈 저장소 내용을 메인 모듈 저장소의 특정 폴더로 가져오고 싶을 때 사용합니다.

메인 모듈 저장소 예시:

```text
backend/auth-module  # copied by git subtree
```

동작:

1. 서브 모듈 저장소의 `main` 또는 `release/*`에 push됩니다.
2. 서브 모듈 workflow가 메인 모듈 저장소로 dispatch를 보냅니다.
3. 메인 모듈 workflow가 `dev`에서 sync branch를 생성합니다.
4. `MODULE_SHA`가 있으면 해당 commit SHA를 우선 사용하고, 없으면 `MODULE_REF`를 사용합니다.
5. 기존 subtree path가 있으면 `git subtree pull --prefix=<module_path>`로 변경사항을 가져옵니다.
6. subtree path가 아직 없으면 `git subtree add --prefix=<module_path>`로 최초 반영합니다.
7. `dev` 대상으로 PR을 생성합니다.

branch나 tag는 workflow 실행 중에 새 커밋을 가리키도록 이동할 수 있습니다.
dispatch payload에 `MODULE_SHA`가 포함된 경우에는 그 SHA를 기준으로 동기화해야 어떤 서브 모듈 커밋이 메인 모듈에 반영되었는지 추적하기 쉽습니다.

## Manual Dispatch

자동 dispatch가 아니라 수동으로 실행할 수도 있습니다.

메인 모듈 저장소의 Actions 탭에서 `Main Module Sync` workflow를 실행하고 다음 값을 입력합니다.

| Input | Example |
| --- | --- |
| `module_name` | `auth-module` |
| `module_path` | `backend/auth-module` |
| `module_repository` | `owner/auth-module` |
| `module_ref` | `main` |
| `module_sha` | `abc1234...` |
| `sync_mode` | `submodule` |

`subtree` mode에서도 재현 가능한 동기화가 필요하면 `module_sha`를 함께 입력합니다.

## Branch Strategy Integration

권장 흐름:

```text
sub module dev -> sub module release/* -> sub module main
                                      ↓
                            repository_dispatch
                                      ↓
                      main module sync/* -> main module dev
```

규칙:

- 서브 모듈의 `main`은 메인 모듈로 가져올 수 있는 안정 상태여야 합니다.
- 메인 모듈에는 자동으로 직접 push하지 않고 sync PR을 생성합니다.
- sync PR에서는 메인 모듈 CI를 반드시 실행합니다.
- sync PR이 실패하면 서브 모듈 변경 또는 메인 모듈 연결 코드를 수정합니다.

## Pull Request Rules

sync PR 본문에는 다음 정보가 포함됩니다.

- module name
- module repository
- module ref
- module SHA
- module path
- sync mode

리뷰어는 다음 항목을 확인합니다.

- 메인 모듈 CI가 통과했는가?
- 서브 모듈 변경이 의도한 버전인가?
- API contract 또는 event schema 변경이 있는가?
- 메인 모듈 설정 변경이 추가로 필요한가?

## Conflict Handling

subtree mode에서 서브 모듈 변경과 메인 모듈의 subtree path 내부 수정이 충돌하면
`git subtree pull`이 실패하고 workflow가 에러로 종료됩니다. 충돌은 자동으로
해결하지 않으며, 다음 절차로 수동 처리합니다.

1. 로컬에서 `scripts/module-sync-local.sh`로 같은 동기화를 재현합니다.
2. 충돌을 해결하고 commit한 뒤 sync branch를 push합니다.
3. `dev` 대상 PR을 수동으로 생성합니다.

같은 commit SHA로 dispatch가 다시 발생하면 기존 sync branch는
`--force-with-lease`로 갱신되고, 이미 열린 PR이 있으면 재사용합니다.

## Security Rules

- `MAIN_MODULE_DISPATCH_TOKEN`은 GitHub Secret으로 관리합니다.
- token은 필요한 저장소와 권한으로만 제한합니다.
- private submodule 또는 subtree를 사용하는 경우 `MODULE_SYNC_TOKEN`에 해당
  저장소 읽기 권한을 부여합니다 (위 "MODULE_SYNC_TOKEN이 필요한 이유" 참고).
- 자동 sync가 너무 넓은 권한으로 동작하지 않도록 repository 단위 권한을 제한합니다.

## Import Command

`dev` 브랜치에서 이 설정을 가져올 때는 다음 명령을 사용합니다.

```bash
git merge --squash origin/modules/sync
git commit -m "init: add module sync workflow"
```

## Standalone Usage

두 workflow는 각각 다른 저장소(서브/메인)에 배치해야 하므로, 이 브랜치를
하나의 저장소에 가져온 뒤 역할에 맞는 workflow만 남기고 사용합니다. 로컬
Docker 도구(scripts/module-sync-local.sh)는 단독으로 동기화 리허설에 사용할
수 있습니다.

## Works With

`modules/main`, `modules/sub` 문서가 이 자동화의 운영 기준(모듈 역할,
의존 방향)을 제공합니다.
