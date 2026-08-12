---
branch: ai/review-copilot
description: GitHub Copilot Code Review 설정 가이드와 저장소 지침 파일
provides:
  - .github/copilot-instructions.md
  - docs/ai-review-copilot.md
requires: []
works-with:
  - branch: ai/review-guide
    reason: provider API 방식과의 차이와 공통 운영 기준을 정의
conflicts: []
placeholders: []
secrets: []
after-import:
  - Copilot 라이선스와 Code Review 사용 가능 여부 확인
  - Rulesets에서 Automatically request Copilot code review 활성화
verify:
  - test -f .github/copilot-instructions.md
---

# GitHub Copilot Code Review Guide

이 문서는 GitHub Copilot Code Review를 Pull Request 리뷰 보조 도구로 사용하는 방법을
정의합니다.

## What This Branch Adds

```text
.github/copilot-instructions.md
docs/ai-review-copilot.md
```

이 브랜치는 OpenAI, Gemini, Claude 브랜치처럼 GitHub Actions workflow를 추가하지 않습니다.
대신 GitHub Copilot Code Review가 참고할 저장소 지침 파일을 추가하고,
GitHub Rulesets로 Copilot 자동 리뷰를 설정하는 방법을 안내합니다.

## When To Use

이 방식을 선택하면 좋은 경우:

- 조직이나 저장소에서 GitHub Copilot을 이미 사용하고 있습니다.
- 별도 provider API key를 GitHub Actions secret에 추가하고 싶지 않습니다.
- PR 생성 시 GitHub Copilot Code Review를 자동으로 요청하고 싶습니다.
- 리뷰 자동화 workflow를 직접 유지보수하고 싶지 않습니다.

OpenAI, Gemini, Claude API를 직접 호출하고 싶다면 해당 provider 브랜치를 사용합니다.

## Required Conditions

Copilot Code Review를 사용하려면 다음 조건을 확인합니다.

| Item | Description |
| --- | --- |
| Copilot license | Copilot Pro, Pro+, Business, Enterprise 등 Code Review를 사용할 수 있는 라이선스 |
| Repository access | Copilot이 해당 저장소에 접근 가능해야 함 |
| Ruleset permission | repository ruleset을 만들거나 수정할 수 있는 권한 |
| Instructions file | `.github/copilot-instructions.md`가 기본 브랜치에 반영되어 있어야 함 |

Reviewers에서 `copilot`을 검색해도 나타나지 않는다면, 현재 계정, 조직, 저장소에서
Copilot Code Review를 사용할 수 없는 상태일 수 있습니다.

## Automatic Review Setup

PR 생성 시 Copilot Code Review를 자동 요청하려면 GitHub Rulesets를 사용합니다.

```text
Repository Settings
-> Rules
-> Rulesets
-> New ruleset
-> New branch ruleset
```

설정 순서:

1. Ruleset 이름을 입력합니다.
2. Enforcement status를 설정합니다.
3. Target branches에서 리뷰를 적용할 브랜치를 선택합니다.
   예: `main`, `dev`, `release/*`
4. Branch rules에서 `Automatically request Copilot code review`를 켭니다.
5. 필요하면 추가 옵션을 켭니다.
   - `Review new pushes`: PR에 새 커밋이 push될 때 다시 리뷰
   - `Review draft pull requests`: draft PR도 리뷰
6. ruleset을 저장합니다.

이 설정을 사용하면 대상 브랜치로 향하는 PR이 만들어질 때 Copilot Code Review가
자동으로 요청됩니다.

## Manual Review Request

자동 리뷰를 사용하지 않거나 특정 PR에서만 Copilot 리뷰를 받고 싶다면 PR 화면에서
수동으로 요청합니다.

```text
Pull request
-> Reviewers
-> Copilot 검색
-> Copilot 선택
```

`Copilot`이 검색 결과에 나타나지 않으면 라이선스, 조직 정책, 저장소 설정을 먼저
확인합니다.

## Cloud Agent Validation Tools

