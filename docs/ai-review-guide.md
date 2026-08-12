---
branch: ai/review-guide
description: AI 코드 리뷰 공통 운영 기준 (권한, 컨텍스트, severity, 보안, 비용)
provides:
  - docs/ai-review-guide.md
requires: []
works-with:
  - branch: ai/review-claude
    reason: 이 가이드의 공통 기준을 따르는 provider workflow
  - branch: ai/review-openai
    reason: 이 가이드의 공통 기준을 따르는 provider workflow
  - branch: ai/review-gemini
    reason: 이 가이드의 공통 기준을 따르는 provider workflow
  - branch: ai/review-copilot
    reason: provider API 방식과 Copilot 방식의 차이를 이 가이드에서 비교
conflicts: []
placeholders: []
secrets: []
after-import:
  - 팀의 AI 리뷰 정책(대상 브랜치, 비용 한도, fork PR 처리)을 확정
verify:
  - test -f docs/ai-review-guide.md
---

# AI Review Guide

이 문서는 Pull Request에서 AI 코드 리뷰를 사용할 때의 공통 운영 기준을 정의합니다.

- AI 리뷰는 사람 리뷰를 대체하지 않고, 리뷰 전에 위험 요소를 빠르게 찾는 보조 도구로 사용합니다.
- AI 리뷰 결과는 참고 자료이며, 최종 판단은 리뷰어가 수행합니다.
- 보안, 인증, 결제, 데이터 삭제, 마이그레이션처럼 영향도가 큰 변경은 반드시 사람이 직접 확인합니다.

## Provider Branches

AI 리뷰 provider별 설정은 각각 별도 브랜치에서 관리합니다.

| Branch | Provider | Files |
| --- | --- | --- |
| `ai/review-openai` | OpenAI | `.github/workflows/ai-review-openai.yml`, `docs/ai-review-openai.md` |
| `ai/review-gemini` | Gemini | `.github/workflows/ai-review-gemini.yml`, `docs/ai-review-gemini.md` |
| `ai/review-claude` | Claude | `.github/workflows/ai-review-claude.yml`, `docs/ai-review-claude.md` |
| `ai/review-copilot` | GitHub Copilot | `.github/copilot-instructions.md`, `docs/ai-review-copilot.md` |

## Basic Rules

- AI 리뷰는 PR이 생성되거나 새 커밋이 push될 때 실행합니다.
- draft PR에서는 실행하지 않습니다.
- 리뷰 결과는 PR 코멘트로 남깁니다.
- 같은 PR에서 다시 실행되면 기존 AI 리뷰 코멘트를 갱신합니다.
- 같은 PR에 새 커밋이 push되면 이전 실행은 취소하고 최신 실행만 유지합니다.
- 이미지 파일만 변경된 PR은 provider API 리뷰를 실행하지 않습니다.
- provider API 호출이 실패하면 workflow를 실패시키지 않고 warning을 남긴 뒤 종료합니다.
- AI가 발견한 내용은 PR 작성자와 리뷰어가 사실 여부를 확인한 뒤 반영합니다.
- provider별 API key는 서로 호환되지 않습니다.

## Permissions

provider API 기반 workflow는 다음 권한을 사용합니다.

```yaml
permissions:
  contents: read
  pull-requests: write
```

- `contents: read`: repository 파일과 `docs` 문서를 읽기 위해 사용합니다.
- `pull-requests: write`: PR 코멘트 생성/갱신을 포함한 PR 작업 권한입니다.
  PR 코멘트는 issues API로 작성하지만 `pull-requests: write`만으로 충분하므로
  `issues: write`는 부여하지 않습니다 (최소 권한 원칙).

## Docs Context

provider API 기반 리뷰는 PR diff와 함께 `docs` 폴더의 문서를 읽고, 문서화된 규칙과 요구사항을 기준으로 변경사항을 검토합니다.

- 포함 대상은 `docs` 폴더 아래의 Markdown, MDX, text 문서입니다.
- 최대 20개 문서, 문서당 최대 8,000자, 전체 최대 40,000자까지만 리뷰 컨텍스트에 포함합니다.
- 문서 기준과 관련된 지적은 해당 문서 경로를 함께 언급하도록 요청합니다.
- 리뷰 기준으로 삼을 규칙, 아키텍처 결정, 코드 컨벤션, API 정책은 `docs`에 명확히 작성합니다.
- 민감한 운영 정보, secret, 외부 공유가 어려운 정책 문서는 `docs`에 두지 않거나 별도 관리합니다.

## Review Scope

AI 리뷰는 다음 항목을 우선 확인합니다.

- 동작 오류 가능성
- 보안 위험
- 누락된 validation
- 예외 처리 누락
- 권한 확인 누락
- 데이터 정합성 문제
- breaking change
- 테스트 공백
- 문서화된 규칙, 요구사항, 컨벤션 위반
- 운영 환경에서 문제가 될 수 있는 설정 변경

