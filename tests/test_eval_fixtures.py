"""Smoke-test deterministic evaluation inputs, not model effectiveness."""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


CASES = Path(__file__).resolve().parents[1] / "evals/cases"


class EvaluationFixtureTests(unittest.TestCase):
    def test_case_material_is_separable_from_scoring(self):
        for case in CASES.iterdir():
            if not case.is_dir():
                continue
            with self.subTest(case=case.name):
                self.assertTrue((case / "prompt.md").read_text(encoding="utf-8").strip())
                self.assertTrue((case / "rubric.md").read_text(encoding="utf-8").strip())
                self.assertTrue(any((case / "input").rglob("*")))
                self.assertFalse((case / "input/rubric.md").exists())

    def test_local_edit_fixture_is_red_and_can_turn_green(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "input"
            shutil.copytree(CASES / "local-edit/input", root)
            command = [sys.executable, "-B", "-m", "unittest", "discover"]
            red = subprocess.run(command, cwd=root, capture_output=True, text=True)
            self.assertEqual(red.returncode, 1)
            self.assertIn("FAIL: test_empty", red.stderr)
            self.assertIn("Ran 2 tests", red.stderr)
            source = root / "greeting.py"
            source.write_text(
                source.read_text(encoding="utf-8").replace("{name}", "{name or 'guest'}"),
                encoding="utf-8",
            )
            green = subprocess.run(command, cwd=root, capture_output=True, text=True)
            self.assertEqual(green.returncode, 0, green.stderr)

    def test_skipped_target_fixture_exhibits_the_coverage_gap(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "input"
            shutil.copytree(CASES / "skipped-target/input", root)
            result = subprocess.run(
                [sys.executable, "-B", "check.py"], cwd=root,
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("ADR-0001.md", result.stdout)
            self.assertNotIn("component-review.md", result.stdout)
            self.assertTrue((root / "records/component-review.md").exists())

    def test_homogeneous_catalog_has_real_peers_with_one_schema(self):
        paths = list((CASES / "homogeneous-peers/input/locales").glob("*.json"))
        self.assertGreaterEqual(len(paths), 20)
        for path in paths:
            self.assertEqual(set(json.loads(path.read_text())), {"greeting", "farewell"})


if __name__ == "__main__":
    unittest.main()
