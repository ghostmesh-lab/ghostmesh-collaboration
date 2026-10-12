# Trust root and signing-key lifecycle: proposed GhostMesh evidence profile

**Status: architecture proposal, not commissioned key management.** It contains no secret material, private key references, live issuer endpoint or authority grants.

## The actual trust problem

A cryptographic verifier can check a signature using a public key. It cannot determine who legitimately controls the signer, whether their signing role was authorized, whether a relying organization opted in, or whether the signed statement is true.

For a real federation, the owner of each sovereign participant must adopt the root, bind the actor to a human/organizational identity, establish permitted roles and policies, and retain the ability to terminate trust. No GhostMesh-wide super-root should silently override local rules.

## Proposed separation of roles

| Role | Responsibility | Separation requirement |
| --- | --- | --- |
| Organization root owner | Decides which external identities and trust roots are recognized | Explicit human consent and recovery mechanism |
| Trust anchor authority | Publishes signed root metadata, key status, version and expiration | Independently authenticated outside the incoming assertion |
| Evidence signing key | Signs narrowly typed observations or bounded attestations | Cannot self-assign a new policy or issuer authority |
| Grant authority | Approves consequential actions with separately governed policy and scope | Not inherited from evidence signing |
| Independent effect witness | Records actual outcomes under independently controlled sensors or observers | Must not be assumed independent because it has a different key |
| Relying verifier | Validates all the above, rejects replay and records UNKNOWN | Must not infer truth/authorization from a signature alone |

## State machine proposal

```text
GENERATED_PRIVATE
    -> ATTESTED_PENDING_OWNER
    -> ACTIVE_SCOPED
    -> ROTATING (new key separately accepted)
    -> EXPIRED / REVOKED / COMPROMISED
    -> RETIRED_FOR_NEW_SIGNING
```

- **Generated:** create signing material on the authorized boundary using a reviewed CSPRNG/HSM/KMS as appropriate. Keep private material outside public source, logs, user messages and ordinary application storage.
- **Pending:** verify accountable sponsor, intended scope/audience, key ownership binding and human acceptance; never promote a self-declared key by itself.
- **Active:** time-bound, role-bound, schema-bound and locally authorized. A valid signature from an unknown actor is still untrusted.
- **Rotating:** a new key receives an independently approved binding; both old and new status records are explicitly versioned. A valid old signature can be retained as evidence without permitting new acts.
- **Expired:** fail closed for new submissions. Historical verification needs a trustworthy timestamp and a signed, time-specific status history; a claimed `issued_at` alone is insufficient.
- **Revoked:** stop accepting new attestations immediately after trusted status update. Relying parties must define outage/staleness behavior; no silent trust in stale status.
- **Compromised:** quarantine affected statements, distinguish compromise window, preserve incident evidence, issue new independently accepted key, reconcile downstream reliance, notify affected owners under consented channels.
- **Retired:** cryptographic key recovery, deletion, and archive verification are separate from trust withdrawal. Retiring a key does not erase past records or fix any false beliefs.

## Revocation and replay rules

- A signed statement is checked against a **separately authenticated** trust snapshot with version/epoch, trusted timestamp, signer role, schema restrictions, and revocation state. The signer cannot certify its own ongoing authorization.
- Replay identifiers should be scoped by issuer, audience, key ID and message purpose, with **atomic persistent uniqueness** and bounded retention. Two in-memory sets in two processes are not a global replay defense.
- Sequence ordering requires an explicit policy per stream. A high sequence may represent dropped history, not proof that no earlier records exist.
- A compromised key demands a defined window-of-trust policy for historical evidence. Do not blindly erase all prior signatures or automatically validate them just because the cryptography still verifies.
- Clock skew, partition tolerance and offline recovery require owner-approved failure policies. C2/C3 operations cannot default to fail-open on missing status.
- Secure logging should record verified references and decisions, not plaintext secrets or unnecessary personal identifiers.

## Operational commissioning gates

1. Approved threat model and legal/governance sponsor for each participant.
2. Independent identity and public-key binding, explicit trust-root adoption and manual/automated revocation path.
3. Audited signing library, cross-language canonical test suite and algorithms acceptable in the deployed jurisdiction.
4. Secret custody and recovery procedures with hardware or managed key support appropriate to consequence.
5. Durable, atomic replay protection with crash/restart, concurrency and network partition tests.
6. Independent outcome witnesses, incident escalation, challenge and human override.
7. Defined revocation, rotation, archive verification and key-compromise drills.
8. Owner-approved release case and test evidence. No bridge to private resources without fresh scoped authorization.

**Current state:** None of this establishes a deployed root, live federated identity, durable replay service, independently audited reviewer or C2/C3 grant. It is deliberately separate from the [synthetic cross-language verifier](../protocol/CROSS_LANGUAGE_SIGNED_EVIDENCE_V0_2.md).
