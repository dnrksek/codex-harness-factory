#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

required_files=(AGENTS.md docs/SPEC.md prompts/analyze.md prompts/plan.md prompts/implement.md prompts/review.md prompts/debug.md scripts/verify.sh README.md)
for path in "${required_files[@]}"; do
  if [[ ! -f "$path" ]]; then
    echo "Missing required harness file: $path" >&2
    exit 1
  fi
done

open_brace='{'
close_brace='}'
bad_word_one="PLACE""HOLDER"
bad_word_two="T""BD"
if grep -R -n -E "${bad_word_one}|${bad_word_two}" AGENTS.md docs prompts README.md scripts >/tmp/writeup-crud-harness-placeholders.txt; then
  cat /tmp/writeup-crud-harness-placeholders.txt >&2
  exit 1
fi
if grep -R -n -F -e "${open_brace}${open_brace}" -e "${close_brace}${close_brace}" AGENTS.md docs prompts README.md scripts >/tmp/writeup-crud-harness-placeholders.txt; then
  cat /tmp/writeup-crud-harness-placeholders.txt >&2
  exit 1
fi

if ! grep -R -q "Writeup" docs/SPEC.md README.md prompts; then
  echo "Request-derived entity not found in generated harness content: Writeup" >&2
  exit 1
fi

echo "Harness verification passed for writeup-crud."
