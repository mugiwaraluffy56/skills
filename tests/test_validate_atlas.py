"""Regression coverage for the installed skill's stdlib-only validator."""
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
SCRIPT = Path(__file__).resolve().parents[1] / "skills/oss-reuse-atlas/scripts/validate_atlas.py"
SPEC = importlib.util.spec_from_file_location("validate_atlas", SCRIPT)
atlas = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(atlas)
PIN = "a" * 40


class AtlasTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="atlas-regression-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "atlas"
        (self.root / "dossiers").mkdir(parents=True)
        for name in ("README.md", "capability-map.md", "research-gaps.md"):
            (self.root / name).write_text("Research", encoding="utf-8")
        self.repo = {
            "id": "owner/repo", "url": "https://github.com/owner/repo",
            "group": "direct", "evidence_level": "D2", "license": "MIT",
            "pinned_commit": PIN, "dossier": "dossiers/owner--repo.md",
        }
        self.decision = {
            "repository_id": "owner/repo", "decision": "copy_or_adapt",
            "status": "selected", "pinned_commit": PIN, "why": "Source-backed fit",
            "upstream_files": ["src/main.py"], "upstream_tests": ["tests/test_main.py"],
            "not_proven": ["Target integration"],
            "possible_equivalence_checks": ["Compare the actual behavior"],
        }
        self.dossier = "\n".join(
            f"https://github.com/owner/repo/blob/{PIN}/{path}"
            for path in ("src/main.py", "tests/test_main.py")
        )
        self.counts = {
            "discovered": 1, "metadata_verified_or_more": 1,
            "code_inspected_or_more": 1, "reproduced": 0,
            "selected": 1, "deferred": 0, "rejected": 0,
        }

    def write(self):
        for name, data in (
            ("repositories.json", {"repositories": [self.repo]}),
            ("reuse-decisions.json", {"decisions": [self.decision]}),
            ("progress.json", {"counts": self.counts}),
        ):
            (self.root / name).write_text(json.dumps(data), encoding="utf-8")
        (self.root / "dossiers/owner--repo.md").write_text(self.dossier, encoding="utf-8")

    def errors(self):
        self.write()
        return atlas.check(self.root)[0]

    def test_accepts_pinned_source_and_test_references(self):
        self.assertEqual(self.errors(), [])

    def test_rejects_dossier_traversal(self):
        (self.root.parent / "outside.md").write_text(self.dossier, encoding="utf-8")
        self.repo["dossier"] = "dossiers/../../outside.md"
        self.assertTrue(self.errors())

    def test_rejects_symlinked_dossier(self):
        outside = self.root.parent / "outside.md"
        outside.write_text(self.dossier, encoding="utf-8")
        try:
            (self.root / "dossiers/link.md").symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest("This system does not permit creating symlinks")
        self.repo["dossier"] = "dossiers/link.md"
        self.assertTrue(self.errors())

    def test_rejects_unpinned_empty_or_mismatched_dossiers(self):
        for dossier in ("", "Source was inspected.", self.dossier.replace(PIN, "main"),
                        self.dossier.replace(PIN, "b" * 40),
                        self.dossier.replace("owner/repo", "other/repo")):
            with self.subTest(dossier=dossier):
                self.dossier = dossier
                self.assertTrue(self.errors())

    def test_requires_citations_for_every_selected_file_and_test(self):
        self.dossier = f"https://github.com/owner/repo/blob/{PIN}/src/main.py"
        self.assertTrue(self.errors())

    def test_rejects_unknown_or_empty_copy_licenses(self):
        for license_name in ("", "   ", "UNKNOWN", " unknown ", "none", "No License", "UNLICENSED", [], True):
            with self.subTest(license=license_name):
                self.repo["license"] = license_name
                self.assertTrue(self.errors())

    def test_unknown_license_can_be_deferred(self):
        self.repo.update(license="unknown", evidence_level="D1", pinned_commit=None, dossier=None)
        self.decision = {"repository_id": "owner/repo", "decision": "defer", "status": "deferred"}
        self.counts.update(code_inspected_or_more=0, selected=0, deferred=1)
        self.assertEqual(self.errors(), [])

    def test_rejects_invalid_file_list_types_and_paths(self):
        for value in (True, "src/main.py", [], [True], [""], ["../outside.py"],
                      ["/absolute.py"], ["C:\\outside.py"], ["https://example.com/file"]):
            with self.subTest(value=value):
                self.decision["upstream_files"] = value
                self.assertTrue(self.errors())

    def test_rejects_malformed_fields_without_crashing(self):
        for target, field in (("repo", "group"), ("repo", "evidence_level"),
                              ("repo", "license"), ("decision", "decision"),
                              ("decision", "status"), ("decision", "why"),
                              ("decision", "not_proven"), ("decision", "possible_equivalence_checks")):
            for value in ([], {}, True, None):
                with self.subTest(target=target, field=field, value=value):
                    repo, decision = copy.deepcopy(self.repo), copy.deepcopy(self.decision)
                    try:
                        getattr(self, target)[field] = value
                        self.assertTrue(self.errors())
                    finally:
                        self.repo, self.decision = repo, decision

    def test_rejects_false_count_even_when_equal_to_zero(self):
        self.counts["reproduced"] = False
        self.assertTrue(self.errors())

    def test_malformed_json_cli_has_no_traceback(self):
        self.write()
        (self.root / "repositories.json").write_text("{", encoding="utf-8")
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("INVALID:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_limits_file_size_and_json_depth(self):
        self.write()
        oversized = self.root / "oversized.json"
        oversized.write_text(" " * (atlas.MAX_FILE_BYTES + 1), encoding="utf-8")
        with self.assertRaises(ValueError):
            atlas.load(oversized)
        deep = self.root / "deep.json"
        deep.write_text("[" * 2000 + "0" + "]" * 2000, encoding="utf-8")
        with self.assertRaises(ValueError):
            atlas.load(deep)


if __name__ == "__main__":
    unittest.main()
