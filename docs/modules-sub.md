---
branch: modules/sub
description: 멀티모듈 구조에서 서브 모듈의 책임과 분리 기준
provides:
  - docs/modules-sub.md
requires: []
works-with:
  - branch: modules/main
    reason: 메인/서브 모듈의 역할 구분을 한 쌍으로 정의
  - branch: modules/sync
    reason: 서브 모듈 변경을 메인 모듈에 반영하는 자동화를 제공
conflicts: []
placeholders: []
secrets: []
after-import:
  - 모듈 분리 기준(when to / when not to)을 팀 상황에 맞게 검토
verify:
  - test -f docs/modules-sub.md
---

# Sub Module Guide

이 문서는 실제 프로젝트에서 서브 모듈을 어떻게 정의하고 운영할지 정리합니다.

- 서브 모듈은 메인 모듈에 조립되는 독립적인 기능, 도메인, 공통 코드, 인프라, 데이터 처리 단위입니다.
- 서브 모듈은 가능한 한 명확한 책임과 경계를 가져야 합니다.
- 서브 모듈은 메인 모듈에 직접 의존하지 않는 것을 기본 원칙으로 합니다.

## Sub Module Definition

서브 모듈은 프로젝트에서 다음 역할을 담당합니다.

- 특정 도메인 기능 제공
- 공통 기능 제공
- 외부 시스템 연동 캡슐화
- 데이터 처리 작업 제공
- UI feature 또는 shared component 제공
- 테스트 가능한 작은 단위로 책임 분리

예시:

```text
backend/auth-module
backend/user-module
backend/payment-module
backend/common-module
frontend/feature-auth
frontend/shared-ui
data/jobs
data/connectors
```

## Sub Module Types

| Type | Example | Purpose |
| --- | --- | --- |
| Domain Module | `auth-module`, `payment-module` | 특정 비즈니스 도메인 담당 |
| Common Module | `common-module`, `shared-ui` | 여러 모듈에서 사용하는 공통 기능 |
| Integration Module | `notification-module`, `payment-client` | 외부 API 또는 시스템 연동 |
| Data Module | `data/jobs`, `data/connectors` | 배치, 스트리밍, 데이터 처리 |
| Feature Module | `feature-auth`, `feature-dashboard` | 프론트엔드 기능 단위 |
| Infra Module | `observability`, `deployment` | 운영, 모니터링, 배포 설정 |

## When To Create Sub Module

다음 조건에 해당하면 서브 모듈 분리를 고려합니다.

- 기능이 독립적인 도메인 책임을 가집니다.
- 변경 이유가 메인 모듈과 다릅니다.
- 여러 모듈에서 재사용됩니다.
- 테스트를 독립적으로 작성할 수 있습니다.
- 외부 시스템 연동을 격리하고 싶습니다.
- 코드가 커져서 메인 모듈의 책임이 불명확해졌습니다.

아직 분리하지 않아도 되는 경우:

- 한 번만 쓰이는 작은 helper입니다.
- 모듈 경계가 명확하지 않습니다.
- 분리하면 의존성만 복잡해집니다.
- 테스트와 배포 흐름이 오히려 어려워집니다.

## Recommended Structure

백엔드 서브 모듈 예시:

```text
backend/
  main-app/
  auth-module/
    src/
    README.md
  user-module/
    src/
    README.md
  common-module/
    src/
    README.md
```

프론트엔드 서브 모듈 예시:

```text
frontend/
  main-app/
  feature-auth/
  feature-dashboard/
  shared-ui/
  shared-utils/
```

데이터 서브 모듈 예시:

```text
data/
  main-pipeline/
  jobs/
  connectors/
  schemas/
```

## Responsibility Rules

서브 모듈은 하나의 명확한 책임을 가져야 합니다.

좋은 서브 모듈:

- 이름만 보고 역할을 알 수 있습니다.
- 입력과 출력이 명확합니다.
- 메인 모듈 없이도 단위 테스트가 가능합니다.
- 내부 구현을 외부에 과도하게 노출하지 않습니다.

