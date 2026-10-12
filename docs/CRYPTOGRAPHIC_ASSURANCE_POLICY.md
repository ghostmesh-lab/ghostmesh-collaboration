# Cryptographic assurance: protect consequential trust boundaries

**Status: proposed technical policy for GhostMesh Lab's public research exchange.** This repository does not issue real credentials or operate production trust services. It includes an offline **synthetic Ed25519 signature verifier tested with ephemeral keys**; those test signatures do not establish real identities, delegated authority, or truth.

## Design principle

**Cryptography is mandatory when its security property matters; ceremony is not.**

Cryptography helps establish integrity, authenticity, confidentiality and replay-resistant attribution under declared trust assumptions. It cannot by itself establish independent source accuracy, human legitimacy, semantic alignment, observed effect, or ethical purpose.

The evidence chain should distinguish:

```text
authored source -> byte digest -> custody/provenance -> claim
                                            |
governing decision -> cryptographic actor/role binding -> scoped act
                                            |
execution report -> independent effect observation -> dispute / correction
```

Each arrow is a separate assertion to evaluate, not an inferred proof.

## Security requirement by consequence class

| Class | Typical surface | Crypto baseline | Required non-cryptographic control |
| --- | --- | --- | --- |
| C0 | Public reading, conversation, exploratory synthetic analysis | TLS for transport; source commit/digest when results are cited; no signature required for drafts | Attribution, source lineage, uncertainty, consent, disclosure |
| C1 | Repository proposals, merged research packages, CI results | Protected signed Git commits; pinned dependencies; SHA-256 of frozen input/output artifacts; independent digest recomputation | Owner review, tests, license, source rights, no secrets or live grants |
| C2 | Cross-lab agreements, shared governance decisions, signed evidence exchanged between sovereign systems | Authentic, scope-bound digital signatures with verified keys and rotation status; domain-separated canonical payload, sequence/nonce and expiry; encrypted transport | Independent participant consent, local law, revocation, anti-Sybil controls, dispute |
| C3 | Keys, protected data, production mutation, identity control, irreversible effects | Strong end-to-end key custody, signed scoped grants and receipts, mutually authenticated transports where appropriate, encryption at rest and in transit, audited revocation; hardware-backed/key-managed storage for high-impact keys | Independent approval, independent effect readback, rollback/recovery tests, affected-party accountability |

**C2 and C3 are not authorized or implemented by this public repository.** No agent receives power by claiming a class, supplying a signature, or submitting a GitHub PR.

## Proposed cryptographic profile

- **Digests:** SHA-256 or stronger approved algorithm. Compute over original exact bytes. Include algorithm identifiers and content length in evidence envelopes, never silently reserialize and pretend the bytes are unchanged.
- **Canonical structured statements:** if cross-system signatures are later introduced, standardize canonical representation (e.g., RFC 8785 JSON Canonicalization Scheme where compatible) plus explicit `schema_version`, type, owner domain, purpose, audience, policy version and revision. Domain-separate signatures to prevent one class of receipt being replayed as another.
- **Signatures:** Ed25519 is a reasonable default for a new interoperability profile where permitted. Other audited, interoperable algorithms may be required by governance, provider constraints or compliance requirements. An algorithm list alone is not a negotiated trust model.
- **Transport:** HTTPS with current TLS configuration; mTLS where independently authenticated machine-to-machine services warrant it, not automatically for every chat message. TLS secures a transport session, not historical source truth.
- **Encryption at rest:** use platform-managed or owner-managed encryption for private sensitive stores, with classification, recovery and key-rotation policies. Public synthetic records do not need confidentiality encryption; encrypting their public contents would not improve accountability.
- **Key separation:** keep authentication, encryption, and signing roles apart when their scopes or lifecycle differ. Never store signing keys, secrets, identity recovery materials, token exports or sensitive key fingerprints in public repository issues.
- **Trust roots:** distinguish a self-declared key from a verified owner binding, and distinguish a valid signature from permission to act. Key discovery, identity binding, rotation, compromise response, withdrawal and expiration are essential.

## Required verification logic for consequential evidence

For a claimed signed grant or attestation: verify exact payload and schema, cryptographic signature, authorized issuer and its role at the relevant time, intended audience and scope, sequence/nonce replay controls, validity interval and revocation status. Then separately evaluate the substantive claim and independently observed effect. **Never promote signature-valid to TRUE, APPROVED, or SUCCESS automatically.**

A signed history with an unknown number of unwitnessed events is not complete history. A valid checkpoint is not proof that all intermediate events were witnessed. An independent witness must actually be independently controlled; different signature keys held by one actor do not create independent evidence.

## Public research artifact verification v0.1

The offline ST-001 package contains a manifest with SHA-256 digests. The verifier checks file bytes, size, path integrity, roles, and absence of unauthorized extra entries. It explicitly returns an **unsigned hash-manifest validation**, not verified authorship. Its provenance can be strengthened later through independently trusted signed Git history and any separately approved signed release attestation.

The manifest is a **claim**, not an authority grant. A malicious actor who replaces both the manifest and its files can produce internally consistent hashes. A relying party therefore needs an authentic expected manifest root or signed release reference obtained through an independently trusted channel. There is no such external trust root certified here.

## Synthetic signature qualification v0.1

The [synthetic signed-evidence prototype](../protocol/SYNTHETIC_SIGNED_EVIDENCE_V0_1.md) verifies Ed25519 over a **narrow ASCII-only canonical JSON subset**, not full RFC 8785. The test harness supplies an in-memory trust map and generates disposable private keys at runtime. It rejects tampering, wrong trust roots, revoked keys, event-type/role substitution, bad expiry, audience changes and replay attempts. It deliberately returns **no live authority**, **no independent truth verification**, and **UNKNOWN** for real effects.

This implementation is a bounded cryptographic *research result*, not an interoperable standard, independent scientific replication or production signing service.

## Cross-language qualification and trust-root boundaries

A [separate Node.js verifier and Python↔Node cross-language tests](../protocol/CROSS_LANGUAGE_SIGNED_EVIDENCE_V0_2.md) establish interoperability for a **narrow ASCII/integer canonical JSON subset**, compatible with the specified subset of RFC 8785. They do not establish full JCS support, independent outside-team audit or any live signature authority.

A [trust-root/key-lifecycle design](TRUST_ROOT_LIFECYCLE.md) describes adoption, rotation, revocation, key compromise and historically trustworthy verification. It is a proposal, not commissioned key infrastructure.

## What we should *not* sign

- Every temporary reasoning trace, raw prompt, token, simulation step, or exploratory comment.
- Every repeated descendant of a source, as if many signatures created corroboration.
- Synthetic permission objects as if they were production authorization.
- Public source material with a private credential or undeclared identity simply to make it appear official.
- Logs containing secrets or personal context, even if encryption is available, before proper classification and minimization.

Unnecessary signatures introduce key risk, overhead, noise, misleading assurance and new recovery obligations.

## Reference standards

- [NIST SP 800-57 Part 1 Rev. 5](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final): cryptographic key protection and lifecycle guidance.
- [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html): canonical JSON for consistent hashing/signing, with strict validation requirements.

Standards establish format and key-management constraints, not the legitimacy of a particular GhostMesh decision. A future operational implementation requires exact protocol conformance and explicit authority.

## Approval and revalidation

This policy is a **proposed research standard**. Adopting it for real GhostMesh or third-party operations requires separate owner approval, threat modeling, scoped key management, interoperable protocol negotiation, failure-injection testing and independent review. Not a public repo merge.
