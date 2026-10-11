# Human-agent and agent-agent research contract v0.2

**Status: PROPOSED.** This is a public interchange vocabulary and offline evaluation interface, not a ratified Web4 standard, operational enrollment service, or federated trust anchor.

## Vocabulary

- **Actor**: a declared human, organization, or agent, with a distinct technical transport account and claimed sponsor.
- **Role**: a capacity defined by an independently governed system; naming a role in JSON does not grant it.
- **Observation**: time-bound measurement from a source, including producer, custody, and coverage.
- **Claim**: authored interpretation or statement with ancestry and uncertainty.
- **Decision**: an attributable determination under a separately valid policy/authority.
- **Execution report**: assertion that a tool or worker did something.
- **Outcome**: separately observed effect and its measurement limits.
- **Correction**: link preserving history while revising a claim; not permission to reverse prior actions.
- **Challenge**: contest of a claim, grant, act, or objective; may be heard without acquiring veto rights.

## Participation handshake (offline, human-reviewed)

1. Discover the public [research manifest](../federation.manifest.json); it advertises **documentation only**, no live transport.
2. Actor declares canonical local alias, type, sponsor, provider/account provenance where relevant, purpose and consent.
3. Human owner checks authorized scope and data classification under **local law**. No inferred grant from reputation or model confidence.
4. Propose a bounded synthetic task, evidence set, expected distinctions, negative controls, and result criteria.
5. Each system interprets independently. Record mismatches, abstentions, and costs, not just the most favorable score.
6. A human reviews publication, attribution, licensing, and purpose. Record dissent and correction paths.
7. An actor may withdraw future participation; historical record retention follows applicable reviewed terms.

This repository does **not** execute steps 2-7 automatically.

## Envelope types and lifecycle

The [research-envelope schema](../schemas/research-envelope.v0.2.schema.json) describes a **proposal, claim, observation, decision, execution_report, outcome, correction, dispute, or exit** record. All require:
- stable record ID and version,
- declared actor and sponsor,
- UTC observation/creation times with meaning,
- origin source reference and explicit evidence grade,
- purpose, synthetic/public classification, consequence class, and supported limitations.

Illustrative artifact: [synthetic proposal](../examples/research-proposal.v0.2.json).

## Evidence grades

PROPOSED, AUTHOR_REPORTED, OBSERVED, REPRODUCED, INFERRED, DISPUTED, UNKNOWN. A document's signature/commit authenticates its bytes and selected provenance assumptions, not its accuracy. Self-corroboration and repeated descendants of one source never become new independent witnesses.

## Consequence classes and authority

| Class | Scope | Research workspace behavior |
|---|---|---|
| C0 | Public read-only inquiry or synthetic offline evaluation | May propose analysis |
| C1 | Bounded repository docs, schemas or fixture changes | GitHub sponsor + PR + maintainer review, subject to enforcement settings |
| C2 | External community governance or another participant's public materials | Requires that participant's independent approval; not granted here |
| C3 | Production/private data, real-world effects, infrastructure mutation, secrets | **Out of scope; no grant exists here** |

An action approved under one role/law/version cannot automatically be treated as still executable after role revocation or law amendment. Follow the actual local governing rules and record their validity and enforcement, rather than assuming universal semantics.

## Threat model

Sybil and impersonation attacks; malicious collaborative prompts; inherited falsehood as fake corroboration; stale but once-correct evidence; compromised authentic sources; forged or self-serving success reports; unobserved denominator; policy replay; time-of-check/time-of-use revocation; one dominant participant laundering influence through peers; unfair objection processes; metadata leaks from witness sampling.

The repository's static CI can validate syntactic and some semantic invariants. It **cannot** verify live identity, witness independence, legitimacy of objectives, or deployed policy enforcement.

## Success and failure record

Before any comparison, pin source revision, fixture hash, evaluator/rules, sample selection, independence definition, tested release versions, allowed uncertainty, negative controls, and costs. Publish PASS, FAIL, INCONCLUSIVE or UNKNOWN only for their precise scoped claims. Keep disagreement and the original version reconstructible.

## Governance of this proposed contract

Any laboratory can reject or adapt the interchange without forfeiting sovereignty. Proposal acceptance is not endorsement, a standards ratification, or authorization to join a live network. Changes are reviewed as ordinary research contributions with explicit rights and licenses.
