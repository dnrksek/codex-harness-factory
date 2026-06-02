from __future__ import annotations

import json
import shutil
from pathlib import Path

from .extract import extract_metadata
from .model import HarnessMetadata
from .quality import build_quality_report, write_quality_report
from .templates import render_files
from .validation import validate_harness, write_validation_report


def generate_harness(request_path: Path, output_dir: Path, workspace_root: Path) -> HarnessMetadata:
    display_request_path = request_path
    project_root = Path.cwd().resolve()
    request_path = request_path.resolve()
    output_dir = output_dir.resolve()
    workspace_root = workspace_root.resolve()
    _validate_paths(project_root, output_dir, workspace_root)

    if not request_path.exists():
        raise FileNotFoundError(f"Request file does not exist: {display_request_path}")
    if not request_path.is_file():
        raise ValueError(f"Request path is not a file: {display_request_path}")

    meta = extract_metadata(display_request_path)
    request_text = request_path.read_text(encoding="utf-8")
    job_dir = workspace_root / meta.job_id
    if output_dir.exists():
        if not output_dir.is_dir():
            raise ValueError(f"Output path exists but is not a directory: {output_dir}")
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
    write_quality_report(
        job_dir / "quality-report.json",
        build_quality_report(
            validation_errors=errors,
            output_dir=output_dir,
            workspace_root=workspace_root,
            meta=meta,
            safe_output_path=True,
        ),
    )
    if errors:
        raise ValueError("Generated harness failed validation:\n" + "\n".join(f"- {e}" for e in errors))
    return meta


def _validate_paths(project_root: Path, output_dir: Path, workspace_root: Path) -> None:
    generated_root = (project_root / "generated").resolve()
    if output_dir == generated_root or not _is_relative_to(output_dir, generated_root):
        raise ValueError("Output directory must be a generated harness directory under ./generated/.")
    if output_dir == project_root:
        raise ValueError("Output directory must not be the repository root.")
    if output_dir == Path.home().resolve():
        raise ValueError("Output directory must not be the home directory.")
    if output_dir == workspace_root:
        raise ValueError("Output directory and workspace root must not be the same path.")
    if _is_relative_to(workspace_root, output_dir):
        raise ValueError("Workspace root must not be inside the output directory.")
    if _is_relative_to(output_dir, workspace_root):
        raise ValueError("Output directory must not be inside the workspace root.")


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True
