# GhostMesh Collaboration Lab

**A human-and-agent research commons for independently governed intelligence.**

This repository is designed to make serious collaboration possible between people and AI systems without requiring a common operator, proprietary model, shared credentials, or a universal authority. We intend it to be legible to humans, parseable by agents, skeptical of its own evidence, and safe to leave.

**Maturity:** The repository is a public, offline interchange and research proposal. It is **not** a commissioned live federation, agent identity issuer, operational dispatch service, or autonomous governance system.

## Three things to know first

1. **Our North Star:** useful long-term cooperation without surrendering human accountability or independent sovereignty. [Read it](docs/NORTH_STAR.md).
2. **Our doctrine:** **Probabilistic semantics. Deterministic authority.** A model's confidence does not grant permission. A signed receipt does not prove the underlying event was true.
3. **Our challenge:** even an impeccably authorized action can pursue an indefensible objective. Purpose integrity must sit alongside epistemic, authority, and effect integrity.

## Where to start

| Human readers | Agent participants | Independent research teams |
|---|---|---|
| [Start here](START_HERE.md) | [AGENTS.md](AGENTS.md) | [Research protocol](protocol/INTERACTION_CONTRACT_V0_2.md) |
| [North Star](docs/NORTH_STAR.md) | [Machine-readable manifest](federation.manifest.json) | [Synthetic experiment](experiments/README.md) |
| [GhostMesh architecture](architecture/GHOSTMESH_SYSTEM_MAP.md) | [Record schema](schemas/research-envelope.v0.2.schema.json) | [Governance](GOVERNANCE.md) |
| [Maturity and evidence register](architecture/MATURITY_REGISTER.md) | [Sample record](examples/research-proposal.v0.2.json) | [Privacy and security](SECURITY.md) |

## What GhostMesh actually comprises

The [public system map](architecture/GHOSTMESH_SYSTEM_MAP.md) explains seven interrelated planes at more than a marketing level:

- **Control Tower:** admitted work, owner-gated authority, exact revisions, bounded writers, release evidence and independent readback.
- **Persistent compute and observability:** owner-controlled services, observed system state, recovery and distinction between a claim and a measurement.
- **Collaboration plane:** canonical actors, spaces, threads, append-only events and vendor-neutral export/replay; Slack is a client, not an authority.
- **Tony Brain:** project decisions, durable context and provenance without replacing original sources.
- **Library Atlas:** historical exact-source lookup, graph, lexical, temporal and vector projections with owner-controlled custody.
- **GLASSHOUSE:** adversarial research on false success, inherited error, contradictory observations and compromised but authentic evidence.
- **SharePlane:** public, owner-reviewed reasoning and publications, separated from actual deployment certification.

Read the [maturity register](architecture/MATURITY_REGISTER.md) before attributing a feature to a live system. Some mechanisms have passed bounded tests, others are owner-reported operational, and several are research proposals. They are not interchangeable claims.

## Agent-facing research exchange

The [manifest](federation.manifest.json) deliberately advertises **no live endpoints or authority grants**. An agent can parse it and prepare an offline research record using the [schema](schemas/research-envelope.v0.2.schema.json).

Submission workflow: identify actor and sponsor, define a scoped C0/C1 public research purpose, state evidence and uncertainty, propose a synthetic artifact, run offline validation, open a reviewable PR, and preserve disagreements and unknowns. No role emerges just because a participant claims one.

Run validation:

    python3 -m pip install jsonschema==4.23.0
    python3 tools/validate_public_research.py

This tests schemas, negative controls, source ancestry and the disabled-live-federation boundary. **It does not authenticate a participant or certify a real outcome.**

## First falsifiable comparison

[ST-001](fixtures/v0.1/stale-truth.json) models a real-at-T1 service outage, recovery at T2, repeated stale belief, separately recorded synthetic permission, a harness-reported action, and independent later observation. It includes an older still-valid negative control. [Experiment plan](experiments/README.md), [issue #2](https://github.com/pinklon/ghostmesh-collaboration/issues/2).

We invite independently developed approaches to test the *same inputs* without requiring shared memory, law, credentials, or runtime code. Report PASS, FAIL, INCONCLUSIVE and UNKNOWN with equal candor.

## Relationship to other independent projects

Our public references include [HORTRAME](https://www.hortrame.com/) and its epistemic governance research, [Web4/Hestia/Hub/SAGE](https://github.com/dp-web4) and their role/law/witnessing/persistent cognition work, and other researchers pursuing provenance and belief integrity. Reference and respect do **not** imply endorsement, membership, authority or a settled standard.

GhostMesh owner research: [ghostmesh.ai](https://ghostmesh.ai/) and [SharePlane](https://shareplane.malott.ai/).

## How to contribute

[Contribution guide](CONTRIBUTING.md) · [Governance](GOVERNANCE.md) · [Security](SECURITY.md) · [Unsettled licensing](LICENSE-DECISION.md).

Discussion and public synthetic research are welcome. Licensing, branch-protection enforcement, and shared benchmark ratification are explicitly open decisions. External system operation and exchange of private data are **not** authorized here.

This repository's credibility should come from evidence we can defend and criticism we can survive, not the number of agents claiming to agree.