나쁜 서브 모듈:

- 여러 도메인의 로직이 섞여 있습니다.
- 메인 모듈의 설정이나 runtime에 강하게 의존합니다.
- 공통 모듈이라는 이름으로 모든 유틸리티가 모입니다.
- 순환 의존성을 만듭니다.

## Dependency Rules

서브 모듈은 메인 모듈에 의존하지 않습니다.

권장 방향:

```text
main module -> sub module
sub module  -> common module
sub module  -> external client module
```

피해야 할 방향:

```text
sub module    -> main module
common module -> domain module
domain module -> another domain module internal implementation
```

도메인 간 협력이 필요하면 다음 방식을 우선 고려합니다.

- API contract
- event
- interface
- shared schema
- service boundary

## Public Interface

서브 모듈은 외부에 공개할 interface를 명확히 해야 합니다.

권장 기준:

- 외부에서 사용할 class, function, component만 공개합니다.
- 내부 구현 파일은 모듈 밖에서 직접 참조하지 않습니다.
- 모듈 간 데이터 전달은 DTO, schema, type을 사용합니다.
- breaking change가 발생하면 영향받는 메인 모듈과 다른 서브 모듈을 함께 확인합니다.

## Configuration Rules

서브 모듈은 자신에게 필요한 설정만 관리합니다.

권장 기준:

- 모듈별 환경 변수는 모듈 README에 작성합니다.
- 공통 설정은 메인 모듈 또는 common module에 둡니다.
- 외부 API key, password, token은 코드에 직접 포함하지 않습니다.
- 서브 모듈 단독 실행이 필요하면 `.env.example`을 제공합니다.

## Test Rules

서브 모듈은 독립 테스트가 가능해야 합니다.

권장 테스트:

| Test | Purpose |
| --- | --- |
| Unit Test | 모듈 내부 로직 검증 |
| Integration Test | DB, 외부 API, message broker 연동 검증 |
| Contract Test | 메인 모듈 또는 다른 모듈과의 interface 검증 |
| Regression Test | 버그 재발 방지 |

메인 모듈은 서브 모듈이 조립된 전체 흐름을 검증합니다.

## README Rules

각 서브 모듈은 `README.md`를 포함하는 것을 권장합니다.

포함할 내용:

- 모듈 목적
- 책임 범위
- public interface
- 실행 방법
- 테스트 방법
- 필요한 환경 변수
- 의존하는 모듈 또는 외부 시스템
- 변경 시 주의사항

## Pull Request Rules

서브 모듈 PR은 변경 범위를 명확히 작성합니다.

PR 본문에 포함할 내용:

- 변경한 서브 모듈
- 변경 이유
- 메인 모듈에 미치는 영향
- 다른 서브 모듈에 미치는 영향
- 테스트 결과

예시:

```text
feat(auth): add token refresh module
refactor(common): split error response model
fix(payment): handle approval timeout
```

## Import Command

`dev` 브랜치에서 이 문서를 가져올 때는 다음 명령을 사용합니다.

```bash
git merge --squash origin/modules/sub
git commit -m "init: add sub module guide"
```

## References

- [3.4. 서브모듈 - 깃(Git) & 깃허브(GitHub)](https://wikidocs.net/300274)

이 문서에서 말하는 서브 모듈은 멀티모듈 구조 안에서 메인 모듈에 조립되는 기능 단위를 의미합니다.
위 레퍼런스는 Git 기능인 `submodule`을 설명하는 자료이므로,
서브 모듈을 별도 Git 저장소로 분리하거나 `modules/sync`의 `submodule` mode를 사용할 때 참고합니다.

## Standalone Usage

이 브랜치는 문서 전용입니다. Git submodule 기능과의 용어 구분은 본문
마지막 절을 참고합니다.

## Works With

`modules/main`, `modules/sync`와 한 세트로 사용합니다.
