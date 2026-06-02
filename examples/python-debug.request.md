# Python Debug Harness

Entity: Python Failure
Domain: Python test and build debugging

## Goal
- Generate a reusable Codex harness for debugging Python test and build failures.
- Guide Codex through failure reproduction, evidence collection, root-cause analysis, fix planning, implementation, and review.
- Keep generated instructions focused on local Python projects, shell commands, and deterministic verification.

## Constraints
- Use deterministic local files and scripts.
- Prefer Python-first diagnostics and repository-local verification commands.
- Preserve failing logs, stack traces, and test output as primary evidence.
- Include all required harness files in the generated output.

## Non-goals
- No runtime LLM API calls.
- No MCP, Headroom, or OMX product integration.
- No plugin architecture or custom template DSL.
- No web UI, database, or persistent memory layer.
