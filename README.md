# codex-harness-factory

## 1. Overview

`codex-harness-factory` is a deterministic, Python-first meta-harness that generates reusable Codex harness directories from natural-language markdown requests.

The MVP intentionally starts with template-based generation. It does not call external LLM APIs, does not run agent orchestration, and does not add product integrations. Its purpose is to prove that a small local factory can turn tracked request fixtures into reproducible Codex harnesses with validation, provenance, and quality evidence.

## 2. MVP Contract

Primary CLI contract:

```bash
python -m codex_harness_factory examples/writeup-crud.request.md --out generated/writeup-crud-harness
```

Second validated fixture:

```bash
python -m codex_harness_factory examples/python-debug.request.md --out generated/python-debug-harness
```

`--out` is constrained to a child directory under `generated/`. Live output directories are local runtime artifacts, not tracked release artifacts.

## 3. Quick Start

From the repository root:

```bash
./scripts/verify.sh
```

This compiles the package, runs stdlib tests, reads fixture mappings from `fixtures.json`, regenerates all registered MVP harnesses, compares them with tracked golden fixtures, runs each generated harness verifier, and checks workspace artifacts.

To generate one harness manually:

```bash
python -m codex_harness_factory examples/writeup-crud.request.md --out generated/writeup-crud-harness
```

## 4. Generated Harness Structure

Each generated harness contains exactly these files:

```text
AGENTS.md
docs/SPEC.md
prompts/analyze.md
prompts/plan.md
prompts/implement.md
prompts/review.md
prompts/debug.md
scripts/verify.sh
README.md
```

The generated harness is designed for Codex task work: analyze, plan, implement, review, debug, and verify. Generated content is deterministic and validated against golden fixtures.

## 5. Verification

Repository verification entrypoint:

```bash
./scripts/verify.sh
```

The verification gate checks:

- Python compileability.
- stdlib unittest coverage.
- deterministic generation for both MVP fixtures.
- golden fixture comparison.
- generated harness `scripts/verify.sh` execution.
- workspace metadata, validation report, and quality report existence.

## 6. Golden Fixtures

`fixtures.json` is the source of truth for golden fixture mappings. Each fixture entry defines:

- `request`: tracked request fixture under `examples/`.
- `output`: ignored live output under `generated/`.
- `golden`: tracked expected output under `tests/fixtures/`.

Current tracked golden fixtures:

```text
tests/fixtures/writeup-crud-harness/
tests/fixtures/python-debug-harness/
tests/fixtures/paper-summary-harness/
```

They prove that the factory is deterministic and not hardcoded only for coding-task harnesses. Live outputs under `generated/` are regenerated and compared against these fixtures.

`./scripts/verify.sh` reads fixture mappings from `fixtures.json`. `./scripts/update-golden.sh` also reads fixture mappings from `fixtures.json`, so normal verification and intentional fixture refresh use the same registry.


## Adding a New Golden Fixture

To add a new fixture, make the fixture explicit in the registry and refresh only that fixture:

1. Add `examples/<name>.request.md`.
2. Add a `fixtures.json` entry with `request`, `output`, and `golden` paths.
3. Generate/update the tracked expected output under `tests/fixtures/<name>-harness/`.
4. Run:
   ```bash
   ./scripts/update-golden.sh <name>
   ```
5. Run:
   ```bash
   ./scripts/verify.sh
   ```

Do not add live `generated/` or `_workspace/` files to git.

## 7. Workspace Artifacts

Runtime intermediates are written under:

```text
_workspace/{job_id}/
```

Current per-job artifacts include:

- `request.md`
- `metadata.json`
- `validation.json`
- `quality-report.json`

`_workspace/` is ignored and must not be committed.

## 8. Quality Report

After successful generation and validation, the factory writes:

```text
_workspace/{job_id}/quality-report.json
```

Required report fields:

- `score`
- `decision`
- `checks`
- `warnings`

Required checks:

- `required_files`
- `verify_script_executable`
- `no_unresolved_template_markers`
- `request_derived_content_present`
- `safe_output_path`
- `provenance_classification_available`

MVP scoring is intentionally simple: all required checks passing produces `score: 1.0` and `decision: "pass"`.

## 9. Provenance Classification

The provenance charter is documented in [`docs/provenance-charter.md`](docs/provenance-charter.md).

Required classifications:

| Path pattern | Classification |
| --- | --- |
| `codex_harness_factory/` | `factory-core` |
| `examples/*.request.md` | `tracked-input-fixture` |
| `tests/fixtures/*` | `tracked-golden-fixture` |
| `generated/*` | `live-output` |
| `_workspace/*` | `runtime-intermediate` |
| `templates/*` | `reusable-template` |
| `scripts/verify.sh` | `repo-quality-gate` |

The classifier is deterministic and path-pattern based; it does not inspect external services or mutable runtime state.

## 10. Release Automation

Release helper:

```bash
./scripts/ship.sh "commit message" [tag]
```

`ship.sh`:

- runs `./scripts/verify.sh` before commit.
- rejects tracked or staged `generated/`, `_workspace/`, and `.omx` files.
- shows diff/status before staging and staged diff stat before commit.
- asks before staging and commit.
- optionally creates an annotated tag.
- asks before pushing branch/tag.
- never auto-pushes without human confirmation.

A release handoff skill is available at:

```text
.agents/skills/release-handoff/SKILL.md
```

## 11. GitHub Actions

GitHub Actions verification lives at:

```text
.github/workflows/verify.yml
```

The workflow runs on `push` and `pull_request` and executes:

```bash
./scripts/verify.sh
```

It is intended to mirror the local MVP quality gate.

## 12. Safety Policy

Safety rules for the MVP:

- `--out` must be under `generated/` and cannot be `generated/` itself.
- Dangerous output paths such as `.`, `/`, `$HOME`, repository root, and outside-project paths are rejected.
- Output/workspace path overlap is rejected.
- `generated/`, `_workspace/`, and `.omx` must remain untracked.
- Existing output directories are removed only after output-path safety validation.
- Release automation requires human confirmation before commit and push.

## 13. MVP Non-Goals

The MVP explicitly does not include:

- external LLM API calls.
- runtime AI integrations.
- MCP server integration.
- Headroom or OMX product integration.
- plugin architecture.
- custom template DSL.
- web UI.
- database or persistent memory layer.
- package publishing or PyPI workflow.
- marketplace features.
- rich semantic extraction.

## 14. Current Tags / Milestones

- `mvp-0.1.0` — hardened golden-tested factory MVP baseline.
- `mvp-0.2.0` — second golden fixture proving generation is not writeup-only.
- `mvp-0.3.0` — provenance classification validation.
- `mvp-0.4.0` — deterministic quality report generation.
- `mvp-0.5.0` — release automation with ship helper, release handoff skill, and GitHub Actions verification.
- `mvp-0.6.0` — explicit golden fixture update workflow.
- `mvp-0.7.0` — third paper-summary fixture for document-processing harness coverage.
- `mvp-0.8.0` — centralized fixture registry in `fixtures.json`.

See [`docs/releases/mvp-0.5.0.md`](docs/releases/mvp-0.5.0.md) and [`docs/releases/mvp-0.8.0.md`](docs/releases/mvp-0.8.0.md) for release notes.
