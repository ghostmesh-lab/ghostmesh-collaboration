# Contract validation

This repository tests an **offline research interchange**, not remote agents.

Run locally with Python 3.11 or newer and the JSON Schema validator:

    python3 -m pip install jsonschema==4.23.0
    python3 tools/validate_public_research.py
    python3 -m unittest discover -s tests -p 'test_*.py'
    python3 tools/evaluate_stale_truth.py

The evaluator's output is a deterministic synthetic reference, not a claim of AI reasoning, measured truth, or independently witnessed real-world effects.

The validator checks:
- the machine-readable research record against the draft 2020-12 schema and date formats;
- explicit actor/sponsor identity uncertainty;
- negative cases for C3 external operations, private data, fabricated truth grades, and missing authorship;
- manifest disclaimers about live federation, endpoints and grants;
- required human and agent orientation documents;
- fixture source ancestry and the distinction between execution reports and independent effects.

**Limits:** A passing validation cannot establish factual accuracy, valid consent, cryptographic identity, real-world authority, independent witness quality, provenance custody, or a safe federation. It verifies local document/fixture structure and selected invariants only.

Changes to test expectations, consequence class, or public disclosure rules require human review. No workflow here may dispatch external agents, deploy, write to private services, or request secrets.
