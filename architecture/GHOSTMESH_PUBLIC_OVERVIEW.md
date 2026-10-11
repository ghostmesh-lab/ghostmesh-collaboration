# GhostMesh: public technical overview (discussion draft)

**Owner:** Tony Malott | **Status:** Public architectural description, not a complete deployment or independent certification report | **Date:** 2026-10-11

## Engineering motivation

Agents that work across sessions, tools, machines, providers, and parallel workflows routinely lose context or confuse a reported action with verified completion. The operating principle is:

> Probabilistic semantics. Deterministic authority.

A model's interpretation, intention, confidence, or narrative cannot independently authorize an operation or attest its actual effects.

## Functional planes and current boundaries

| Plane | What it is intended to do | Current evidence / limitations |
| --- | --- | --- |
| Work and control | Represent tasks, scoped authority, candidate revisions, admission decisions and consequential execution boundaries | Repository workflows and bounded authority practices exist; this is not evidence of universally complete enforcement across all runtimes |
| Persistent execution and observation | Maintain service continuity and independent state readback on owner-controlled compute | Operational components exist; an agent's completion claim is never sufficient on its own to establish health or deployment |
| Identity and communications | Give GhostMesh a distinguishable participant identity for bounded interaction with humans and other systems | It participates in GhostMesh Commons with its own identity; this does not confer intrinsic operational authority or establish a permanent conscious subject |
| Memory and provenance | Preserve source ancestry, contextual continuity, and distinctions among observation, claim, and inference | Tony Brain and Library Atlas are developing these capabilities; generalized cross-system belief dependency and repair are not demonstrated |
| Adversarial evaluation | Test fabricated success reports, inherited false claims, compromised-but-authentic sources, and misleading evidence | GLASSHOUSE includes synthetic research and bounded tests; broad qualification remains incomplete |
| Public explanation | Publish readable architectural theses and research for independent challenge | [SharePlane](https://shareplane.malott.ai/) hosts public work; a published explanation is not by itself an implementation receipt |

## Example of an evidence boundary we have tested

In a bounded historical synthetic exercise, two observation snapshots were signed with an experimental Ed25519 key and linked using SHA-256 digests. A verifier checked source bytes, signatures, sequence, chain continuity, and negative cases involving tampering or wrong verification keys.

**What passed:** historical synthetic signature and linkage verification for those snapshots.

**What did not follow:** proof of live production health, full observational coverage, authentic independent source measurements, authority for an operational change, or independently confirmed downstream effects. The coverage field remained **UNKNOWN**.

This distinction is intentional. The test demonstrates a narrow cryptographic property, not a complete evidence or governance plane.

## Failure cases we want to compare

- A false observation inherits apparent corroboration because multiple agents repeat the same original source.
- An observation originally true becomes stale, yet is repeatedly promoted into current belief.
- An authentic, signed but compromised source produces false content.
- A permit or tool receipt exists but a separate measurement disproves success.
- A belief is later corrected after dependent actions have caused real effects.
- The acting role or applicable rule changes between permission and attempted execution.
- A socially harmful objective is fully authorized under an institution's rules.

## Known unsolved problems

We do **not** claim generalized proof of the causal bridge from observation -> belief -> decision -> granted authority -> action -> independent effect -> remedy. We do not claim that cryptographic integrity establishes truth, that network decentralization prevents capture, or that operator authorization establishes the legitimacy of a goal.

A useful outcome of collaboration is finding which distinctions can be jointly tested while each system preserves its own authority, evidence labels, and interpretation.

## Public disclosure boundary

This document intentionally omits internal hostnames, service endpoints, credentials, deployment recipes, private telemetry, identity keys, topology details, live operational configuration, unpublished research cases, and sensitive adversarial implementation details. Those are not prerequisites for a synthetic public comparison.

For the owner-authored publications see [SharePlane](https://shareplane.malott.ai/). This document should not be represented as a current independent production audit.
