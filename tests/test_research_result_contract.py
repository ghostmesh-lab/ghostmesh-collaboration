#!/usr/bin/env python3
"""Adversarial schema tests for research-result claims of independent evaluation."""
import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas/research-result.v0.1.schema.json").read_text())
TEMPLATE = json.loads((ROOT / "examples/research-result-template.v0.1.json").read_text())


class ResearchResultContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Draft202012Validator.check_schema(SCHEMA)
        cls.validator = Draft202012Validator(SCHEMA, format_checker=FormatChecker())

    def assert_invalid(self, case):
        self.assertFalse(self.validator.is_valid(case))

    def test_template_valid_but_not_an_experiment(self):
        self.assertTrue(self.validator.is_valid(TEMPLATE))
        self.assertEqual(TEMPLATE["status"], "EXAMPLE_NOT_RUN")
        self.assertEqual(TEMPLATE["human_review"], "PENDING")
        self.assertIsNone(TEMPLATE["started_at"])
        self.assertTrue(all(x["verdict"] == "NOT_EVALUATED" for x in TEMPLATE["claims"]))

    def test_cannot_promote_template_to_independent_evidence(self):
        case = copy.deepcopy(TEMPLATE)
        case["status"] = "INDEPENDENTLY_REPRODUCED"
        self.assert_invalid(case)

    def test_not_run_cannot_claim_supported_results(self):
        case = copy.deepcopy(TEMPLATE)
        case["claims"][0]["verdict"] = "SUPPORTED"
        self.assert_invalid(case)

    def test_no_external_authority(self):
        case = copy.deepcopy(TEMPLATE)
        case["external_authority"] = "LIVE_GRANT"
        self.assert_invalid(case)

    def test_no_private_data(self):
        case = copy.deepcopy(TEMPLATE)
        case["privacy"] = "PRIVATE_DATA"
        self.assert_invalid(case)

    def test_independent_status_requires_scope_metadata(self):
        case = copy.deepcopy(TEMPLATE)
        case["status"] = "INDEPENDENTLY_REPRODUCED"
        case["started_at"] = "2026-10-11T22:00:00Z"
        case["claims"][0]["verdict"] = "SUPPORTED"
        case["claims"][1]["verdict"] = "UNKNOWN"
        self.assert_invalid(case)
        case["human_review"] = "REVIEWED"
        case["evidence"] = ["public independently reproduced method and output"]
        self.assert_invalid(case)
        case["method"]["independent_from_fixture_author"] = True
        self.assertTrue(self.validator.is_valid(case))
        # A valid record can still contain a false claim. Schema is not an attestator.

    def test_reject_unexpected_actor_field(self):
        case = copy.deepcopy(TEMPLATE)
        case["participant"]["credential"] = "no real credential"
        self.assert_invalid(case)


if __name__ == "__main__":
    unittest.main()
