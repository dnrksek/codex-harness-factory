from __future__ import annotations

from pathlib import Path

FACTORY_CORE = "factory-core"
TRACKED_INPUT_FIXTURE = "tracked-input-fixture"
TRACKED_GOLDEN_FIXTURE = "tracked-golden-fixture"
LIVE_OUTPUT = "live-output"
RUNTIME_INTERMEDIATE = "runtime-intermediate"
REUSABLE_TEMPLATE = "reusable-template"
REPO_QUALITY_GATE = "repo-quality-gate"
UNKNOWN = "unknown"


def classify_path(path: str | Path) -> str:
    """Classify a repository-relative path by MVP provenance."""

    normalized = _normalize(path)
    parts = normalized.parts
    if not parts:
        return UNKNOWN
    if normalized == Path("scripts/verify.sh"):
        return REPO_QUALITY_GATE
    if parts[0] == "codex_harness_factory":
        return FACTORY_CORE
    if parts[0] == "examples" and normalized.name.endswith(".request.md"):
        return TRACKED_INPUT_FIXTURE
    if len(parts) >= 3 and parts[0] == "tests" and parts[1] == "fixtures":
        return TRACKED_GOLDEN_FIXTURE
    if parts[0] == "generated" and len(parts) >= 2:
        return LIVE_OUTPUT
    if parts[0] == "_workspace" and len(parts) >= 2:
        return RUNTIME_INTERMEDIATE
    if parts[0] == "templates" and len(parts) >= 2:
        return REUSABLE_TEMPLATE
    return UNKNOWN


def _normalize(path: str | Path) -> Path:
    raw = Path(path)
    return Path(*[part for part in raw.parts if part not in ("", ".")])
