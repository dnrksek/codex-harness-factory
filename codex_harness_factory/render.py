from __future__ import annotations

import json
import shutil
from pathlib import Path

from .extract import extract_metadata
from .model import HarnessMetadata
from .templates import render_files
from .validation import validate_harness, write_validation_report


def generate_harness(request_path: Path, output_dir: Path, workspace_root: Path) -> HarnessMetadata:
    display_request_path = request_path
    request_path = request_path.resolve()
    output_dir = output_dir.resolve()
    workspace_root = workspace_root.resolve()
    if not request_path.exists():
        raise FileNotFoundError(f"Request file does not exist: {display_request_path}")
    if not request_path.is_file():
        raise ValueError(f"Request path is not a file: {display_request_path}")

    meta = extract_metadata(display_request_path)
    request_text = request_path.read_text(encoding="utf-8")
    job_dir = workspace_root / meta.job_id
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    job_dir.mkdir(parents=True, exist_ok=True)

    shutil.copyfile(request_path, job_dir / "request.md")
    (job_dir / "metadata.json").write_text(
        json.dumps(meta.to_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    for rel, content in render_files(meta, request_text).items():
        target = output_dir / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    verify_path = output_dir / "scripts/verify.sh"
    verify_path.chmod(0o755)

    errors = validate_harness(output_dir, meta)
    write_validation_report(job_dir / "validation.json", errors)
    if errors:
        raise ValueError("Generated harness failed validation:\n" + "\n".join(f"- {e}" for e in errors))
    return meta
