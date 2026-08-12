---
branch: github/ci
description: 스택 자동 감지 기반 빌드/테스트 CI workflow (Node, Python, Gradle)
provides:
  - .github/workflows/ci.yml
  - docs/github-ci.md
requires: []
works-with:
  - branch: github/slack-notification
    reason: workflow_run 대상 'CI'가 이 workflow의 name과 일치해 빌드 실패 알림이 동작
  - branch: github/semantic-pr
    reason: CI와 함께 branch protection required check로 등록하면 병합 조건이 완성됨
conflicts: []
placeholders: []
secrets: []
after-import:
  - 모노레포라면 detect 단계의 manifest 경로를 하위 폴더로 조정
  - branch protection의 required status check로 등록 검토
verify:
  - actionlint .github/workflows/ci.yml
---

# CI Workflow Guide

이 문서는 저장소의 스택을 자동 감지해 빌드/테스트를 실행하는 CI workflow의
운영 기준을 정의합니다.

## Purpose

- PR과 main/dev push에서 빌드·테스트를 자동 실행합니다.
- 하나의 workflow(`name: CI`)로 Node, Python, Gradle 스택을 처리합니다.
- 존재하지 않는 스택의 job은 실행하지 않습니다 (detect job이 manifest 존재를
  확인).

## Stack Detection

| Stack | 감지 기준 | 실행 내용 |
| --- | --- | --- |
| Node | `package.json` | `npm ci` 후 lint/typecheck/test/build (`--if-present`) |
| Python | `pyproject.toml` 또는 `requirements.txt` | 의존성 설치 후 ruff, pytest (설치된 경우만) |
| Gradle | `gradlew` | `./gradlew build` |

루트가 아닌 하위 폴더에 프로젝트가 있는 모노레포는 detect 단계의 경로와 각
job의 `working-directory`를 조정합니다.

## Branch Protection

CI를 병합 조건으로 만들려면 branch protection(또는 Rulesets)의
required status check에 이 workflow의 job 이름을 등록합니다.
`github/semantic-pr`의 제목 검사와 함께 등록하는 것을 권장합니다.

## Slack Notification Integration

`github/slack-notification`의 `workflow_run.workflows` 기본값에 `CI`가
포함되어 있습니다. 이 브랜치를 적용하면 CI 완료/실패 알림이 바로 동작합니다.

## Standalone Usage

이 브랜치만 가져와도 즉시 동작합니다. 감지되는 스택이 없으면 detect job만
실행되고 통과합니다.

## Works With

`github/slack-notification`(실패 알림), `github/semantic-pr`(병합 조건),
`github/release`(release-please가 CI 통과를 전제로 release PR 관리)와 함께
사용합니다.
