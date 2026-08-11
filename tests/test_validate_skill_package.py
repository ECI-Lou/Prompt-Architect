from __future__ import annotations

import hashlib
import importlib.util
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


VALIDATOR = load_module(
    "validate_skill_package", "scripts/validate_skill_package.py"
)
PACKAGER = load_module("package_skill", "scripts/package_skill.py")


class SkillPackageTests(unittest.TestCase):
    def test_repository_contract_passes(self):
        self.assertEqual(
            VALIDATOR.validate_repository(ROOT, check_git=False),
            [],
        )

    def test_local_and_binary_paths_are_forbidden(self):
        forbidden = (
            "projects/client/source.docx",
            ".codex/analysis.json",
            "scripts/__pycache__/validator.pyc",
            "local/reference.pdf",
            "node_modules/package/index.js",
        )
        for path in forbidden:
            with self.subTest(path=path):
                self.assertTrue(VALIDATOR.is_forbidden_path(path))
        self.assertFalse(VALIDATOR.is_forbidden_path("references/template.md"))

    def test_release_archive_is_clean_and_reproducible(self):
        with tempfile.TemporaryDirectory() as temp_directory:
            temp = Path(temp_directory)
            first = PACKAGER.build_archive(ROOT, temp / "first.skill")
            second = PACKAGER.build_archive(ROOT, temp / "second.skill")
            self.assertEqual(
                hashlib.sha256(first.read_bytes()).digest(),
                hashlib.sha256(second.read_bytes()).digest(),
            )
            self.assertEqual(VALIDATOR.validate_archive(first), [])
            with zipfile.ZipFile(first) as archive:
                names = archive.namelist()
            self.assertIn("prompt-architect/SKILL.md", names)
            self.assertNotIn("prompt-architect/tests/test_validate_skill_package.py", names)
            self.assertFalse(any("projects/" in name for name in names))


if __name__ == "__main__":
    unittest.main()
