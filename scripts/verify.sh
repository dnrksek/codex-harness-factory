#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python3 -m compileall -q codex_harness_factory
python3 -m unittest discover -s tests -p 'test_*.py'
python3 -m codex_harness_factory \
  examples/writeup-crud.request.md \
  --out generated/writeup-crud-harness \
  --workspace-root _workspace \
  --golden tests/fixtures/writeup-crud-harness

./generated/writeup-crud-harness/scripts/verify.sh

test -f _workspace/writeup-crud-*/metadata.json
test -f _workspace/writeup-crud-*/validation.json

echo "Repository verification passed."
