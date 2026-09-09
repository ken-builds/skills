"""Exercise artifact CLI coverage against valid, invalid, and unsupported targets."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALID_ADR = ROOT / "skills/greenfield-foundation/tests/fixtures/valid-adr.md"
VALIDATORS = (
    ROOT / "skills/architecture-design/scripts/validate_artifacts.py",
    ROOT / "skills/greenfield-foundation/scripts/validate_foundation.py",
)


class ArtifactCoverageTests(unittest.TestCase):
    def run_validator(self, script, target, *options):
        return subprocess.run(
            [sys.executable, str(script), str(target), *options],
            capture_output=True, text=True, check=False,
        )

    def test_valid_then_unsupported_record_in_same_gate(self):
        for script in VALIDATORS:
            with self.subTest(script=script), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                (root / "ADR-0001.md").write_bytes(VALID_ADR.read_bytes())
                valid = self.run_validator(script, root, "--fail-on-skip")
                self.assertEqual(valid.returncode, 0, valid.stdout + valid.stderr)
                (root / "structure.md").write_text("# Structure Review: new\n", encoding="utf-8")
                advisory = self.run_validator(script, root)
                self.assertEqual(advisory.returncode, 0, advisory.stdout)
                self.assertIn("selected=1, skipped=1, failed=0", advisory.stdout)
                strict = self.run_validator(script, root, "--fail-on-skip", "--quiet")
                self.assertEqual(strict.returncode, 1, strict.stdout)
                self.assertIn("unsupported artifact kind", strict.stdout)
                self.assertIn("structure.md", strict.stdout)

    def test_contract_violation_fails_without_coverage_failure(self):
        for script in VALIDATORS:
            with self.subTest(script=script), tempfile.TemporaryDirectory() as directory:
                target = Path(directory) / "ADR-0001.md"
                target.write_text(
                    VALID_ADR.read_text(encoding="utf-8").replace("Status: proposed", "Status: invented"),
                    encoding="utf-8",
                )
                result = self.run_validator(script, target, "--fail-on-skip")
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("unsupported ADR status", result.stdout)
                self.assertIn("selected=1, skipped=0, failed=1", result.stdout)

    def test_undecodable_target_is_not_silently_ignored(self):
        for script in VALIDATORS:
            with self.subTest(script=script), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                (root / "ADR-0001.md").write_bytes(VALID_ADR.read_bytes())
                (root / "broken.md").write_bytes(b"\xff")
                result = self.run_validator(script, root)
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("cannot decode UTF-8", result.stdout)

    def test_empty_or_only_unsupported_scope_never_passes(self):
        for script in VALIDATORS:
            with self.subTest(script=script), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.assertEqual(self.run_validator(script, root).returncode, 2)
                (root / "notes.md").write_text("# Notes\n", encoding="utf-8")
                self.assertEqual(self.run_validator(script, root).returncode, 2)
                self.assertEqual(self.run_validator(script, root, "--fail-on-skip").returncode, 2)


if __name__ == "__main__":
    unittest.main()
