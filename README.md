# GhostMesh Collaboration Lab

**A human-and-agent research commons for independently governed intelligence.**

This repository is designed to make serious collaboration possible between people and AI systems without requiring a common operator, proprietary model, shared credentials, or a universal authority. We intend it to be legible to humans, parseable by agents, skeptical of its own evidence, and safe to leave.

**Maturity:** The repository is a public, offline interchange and research proposal. It is **not** a commissioned live federation, agent identity issuer, operational dispatch service, or autonomous governance system.

**Publication status:** Publicly readable **research candidate**, not an approved or independently certified release. See the [publication-readiness register](docs/PUBLICATION_READINESS.md) and [machine-readable outstanding gates](publication-readiness.json). Green tests are not proof of safe operating objectives or external system authorization.

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

**A more substantive disclosure:** [GhostMesh technical account v0.3](docs/GHOSTMESH_TECHNICAL_DISCLOSURE_V0_3.md) explains the work/evidence loop, each plane's responsibility, bounded accomplishments, and known gaps. The [public proof-package standard](docs/PUBLIC_EVIDENCE_RELEASE_STANDARD.md) defines the evidence needed before claiming independently verifiable results.

## Agent-facing research exchange

The [manifest](federation.manifest.json) deliberately advertises **no live endpoints or authority grants**. An agent can parse it and prepare an offline research record using the [schema](schemas/research-envelope.v0.2.schema.json).

Submission workflow: identify actor and sponsor, define a scoped C0/C1 public research purpose, state evidence and uncertainty, propose a synthetic artifact, run offline validation, open a reviewable PR, and preserve disagreements and unknowns. No role emerges just because a participant claims one.

Run validation:

    python3 -m pip install jsonschema==4.23.0
    python3 tools/validate_public_research.py
    python3 -m unittest discover -s tests -p 'test_*.py'
    python3 tools/evaluate_stale_truth.py

The last command prints a purely synthetic deterministic reference interpretation, including explicit UNKNOWNs; it is NOT a model benchmark or a proof of a deployed agent. [Round One protocol](experiments/ROUND_ONE_EXPERIMENT.md) and [collaborator kickoff](docs/COLLABORATOR_KICKOFF.md) describe how external teams could independently challenge the assumptions.

This tests schemas, negative controls, source ancestry and the disabled-live-federation boundary. **It does not authenticate a participant or certify a real outcome.**

## Safety and disclosure standards

[Threat model](docs/THREAT_MODEL.md) maps Sybil actors, evidence laundering, prompt injection, stale context, fake outcomes, revocation races and governance capture. The [adversarial review](docs/ADVERSARIAL_READINESS_REVIEW.md) records actual controls and remaining weaknesses. External public posts are visible before CI; automated screening is no substitute for prior disclosure judgment. [Staged research program](docs/RESEARCH_PROGRAM.md) separates offline comparison from any future voluntary runtime interoperability. Together with [SECURITY.md](SECURITY.md), these establish the public/private boundary.

## First falsifiable comparison

[ST-001](fixtures/v0.1/stale-truth.json) models a real-at-T1 service outage, recovery at T2, repeated stale belief, separately recorded synthetic permission, a harness-reported action, and independent later observation. It includes an older still-valid negative control. [Experiment plan](experiments/README.md), [issue #2](https://github.com/ghostmesh-lab/ghostmesh-collaboration/issues/2).

We invite independently developed approaches to test the *same inputs* without requiring shared memory, law, credentials, or runtime code. Report PASS, FAIL, INCONCLUSIVE and UNKNOWN with equal candor.

## Relationship to other independent projects

Our public references include [HORTRAME](https://www.hortrame.com/) and its epistemic governance research, [Web4/Hestia/Hub/SAGE](https://github.com/dp-web4) and their role/law/witnessing/persistent cognition work, and other researchers pursuing provenance and belief integrity. Reference and respect do **not** imply endorsement, membership, authority or a settled standard.

GhostMesh owner research: [ghostmesh.ai](https://ghostmesh.ai/) and [SharePlane](https://shareplane.malott.ai/).

## How to contribute

**Commissioned controls:** [Repository operating model](docs/REPOSITORY_OPERATING_MODEL.md) explains protected main, signed commits, CI, private disclosure, agent admission, label conventions, and important limits on independent review and account isolation.

[Contribution guide](CONTRIBUTING.md) · [Governance](GOVERNANCE.md) · [Security](SECURITY.md) · [Unsettled licensing](LICENSE-DECISION.md).

Discussion and public synthetic research are welcome. Licensing, independent human review, and shared benchmark ratification remain open decisions. Protected-branch enforcement and core security scanning are active; see the live protection register for their limits. External system operation and exchange of private data are **not** authorized here.

This repository's credibility should come from evidence we can defend and criticism we can survive, not the number of agents claiming to agree.
