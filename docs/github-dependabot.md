---
branch: github/dependabot
description: 의존성 자동 업데이트 (기본은 GitHub Actions, 스택별 ecosystem은 opt-in)
provides:
  - .github/dependabot.yml
  - docs/github-dependabot.md
requires: []
works-with:
  - branch: github/ci
    reason: Dependabot PR도 CI 검증을 거쳐 병합 안전성을 확보
  - branch: github/labels
    reason: Dependabot이 만드는 dependencies 라벨 등을 라벨 정책과 함께 관리
conflicts: []
placeholders: []
secrets: []
after-import:
  - 사용하는 스택의 ecosystem 주석 해제 (npm, pip, gradle, docker)
  - 모노레포라면 directory를 하위 폴더로 조정
verify:
  - test -f .github/dependabot.yml
---

# Dependabot Guide

이 문서는 의존성 자동 업데이트 설정의 운영 기준을 정의합니다.

## Default Behavior

기본 설정은 **GitHub Actions 버전 업데이트만** 활성화합니다. 모든 액션을
하나의 그룹 PR로 묶어 주 1회 갱신합니다. 이 저장소의 workflow들은 커밋 SHA로
고정되어 있는데, Dependabot은 SHA 고정 방식도 인식해 새 릴리스 SHA로 올리는
PR을 만듭니다.

## Enabling Stack Ecosystems

`npm`, `pip`, `gradle`, `docker` 블록은 주석 상태로 제공됩니다. 해당 manifest가
없는 저장소에서 ecosystem을 켜두면 Dependabot 탭에 오류 로그가 남으므로,
실제 사용하는 스택만 주석을 해제합니다.

모노레포는 `directory`를 프로젝트 폴더로 조정합니다.

```yaml
- package-ecosystem: npm
  directory: /frontend/react-vite-app
  schedule:
    interval: weekly
```

## Noise Control

- `groups`로 minor/patch 업데이트를 하나의 PR로 묶으면 PR 수가 크게 줄어듭니다.
- 특정 패키지를 제외하려면 `ignore` 블록을 사용합니다.
- 보안 업데이트는 이 설정과 무관하게 저장소의 Dependabot security updates
  설정을 따릅니다 (Settings → Code security).

## Standalone Usage

이 브랜치만 가져와도 GitHub Actions 업데이트가 즉시 동작합니다. 별도 secret이
필요 없습니다.

## Works With

`github/ci`가 있으면 Dependabot PR도 CI 검증을 거칩니다. required status
check와 함께 쓰면 자동 업데이트의 안전망이 완성됩니다.
