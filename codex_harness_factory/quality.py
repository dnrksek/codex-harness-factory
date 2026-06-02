from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .model import HarnessMetadata
from .provenance import LIVE_OUTPUT, RUNTIME_INTERMEDIATE, classify_path

REQUIRED_CHECKS = (
    "required_files",
    "verify_script_executable",
    "no_unresolved_template_markers",
    "request_derived_content_present",
    "safe_output_path",
    "provenance_classification_available",
)


def build_quality_report(
    *,
    validation_errors: list[str],
    output_dir: Path,
    workspace_root: Path,
    meta: HarnessMetadata,
    safe_output_path: bool,
) -> dict[str, Any]:
    checks = {
        "required_files": not _has_error(validation_errors, ("Missing required files", "Unexpected generated files")),
        "verify_script_executable": not _has_error(validation_errors, ("scripts/verify.sh is not executable",)),
        "no_unresolved_template_markers": not _has_error(validation_errors, ("Unresolved marker",)),
        "request_derived_content_present": not _has_error(validation_errors, ("Request-derived",)),
        "safe_output_path": safe_output_path,
        "provenance_classification_available": _provenance_available(output_dir, workspace_root, meta),
    }
    decision = "pass" if all(checks.values()) else "fail"
    return {
        "score": 1.0 if decision == "pass" else 0.0,
        "decision": decision,
        "checks": checks,
        "warnings": [],
    }


def write_quality_report(path: Path, report: dict[str, Any]) -> None:
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _has_error(errors: list[str], prefixes: tuple[str, ...]) -> bool:
    return any(error.startswith(prefixes) for error in errors)


def _provenance_available(output_dir: Path, workspace_root: Path, meta: HarnessMetadata) -> bool:
    project_root = Path.cwd().resolve()
    return (
        classify_path(_repo_relative(output_dir, project_root)) == LIVE_OUTPUT
        and classify_path(_repo_relative(workspace_root / meta.job_id, project_root)) == RUNTIME_INTERMEDIATE
    )


def _repo_relative(path: Path, project_root: Path) -> Path:
    resolved = path.resolve()
    try:
        return resolved.relative_to(project_root)
    except ValueError:
        return path
