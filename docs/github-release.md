---
branch: github/release
description: release-please 기반 릴리즈 자동화 (버전 산정, CHANGELOG, GitHub Release)
provides:
  - .github/workflows/release-please.yml
  - .github/release-please-config.json
  - .github/.release-please-manifest.json
  - docs/github-release.md
requires:
  - standards/commit-strategy
works-with:
  - branch: github/semantic-pr
    reason: squash merge 시 PR 제목이 커밋이 되므로 release-please의 입력 품질을 보장
  - branch: github/ci
    reason: release PR도 CI 검증을 거침 (PAT 등록 시)
conflicts: []
placeholders: []
secrets:
  - RELEASE_PLEASE_TOKEN
after-import:
  - .release-please-manifest.json의 시작 버전을 프로젝트에 맞게 조정
  - release PR에서 CI를 실행하려면 RELEASE_PLEASE_TOKEN(PAT) 등록
verify:
  - actionlint .github/workflows/release-please.yml
---

# Release Automation Guide

이 문서는 release-please 기반 릴리즈 자동화의 운영 기준을 정의합니다.

## How It Works

1. `main`에 커밋이 push되면 release-please가 Conventional Commits를 분석합니다.
2. `feat`(minor), `fix`(patch), `feat!`/`BREAKING CHANGE`(major) 기준으로 다음
   버전을 산정하고, CHANGELOG를 포함한 **release PR**을 자동 생성/갱신합니다.
3. release PR을 병합하면 GitHub Release와 태그가 자동 생성됩니다.

## Commit Convention Dependency

이 자동화는 커밋 메시지가 Conventional Commits 형식이라는 전제 위에서
동작합니다 (`requires: standards/commit-strategy`). squash merge를 쓴다면
`github/semantic-pr`로 PR 제목을 검사해 입력 품질을 보장하는 것을 강력히
권장합니다.

커스텀 type(`init`, `release`)은 config의 `changelog-sections`에 hidden으로
등록되어 있어 검사 오류 없이 CHANGELOG에서만 제외됩니다.

## Token

기본 `github.token`으로 생성된 release PR은 `pull_request` workflow(CI)를
트리거하지 않습니다. release PR에서 CI를 실행하려면 `RELEASE_PLEASE_TOKEN`
secret에 PAT(contents: write, pull-requests: write)을 등록합니다. workflow는
secret이 있으면 자동으로 사용합니다.

## Version Files

`release-type: simple`은 `version.txt`와 CHANGELOG만 관리합니다. 언어별 버전
파일(package.json, pyproject.toml 등)을 함께 올리려면 `release-type`을
`node`, `python` 등으로 바꿉니다.

## Standalone Usage

이 브랜치만 가져와도 동작하지만, 커밋이 Conventional Commits 형식이 아니면
버전 산정이 되지 않습니다. 커밋 전략 문서와 함께 사용하세요.

## Works With

`standards/commit-strategy`(필수 전제), `github/semantic-pr`(입력 품질),
`github/ci`(release PR 검증)와 함께 사용합니다.
