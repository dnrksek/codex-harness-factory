from __future__ import annotations

import json
import os
import shutil
import unittest
from pathlib import Path

from codex_harness_factory.extract import extract_metadata
from codex_harness_factory.render import generate_harness


class QualityReportTests(unittest.TestCase):
    def setUp(self) -> None:
        self._old_cwd = Path.cwd()
        self.project = Path(__file__).resolve().parents[1]
        os.chdir(self.project)

    def tearDown(self) -> None:
        os.chdir(self._old_cwd)

    def test_quality_report_exists_and_passes_for_mvp_fixtures(self) -> None:
        for slug in ("writeup-crud", "python-debug"):
            with self.subTest(slug=slug):
                report = self._generate_and_read_report(slug)
                self.assertEqual(set(report), {"score", "decision", "checks", "warnings"})
                self.assertEqual(report["decision"], "pass")
                self.assertEqual(report["score"], 1.0)
                self.assertEqual(report["warnings"], [])
                self.assertEqual(
                    set(report["checks"]),
                    {
                        "required_files",
                        "verify_script_executable",
                        "no_unresolved_template_markers",
                        "request_derived_content_present",
                        "safe_output_path",
                        "provenance_classification_available",
                    },
                )
                self.assertTrue(all(report["checks"].values()))

    def test_quality_report_is_deterministic(self) -> None:
        first = self._generate_and_read_report("writeup-crud")
        second = self._generate_and_read_report("writeup-crud")
        self.assertEqual(first, second)

    def _generate_and_read_report(self, slug: str) -> dict[str, object]:
        request = Path(f"examples/{slug}.request.md")
        output = Path(f"generated/{slug}-harness")
        workspace = Path("_workspace")
        meta = extract_metadata(request)
        shutil.rmtree(workspace / meta.job_id, ignore_errors=True)
        generate_harness(request, output, workspace)
        report_path = workspace / meta.job_id / "quality-report.json"
        self.assertTrue(report_path.exists())
        with report_path.open(encoding="utf-8") as handle:
            return json.load(handle)


if __name__ == "__main__":
    unittest.main()
