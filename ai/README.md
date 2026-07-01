# AI Import Guide

이 문서는 AI 코드 리뷰와 AI 협업 가이드 브랜치를 `dev` 브랜치로 가져오는 명령어를
정리합니다.

## Available Branches

| Branch | Description | Result Path |
| --- | --- | --- |
| `ai/review-guide` | AI 리뷰 공통 운영 가이드 | `docs/ai-review-guide.md` |
| `ai/review-openai` | OpenAI API 기반 PR 자동 리뷰 | `.github/workflows/ai-review-openai.yml`, `docs/ai-review-openai.md` |
| `ai/review-gemini` | Gemini API 기반 PR 자동 리뷰 | `.github/workflows/ai-review-gemini.yml`, `docs/ai-review-gemini.md` |
| `ai/review-claude` | Claude API 기반 PR 자동 리뷰 | `.github/workflows/ai-review-claude.yml`, `docs/ai-review-claude.md` |
| `ai/review-copilot` | GitHub Copilot Code Review 가이드 | `.github/copilot-instructions.md`, `docs/ai-review-copilot.md` |

## Before Import

```bash
git switch dev
git fetch origin
```

## AI Review Guide

Single Commit Mode:

```bash
git merge --squash origin/ai/review-guide
git commit -m "init: add AI review guide"
```

Full History Mode:

```bash
git merge --no-ff -m "init: merge AI review guide" origin/ai/review-guide
```

## OpenAI Code Review

Single Commit Mode:

```bash
git merge --squash origin/ai/review-openai
git commit -m "init: add OpenAI code review"
```

Full History Mode:

```bash
git merge --no-ff -m "init: merge OpenAI code review" origin/ai/review-openai
```

## Gemini Code Review

Single Commit Mode:

```bash
git merge --squash origin/ai/review-gemini
git commit -m "init: add Gemini code review"
```

Full History Mode:

```bash
git merge --no-ff -m "init: merge Gemini code review" origin/ai/review-gemini
```

## Claude Code Review

Single Commit Mode:

```bash
git merge --squash origin/ai/review-claude
git commit -m "init: add Claude code review"
```

Full History Mode:

```bash
git merge --no-ff -m "init: merge Claude code review" origin/ai/review-claude
```

## GitHub Copilot Code Review

Single Commit Mode:

```bash
git merge --squash origin/ai/review-copilot
git commit -m "init: add Copilot code review guide"
```

Full History Mode:

```bash
git merge --no-ff -m "init: merge Copilot code review guide" origin/ai/review-copilot
```

## Notes

- OpenAI, Gemini, Claude는 서로 다른 API key와 workflow를 사용합니다.
- Copilot은 API key 방식이 아니라 GitHub 제품 설정 기반입니다.
- 자동 리뷰 workflow는 비용과 권한 정책을 확인한 뒤 적용합니다.
