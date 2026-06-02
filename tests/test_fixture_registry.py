from __future__ import annotations

import json
import unittest
from pathlib import Path


class FixtureRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(__file__).resolve().parents[1]
        with (self.root / "fixtures.json").open(encoding="utf-8") as handle:
            self.registry = json.load(handle)["fixtures"]

    def test_expected_fixture_names_are_registered(self) -> None:
        self.assertEqual(set(self.registry), {"writeup-crud", "python-debug", "paper-summary"})

    def test_registered_paths_are_safe_and_exist(self) -> None:
        for name, entry in self.registry.items():
            with self.subTest(name=name):
                self.assertEqual(set(entry), {"request", "output", "golden"})
                request = Path(entry["request"])
                output = Path(entry["output"])
                golden = Path(entry["golden"])

                self.assertEqual(request, Path("examples") / f"{name}.request.md")
                self.assertEqual(output, Path("generated") / f"{name}-harness")
                self.assertEqual(golden, Path("tests/fixtures") / f"{name}-harness")

                self.assertTrue((self.root / request).is_file())
                self.assertTrue((self.root / golden).is_dir())
                self.assertFalse(request.is_absolute())
                self.assertFalse(output.is_absolute())
                self.assertFalse(golden.is_absolute())


if __name__ == "__main__":
    unittest.main()
