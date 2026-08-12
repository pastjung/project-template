---
name: assemble-project
description: 이 템플릿 저장소의 브랜치들을 조립해 새 프로젝트를 세팅한다. 사용자가 필요한 기능(백엔드 스택, DB, CI 등)을 말하면 브랜치를 선택·병합하고 placeholder 치환과 검증까지 수행한다.
---

# Assemble Project Skill

템플릿 저장소(pastjung/project-template)의 브랜치를 조립해 새 프로젝트를
세팅하는 절차입니다. 이 파일을 `.claude/skills/assemble-project/`(프로젝트)
또는 `~/.claude/skills/assemble-project/`(전역)에 복사하면 Claude Code에서
`/assemble-project`로 사용할 수 있습니다. Codex 등 다른 Agent에는 이 본문을
프롬프트로 제공합니다.

## 전제

- 템플릿 저장소가 clone되어 있고 `dev` 브랜치에 있어야 합니다.
- 조립 규칙의 단일 기준은 각 브랜치 `docs/<branch '/'→'-'>.md`의 YAML front
  matter입니다. 이 스킬은 front matter를 파싱해 의존성/충돌/후속 작업을
  결정합니다. 추측하지 마세요.

## 절차

1. **카탈로그 수집**: 모든 원격 브랜치의 front matter를 수집합니다.

   ```bash
   git fetch origin
   # 브랜치 목록
   git branch -r --format='%(refname:short)'
   # 각 루트 병합 브랜치의 front matter (backend/frontend/data/observability 제외)
   git show origin/<branch>:docs/<branch를 -로 치환>.md
   ```

   또는 검증 스크립트를 사용합니다: `uv run scripts/validate_composition.py catalog`
   (main 브랜치의 scripts/ 참고)

2. **요구사항 → 브랜치 매핑**: 사용자가 말한 기능을 브랜치로 변환합니다.
   - 기본 세팅(항상 권장): `settings/editor-config`, `git/attributes`,
     `git/ignore`
   - 사용자가 언급한 스택: `backend/*`, `frontend/*`, `data/*`,
     `observability/*` 중 해당 항목
   - 각 선택 브랜치의 front matter에서 `requires`를 재귀적으로 추가하고,
     `works-with`는 이유를 보여주며 사용자에게 추가 여부를 물어봅니다.
   - `conflicts`에 걸리는 조합이 있으면 병합 전에 사용자에게 알리고
     선택을 받습니다.

3. **병합 순서 결정**: main 브랜치 README의 Recommended Project Setup Order를
   따릅니다. 목록에 없는 브랜치는 설정 계열 → 문서 계열 → workflow 계열 →
   앱 계열 순서로 병합합니다.

4. **병합 실행**:
   - 루트 병합 브랜치: `git merge --squash origin/<branch>` 후
     `git commit -m "init: add <설명>"`
   - 앱/인프라 브랜치(backend/frontend/data/observability):
     `git read-tree --prefix=<대상폴더>/ -u origin/<branch>` 후 커밋
     (폴더명은 사용자에게 확인)

5. **placeholder 치환**: 설치된 문서들의 front matter `placeholders` 목록을
   모아 사용자에게 실제 값을 묻고 일괄 치환합니다 (`{{OWNER}}`, `{{TEAM}}`,
   `{{REPOSITORY}}`, `{{SECURITY_CONTACT}}` 등).

6. **조립 검증**: 조립된 프로젝트에서 검증을 실행합니다.

   ```bash
   uv run scripts/validate_composition.py project
   ```

   requires 미충족/충돌/provides 누락이 0건이어야 합니다. 이어서 각 front
   matter의 `verify` 명령을 실행해 결과를 보고합니다.

7. **후속 작업 안내**: front matter의 `after-import`와 `secrets`를 모아
   사용자에게 체크리스트로 제시합니다 (GitHub secret 등록 등 Agent가 직접
   할 수 없는 작업 포함).

8. **마무리**: main 브랜치 README의 New Project Workflow 절차대로 remote
   교체와 브랜치 정리를 안내합니다 (원격 저장소 push는 사용자 확인 후).

## 주의

- front matter가 없는 문서를 만나면 조립 대상이 아닌 일반 문서입니다.
- `.env.example`은 복사 원본입니다. 실제 `.env`를 만들되 커밋하지 않습니다.
- 병합 충돌이 나면 중단하고 충돌 파일과 원인 브랜치를 사용자에게 보고합니다.
