# Update Golden Fixture

Use this skill when a generated harness change is intentional and the tracked golden fixture must be refreshed.

## Purpose

Make golden fixture updates explicit, fixture-scoped, repeatable, and reviewable. Normal verification must compare against golden fixtures; it must not mutate them.

## Workflow

1. Choose exactly one known fixture:
   - `writeup-crud`
   - `python-debug`
2. Run:
   ```bash
   ./scripts/update-golden.sh <fixture>
   ```
3. Confirm the script completes `./scripts/verify.sh` successfully.
4. Inspect the changed fixture before committing:
   ```bash
   git diff -- tests/fixtures/<fixture>-harness
   ```
5. Confirm no runtime directories are tracked:
   ```bash
   git ls-files generated _workspace .omx
   ```

## Safety rules

- Do not use this workflow for speculative or accidental generated output changes.
- Do not update all fixtures unless a future approved workflow explicitly adds that behavior.
- Do not force-add `generated/`, `_workspace/`, or `.omx`.
- Do not commit from this skill automatically.
- Do not add runtime AI, MCP, Headroom/OMX product integration, web UI, DB, custom DSL, package publishing, plugin architecture, or marketplace behavior.
- Keep the factory CLI contract unchanged.
