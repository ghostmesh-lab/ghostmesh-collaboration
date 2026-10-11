#!/usr/bin/env python3
"""Validate the public, offline research package. No network or execution."""
import copy
import hashlib
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]

def load(name):
    with (ROOT / name).open(encoding="utf-8") as stream:
        return json.load(stream)

def check(ok, message):
    if not ok:
        raise AssertionError(message)

def main():
    for path in [
        "START_HERE.md", "AGENTS.md", "docs/NORTH_STAR.md",
        "architecture/GHOSTMESH_SYSTEM_MAP.md",
        "architecture/MATURITY_REGISTER.md", "GOVERNANCE.md",
        "SECURITY.md", "CONTRIBUTING.md",
        "protocol/INTERACTION_CONTRACT_V0_2.md",
    ]:
        check((ROOT / path).is_file(), "Missing: " + path)

    schema = load("schemas/research-envelope.v0.2.schema.json")
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    example = load("examples/research-proposal.v0.2.json")
    check(validator.is_valid(example), "Example fails schema")
    check(example["review"]["human_review_status"] == "PENDING", "False approval")
    check(example["actor"]["identity_assurance"] == "SELF_DECLARED", "False identity")
    for field, value in [
        ("consequence_class", "C3"),
        ("classification", "PRIVATE"),
        ("status", "VERIFIED_TRUE"),
    ]:
        bad = copy.deepcopy(example)
        bad[field] = value
        check(not validator.is_valid(bad), "Invalid record accepted: " + field)
    bad = copy.deepcopy(example)
    del bad["actor"]
    check(not validator.is_valid(bad), "Missing actor accepted")

    result_schema = load("schemas/research-result.v0.1.schema.json")
    Draft202012Validator.check_schema(result_schema)
    result_validator = Draft202012Validator(result_schema, format_checker=FormatChecker())
    template = load("examples/research-result-template.v0.1.json")
    check(result_validator.is_valid(template), "Research result template fails schema")
    check(template["status"] == "EXAMPLE_NOT_RUN" and template["human_review"] == "PENDING",
          "Unexecuted example cannot claim a verified result")
    check(len({c["claim_id"] for c in template["claims"]}) == len(template["claims"]),
          "Duplicate claim identifiers")
    fixture_bytes = (ROOT / "fixtures/v0.1/stale-truth.json").read_bytes()
    check(template["fixture_sha256"] == hashlib.sha256(fixture_bytes).hexdigest(),
          "Result template fixture digest does not match the actual published input")

    manifest = load("federation.manifest.json")
    check(manifest["live_federation"] is False, "Cannot advertise live federation")
    check(manifest["enrollment_endpoint"] is None, "Cannot advertise enrollment")
    check(manifest["execution_endpoint"] is None, "Cannot advertise execution")
    check(manifest["authority_grants"] == [], "No grants may be issued here")
    check(manifest["consequence_classes"] == ["C0", "C1"], "Scope widened")
    for path in manifest["links"].values():
        check((ROOT / path).is_file(), "Broken manifest link: " + path)
    check((ROOT / manifest["reference_evaluator"]).is_file(), "Missing offline evaluator")
    check(manifest["reference_evaluator_maturity"] == "DETERMINISTIC_SYNTHETIC_ONLY",
          "Reference evaluator must not claim operational maturity")

    fixture = load("fixtures/v0.1/stale-truth.json")
    check(fixture["classification"] == "public-synthetic", "Non-synthetic fixture")
    check(fixture["external_actions_permitted"] is False, "External actions not allowed")
    events = {event["id"]: event for event in fixture["timeline"]}
    check(len(events) == len(fixture["timeline"]), "Duplicate event IDs")
    check({"O1", "O2", "C1", "P1", "E1", "O3", "N1"} <= events.keys(), "Incomplete fixture")
    check(events["C1"]["new_independent_observation"] is False, "Inherited source counted twice")
    check("O1" in events["C1"]["derived_from"], "Missing lineage")
    check(events["E1"]["independently_verified"] is False, "Self-reported completion promoted")
    print("PASS: agent docs, schema, example, negatives, manifest and synthetic fixture")

if __name__ == "__main__":
    main()