다음 설정은 일반 PR 자동 리뷰 설정과 다릅니다.

```text
Repository Settings
-> Copilot
-> Cloud agent
-> Validation tools
-> Copilot code review
```

이 항목은 Copilot cloud agent가 작업한 내용을 사람에게 리뷰 요청하기 전에 검증할 때
사용하는 도구 설정입니다. 일반 PR에 Copilot Code Review를 자동 요청하려면 Rulesets의
`Automatically request Copilot code review`를 설정해야 합니다.

## How It Works

Copilot Code Review는 GitHub가 제공하는 기능입니다.

- 별도의 workflow 파일이 필요하지 않을 수 있습니다.
- 별도의 `COPILOT_API_KEY` 같은 secret을 설정하지 않습니다.
- `.github/copilot-instructions.md`는 Copilot이 리뷰할 때 참고하는 프로젝트 지침으로
  사용합니다.
- 이 저장소의 instructions는 `docs` 폴더의 문서와 PR diff를 함께 고려하도록
  Copilot에 요청합니다.

## Review Scope

Copilot에는 다음 항목을 우선 검토하도록 지시합니다.

- 동작 오류 가능성
- 보안 위험
- 누락된 validation
- 예외 처리 누락
- 인증, 권한, 결제, 개인정보, 데이터 삭제 관련 위험
- secret, token, password, API key 노출
- 외부 API 연동의 timeout, retry, fallback, error handling
- 테스트 공백
- `docs`에 작성된 브랜치 전략, 커밋 규칙, 코드 컨벤션, API 정책 위반

## Docs Context

Copilot instructions에는 `docs` 폴더의 문서를 참고하라는 지시가 포함되어 있습니다.

- 리뷰 기준으로 삼을 규칙은 `docs`에 명확히 작성합니다.
- 문서 기준과 관련된 리뷰는 가능한 한 문서 경로를 함께 언급하도록 요청합니다.
- 코드 변경과 문서가 충돌하면 문서 갱신 필요성도 함께 확인하도록 요청합니다.
- 민감한 운영 정보, secret, 외부 공유가 어려운 정책 문서는 `docs`에 두지 않거나
  별도 관리합니다.

## Difference From Provider API Branches

| Item | Copilot | OpenAI/Gemini/Claude |
| --- | --- | --- |
| 실행 방식 | GitHub Copilot Code Review + Rulesets | GitHub Actions workflow |
| API key | 별도 secret 없음 | provider API key 필요 |
| 자동 실행 | Rulesets에서 자동 리뷰 요청 설정 | PR 이벤트로 workflow 실행 |
| 수동 실행 | PR Reviewers에서 Copilot 요청 | workflow 재실행 또는 PR 이벤트 |
| 코멘트 관리 | GitHub Copilot 기능에 따름 | workflow가 PR 코멘트 생성/갱신 |
| 커스터마이징 | `.github/copilot-instructions.md` 중심 | workflow script와 prompt 수정 |

## Usage Notes

- 이 브랜치는 GitHub Copilot Code Review 전용입니다.
- Copilot 자동 리뷰는 GitHub Rulesets로 설정합니다.
- 조직 정책에 따라 Copilot 사용 가능 여부와 리뷰 기능이 달라질 수 있습니다.
- Copilot 리뷰는 사람 리뷰를 대체하지 않습니다.
- 보안, 인증, 결제, 데이터 삭제, 마이그레이션 변경은 반드시 사람이 직접 확인합니다.

## References

- [GitHub Copilot 자동 코드 검토 구성](https://docs.github.com/ko/copilot/how-tos/copilot-on-github/set-up-copilot/configure-automatic-review)

## Standalone Usage

이 브랜치는 workflow 없이 지침 파일과 설정 가이드만 제공합니다. Copilot
Code Review 라이선스가 있으면 Rulesets 설정만으로 동작합니다. API secret은
필요 없습니다.

## Works With

provider API 브랜치(ai/review-claude 등)와 병행할 수 있으며, 차이 비교는
`ai/review-guide`를 참고합니다.
