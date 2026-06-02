# Provenance Charter

This repository separates reusable factory code, tracked fixtures, live generated output, and runtime intermediates so MVP validation can tell what should be committed from what should remain local.

## Classifications

| Path pattern | Classification | Commit expectation |
| --- | --- | --- |
| `codex_harness_factory/` | `factory-core` | Tracked source code for the deterministic harness factory. |
| `examples/*.request.md` | `tracked-input-fixture` | Tracked request fixtures used by verification. |
| `tests/fixtures/*` | `tracked-golden-fixture` | Tracked golden generated harnesses used for deterministic comparison. |
| `generated/*` | `live-output` | Ignored local output produced by the factory CLI. |
| `_workspace/*` | `runtime-intermediate` | Ignored local run metadata and validation reports. |
| `templates/*` | `reusable-template` | Tracked reusable templates if a templates directory is introduced. |
| `scripts/verify.sh` | `repo-quality-gate` | Tracked repository verification entrypoint. |

## Rules

- Live generated outputs under `generated/` are not golden fixtures.
- Workspace intermediates under `_workspace/` are not reusable templates.
- Golden fixtures live under `tests/fixtures/` and are intentionally tracked.
- Factory source under `codex_harness_factory/` must remain deterministic and local.
- The repository quality gate is `./scripts/verify.sh`.
