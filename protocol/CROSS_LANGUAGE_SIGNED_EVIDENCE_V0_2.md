# Cross-language signed synthetic evidence qualification v0.2

**Status:** offline research qualification. **Not a production identity system, universal canonical JSON implementation, independent lab endorsement, or authority grant.**

## What is genuinely new

Two different implementations, **Python using `cryptography`** and **Node.js using its standard `crypto` module**, now verify the same Ed25519 synthetic envelope in both directions. The implementations share a written restricted signing grammar and fixtures; they do **not** share cryptographic signing/verification source. Both were authored within GhostMesh Lab, so this is **cross-language implementation reproducibility, not an independent outside research-team review**.

The Node verifier supplies its own structure checks, canonical serialization, trust role checks and Ed25519 verification. Python tests generate fresh ephemeral keys in memory, pass public keys only across the process boundary and assert the Node result. Node also generates an ephemeral private key in memory and emits only a signed sample and test public key for Python verification.

## Canonicalization and interoperability scope

The signed payload is the v0.1 [synthetic signed-evidence schema](SYNTHETIC_SIGNED_EVIDENCE_V0_1.md), with all its field restrictions. Canonicalization uses the following **JCS-compatible subset**:

- JSON object properties: ASCII printable keys, sorted lexicographically by ASCII code point (equal to UTF-16 ordering within that subset).
- Strings: printable ASCII U+0020 to U+007E only. No Unicode outside that range, no control characters, no DEL, no unpaired surrogates.
- Numbers: safe JSON integers only (absolute value no greater than 2^53 - 1), excluding floats, exponents, NaN, infinity and negative zero.
- Boolean and null are allowed in the canonicalizer but not where the strict attestation field grammar forbids them.
- JSON whitespace omitted; string quoting and escaping follow the standard JSON rules used by Python `json.dumps(...sort_keys=True, separators=(',', ':'), ensure_ascii=True)` and JavaScript `JSON.stringify` on the accepted domain.
- Canonical input must **exactly equal** the serialized bytes. Duplicate fields, extra fields and noncanonical formats fail before authority-like results are returned.
- The Ed25519 signing preimage is the fixed domain `ghostmesh-lab.synthetic-attestation.v0.1` plus one zero byte plus the canonical bytes of `{"key_id":..., "payload":...}`. The key ID is itself cryptographically bound.

**Important:** This subset is compatible with the defined portions of RFC 8785 JSON Canonicalization Scheme, but it is not a complete RFC 8785 implementation or a general interchange parser. Full Unicode, ECMAScript number formatting and a third-party interoperability standard remain unresolved. Do **not** describe this as universal JCS support.

The GitHub workflow pins its Python crypto dependency and the `actions/setup-node` action SHA. Node uses the built-in `crypto` library, no npm dependencies. Public CI verifies the exact source revision through protected PR gates.

## Boundaries of verification

The verifier accepts a **synthetic trust map provided separately by its caller**, binding key ID, Ed25519 public key, issuer, role, allowed audiences, validity and active/revoked state. An untrusted actor can supply a public key to itself; therefore accepting a caller-supplied map is **not identity assurance** or a trusted root.

A valid signature establishes that matching signed bytes were produced by whoever controls that key, subject to the verifier's trust assumption. It does **not** prove:

- that the issuer is a real independently governed human or agent;
- that the observation is accurate, source-independent or complete;
- that a policy version carries legitimate legal/governance authority;
- that the claimed operation was executed or had the asserted effects;
- that replay is impossible across processes (the current store is process-local only).

In every successful synthetic test, the output keeps `source_truth_verified=false`, `independent_witness_verified=false`, `real_world_authority=NONE` and `actual_effect=UNKNOWN`.

## Tests

Run from the repository root:

```bash
python3 -m unittest tests/test_synthetic_attestation.py tests/test_cross_language_attestation.py -v
```

Python requires the pinned `cryptography` package. Node.js 22 is set up by SHA-pinned GitHub Actions. Tests exercise Python-signed/Node-verified and Node-signed/Python-verified messages, key substitution, role/audience change, revocation, expiration, noncanonical JSON, byte tampering and authentic false claims.

No long-lived private key or "official" trust root is published. Random ephemeral keys are generated solely in local process memory; a successful test record may not be reused as a live attestation.

## Next gate

An independently authored third-party verifier and full published canonical test vectors are still needed before interoperability is claimed beyond this subset. The separate [trust-root lifecycle specification](../docs/TRUST_ROOT_LIFECYCLE.md) remains a proposal and does not activate C2/C3 federation.
