#!/usr/bin/env python3
"""Negative controls for the offline publication-readiness gate."""
from __future__ import annotations
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("publication_gate", ROOT / "tools/check_publication.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class PublicationReadinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = json.loads((ROOT / "publication-readiness.json").read_text(encoding="utf-8"))

    def test_open_gates_are_not_marked_as_release(self):
        self.assertEqual(gate.check_readiness(self.package), [])

    def test_false_release_claim_rejected(self):
        wrong = copy.deepcopy(self.package)
        wrong["status"] = "CERTIFIED_AND_RELEASED"
        self.assertTrue(gate.check_readiness(wrong))

    def test_unsupported_signature_claim_rejected(self):
        wrong = copy.deepcopy(self.package)
        wrong["release_gates"]["cryptographic_artifact_integrity"] = "SIGNED_VERIFIED"
        self.assertTrue(gate.check_readiness(wrong))

    def test_cross_language_qualification_cannot_claim_production(self):
        wrong = copy.deepcopy(self.package)
        wrong["release_gates"]["cross_language_signature_interchange"] = "PRODUCTION_TRUST_COMMISSIONED"
        self.assertTrue(gate.check_readiness(wrong))

    def test_federation_grant_rejected(self):
        wrong = copy.deepcopy(self.package)
        wrong["live_federation"] = True
        self.assertTrue(gate.check_readiness(wrong))
        wrong["live_federation"] = False
        wrong["agent_authority_granted"] = True
        self.assertTrue(gate.check_readiness(wrong))

    def test_empty_unresolved_issues_not_accepted(self):
        wrong = copy.deepcopy(self.package)
        wrong["unresolved"] = []
        self.assertTrue(gate.check_readiness(wrong))

    def test_missing_approval_gate_detected(self):
        wrong = copy.deepcopy(self.package)
        del wrong["release_gates"]["owner_disclosure_review"]
        self.assertTrue(gate.check_readiness(wrong))

    def test_relative_link_and_escape(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "docs").mkdir()
            (root / "docs" / "x.md").write_text("ok")
            source = root / "README.md"
            source.write_text("text")
            self.assertIsNone(gate.check_link(source, "docs/x.md", root))
            self.assertEqual(gate.check_link(source, "../../sensitive.txt", root), "path escapes repository")
            self.assertEqual(gate.check_link(source, "/etc/passwd", root), "absolute local path")
            self.assertEqual(gate.check_link(source, "docs/missing.md", root), "broken relative link")
            self.assertEqual(gate.check_link(source, "file:///etc/passwd", root), "unexpected link scheme")
            self.assertIsNone(gate.check_link(source, "https://github.com/example/repo", root))

    def test_symlink_reference_blocked(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / "target.md"
            target.write_text("ok")
            alias = root / "alias.md"
            alias.symlink_to(target)
            source = root / "README.md"
            source.write_text("text")
            # Explicit links to links should not silently cross trust boundaries.
            self.assertEqual(gate.check_link(source, "alias.md", root), "symlink target prohibited")


if __name__ == "__main__":
    unittest.main()
