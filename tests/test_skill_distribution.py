"""Verify each source skill's concrete Markdown pointers survive standalone copying."""

import re
import shutil
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]


def missing_references(skill):
    missing = []
    for document in [skill / "SKILL.md", *sorted((skill / "references").glob("*.md"))]:
        text = re.sub(r"```.*?```", "", document.read_text(encoding="utf-8"), flags=re.DOTALL)
        for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", text):
            url = urlsplit(target)
            if url.scheme or url.netloc or not url.path or "<" in url.path:
                continue
            path = (document.parent / unquote(url.path)).resolve()
            if not path.is_relative_to(skill.resolve()) or not path.exists():
                missing.append((str(document.relative_to(skill)), target))
    return missing


class SkillDistributionTests(unittest.TestCase):
    def test_standalone_skill_references(self):
        for skill in sorted((ROOT / "skills").iterdir()):
            if not (skill / "SKILL.md").is_file():
                continue
            with self.subTest(skill=skill.name), tempfile.TemporaryDirectory() as directory:
                installed = Path(directory) / skill.name
                shutil.copytree(skill, installed)
                self.assertEqual(missing_references(installed), [])

    def test_missing_and_sibling_only_references_are_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "standalone"
            skill.mkdir()
            (skill / "SKILL.md").write_text(
                "[local](references/missing.md)\n[sibling](../other/SKILL.md)\n",
                encoding="utf-8",
            )
            other = skill.parent / "other"
            other.mkdir()
            (other / "SKILL.md").write_text("# Other\n", encoding="utf-8")
            self.assertEqual(len(missing_references(skill)), 2)


if __name__ == "__main__":
    unittest.main()
