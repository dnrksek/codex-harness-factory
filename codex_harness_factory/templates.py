from __future__ import annotations

from .model import HarnessMetadata

REQUIRED_FILES = (
    "AGENTS.md",
    "docs/SPEC.md",
    "prompts/analyze.md",
    "prompts/plan.md",
    "prompts/implement.md",
    "prompts/review.md",
    "prompts/debug.md",
    "scripts/verify.sh",
    "README.md",
)


def render_files(meta: HarnessMetadata, request_text: str) -> dict[str, str]:
    return {
        "AGENTS.md": _agents(meta),
        "docs/SPEC.md": _spec(meta, request_text),
        "prompts/analyze.md": _prompt(meta, "analyze", "Map the request, risks, unknowns, and repository constraints before planning."),
        "prompts/plan.md": _prompt(meta, "plan", "Turn the analyzed request into an ordered implementation plan with tests and stop conditions."),
        "prompts/implement.md": _prompt(meta, "implement", "Execute the approved plan with small deterministic edits and no out-of-scope features."),
        "prompts/review.md": _prompt(meta, "review", "Review the resulting harness against the specification, constraints, and verification evidence."),
        "prompts/debug.md": _prompt(meta, "debug", "Diagnose failed verification or behavior mismatches using evidence before editing."),
        "scripts/verify.sh": _verify_script(meta),
        "README.md": _readme(meta),
    }


def _bullet(items: tuple[str, ...], fallback: str) -> str:
    values = items or (fallback,)
    return "\n".join(f"- {item}" for item in values)


def _agents(meta: HarnessMetadata) -> str:
    return f"""# {meta.title} Codex Harness

This generated harness guides Codex work for {meta.domain}.

## Operating rules
- Start by reading `docs/SPEC.md` and the prompt that matches the task phase.
- Keep work deterministic and local unless the spec explicitly allows otherwise.
- Do not call external LLM APIs from this harness.
- Do not add web UI, database, persistent memory, MCP server, Headroom, OMX, or agent-runtime integrations unless a future approved spec changes scope.
- Prefer small, reviewable changes and verify before claiming completion.

## Required verification
Run `./scripts/verify.sh` from this harness root before final handoff.
"""


def _spec(meta: HarnessMetadata, request_text: str) -> str:
    return f"""# SPEC: {meta.title}

## Source
- Request file: `{meta.source_request}`
- Harness slug: `{meta.slug}`
- Primary entity: {meta.entity}
- Domain: {meta.domain}

## Goal
{_bullet(meta.goals, f"Build and maintain a Codex harness for {meta.domain}.")}

## Supported operations
{_bullet(meta.operations, "Analyze, plan, implement, review, and debug changes.")}

## Constraints
{_bullet(meta.constraints, "Keep the harness deterministic, local, and easy to verify.")}

## Non-goals
{_bullet(meta.non_goals, "No out-of-scope runtime integrations or unnecessary infrastructure.")}

## Required harness files
{_bullet(REQUIRED_FILES, "Required generated files must exist.")}

## Original request

```markdown
{request_text.strip()}
```
"""


def _prompt(meta: HarnessMetadata, phase: str, purpose: str) -> str:
    return f"""# {phase.title()} Prompt: {meta.title}

## Purpose
{purpose}

## Context
- Harness: {meta.title}
- Domain: {meta.domain}
- Entity: {meta.entity}
- Operations: {", ".join(meta.operations)}

## Instructions
1. Read `docs/SPEC.md` before acting.
2. Stay within the MVP constraints and non-goals in the spec.
3. Preserve deterministic behavior and avoid unnecessary dependencies.
4. Record assumptions explicitly when information is missing.
5. Run `./scripts/verify.sh` before final handoff when files changed.

## Phase output
Return concise findings, changed files if any, verification evidence, and remaining risks.
"""


def _verify_script(meta: HarnessMetadata) -> str:
    required = " ".join(REQUIRED_FILES)
    return f"""#!/usr/bin/env bash
set -euo pipefail

ROOT=\"$(cd \"$(dirname \"${{BASH_SOURCE[0]}}\")/..\" && pwd)\"
cd \"$ROOT\"

required_files=({required})
for path in \"${{required_files[@]}}\"; do
  if [[ ! -f \"$path\" ]]; then
    echo \"Missing required harness file: $path\" >&2
    exit 1
  fi
done

open_brace='{{'
close_brace='}}'
bad_word_one="PLACE""HOLDER"
bad_word_two="T""BD"
if grep -R -n -E "${{bad_word_one}}|${{bad_word_two}}" AGENTS.md docs prompts README.md scripts >/tmp/{meta.slug}-harness-placeholders.txt; then
  cat /tmp/{meta.slug}-harness-placeholders.txt >&2
  exit 1
fi
if grep -R -n -F -e \"${{open_brace}}${{open_brace}}\" -e \"${{close_brace}}${{close_brace}}\" AGENTS.md docs prompts README.md scripts >/tmp/{meta.slug}-harness-placeholders.txt; then
  cat /tmp/{meta.slug}-harness-placeholders.txt >&2
  exit 1
fi

if ! grep -R -q \"{meta.entity}\" docs/SPEC.md README.md prompts; then
  echo \"Request-derived entity not found in generated harness content: {meta.entity}\" >&2
  exit 1
fi

echo \"Harness verification passed for {meta.slug}.\"
"""


def _readme(meta: HarnessMetadata) -> str:
    return f"""# {meta.title} Harness

This is a deterministic Codex harness for {meta.domain}.

## Contents
{_bullet(REQUIRED_FILES, "Generated harness files.")}

## How to use
1. Read `AGENTS.md` for operating rules.
2. Read `docs/SPEC.md` for scope, constraints, and non-goals.
3. Use the prompt in `prompts/` that matches your work phase.
4. Run `./scripts/verify.sh` before final handoff.

## Extracted metadata
- Slug: `{meta.slug}`
- Entity: {meta.entity}
- Operations: {", ".join(meta.operations)}

Generated by `codex-harness-factory` using deterministic templates.
"""
