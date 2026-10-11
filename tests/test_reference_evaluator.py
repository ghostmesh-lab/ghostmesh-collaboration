#!/usr/bin/env python3
"""Self-contained negative tests for a purely synthetic reference evaluator."""
import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from evaluate_stale_truth import assess


class StaleTruthReference(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads((ROOT / "fixtures/v0.1/stale-truth.json").read_text())

    def test_expected_separation(self):
        result = assess(self.fixture)
        self.assertEqual(result["decision_causality"].split(":")[0], "UNKNOWN")
        self.assertEqual(result["execution"]["actual_effect"].split(":")[0], "UNKNOWN")
        self.assertEqual(result["authority"]["real_world_permission"], "NONE")
        self.assertEqual(result["remediation_authority"], "NOT_GRANTED")
        self.assertTrue(result["stale_claim"]["contradicted_by_later_observation"])
        self.assertEqual(result["negative_control"]["result"], "OLD_DOES_NOT_IMPLY_INVALID")

    def test_checked_in_reference_reproducible(self):
        """A changed fixture or evaluator cannot silently alter the published baseline."""
        raw = (ROOT / "fixtures/v0.1/stale-truth.json").read_bytes()
        expected = json.loads((ROOT / "examples/stale-truth-reference-output.json").read_text())
        actual = assess(json.loads(raw))
        actual["fixture_sha256"] = hashlib.sha256(raw).hexdigest()
        self.assertEqual(actual, expected)

    def test_later_observation_changes_verdict(self):
        altered = copy.deepcopy(self.fixture)
        for event in altered["timeline"]:
            if event["id"] == "O2":
                event["claim"] = "service unavailable"
        self.assertFalse(assess(altered)["stale_claim"]["contradicted_by_later_observation"])

    def test_duplicate_event_fails(self):
        altered = copy.deepcopy(self.fixture)
        altered["timeline"].append(copy.deepcopy(altered["timeline"][0]))
        with self.assertRaises(ValueError):
            assess(altered)

    def test_fake_live_authority_fails(self):
        altered = copy.deepcopy(self.fixture)
        for event in altered["timeline"]:
            if event["id"] == "P1":
                event["is_a_live_grant"] = True
        with self.assertRaises(ValueError):
            assess(altered)

    def test_fake_new_corroboration_fails(self):
        altered = copy.deepcopy(self.fixture)
        for event in altered["timeline"]:
            if event["id"] == "C1":
                event["new_independent_observation"] = True
        with self.assertRaises(ValueError):
            assess(altered)

    def test_mismatched_action_fails(self):
        altered = copy.deepcopy(self.fixture)
        for event in altered["timeline"]:
            if event["id"] == "E1":
                event["action_id"] = "OTHER"
        with self.assertRaises(ValueError):
            assess(altered)

    def test_non_synthetic_refused(self):
        altered = copy.deepcopy(self.fixture)
        altered["classification"] = "production"
        with self.assertRaises(ValueError):
            assess(altered)

    def test_external_action_not_allowed(self):
        altered = copy.deepcopy(self.fixture)
        altered["external_actions_permitted"] = True
        with self.assertRaises(ValueError):
            assess(altered)


if __name__ == "__main__":
    unittest.main()
