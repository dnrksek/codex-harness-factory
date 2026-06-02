#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python3 -m compileall -q codex_harness_factory
python3 -m unittest discover -s tests -p 'test_*.py'

fixture_names() {
  python3 - <<'PY'
import json
with open("fixtures.json", encoding="utf-8") as handle:
    registry = json.load(handle)["fixtures"]
for name in registry:
    print(name)
PY
}

fixture_field() {
  local slug="$1"
  local field="$2"
  python3 - "$slug" "$field" <<'PY'
import json
import sys
slug, field = sys.argv[1], sys.argv[2]
with open("fixtures.json", encoding="utf-8") as handle:
    registry = json.load(handle)["fixtures"]
print(registry[slug][field])
PY
}

generate_and_verify() {
  local slug="$1"
  local request output golden
  request="$(fixture_field "$slug" request)"
  output="$(fixture_field "$slug" output)"
  golden="$(fixture_field "$slug" golden)"

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

while IFS= read -r fixture; do
  generate_and_verify "$fixture"
done < <(fixture_names)

echo "Repository verification passed."
