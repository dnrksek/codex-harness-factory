#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: ./scripts/update-golden.sh <fixture>

Known fixtures:
  writeup-crud
  python-debug

Regenerates the selected live output, replaces only that fixture's tracked
golden directory, then runs ./scripts/verify.sh. This script does not commit.
EOF
}

resolve_path() {
  python3 -c 'from pathlib import Path; import sys; print(Path(sys.argv[1]).resolve())' "$1"
}

is_under_dir() {
  local child="$1"
  local parent="$2"
  [[ "$child" == "$parent"/* ]]
}

reject_empty_path() {
  local label="$1"
  local value="$2"
  if [[ -z "$value" || "$value" == "." || "$value" == "/" ]]; then
    echo "Unsafe ${label} path: ${value:-<empty>}" >&2
    exit 1
  fi
}

if [[ $# -ne 1 ]]; then
  usage >&2
  exit 2
fi

fixture="$1"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

case "$fixture" in
  writeup-crud)
    request="examples/writeup-crud.request.md"
    output="generated/writeup-crud-harness"
    golden="tests/fixtures/writeup-crud-harness"
    ;;
  python-debug)
    request="examples/python-debug.request.md"
    output="generated/python-debug-harness"
    golden="tests/fixtures/python-debug-harness"
    ;;
  *)
    echo "Unknown fixture: $fixture" >&2
    usage >&2
    exit 2
    ;;
esac

reject_empty_path request "$request"
reject_empty_path output "$output"
reject_empty_path golden "$golden"

if [[ ! -f "$request" ]]; then
  echo "Request fixture does not exist: $request" >&2
  exit 1
fi

generated_root_abs="$(resolve_path generated)"
fixtures_root_abs="$(resolve_path tests/fixtures)"
output_abs="$(resolve_path "$output")"
golden_abs="$(resolve_path "$golden")"

if ! is_under_dir "$output_abs" "$generated_root_abs"; then
  echo "Refusing unsafe output path outside generated/: $output" >&2
  exit 1
fi

if [[ "$golden_abs" == "$fixtures_root_abs" ]] || ! is_under_dir "$golden_abs" "$fixtures_root_abs"; then
  echo "Refusing unsafe golden path outside tests/fixtures/: $golden" >&2
  exit 1
fi

python3 -m codex_harness_factory "$request" --out "$output" --workspace-root _workspace

if [[ ! -d "$output" ]]; then
  echo "Generated output directory was not created: $output" >&2
  exit 1
fi

rm -rf -- "$golden"
mkdir -p -- "$(dirname "$golden")"
cp -a -- "$output" "$golden"

./scripts/verify.sh

cat <<EOF
Updated golden fixture: $golden
Inspect the fixture diff before committing:
  git diff -- $golden
EOF
