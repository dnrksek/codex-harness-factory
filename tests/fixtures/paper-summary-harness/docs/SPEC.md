# SPEC: Paper Summary Harness

## Source
- Request file: `examples/paper-summary.request.md`
- Harness slug: `paper-summary`
- Primary entity: Research Paper
- Domain: Document summarization and review pipeline

## Goal
- Generate a reusable Codex harness for summarizing and reviewing research papers or long technical documents.
- Guide Codex through document intake, structure extraction, claim/evidence mapping, summary drafting, review, and debugging of unclear or inconsistent notes.
- Keep generated instructions focused on deterministic local document-processing workflows and review evidence.

## Supported operations
- Search

## Constraints
- Use deterministic local files and scripts.
- Preserve source document titles, section headings, claims, limitations, and citation cues as primary evidence.
- Prefer concise structured summaries with explicit assumptions and unresolved questions.
- Include all required harness files in the generated output.

## Non-goals
- No runtime LLM API calls.
- No MCP, Headroom, or OMX product integration.
- No plugin architecture or custom template DSL.
- No web UI, database, persistent memory, or package publishing workflow.

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
# Paper Summary Harness

Entity: Research Paper
Domain: Document summarization and review pipeline

## Goal
- Generate a reusable Codex harness for summarizing and reviewing research papers or long technical documents.
- Guide Codex through document intake, structure extraction, claim/evidence mapping, summary drafting, review, and debugging of unclear or inconsistent notes.
- Keep generated instructions focused on deterministic local document-processing workflows and review evidence.

## Constraints
- Use deterministic local files and scripts.
- Preserve source document titles, section headings, claims, limitations, and citation cues as primary evidence.
- Prefer concise structured summaries with explicit assumptions and unresolved questions.
- Include all required harness files in the generated output.

## Non-goals
- No runtime LLM API calls.
- No MCP, Headroom, or OMX product integration.
- No plugin architecture or custom template DSL.
- No web UI, database, persistent memory, or package publishing workflow.
```
