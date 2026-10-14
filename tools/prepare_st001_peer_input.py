#!/usr/bin/env python3
"""Produce an answer-suppressed ST-001 peer input from the frozen public fixture.

Not a secret blind test, independent witness, truth oracle, or authority grant.
This deliberately does not alter the canonical unsigned research bundle.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "fixtures/v0.1/stale-truth.json"
EXPECTED_SOURCE_SHA256 = "ea1a9a443e3b80d7140dacd8f4869af90e6945c7546ad6cf39dbcb2b89ffbf5d"

# Explicit allowlist. If the canonical fixture acquires more answer fields,
# they remain suppressed. Only these fields are exposed to the peer.
VISIBLE_EVENT_FIELDS = frozenset({
    "id", "time", "kind", "source", "claim", "valid_at",
    "derived_from", "actor", "action", "justification_claims",
    "authority", "action_id", "decision", "rule", "reported_success",
})
EVENT_IDS = frozenset({"O1", "O2", "C1", "A1", "P1", "E1", "O3", "N1"})
NORMALIZED_KINDS = {
    "inherited_claim": "claim",
    "negative_control_observation": "observation",
}


def prepare(raw: bytes) -> bytes:
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_SOURCE_SHA256:
        raise ValueError("Frozen ST-001 source digest mismatch; no output created")
    original = json.loads(raw)
    if (original.get("case_id") != "ST-001"
            or original.get("classification") != "public-synthetic"
            or original.get("external_actions_permitted") is not False):
        raise ValueError("Unsupported or unsafe fixture")

    events = original.get("timeline")
    if not isinstance(events, list) or len(events) != len(EVENT_IDS):
        raise ValueError("Unexpected event count")
    ids = [e.get("id") for e in events if isinstance(e, dict)]
    if len(ids) != len(EVENT_IDS) or set(ids) != EVENT_IDS:
        raise ValueError("Unexpected, missing, or duplicate event IDs")

    exposed = []
    for event in events:
        item = {key: event[key] for key in sorted(VISIBLE_EVENT_FIELDS) if key in event}
        item["kind"] = NORMALIZED_KINDS.get(item.get("kind"), item.get("kind"))
        exposed.append(item)

    result = {
        "schema": "ghostmesh.st001.peer-input/v0.1",
        "case_id": "ST-001",
        "classification": "public-synthetic",
        "mode": "ANSWER_SUPPRESSED_NOT_SECRET_BLIND",
        "source_fixture_sha256": digest,
        "external_actions_permitted": False,
        "timeline": exposed,
    }
    return (json.dumps(result, indent=2, sort_keys=True, ensure_ascii=True) + "\n").encode("utf-8")


def main() -> int:
    try:
        output = prepare(SOURCE.read_bytes())
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"BLOCK: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    sys.stdout.buffer.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
