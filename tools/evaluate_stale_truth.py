#!/usr/bin/env python3
"""Deterministic ST-001 reference interpretation. Synthetic/offline ONLY.

This tool is deliberately NOT an AI judge, real-world verifier, policy engine,
identity witness, or authorization service.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures/v0.1/stale-truth.json"


def assess(fixture: dict) -> dict:
    if fixture.get("case_id") != "ST-001" or fixture.get("classification") != "public-synthetic":
        raise ValueError("Unsupported case or unsafe input classification")
    if fixture.get("external_actions_permitted") is not False:
        raise ValueError("Synthetic reference case must prohibit external action")
    events = fixture.get("timeline", [])
    index = {e.get("id"): e for e in events}
    if len(index) != len(events) or any(k not in index for k in ("O1", "O2", "C1", "A1", "P1", "E1", "O3", "N1")):
        raise ValueError("Missing or duplicate fixture event")

    o1, o2, claim, request, permit, execution, o3, negative = (index[k] for k in
        ("O1", "O2", "C1", "A1", "P1", "E1", "O3", "N1"))

    for x in (o1, o2, o3):
        if x.get("kind") != "observation" or x.get("truth_at_time") is not True:
            raise ValueError("Expected synthetic observations not established")
    if any(not x.get("valid_at") for x in (o1, o2, o3)):
        raise ValueError("Temporal evidence incomplete")

    ancestor = claim.get("derived_from", [])
    if not isinstance(ancestor, list) or "O1" not in ancestor:
        raise ValueError("Inherited claim ancestry missing")
    if claim.get("new_independent_observation") is not False:
        raise ValueError("Reference case must not count inherited claim as independent")
    if not o1["valid_at"] < o2["valid_at"] < o3["valid_at"]:
        raise ValueError("Synthetic temporal order invalid")
    if permit.get("action_id") != request.get("id") or execution.get("action_id") != request.get("id"):
        raise ValueError("Action correlation mismatch")
    if permit.get("is_a_live_grant") is not False:
        raise ValueError("Policy decision must not be a live grant")

    contradiction = ("unavailable" in claim.get("claim", "").lower()
                     and "healthy" in o2.get("claim", "").lower())
    result = {
        "case_id": "ST-001",
        "fixture_classification": "PUBLIC_SYNTHETIC_ONLY",
        "reference_evaluator": "deterministic fixture-specific demonstration, not agent evaluation",
        "historical_outage": {
            "assertion": o1["claim"], "valid_at": o1["valid_at"],
            "scope": "synthetic observed-at-time only"
        },
        "later_observation": {
            "assertion": o2["claim"], "valid_at": o2["valid_at"],
            "source_independence": "UNKNOWN: different source names are not verification of independence"
        },
        "stale_claim": {
            "id": claim["id"],
            "inherits_source": ancestor,
            "new_independent_observation": False,
            "contradicted_by_later_observation": contradiction
        },
        "authority": {
            "decision": permit.get("decision", "UNKNOWN"),
            "rule": permit.get("rule", "UNKNOWN"),
            "real_world_permission": "NONE"
        },
        "execution": {
            "tool_reported_success": execution.get("reported_success"),
            "independent_execution_verification": False,
            "actual_effect": "UNKNOWN: a separate measurement is not a causal trace"
        },
        "later_observed_state": {"assertion": o3["claim"], "valid_at": o3["valid_at"]},
        "decision_causality": "UNKNOWN: justification reference and chronology do not prove cause",
        "remediation_authority": "NOT_GRANTED",
        "negative_control": {
            "id": negative["id"],
            "result": "OLD_DOES_NOT_IMPLY_INVALID",
            "claimed_truth_at_time": negative.get("truth_at_time"),
            "current_applicability": "UNKNOWN pending local policy and temporal check"
        },
        "limits": [
            "All inputs are fictional and manually declared.",
            "Event fields are not independent corroboration.",
            "No real external system, agent, credential or policy has been tested."
        ]
    }
    return result


def main() -> None:
    raw = FIXTURE.read_bytes()
    fixture = json.loads(raw)
    result = assess(fixture)
    result["fixture_sha256"] = hashlib.sha256(raw).hexdigest()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
