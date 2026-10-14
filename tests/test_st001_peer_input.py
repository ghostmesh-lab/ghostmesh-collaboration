"""Tests for the pinned synthetic ST-001 answer-suppressed peer view."""
import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from prepare_st001_peer_input import (  # noqa: E402
    EXPECTED_SOURCE_SHA256, SOURCE, prepare,
)


class PeerInputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source_bytes = SOURCE.read_bytes()
        cls.output_bytes = prepare(cls.source_bytes)
        cls.output = json.loads(cls.output_bytes)
        cls.events = {e["id"]: e for e in cls.output["timeline"]}

    def test_pinned_fixture_unchanged(self):
        self.assertEqual(hashlib.sha256(self.source_bytes).hexdigest(),
                         EXPECTED_SOURCE_SHA256)
        self.assertEqual(self.output["source_fixture_sha256"], EXPECTED_SOURCE_SHA256)

    def test_deterministic_render(self):
        self.assertEqual(self.output_bytes, prepare(self.source_bytes))

    def test_answer_fields_not_exposed(self):
        banned = {"evaluation_expectations", "truth_at_time", "confidence",
                  "new_independent_observation", "independently_verified",
                  "is_a_live_grant"}
        self.assertTrue(banned.isdisjoint(self.output))
        for event in self.output["timeline"]:
            self.assertTrue(banned.isdisjoint(event))

    def test_preserves_evidence_and_hides_shortcut_labels(self):
        self.assertEqual(self.events["C1"]["derived_from"], ["O1"])
        self.assertEqual(self.events["C1"]["kind"], "claim")
        self.assertEqual(self.events["N1"]["kind"], "observation")
        self.assertEqual(self.events["P1"]["decision"], "allow")
        self.assertTrue(self.events["E1"]["reported_success"])
        self.assertEqual(len(self.events), 8)

    def test_fail_closed_on_source_mutation(self):
        with self.assertRaisesRegex(ValueError, "digest mismatch"):
            prepare(self.source_bytes + b" ")

    def test_no_external_authority(self):
        self.assertIs(self.output["external_actions_permitted"], False)
        self.assertEqual(self.output["classification"], "public-synthetic")


if __name__ == "__main__":
    unittest.main()
