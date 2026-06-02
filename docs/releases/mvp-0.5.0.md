# Release Notes: mvp-0.5.0

## Summary

`mvp-0.5.0` hardens the repository for GitHub-facing use by adding safe release automation while preserving the deterministic factory MVP. It keeps the primary CLI contract unchanged and continues to rely on `./scripts/verify.sh` as the release quality gate.

## Milestone History

### mvp-0.1.0 — Golden-tested factory MVP

- Added the deterministic Python-first factory MVP.
- Generated the `writeup-crud` harness from `examples/writeup-crud.request.md`.
- Added tracked golden fixture validation.
- Hardened output path safety so live generated output remains under `generated/`.
- Kept `_workspace/` as ignored runtime intermediates.

### mvp-0.2.0 — Second fixture

- Added `examples/python-debug.request.md`.
- Added `tests/fixtures/python-debug-harness/`.
- Extended verification so both `writeup-crud` and `python-debug` fixtures are generated and compared.
- Proved the MVP is not hardcoded only for the writeup CRUD example.

### mvp-0.3.0 — Provenance classification

- Added `docs/provenance-charter.md`.
- Added deterministic provenance classification for factory core, tracked input fixtures, tracked golden fixtures, live outputs, runtime intermediates, reusable templates, and the repo quality gate.
- Added tests for expected path classifications.

### mvp-0.4.0 — Quality report

- Added deterministic quality report generation.
- Wrote `_workspace/{job_id}/quality-report.json` after generation and validation.
- Added checks for required files, executable generated verifier, unresolved template markers, request-derived content, safe output path, and provenance classification availability.
- Kept scoring simple: all checks passing produces `score: 1.0` and `decision: "pass"`.

### mvp-0.5.0 — Release automation

- Added `scripts/ship.sh` for verified local release handoff.
- Added `.agents/skills/release-handoff/SKILL.md`.
- Added `.github/workflows/verify.yml` to run `./scripts/verify.sh` on `push` and `pull_request`.
- Preserved safety by requiring confirmation before commit and push.
- Rejected tracked/staged `generated/`, `_workspace/`, and `.omx` runtime artifacts during ship flow.

## Verification

Release quality gate:

```bash
./scripts/verify.sh
```

Expected invariants:

```bash
git ls-files generated _workspace .omx
# no output
```

## Non-Goals Preserved

This release does not add runtime AI integrations, external LLM API calls, MCP, Headroom/OMX product integration, package publishing, web UI, database or persistent memory, marketplace features, custom template DSL, or rich semantic extraction.
