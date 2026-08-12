#!/usr/bin/env bash
set -euo pipefail

required() {
  local name="$1"
  local value="${!name:-}"

  if [ -z "$value" ]; then
    echo "$name is required."
    exit 1
  fi
}

required MODULE_NAME
required MODULE_PATH
required MODULE_REPOSITORY

MODULE_REF="${MODULE_REF:-main}"
MODULE_SHA="${MODULE_SHA:-}"
MODULE_SYNC_MODE="${MODULE_SYNC_MODE:-subtree}"
SYNC_BRANCH_PREFIX="${SYNC_BRANCH_PREFIX:-sync}"
MODULE_REMOTE_NAME="module-sync"

if [ ! -d .git ]; then
  echo "The mounted main module path must be a Git repository."
  exit 1
fi

# 컨테이너가 호스트 저장소를 마운트하면 소유자가 달라 git이
# "dubious ownership" 오류를 냅니다. 마운트된 경로를 신뢰 목록에 추가합니다.
git config --global --add safe.directory "$(pwd)"

git fetch origin dev
git switch dev
git pull origin dev

SHORT_SHA="${MODULE_SHA:0:7}"
if [ -z "$SHORT_SHA" ]; then
  SHORT_SHA="$(date +%Y%m%d%H%M%S)"
fi

SYNC_BRANCH="${SYNC_BRANCH_PREFIX}/${MODULE_NAME}-${SHORT_SHA}"
git switch -c "$SYNC_BRANCH"

if [ "$MODULE_SYNC_MODE" = "submodule" ]; then
  required MODULE_SHA

  git submodule update --init --recursive "$MODULE_PATH"
  git -C "$MODULE_PATH" fetch origin "$MODULE_REF"
  git -C "$MODULE_PATH" checkout "$MODULE_SHA"
  git add "$MODULE_PATH"
  if ! git diff --cached --quiet; then
    git commit -m "chore: sync ${MODULE_NAME} sub module"
  fi
elif [ "$MODULE_SYNC_MODE" = "subtree" ]; then
  git remote add "$MODULE_REMOTE_NAME" "https://github.com/${MODULE_REPOSITORY}.git" 2>/dev/null \
    || git remote set-url "$MODULE_REMOTE_NAME" "https://github.com/${MODULE_REPOSITORY}.git"
  git fetch "$MODULE_REMOTE_NAME" "$MODULE_REF"

  MODULE_TARGET="$MODULE_REF"
  if [ -n "${MODULE_SHA:-}" ]; then
    if ! git cat-file -e "${MODULE_SHA}^{commit}"; then
      echo "MODULE_SHA ${MODULE_SHA} was not found after fetching ${MODULE_REF}."
      exit 1
    fi
    MODULE_TARGET="$MODULE_SHA"
  fi

  if [ -d "$MODULE_PATH" ]; then
    if ! git subtree pull \
      --prefix="$MODULE_PATH" \
      "$MODULE_REMOTE_NAME" "$MODULE_TARGET" \
      --squash \
      -m "chore: sync ${MODULE_NAME} sub module"; then
      echo "git subtree pull failed for ${MODULE_PATH}."
      echo "Merge conflict가 발생했을 가능성이 큽니다. 충돌을 해결하고 commit한 뒤 브랜치를 push하세요."
      exit 1
    fi
  else
    mkdir -p "$(dirname "$MODULE_PATH")"
    git subtree add \
      --prefix="$MODULE_PATH" \
      "$MODULE_REMOTE_NAME" "$MODULE_TARGET" \
      --squash \
      -m "chore: sync ${MODULE_NAME} sub module"
  fi
else
  echo "Unsupported MODULE_SYNC_MODE: $MODULE_SYNC_MODE"
  exit 1
fi

if git diff --quiet dev HEAD; then
  echo "No module sync changes."
  exit 0
fi

echo "Created local sync branch: $SYNC_BRANCH"
echo "Review changes and push the branch when ready."
