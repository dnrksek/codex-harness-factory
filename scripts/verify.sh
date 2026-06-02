#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python3 -m compileall -q codex_harness_factory
python3 -m unittest discover -s tests -p 'test_*.py'

generate_and_verify() {
  local slug="$1"
  local request="examples/${slug}.request.md"
  local output="generated/${slug}-harness"
  local golden="tests/fixtures/${slug}-harness"

  python3 -m codex_harness_factory \
    "$request" \
    --out "$output" \
    --workspace-root _workspace \
    --golden "$golden"

  "./${output}/scripts/verify.sh"

  test -f _workspace/${slug}-*/metadata.json
  test -f _workspace/${slug}-*/validation.json
  test -f _workspace/${slug}-*/quality-report.json
}

generate_and_verify writeup-crud
generate_and_verify python-debug
generate_and_verify paper-summary

echo "Repository verification passed."
