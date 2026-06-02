from __future__ import annotations

import unittest

from codex_harness_factory.provenance import (
    FACTORY_CORE,
    LIVE_OUTPUT,
    REPO_QUALITY_GATE,
    REUSABLE_TEMPLATE,
    RUNTIME_INTERMEDIATE,
    TRACKED_GOLDEN_FIXTURE,
    TRACKED_INPUT_FIXTURE,
    UNKNOWN,
    classify_path,
)


class ProvenanceClassificationTests(unittest.TestCase):
    def test_required_path_classifications(self) -> None:
        cases = {
            "codex_harness_factory/": FACTORY_CORE,
            "codex_harness_factory/render.py": FACTORY_CORE,
            "examples/writeup-crud.request.md": TRACKED_INPUT_FIXTURE,
            "examples/python-debug.request.md": TRACKED_INPUT_FIXTURE,
            "tests/fixtures/writeup-crud-harness/AGENTS.md": TRACKED_GOLDEN_FIXTURE,
            "tests/fixtures/python-debug-harness/docs/SPEC.md": TRACKED_GOLDEN_FIXTURE,
            "generated/writeup-crud-harness/AGENTS.md": LIVE_OUTPUT,
            "generated/python-debug-harness/docs/SPEC.md": LIVE_OUTPUT,
            "_workspace/writeup-crud-abc123/metadata.json": RUNTIME_INTERMEDIATE,
            "_workspace/python-debug-abc123/validation.json": RUNTIME_INTERMEDIATE,
            "templates/base.md": REUSABLE_TEMPLATE,
            "scripts/verify.sh": REPO_QUALITY_GATE,
        }
        for path, expected in cases.items():
            with self.subTest(path=path):
                self.assertEqual(classify_path(path), expected)

    def test_unknown_paths_do_not_get_fixture_or_output_classification(self) -> None:
        for path in ("README.md", "docs/provenance-charter.md", "examples/readme.md", "generated"):
            with self.subTest(path=path):
                self.assertEqual(classify_path(path), UNKNOWN)


if __name__ == "__main__":
    unittest.main()
