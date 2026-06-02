# Release Notes: mvp-0.8.0

## Summary

`mvp-0.8.0` documents and finalizes the centralized fixture registry introduced in Phase 9. The registry keeps golden fixture mappings in one root-level file so verification and intentional golden updates share the same source of truth.

## What changed

- Added `fixtures.json` at the repository root as the canonical fixture mapping registry.
- Moved mappings for `writeup-crud`, `python-debug`, and `paper-summary` into `fixtures.json`.
- Updated `scripts/verify.sh` to read fixture names and request/output/golden paths from `fixtures.json`.
- Updated `scripts/update-golden.sh` to read the selected fixture mapping from `fixtures.json`.
- Added stdlib tests for fixture registry validity.
- Updated golden fixture documentation to reference `fixtures.json` as the source of truth.

## Fixture registry shape

Each fixture entry has exactly these MVP fields:

```json
{
  "request": "examples/<name>.request.md",
  "output": "generated/<name>-harness",
  "golden": "tests/fixtures/<name>-harness"
}
```

The MVP registry schema is intentionally small and does not add new dependencies.

## Adding a fixture

To add a new fixture:

1. Add `examples/<name>.request.md`.
2. Add a `fixtures.json` entry.
3. Generate the expected output under `tests/fixtures/<name>-harness/`.
4. Run:
   ```bash
   ./scripts/update-golden.sh <name>
   ```
5. Run:
   ```bash
   ./scripts/verify.sh
   ```

Normal verification must not mutate golden fixtures. `update-golden.sh` remains explicit and fixture-scoped.

## Verification

Release quality gate:

```bash
./scripts/verify.sh
```

Runtime tracking invariant:

```bash
git ls-files generated _workspace .omx
# no output
```

## Non-goals preserved

This release does not change the factory CLI contract, generated harness content, golden fixture contents, output path safety, registry schema scope, or MVP non-goals. It adds no runtime AI, MCP, Headroom/OMX product integration, package publishing, web UI, database, persistent memory, or Python dependencies.
