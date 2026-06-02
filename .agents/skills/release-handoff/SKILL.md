# Release Handoff

Use this skill when preparing a verified local release handoff for `codex-harness-factory`.

## Purpose

Run the repository quality gate, commit reviewed changes, optionally create a tag, and only push after explicit human confirmation.

## Workflow

1. Inspect current state:
   ```bash
   git status --short --ignored
   git ls-files generated _workspace .omx
   ```
2. Confirm `generated/`, `_workspace/`, and `.omx` are not tracked.
3. Run the ship helper with a concise commit message and optional tag:
   ```bash
   ./scripts/ship.sh "<commit message>" [tag]
   ```
4. Review the diff stat printed by the helper.
5. Answer the commit prompt only after confirming the scope is intended.
6. Answer the push prompt only when the human explicitly wants the branch/tag pushed.

## Safety rules

- Do not bypass `./scripts/verify.sh`.
- Do not force-add ignored runtime outputs.
- Do not push automatically.
- Do not add runtime AI, MCP, Headroom/OMX product integration, package publishing, web UI, DB, custom DSL, or marketplace behavior as part of release handoff.
- Keep the factory CLI contract unchanged.
