from __future__ import annotations

import filecmp
import json
import os
import stat
from pathlib import Path

from .model import HarnessMetadata
from .templates import REQUIRED_FILES

_FORBIDDEN_MARKERS = ("__TEMPLATE_", "{{TEMPLATE_", "@@TEMPLATE_")


def validate_harness(root: Path, meta: HarnessMetadata | None = None) -> list[str]:
    errors: list[str] = []
    if not root.exists():
        return [f"Output directory does not exist: {root}"]
    actual = sorted(_relative_files(root))
    expected = sorted(REQUIRED_FILES)
    if actual != expected:
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        if missing:
            errors.append(f"Missing required files: {', '.join(missing)}")
        if extra:
            errors.append(f"Unexpected generated files: {', '.join(extra)}")
    verify_path = root / "scripts/verify.sh"
    if verify_path.exists() and not os.access(verify_path, os.X_OK):
        errors.append("scripts/verify.sh is not executable")
    for rel in actual:
        text = (root / rel).read_text(encoding="utf-8")
        for marker in _FORBIDDEN_MARKERS:
            if marker in text:
                errors.append(f"Unresolved marker {marker!r} in {rel}")
    if meta is not None:
        combined = "\n".join((root / rel).read_text(encoding="utf-8") for rel in actual)
        for label, value in (("title", meta.title), ("slug", meta.slug), ("entity", meta.entity)):
            if value not in combined:
                errors.append(f"Request-derived {label} not found in generated content: {value}")
    return errors


def compare_to_golden(output: Path, golden: Path) -> list[str]:
    errors: list[str] = []
    if not golden.exists():
        return [f"Golden fixture does not exist: {golden}"]
    output_files = sorted(_relative_files(output))
    golden_files = sorted(_relative_files(golden))
    if output_files != golden_files:
        errors.append(f"Golden file set mismatch: output={output_files} golden={golden_files}")
        return errors
    for rel in golden_files:
        out_path = output / rel
        golden_path = golden / rel
        if not filecmp.cmp(out_path, golden_path, shallow=False):
            errors.append(f"Golden content mismatch: {rel}")
        out_exec = bool(out_path.stat().st_mode & stat.S_IXUSR)
        golden_exec = bool(golden_path.stat().st_mode & stat.S_IXUSR)
        if out_exec != golden_exec:
            errors.append(f"Golden executable-bit mismatch: {rel}")
    return errors


def write_validation_report(path: Path, errors: list[str]) -> None:
    path.write_text(
        json.dumps({"ok": not errors, "errors": errors}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _relative_files(root: Path) -> list[str]:
    result: list[str] = []
    for path in root.rglob("*"):
        if path.is_file():
            result.append(path.relative_to(root).as_posix())
    return result
