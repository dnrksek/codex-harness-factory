from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .render import generate_harness
from .validation import compare_to_golden


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m codex_harness_factory",
        description="Generate deterministic reusable Codex harnesses from markdown requests.",
    )
    parser.add_argument("request", type=Path, help="Natural-language markdown request file")
    parser.add_argument("--out", required=True, type=Path, help="Generated harness output directory")
    parser.add_argument(
        "--workspace-root",
        default=Path("_workspace"),
        type=Path,
        help="Root for intermediate artifacts; job files are stored under _workspace/{job_id}",
    )
    parser.add_argument(
        "--golden",
        type=Path,
        default=None,
        help="Optional tracked golden fixture directory to compare with generated output",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        meta = generate_harness(args.request, args.out, args.workspace_root)
        if args.golden is not None:
            errors = compare_to_golden(args.out, args.golden)
            if errors:
                for error in errors:
                    print(error, file=sys.stderr)
                return 1
        print(f"Generated {meta.slug} harness at {args.out}")
        print(f"Workspace artifacts: {args.workspace_root / meta.job_id}")
        return 0
    except Exception as exc:  # noqa: BLE001 - CLI boundary should print concise failures.
        print(f"error: {exc}", file=sys.stderr)
        return 1
