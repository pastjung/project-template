# CLAUDE.md

이 저장소는 브랜치 단위로 기능을 쪼개 놓은 **프로젝트 템플릿 저장소**입니다.
일반적인 앱 저장소와 운영 규칙이 다르므로 작업 전에 반드시 아래 규칙을 따르세요.

## 저장소 구조

- `main`: 카탈로그와 사용법. 유일하게 일반 커밋으로 운영.
- `dev`: 조립용 빈 브랜치 (루트 커밋 하나). 직접 수정 금지.
- 나머지 브랜치: 기능 템플릿. **전부 공통 루트 커밋 `d48d8ad`에서 분기.**
- `backend/*`, `frontend/*`, `data/*`, `observability/*`는 `read-tree --prefix`로
  하위 폴더에 들어가는 앱 브랜치, 그 외는 루트에 병합되는 설정 브랜치.

## 서브 브랜치 수정 규칙 (필수)

fix 커밋을 히스토리에 남기지 않는다. 수정 절차:

```bash
git switch <branch>
# 작업하며 커밋은 자유롭게 쌓기
git reset --soft d48d8ad
git commit -m "✨ feat: add <X> template"   # 논리 단위 1~N개로 재작성
git push --force-with-lease origin <branch>
```

수정 후 검증: 해당 브랜치 `docs/<브랜치명 '/'→'-'>.md` front matter의 `verify`
명령 실행 + `uv run scripts/validate_composition.py catalog` (main의 스크립트).

## 루트 병합 브랜치 불변식

- 루트 `README.md`는 **1바이트 빈 파일 유지** (내용 추가 금지 — 조립 시 새
  프로젝트의 README 자리를 비워두는 설계).
- 문서는 `docs/<브랜치명 '/'→'-'>.md` 하나, 상단에 YAML front matter 필수.
  스키마와 placeholder 규칙은 main의 `docs/README.md` 참고.
- compose의 `env_file`은 `.env`(비추적) 참조, `.env.example`은 복사 원본.
- GitHub Actions는 커밋 SHA로 고정 (`@<sha> # vX` 주석).

## main 브랜치 push 규칙

`docs/plans/` 아래 계획 문서는 **로컬 전용 — push 금지**. main을 push할 때:

```bash
git reset --soft origin/main
git restore --staged docs/plans
# 나머지 변경 커밋 → push → 계획 문서 다시 로컬 커밋
```

## 주요 문서

- 조립 자동화 스킬: `skills/assemble-project/SKILL.md` (main)
- 문서 표준(front matter 스키마): `docs/README.md` (main)
- 정기 점검 절차: `docs/maintenance.md` (main)
- 커밋 컨벤션: `<emoji> <type>: <subject>` (예: `✨ feat: ...`, `📝 docs: ...`)

## 주의

- 이 CLAUDE.md는 main에만 있으므로, 서브 브랜치로 전환한 뒤 시작한 세션에는
  로드되지 않을 수 있다. 브랜치 작업 전 main의 이 파일을 먼저 확인할 것.
- 원격 브랜치 삭제/개명은 사용자 확인 후 진행.
