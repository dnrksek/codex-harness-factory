# Debug Prompt: Python Debug Harness

## Purpose
Diagnose failed verification or behavior mismatches using evidence before editing.

## Context
- Harness: Python Debug Harness
- Domain: Python test and build debugging
- Entity: Python Failure
- Operations: Analyze, Plan, Implement, Review, Debug

## Instructions
1. Read `docs/SPEC.md` before acting.
2. Stay within the MVP constraints and non-goals in the spec.
3. Preserve deterministic behavior and avoid unnecessary dependencies.
4. Record assumptions explicitly when information is missing.
5. Run `./scripts/verify.sh` before final handoff when files changed.

## Phase output
Return concise findings, changed files if any, verification evidence, and remaining risks.
