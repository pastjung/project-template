# Contributing Guide

이 프로젝트에 기여하는 방법을 안내합니다.

## 시작하기

1. 이슈를 먼저 확인하고, 작업할 내용이 없다면 이슈를 생성합니다.
2. `dev` 브랜치에서 작업 브랜치를 만듭니다.

   ```bash
   git switch dev
   git switch -c feat/{{FEATURE_NAME}}
   ```

3. 브랜치 이름은 브랜치 전략 문서를 따릅니다:
   `feat/*`, `bugfix/*`, `refactor/*`, `docs/*`, `hotfix/*`

## 커밋 규칙

Conventional Commits 형식을 사용합니다.

```text
<type>(<scope>): <subject>
```

- 허용 type: `init feat fix build chore ci docs style refactor test perf revert release`
- 자세한 규칙은 커밋 전략 문서를 참고합니다.
- git hook이 설정되어 있다면 형식이 자동 검사됩니다.

## Pull Request

1. PR은 `dev` 브랜치를 대상으로 생성합니다 (`hotfix/*`, `release/*`는 `main`).
2. PR 제목도 Conventional Commits 형식을 사용합니다 (자동 검사됨).
3. PR 템플릿의 체크리스트를 작성합니다.
4. CI가 통과하고 리뷰 승인을 받은 뒤 병합합니다.

## 개발 환경

프로젝트 실행 방법은 각 애플리케이션 폴더의 README를 참고합니다.

## 질문

이슈 또는 Discussions를 이용해주세요.
