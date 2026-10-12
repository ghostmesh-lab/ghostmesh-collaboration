# Contract validation

This repository tests an **offline research interchange**, not remote agents.

Run locally with Python 3.11 or newer and the JSON Schema validator:

    python3 -m pip install jsonschema==4.23.0
    python3 tools/validate_public_research.py
    python3 tools/verify_bundle.py
    python3 -m unittest discover -s tests -p 'test_*.py'
    python3 tools/evaluate_stale_truth.py

The evaluator's output is a deterministic synthetic reference, not a claim of AI reasoning, measured truth, or independently witnessed real-world effects.

The synthetic Ed25519 suite additionally requires `cryptography==46.0.5`, pinned in GitHub CI. It generates in-memory ephemeral test keys only and checks authentic-but-false observations and reported-but-unverified effects:

    python3 -m unittest tests/test_synthetic_attestation.py -v

Cross-language tests use Node.js 22 and two distinct verifiers. Run locally:

    python3 -m unittest tests/test_cross_language_attestation.py -v
    node --test tests/test_node_attestation.mjs

The cross-language fixture creates **in-memory ephemeral keys**, exchanges only public key material and signed synthetic assertions, and does not establish identity/authority. Python and Node use a bounded printable-ASCII/integer canonical JSON subset, **not** full RFC 8785.

The validator checks:
- the machine-readable research record against the draft 2020-12 schema and date formats;
- explicit actor/sponsor identity uncertainty;
- negative cases for C3 external operations, private data, fabricated truth grades, and missing authorship;
- manifest disclaimers about live federation, endpoints and grants;
- required human and agent orientation documents;
- fixture source ancestry and the distinction between execution reports and independent effects.

**Limits:** A passing validation cannot establish factual accuracy, valid consent, cryptographic identity, real-world authority, independent witness quality, provenance custody, or a safe federation. It verifies local document/fixture structure and selected invariants only.

Changes to test expectations, consequence class, or public disclosure rules require human review. No workflow here may dispatch external agents, deploy, write to private services, or request secrets.
