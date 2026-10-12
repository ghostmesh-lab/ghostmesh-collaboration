#!/usr/bin/env python3
"""Static invariants for deliberately separated OFFLINE Node test drivers."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class NodeTestDriverIsolation(unittest.TestCase):
    def setUp(self):
        self.verify = (ROOT / "tests/attestation_node_verify_driver.mjs").read_text()
        self.issue = (ROOT / "tests/attestation_node_issue_driver.mjs").read_text()

    def test_verification_driver_cannot_issue_or_generate_signing_keys(self):
        self.assertIn("verifySynthetic(", self.verify)
        self.assertNotIn("generateKeyPairSync", self.verify)
        self.assertNotIn("sign(null", self.verify)
        self.assertNotIn("request.operation", self.verify)

    def test_ephemeral_issue_driver_cannot_verify_or_grant_authority(self):
        self.assertIn("generateKeyPairSync", self.issue)
        self.assertNotIn("verifySynthetic(", self.issue)
        self.assertNotIn("request.operation", self.issue)
        self.assertNotIn("production_grant", self.issue)

    def test_multipurpose_driver_not_present(self):
        self.assertFalse((ROOT / "tests/attestation_node_driver.mjs").exists())


if __name__ == "__main__":
    unittest.main()
