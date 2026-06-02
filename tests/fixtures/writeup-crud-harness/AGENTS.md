# Writeup CRUD Harness Codex Harness

This generated harness guides Codex work for Writeup CRUD.

## Operating rules
- Start by reading `docs/SPEC.md` and the prompt that matches the task phase.
- Keep work deterministic and local unless the spec explicitly allows otherwise.
- Do not call external LLM APIs from this harness.
- Do not add web UI, database, persistent memory, MCP server, Headroom, OMX, or agent-runtime integrations unless a future approved spec changes scope.
- Prefer small, reviewable changes and verify before claiming completion.

## Required verification
Run `./scripts/verify.sh` from this harness root before final handoff.
