---
branch: modules/main
description: 멀티모듈 구조에서 메인 모듈의 책임과 의존 방향 기준
provides:
  - docs/modules-main.md
requires: []
works-with:
  - branch: modules/sub
    reason: 메인/서브 모듈의 역할 구분을 한 쌍으로 정의
  - branch: modules/sync
    reason: 서브 모듈 변경을 메인 모듈에 반영하는 자동화를 제공
conflicts: []
placeholders: []
secrets: []
after-import:
  - 모듈 이름과 의존 방향을 실제 프로젝트 구조에 맞게 조정
verify:
  - test -f docs/modules-main.md
---

# Main Module Guide

이 문서는 실제 프로젝트에서 메인 모듈을 어떻게 정의하고 운영할지 정리합니다.

- 메인 모듈은 프로젝트의 중심 실행 단위 또는 조립 기준이 되는 모듈입니다.
- 서브 모듈은 메인 모듈이 사용하는 기능, 도메인, 인프라, 데이터 처리 단위로 분리합니다.
- 메인 모듈은 전체 프로젝트의 실행 흐름, 공통 설정, 모듈 연결 규칙을 관리합니다.

## Main Module Definition

메인 모듈은 프로젝트에서 다음 역할을 담당합니다.

- 애플리케이션 진입점 관리
- 공통 설정 조립
- 서브 모듈 연결
- 전체 실행 방법 제공
- 배포 기준 제공
- 공통 환경 변수 관리
- 전체 테스트와 통합 검증 기준 제공

예시:

```text
backend/spring-boot-app/        # 백엔드 중심 프로젝트의 메인 모듈
frontend/react-vite-app/        # 프론트엔드 중심 프로젝트의 메인 모듈
backend/api-gateway/            # 여러 서비스 앞단의 메인 모듈
```

## Recommended Structure

메인 모듈이 있는 프로젝트는 다음처럼 구성할 수 있습니다.

```text
.
├── backend/
│   ├── main-app/
│   ├── auth-module/
│   ├── user-module/
│   └── common-module/
├── frontend/
│   ├── main-app/
│   ├── feature-auth/
│   └── shared-ui/
├── data/
│   ├── main-pipeline/
│   └── jobs/
├── docs/
└── .github/
```

모듈 이름은 프로젝트 성격에 맞게 변경할 수 있습니다.

```text
backend/spring-boot-app
backend/auth-module
backend/payment-module
backend/common-module
```

## Main Module Responsibilities

메인 모듈은 다음 책임을 가집니다.

| Responsibility | Description |
| --- | --- |
| Entry Point | 애플리케이션 시작 지점 관리 |
| Configuration | 공통 설정, 환경 변수, profile 관리 |
| Module Wiring | 서브 모듈 의존성 연결 |
| Runtime | 로컬 실행, Docker 실행, 배포 실행 기준 제공 |
| Integration | 서브 모듈 간 통합 흐름 검증 |
| Documentation | 전체 프로젝트 실행 방법과 운영 기준 설명 |

## What Should Be In Main Module

메인 모듈에 포함하기 좋은 항목:

- 애플리케이션 bootstrap 코드
- routing 또는 controller entry point
- dependency injection 설정
- 공통 middleware, interceptor, filter 설정
- 공통 exception handler 연결
- 공통 security 설정 연결
- profile별 configuration
- 전체 실행용 Dockerfile 또는 compose 연결

예시:

```text
main-app/
  src/
    main/
    config/
    bootstrap/
  Dockerfile
  README.md
```

## What Should Not Be In Main Module

메인 모듈에 모든 기능을 몰아넣지 않습니다.

피해야 할 항목:

- 특정 도메인 비즈니스 로직 전체
- 여러 도메인의 repository 직접 구현
- 공통 유틸리티가 아닌 임시 helper 모음
- 서브 모듈 내부 구현에 대한 과도한 의존
- 테스트하기 어려운 거대한 service class

메인 모듈이 너무 커지면 서브 모듈 분리를 검토합니다.

## Dependency Rules

