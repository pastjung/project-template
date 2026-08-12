---
branch: ai/review-claude
description: Claude API 기반 PR 자동 리뷰 workflow
provides:
  - .github/workflows/ai-review-claude.yml
  - docs/ai-review-claude.md
requires: []
works-with:
  - branch: ai/review-guide
    reason: 4개 provider 공통 운영 기준(권한, 컨텍스트 한도, severity)을 정의
conflicts: []
placeholders: []
secrets:
  - ANTHROPIC_API_KEY
after-import:
  - ANTHROPIC_API_KEY secret 등록
  - 모델/비용 정책 확인 (CLAUDE_REVIEW_MODEL variable로 모델 변경 가능)
verify:
  - actionlint .github/workflows/ai-review-claude.yml
---

# Claude Code Review Guide

이 문서는 Claude API를 사용해 Pull Request 코드 리뷰를 자동으로 실행하는 방법을
정의합니다.

## Workflow File

```text
.github/workflows/ai-review-claude.yml
```

이 워크플로는 PR diff와 `docs` 폴더의 문서를 Anthropic Messages API로 전달하고,
리뷰 결과를 PR 코멘트로 작성합니다.

## Required Settings

GitHub repository settings에서 secret을 추가합니다.

```text
Settings -> Secrets and variables -> Actions -> Repository secrets
```

필수 secret:

| Name | Description |
| --- | --- |
| `ANTHROPIC_API_KEY` | Anthropic Claude API key |

선택 variable:

| Name | Description | Default |
| --- | --- | --- |
| `CLAUDE_REVIEW_MODEL` | 리뷰에 사용할 Claude 모델 | `claude-haiku-4-5` |

## Review Scope

- PR diff를 기준으로 정확성, 보안, 검증 누락, 엣지 케이스, 테스트 공백을 검토합니다.
- `docs` 폴더의 Markdown, MDX, text 문서를 함께 읽고 문서화된 규칙과 요구사항을
  따르는지 확인합니다.
- 문서 기준과 관련된 지적은 해당 문서 경로를 함께 언급하도록 요청합니다.
- `docs` 문서는 최대 20개, 문서당 최대 8,000자, 전체 최대 40,000자까지만 리뷰
  컨텍스트에 포함합니다.

## Workflow Behavior

- 같은 PR에 새 커밋이 push되면 이전 Claude 리뷰 실행은 취소하고 최신 실행만
  유지합니다.
- 이미지 파일만 변경된 PR은 리뷰를 실행하지 않습니다.
- Claude API 호출이 실패하면 워크플로를 실패시키지 않고 warning을 남긴 뒤
  종료합니다.

## Usage Notes

- 이 브랜치는 Claude API 전용입니다.
- OpenAI, Gemini, Copilot API key와 호환되지 않습니다.
- 다른 provider를 사용하려면 해당 provider용 브랜치를 사용합니다.
- private repository에서는 코드 diff와 `docs` 문서가 Anthropic API로 전송되는 점을
  팀과 합의합니다.
- 민감한 운영 정보, secret, 외부 공유가 어려운 정책 문서는 `docs`에 두지 않거나
  별도 관리합니다.

## Alternative: claude-code-action

Anthropic이 관리하는 공식 GitHub Action인
[`anthropics/claude-code-action`](https://github.com/anthropics/claude-code-action)을
사용하는 방법도 있습니다. 인라인 리뷰 코멘트, 코멘트 관리, 프롬프트 구성이
내장되어 있어 유지보수 부담이 적습니다. 이 브랜치의 자체 구현은 (1) 프롬프트와
비용을 세밀하게 통제하고 싶을 때, (2) 다른 provider 브랜치들과 동일한 동작
방식을 유지하고 싶을 때 적합합니다.

## Standalone Usage

`ANTHROPIC_API_KEY` secret만 등록하면 PR 리뷰가 즉시 동작합니다. secret이 없으면
workflow는 조용히 skip합니다.

## Works With

공통 운영 기준(권한, 비용 통제, 프롬프트 인젝션 주의)은 `ai/review-guide`
문서를 함께 참고합니다. 다른 provider 브랜치와 동시에 적용해도 각자 별도
코멘트를 관리하므로 충돌하지 않습니다.
