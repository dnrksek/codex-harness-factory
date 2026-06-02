#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: ./scripts/ship.sh \"commit message\" [tag]"
  exit 2
fi

COMMIT_MESSAGE="$1"
TAG="${2:-}"

echo "== Ensure we are in a git repository =="
git rev-parse --show-toplevel >/dev/null

echo "== Run repository verification =="
./scripts/verify.sh

echo "== Ensure runtime outputs are not tracked =="
TRACKED_RUNTIME="$(git ls-files generated _workspace .omx || true)"
if [ -n "$TRACKED_RUNTIME" ]; then
  echo "ERROR: runtime output is tracked:"
  echo "$TRACKED_RUNTIME"
  exit 1
fi

echo "== Show git status =="
git status --short

echo "== Show diff summary =="
git diff --stat

echo
echo "Review the diff above."
read -r -p "Continue with commit and push? [y/N] " CONFIRM
if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
  echo "Aborted."
  exit 1
fi

echo "== Stage source changes =="
git add .

echo "== Re-check staged runtime files =="
STAGED_RUNTIME="$(git diff --cached --name-only | grep -E '^(generated|_workspace|\.omx)/' || true)"
if [ -n "$STAGED_RUNTIME" ]; then
  echo "ERROR: runtime output staged:"
  echo "$STAGED_RUNTIME"
  exit 1
fi

echo "== Commit =="
git commit -m "$COMMIT_MESSAGE"

if [ -n "$TAG" ]; then
  echo "== Create tag =="
  if git rev-parse "$TAG" >/dev/null 2>&1; then
    echo "ERROR: tag already exists: $TAG"
    exit 1
  fi
  git tag "$TAG"
fi

echo "== Push branch =="
git push

if [ -n "$TAG" ]; then
  echo "== Push tag =="
  git push origin "$TAG"
fi

echo "== Done =="
