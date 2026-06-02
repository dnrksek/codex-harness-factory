# SPEC: Writeup CRUD Harness

## Source
- Request file: `examples/writeup-crud.request.md`
- Harness slug: `writeup-crud`
- Primary entity: Writeup
- Domain: Writeup CRUD

## Goal
- Generate a reusable Codex harness for implementing a small writeup CRUD feature.
- Guide Codex through analysis, planning, implementation, review, and debugging phases.
- Keep generated instructions specific enough for create, read, update, and delete workflows.

## Supported operations
- Create
- Read
- Update
- Delete

## Constraints
- Use deterministic local files and scripts.
- Prefer Python-first tooling and shell verification.
- Keep the harness readable, reusable, and easy to review.
- Include all required harness files in the generated output.

## Non-goals
- No web UI requirement in the harness itself.
- No external LLM API calls.
- No database or persistent memory layer.
- No runtime agent orchestration.

## Required harness files
- AGENTS.md
- docs/SPEC.md
- prompts/analyze.md
- prompts/plan.md
- prompts/implement.md
- prompts/review.md
- prompts/debug.md
- scripts/verify.sh
- README.md

## Original request

```markdown
# Writeup CRUD Harness

Entity: Writeup
Domain: Writeup CRUD

## Goal
- Generate a reusable Codex harness for implementing a small writeup CRUD feature.
- Guide Codex through analysis, planning, implementation, review, and debugging phases.
- Keep generated instructions specific enough for create, read, update, and delete workflows.

## Constraints
- Use deterministic local files and scripts.
- Prefer Python-first tooling and shell verification.
- Keep the harness readable, reusable, and easy to review.
- Include all required harness files in the generated output.

## Non-goals
- No web UI requirement in the harness itself.
- No external LLM API calls.
- No database or persistent memory layer.
- No runtime agent orchestration.
```
