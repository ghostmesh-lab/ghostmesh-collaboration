# Signed synthetic evidence, v0.1

**Research prototype. Not deployed federation authentication, key issuance, cryptographic identity certification, or permission to operate any real system.**

This document qualifies a narrow Ed25519 test verifier and its negative controls. It does **not** claim full RFC 8785 JCS compliance, production-grade replay handling, or portable trust roots.

## Why this exists

Our prior [unsigned ST-001 bundle](../bundles/st001/README.md) can detect changed public bytes relative to its own manifest, but cannot authenticate a publisher who controls both the files and manifest.

This prototype tests one additional property: **a synthetic assertion was signed by the private key corresponding to a key record that the verifier itself already trusts for a particular issuer, role, audience and time**. This is conditional on the authenticity of the verifier's trust record. A public key presented by an attacker is not automatically trustworthy.

## Payload contract

The synthetic assertion is a JSON object with exactly these fields:

| Field | Test meaning |
| --- | --- |
| `schema` | Literal `ghostmesh.synthetic-attestation/v0.1` |
| `event_type` | `synthetic.observation` or `synthetic.harness-report` only |
| `issuer`, `subject` | ASCII synthetic names, not real identity claims |
| `audience` | Exact expected fictional recipient |
| `policy_version` | Literal `synthetic-policy-v1` |
| `issued_at`, `expires_at` | Integer Unix seconds, bounded to 1 hour |
| `nonce` | Exactly 16-byte lowercase hex identifier, used once per signing key |
| `sequence` | Positive bounded integer, once per signing key |
| `claim` | Human-readable ASCII assertion, not a verified measurement |

Envelope: `{"payload":..., "signature":{"algorithm":"Ed25519","key_id":"...","value":"..."}}`, serialized as one canonical ASCII JSON byte string. The signature is unpadded URL-safe base64 of exactly 64 Ed25519 bytes.

Signing preimage is the ASCII domain separator `ghostmesh-lab.synthetic-attestation.v0.1` plus a terminal zero byte, followed by the canonical bytes of `{"key_id":"...","payload":{...}}`. Binding `key_id` in the signed bytes prevents relabeling the same key under another trust-map entry.

The canonicalization is intentionally **a restricted Python-defined ASCII JSON profile**:
- dictionaries sorted by ASCII key order, without whitespace;
- exact JSON string escaping as encoded by Python's `json.dumps(..., sort_keys=True, separators=(',', ':'), ensure_ascii=True)`;
- no Unicode, floating-point, unknown nested structures, NaN, Infinity or duplicate keys;
- narrow sizes and nesting; raw envelopes must already have exactly this byte representation.

**This is not RFC 8785.** In particular, arbitrary Unicode normalization, cross-language serialization equivalence, JSON-number portability, and a standards-level interoperability profile are not established. An actual cross-language protocol requires a ratified canonical format and independently authored language implementations.

## Verifier trust and constraints

The caller, not the payload, supplies an allowlisted key map: key ID, public key, issuer, synthetic observer/reporter role, allowed audiences, validity interval and revocation status. These entries are **test authority inside an in-memory harness only**, not real certificates or law.

The verifier checks structure, exact bytes, signature, key/issuer binding, time bounds, role, audience, policy, event type and duplicate nonce/sequence markers. It returns `CRYPTO_VERIFIED_SYNTHETIC_ONLY` while explicitly reporting:

- `source_truth_verified: false`
- `independent_witness_verified: false`
- `real_world_authority: NONE`
- `actual_effect: UNKNOWN`

The in-memory replay set is not safe across processes or crashes. A production verifier needs durable, atomic, correctly scoped replay state and independently managed trust-anchor distribution.

## Negative cases

The automated suite includes tampering, forged trust roots, revoked/expired keys, issuer/role/policy/audience substitutions, unknown events, time travel, overly broad lifetimes, replayed nonces, repeated sequences, malformed JSON, duplicate fields, noncanonical encodings, and key-alias substitution. It also demonstrates that an **authentically signed false claim** and an **authentically signed false success report** remain unverified claims.

## How to test

On a disposable checkout with Python 3.11+ and pinned `cryptography` as used in CI:

```bash
python3 -m unittest tests/test_synthetic_attestation.py -v
```

The tests generate fresh **ephemeral Ed25519 test keys in memory** and discard them. No sample signing private key is committed. Do not reuse any test trust anchor, source, or interface for production signatures.

## Cross-language subset qualification

A separate [Node.js verification implementation](../tools/verify_synthetic_attestation.mjs) and [cross-language qualification report](CROSS_LANGUAGE_SIGNED_EVIDENCE_V0_2.md) have been added. Both accept a bounded printable-ASCII/integer JSON subset with aligned encoding, not full RFC 8785/JCS. Trust-anchor acceptance remains caller supplied in synthetic tests; real identity and authorization remain out of scope.

## Explicit next gates

A real multi-party profile needs an independently agreed encoding (RFC 8785/JCS or equivalent), test vectors, external trust-root binding, key custody and rotation, durable replay ledger, independent verification implementation, identity proof, scoped consent/law, and a separate owner-controlled approval path. Formal research release remains `CANDIDATE_NOT_RELEASED`.

See [cryptographic policy](../docs/CRYPTOGRAPHIC_ASSURANCE_POLICY.md), [independent review](../docs/INDEPENDENT_REVIEW_CONTRACT.md), and [CRYPTO-001](https://github.com/ghostmesh-lab/ghostmesh-collaboration/issues/17).
