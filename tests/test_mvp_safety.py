from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from codex_harness_factory.render import generate_harness


class HarnessFactorySafetyTests(unittest.TestCase):
    def setUp(self) -> None:
        self._old_cwd = Path.cwd()
        self._tmp = tempfile.TemporaryDirectory()
        self.project = Path(self._tmp.name)
        os.chdir(self.project)
        self.request = Path("writeup-crud.request.md")
        self.request.write_text(
            "# Writeup CRUD Harness\n\n"
            "Entity: Writeup\n"
            "Domain: Writeup CRUD\n\n"
            "## Goal\n"
            "- Generate a deterministic harness.\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        os.chdir(self._old_cwd)
        self._tmp.cleanup()

    def test_rejects_unsafe_output_paths(self) -> None:
        unsafe_paths = [
            Path("."),
            Path("/"),
            Path.home(),
            self.project,
            Path("outside-harness"),
            Path("../outside-harness"),
            Path("generated"),
        ]
        for output_path in unsafe_paths:
            with self.subTest(output_path=output_path):
                with self.assertRaises(ValueError):
                    generate_harness(self.request, output_path, Path("_workspace"))

    def test_rejects_output_workspace_overlap(self) -> None:
        overlap_cases = [
            (Path("generated/writeup-crud-harness"), Path("generated/writeup-crud-harness")),
            (Path("generated/writeup-crud-harness"), Path("generated/writeup-crud-harness/_workspace")),
            (Path("generated/workspace/writeup-crud-harness"), Path("generated/workspace")),
        ]
        for output_path, workspace_root in overlap_cases:
            with self.subTest(output_path=output_path, workspace_root=workspace_root):
                with self.assertRaises(ValueError):
                    generate_harness(self.request, output_path, workspace_root)

    def test_request_text_with_common_placeholder_words_is_allowed(self) -> None:
        request = Path("placeholder.request.md")
        request.write_text(
            "# Placeholder Harness\n\n"
            "Entity: Note\n"
            "Domain: Note CRUD\n\n"
            "## Goal\n"
            "- Preserve literal TBD text from the request.\n"
            "- Preserve literal {{example}} text from the request.\n",
            encoding="utf-8",
        )
        output = Path("generated/placeholder-harness")
        generate_harness(request, output, Path("_workspace"))

        spec = (output / "docs/SPEC.md").read_text(encoding="utf-8")
        self.assertIn("TBD", spec)
        self.assertIn("{{example}}", spec)
        subprocess.run([str(output / "scripts/verify.sh")], check=True)


if __name__ == "__main__":
    unittest.main()
