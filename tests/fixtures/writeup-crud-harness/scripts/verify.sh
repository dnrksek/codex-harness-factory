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

template_marker_one="__""TEMPLATE_"
template_marker_two="{""{TEMPLATE_"
template_marker_three="@@""TEMPLATE_"
if grep -R -n -F -e "${template_marker_one}" -e "${template_marker_two}" -e "${template_marker_three}" AGENTS.md docs prompts README.md scripts >/tmp/writeup-crud-harness-placeholders.txt; then
  cat /tmp/writeup-crud-harness-placeholders.txt >&2
  exit 1
fi

if ! grep -R -q "Writeup" docs/SPEC.md README.md prompts; then
  echo "Request-derived entity not found in generated harness content: Writeup" >&2
  exit 1
fi

echo "Harness verification passed for writeup-crud."
