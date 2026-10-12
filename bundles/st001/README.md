# ST-001: offline verifiable research bundle

**Status: unsigned public synthetic evidence bundle. Not a cryptographically signed release, independent experimental result, real measurement, or grant of authority.**

## Run

From the repository root with Python 3.11+:

```bash
python3 tools/verify_bundle.py
python3 tools/evaluate_stale_truth.py
python3 -m unittest tests/test_bundle_integrity.py -v
```

No keys, credentials, internet access, or private services are required. [Research manifest](manifest.json) names the exact published input, evaluator, reference result and preregistration, with SHA-256 hashes and lengths. Verification reads only those four allowlisted paths and rejects symlinks, traversal, role swaps, invalid digests, and misleading signature/authority fields.

The bundle **does not** include an externally trusted signing key, detached attestation, transparent timestamp, or independent witness. Its matching hash result only demonstrates internal byte consistency. Verify the expected source commit through independently trusted Git/GitHub evidence if origin matters, and do not treat multiple copies of one source as corroboration.

## Why cryptography is here

- It freezes a reproducible baseline: changing a single input byte produces a digest mismatch.
- It prevents an accidental report from silently drifting away from the exact evaluator and synthetic fixture.
- It gives another lab a precise object to critique without requiring GhostMesh accounts or private operational data.

## What cryptography cannot do

A valid hash does not establish truthful source content. A signer can authenticate their own incorrect statement. A cryptographic permit without applicable governance is not an action grant. A post-execution receipt is not a health measurement. If a source is missing or a result is beyond available observation coverage, record **UNKNOWN**.

For design policy, see [cryptographic assurance](../../docs/CRYPTOGRAPHIC_ASSURANCE_POLICY.md), [licensing proposal](../../docs/LICENSE_RATIFICATION_PROPOSAL.md), and [independent review](../../docs/INDEPENDENT_REVIEW_CONTRACT.md).

## Independent reproduction invitation

Reproduce the bundle on an independently operated environment, record the exact commit, manifest digest, verifier implementation, observed output, exceptions, and any false-positive/negative behavior. Independently running the same code is a useful cross-environment check, **not** an independent reimplementation or independent judgment about system truth.

No human or AI receives repository write, network, infrastructure or production authority from passing this test.