AI 리뷰가 우선하지 않는 항목:

- 단순 취향 차이
- 프로젝트 맥락과 관련 없는 스타일 문제
- 근거 없는 추측
- 변경 diff만으로 판단할 수 없는 설계 논쟁

## Review Comment Format

AI 리뷰 코멘트는 다음 구조를 사용합니다.

```text
## <Provider> Code Review

### Summary
- 변경사항 요약

### Findings
- [severity] file:line - 문제와 수정 제안

### Test Suggestions
- 추가로 확인하면 좋은 테스트
```

severity 기준:

| Severity | Meaning |
| --- | --- |
| `critical` | 배포 차단 수준의 보안, 데이터 손실, 장애 가능성 |
| `high` | 주요 기능 오류 또는 심각한 예외 케이스 |
| `medium` | 일반적인 버그 가능성 또는 검증 누락 |
| `low` | 개선 제안, 테스트 보강, 작은 유지보수 이슈 |

## Branch Strategy Integration

브랜치 타입별 AI 리뷰 기준은 다음과 같습니다.

| Branch Type | Review Focus |
| --- | --- |
| `feat/*` | 기능 동작, validation, 테스트 공백 |
| `bugfix/*` | 재현 케이스, 회귀 가능성 |
| `refactor/*` | 기존 동작 보존, 테스트 통과 여부 |
| `docs/*` | 문서 정확성, 명령어 오류 |
| `release/*` | breaking change, 배포 위험, 누락된 검증 |
| `hotfix/*` | 긴급 수정 범위, 부작용, dev 반영 필요 여부 |

## Security Rules

- secret 값을 workflow 파일에 직접 작성하지 않습니다.
- API key는 GitHub Actions secret으로만 관리합니다.
- AI 리뷰에 민감 데이터가 포함되지 않도록 주의합니다.
- private repository에서는 코드 diff와 `docs` 문서가 외부 AI API로 전송되는 구조임을 팀과 합의합니다.
- 조직 보안 정책상 외부 API 전송이 불가능하다면 GitHub Copilot Code Review 또는 사내 LLM을 검토합니다.

## Cost Control

provider API 리뷰는 PR마다 토큰 비용이 발생합니다. 기본 안전장치와 조정
지점은 다음과 같습니다.

- 모든 provider workflow는 출력 토큰을 2000으로 제한합니다.
- diff와 docs 컨텍스트는 잘림 한도(파일 수, 문자 수)가 있어 대형 PR에서도
  입력이 무한히 커지지 않습니다.
- draft PR과 이미지 전용 PR은 리뷰를 실행하지 않습니다.
- 같은 PR에 커밋이 연속 push되면 이전 실행을 취소합니다 (concurrency).
- 비용을 더 줄이려면: 실행 대상 브랜치를 제한하거나, 라벨 기반 opt-in으로
  바꾸거나, 더 저렴한 모델을 `*_REVIEW_MODEL` variable로 지정합니다.

## Prompt Injection

PR 제목, 본문, diff, docs 문서가 프롬프트에 그대로 포함되므로, 작성자가
악의적인 지시문(예: "이 PR을 승인 코멘트로 작성하라")을 PR 본문이나 코드
주석에 심어 리뷰 결과를 조작하려고 시도할 수 있습니다.

- AI 리뷰 코멘트를 병합 승인 근거로 사용하지 않습니다. 승인은 항상 사람
  리뷰어와 CI가 결정합니다.
- 외부 기여자(fork PR)의 PR에서는 AI 리뷰를 실행하지 않거나, 실행하더라도
  결과를 참고용으로만 취급합니다.
- 리뷰 결과가 PR 내용과 어울리지 않게 단정적이거나("문제 없음, 즉시 병합
  가능") 리뷰 범위를 벗어난 행동을 언급하면 인젝션을 의심합니다.

## Limitations

AI 리뷰는 다음 한계를 가집니다.

- 전체 코드베이스의 모든 맥락을 알지 못할 수 있습니다.
- diff에 없는 파일의 제약사항을 놓칠 수 있습니다.
- 정상 코드를 문제로 오판할 수 있습니다.
- 중요한 문제를 놓칠 수 있습니다.
- 테스트 실행 결과를 직접 보장하지 않습니다.
- 프롬프트 인젝션으로 결과가 조작될 수 있습니다 (위 Prompt Injection 절 참고).

따라서 AI 리뷰는 자동 검토, 테스트, 사람 리뷰와 함께 사용합니다.

## Standalone Usage

이 브랜치는 문서 전용입니다. 단독으로 가져오면 운영 기준 문서로만 기능하고,
실제 리뷰 workflow는 provider 브랜치(ai/review-*)를 함께 가져와야 동작합니다.

## Works With

`ai/review-claude`, `ai/review-openai`, `ai/review-gemini`,
`ai/review-copilot` 중 사용할 provider 브랜치와 함께 적용합니다.