메인 모듈은 서브 모듈을 조립할 수 있지만, 서브 모듈은 메인 모듈에 의존하지 않는 것을 기본 원칙으로 합니다.

권장 방향:

```text
main module -> sub module
main module -> common module
sub module  -> common module
```

피해야 할 방향:

```text
sub module -> main module
common module -> main module
common module -> sub module
```

의존 방향은 문서 규칙만으로는 강제되지 않습니다. 다음 도구로 순환 의존을
빌드/CI에서 검출하는 것을 권장합니다.

| Stack | Tool |
| --- | --- |
| JVM | ArchUnit (`layeredArchitecture` 규칙) |
| JS/TS | dependency-cruiser |
| Python | import-linter |

## Build Tool Examples

스택별 멀티모듈 구성의 최소 예시입니다.

### Gradle (settings.gradle)

```groovy
rootProject.name = 'my-service'

include 'app'          // main module: 조립과 실행
include 'module-auth'  // sub module
include 'module-order' // sub module
include 'common'       // common module
```

```groovy
// app/build.gradle — main module만 서브 모듈을 조립합니다.
dependencies {
    implementation project(':module-auth')
    implementation project(':module-order')
    implementation project(':common')
}
```

### pnpm workspace (pnpm-workspace.yaml)

```yaml
packages:
  - apps/*      # main module (예: apps/web)
  - packages/*  # sub/common module (예: packages/auth, packages/ui)
```

```json
// apps/web/package.json — workspace 프로토콜로 서브 모듈을 참조합니다.
{
  "dependencies": {
    "@my-service/auth": "workspace:*",
    "@my-service/ui": "workspace:*"
  }
}
```

### uv workspace (pyproject.toml)

```toml
# 루트 pyproject.toml
[tool.uv.workspace]
members = ["apps/api", "packages/auth", "packages/common"]
```

```toml
# apps/api/pyproject.toml — main module
[project]
dependencies = ["my-service-auth", "my-service-common"]

[tool.uv.sources]
my-service-auth = { workspace = true }
my-service-common = { workspace = true }
```

## Configuration Rules

메인 모듈은 전체 프로젝트 실행에 필요한 설정을 관리합니다.

권장 기준:

- 공통 환경 변수는 메인 모듈 README에 정리합니다.
- 모듈별 환경 변수는 각 서브 모듈 README에 정리합니다.
- secret 값은 코드에 직접 포함하지 않습니다.
- profile 또는 environment별 설정을 명확히 분리합니다.

예시:

```text
main-app/
  .env.example
  application-local.yml
  application-dev.yml
  application-prod.yml
```

## Test Rules

메인 모듈은 전체 조립이 정상적으로 동작하는지 확인합니다.

권장 테스트:

| Test | Purpose |
| --- | --- |
| Smoke Test | 애플리케이션이 정상적으로 시작되는지 확인 |
| Integration Test | 서브 모듈 연결과 주요 흐름 확인 |
| Contract Test | API 요청/응답 또는 event schema 확인 |
| E2E Test | 실제 사용자 흐름 확인 |

서브 모듈의 상세 단위 테스트는 각 서브 모듈에서 관리합니다.

## Pull Request Rules

메인 모듈을 수정하는 PR은 영향 범위를 명확히 작성합니다.

PR 본문에 포함할 내용:

- 변경된 설정
- 연결된 서브 모듈
- 실행 또는 배포 영향
- 확인한 테스트
- rollback 또는 복구 방법

## Import Command

`dev` 브랜치에서 이 문서를 가져올 때는 다음 명령을 사용합니다.

```bash
git merge --squash origin/modules/main
git commit -m "init: add main module guide"
```

## Standalone Usage

이 브랜치는 문서 전용입니다. 빌드 도구 설정(Gradle include, pnpm workspace
등)은 포함하지 않으므로 스택에 맞는 모듈 설정을 별도로 구성합니다.

## Works With

`modules/sub`(서브 모듈 기준), `modules/sync`(저장소 간 동기화 자동화)와
한 세트로 사용합니다.
