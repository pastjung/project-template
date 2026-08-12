# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""브랜치 front matter 기반 조립 검증 도구.

두 가지 모드를 제공합니다.

catalog 모드 (템플릿 저장소에서 실행):
    모든 원격 브랜치의 docs front matter를 수집해 다음을 검사합니다.
    - front matter 파싱과 필수 키
    - branch 필드와 파일명 규칙(docs/<branch '/'→'-'>.md) 일치
    - requires / works-with / conflicts가 가리키는 브랜치의 존재
    - 루트 병합 브랜치 간 provides 경로 충돌

project 모드 (조립된 프로젝트에서 실행):
    로컬 docs/*.md의 front matter를 수집해 다음을 검사합니다.
    - 설치된 브랜치 목록과 requires 충족 여부
    - conflicts 쌍이 함께 설치되어 있는지
    - 치환되지 않은 {{PLACEHOLDER}} 잔존
    - after-import 체크리스트와 verify 명령 출력

실행:
    uv run scripts/validate_composition.py catalog
    uv run scripts/validate_composition.py project
    (uv가 없으면: pip install pyyaml 후 python scripts/validate_composition.py ...)
"""

from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys

import yaml

REQUIRED_KEYS = [
    "branch",
    "description",
    "provides",
    "requires",
    "works-with",
    "conflicts",
    "after-import",
    "verify",
]

# read-tree --prefix로 하위 폴더에 들어가는 app/infra 브랜치는
# 루트 docs 표준의 대상이 아닙니다.
PREFIXED_GROUPS = ("backend/", "frontend/", "data/", "observability/")

PLACEHOLDER_PATTERN = re.compile(r"\{\{[A-Z_]+\}\}")


def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], capture_output=True, text=True, encoding="utf-8"
    )
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def parse_front_matter(text: str) -> dict | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = next(i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        return None
    return yaml.safe_load("\n".join(lines[1:end]))


def works_with_branches(data: dict) -> list[str]:
    return [
        entry["branch"] if isinstance(entry, dict) else str(entry)
        for entry in data.get("works-with", []) or []
    ]


def validate_entry(data: dict, expected_slug: str, errors: list[str]) -> None:
    missing = [key for key in REQUIRED_KEYS if key not in data]
    if missing:
        errors.append(f"{expected_slug}: 필수 키 누락 {missing}")
    branch = data.get("branch", "")
    if branch.replace("/", "-") != expected_slug:
        errors.append(f"{expected_slug}: branch 필드({branch})가 파일명 규칙과 불일치")


def catalog_mode(use_local: bool = False) -> int:
    if use_local:
        prefix = ""
        branches = [
            line.strip()
            for line in run_git("branch", "--format=%(refname:short)").splitlines()
            if line.strip() not in ("main", "dev")
        ]
    else:
        prefix = "origin/"
        branches = [
            line.strip().removeprefix("origin/")
            for line in run_git("branch", "-r", "--format=%(refname:short)").splitlines()
            if line.strip().startswith("origin/")
            and not line.strip().endswith("HEAD")
            and line.strip() != "origin/main"
            and line.strip() != "origin/dev"
        ]
    root_branches = [b for b in branches if not b.startswith(PREFIXED_GROUPS)]

    errors: list[str] = []
    catalog: dict[str, dict] = {}

    for branch in root_branches:
        slug = branch.replace("/", "-")
        doc_path = f"docs/{slug}.md"
        try:
            text = run_git("show", f"{prefix}{branch}:{doc_path}")
        except RuntimeError:
            errors.append(f"{branch}: {doc_path} 없음 (파일명 규칙 위반)")
            continue
        data = parse_front_matter(text)
        if data is None:
            errors.append(f"{branch}: front matter 파싱 실패")
            continue
        validate_entry(data, slug, errors)
        catalog[branch] = data

    known = set(catalog) | set(branches)
    provides_owner: dict[str, str] = {}
    for branch, data in catalog.items():
        for ref in (data.get("requires") or []) + works_with_branches(data) + list(
            data.get("conflicts") or []
        ):
            if ref not in known:
                errors.append(f"{branch}: 존재하지 않는 브랜치 참조 '{ref}'")
        for path in data.get("provides") or []:
            if path in provides_owner:
                errors.append(
                    f"provides 충돌: '{path}' ← {provides_owner[path]} vs {branch}"
                )
            provides_owner[path] = branch

    print(f"브랜치 {len(root_branches)}개 검사 (front matter {len(catalog)}개 수집)")
    if errors:
        print(f"\n오류 {len(errors)}건:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("카탈로그 정합성 OK — 누락/불일치/충돌 없음")
    return 0


def project_mode() -> int:
    docs_dir = pathlib.Path("docs")
    if not docs_dir.is_dir():
        print("docs/ 폴더가 없습니다. 조립된 프로젝트 루트에서 실행하세요.")
        return 1

    errors: list[str] = []
    warnings: list[str] = []
    installed: dict[str, dict] = {}

    for doc in sorted(docs_dir.glob("*.md")):
        data = parse_front_matter(doc.read_text(encoding="utf-8"))
        if data is None or "branch" not in data:
            continue  # front matter 없는 일반 문서는 무시
        installed[data["branch"]] = data

    if not installed:
        print("front matter가 있는 브랜치 문서를 찾지 못했습니다.")
        return 1

    print(f"설치된 브랜치 {len(installed)}개:")
    for branch, data in installed.items():
        print(f"  - {branch}: {data.get('description', '')}")

    for branch, data in installed.items():
        for req in data.get("requires") or []:
            if req not in installed:
                errors.append(f"{branch}: 필수 브랜치 '{req}' 미설치")
        for conflict in data.get("conflicts") or []:
            if conflict in installed:
                errors.append(f"{branch}: 충돌 브랜치 '{conflict}'와 함께 설치됨")
        for path in data.get("provides") or []:
            if not pathlib.Path(path).exists():
                errors.append(f"{branch}: provides 파일 '{path}' 없음")

    for branch, data in installed.items():
        for item in data.get("placeholders") or []:
            file = item.get("file") if isinstance(item, dict) else None
            if file and pathlib.Path(file).exists():
                content = pathlib.Path(file).read_text(encoding="utf-8", errors="ignore")
                remaining = sorted(set(PLACEHOLDER_PATTERN.findall(content)))
                if remaining:
                    warnings.append(f"{branch}: {file}에 미치환 placeholder {remaining}")

    pending: list[str] = []
    for branch, data in installed.items():
        for step in data.get("after-import") or []:
            pending.append(f"[{branch}] {step}")
        for secret in data.get("secrets") or []:
            pending.append(f"[{branch}] GitHub secret 등록: {secret}")

    if pending:
        print(f"\n병합 후 수동 작업 {len(pending)}건:")
        for item in pending:
            print(f"  - {item}")

    verify_commands = [
        f"[{branch}] {cmd}"
        for branch, data in installed.items()
        for cmd in data.get("verify") or []
    ]
    if verify_commands:
        print(f"\nverify 명령 {len(verify_commands)}건 (직접 실행해 확인):")
        for cmd in verify_commands:
            print(f"  - {cmd}")

    if warnings:
        print(f"\n경고 {len(warnings)}건:")
        for warning in warnings:
            print(f"  - {warning}")

    if errors:
        print(f"\n오류 {len(errors)}건:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("\n조립 상태 OK — requires/conflicts/provides 문제 없음")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["catalog", "project"])
    parser.add_argument(
        "--local",
        action="store_true",
        help="catalog 모드에서 원격 대신 로컬 브랜치를 검사 (push 전 검증용)",
    )
    args = parser.parse_args()
    return catalog_mode(use_local=args.local) if args.mode == "catalog" else project_mode()


if __name__ == "__main__":
    sys.exit(main())
