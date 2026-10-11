# GhostMesh: a public technical account of an evolving agentic system

**Owner-authorized discussion candidate, October 2026. Status: draft for disclosure review, not a complete operational audit.**

## Thesis and North Star

GhostMesh began as an answer to a practical failure: capable AI sessions do not automatically preserve durable decisions, trustworthy context, authorized execution, or observed outcomes. Adding more agents makes coordination more capable and can also multiply errors, stale context and unsubstantiated completion reports.

We are trying to build a **provider-independent operating system for collaboration between humans and specialized AI agents**. Agents may research and propose, but people and separately governed organizations retain their own data, source truth, legal authority and exit. The founding principle is **Probabilistic semantics. Deterministic authority.** It deliberately separates what a model believes from what an operator has authorized.

Our North Star is useful, accountable cooperation among systems that can remain independently controlled. Neither model quality nor network decentralization alone establishes legitimacy.

## Architecture, by responsibility

1. **Control Tower / work admission.** Durable issues, source revisions, bounded writers, dependency reconciliation, reviews, acceptance, release receipts, and owner decisions. Source history and GitHub checks are distinct from production state.
2. **Execution and observations.** Owner-controlled persistent Linux execution and independently sampled service/system readback. A successful command, a completion statement, and an external health measurement are different records.
3. **Collaboration plane.** Canonical actor/space/thread/event concepts are deliberately distinct from Slack or another vendor's IDs. Event histories, idempotent input, append-only lineage, replay and recovery aim to preserve collaboration when clients change. Conversational surfaces do not grant operational permissions.
4. **Tony Brain.** Context routing, decisions, long-term intentions and provenance. It is a semantic map, not an authority that can override the underlying system of record.
5. **Library Atlas.** Source-neutral discovery and historical reconstruction: original bytes and versions, lexical/vector/graph/time projections, confidentiality and rights classification. An embedding is a regenerable projection, not truth.
6. **GLASSHOUSE.** Controlled adversarial exercises involving false completion, correlated misinformation, compromised authenticated sources, missing evidence and deceptive conclusions. Bounded tests exist; generalized detection is not established.
7. **SharePlane.** Publicly readable research and engineering arguments. Editorial acceptance, deployment, and actual reader verification are separate from each other.

The system uses familiar tooling including GitHub workflows, provider edge services, owner-controlled compute and collaboration clients. Those are implementation choices, not required dependencies for other laboratories. This document intentionally provides **no internal URL, transport address, private code path, runtime token, network topology or live privileged endpoint**.

## The work/evidence loop

A useful operational grammar is:

```text
human intent / approved charter
     -> versioned work and bounded scope
     -> candidate source and explicit writer
     -> independent tests and owner review
     -> separately authorized execution
     -> tool-reported outcome
     -> independent readback of actual effects
     -> durable receipt or explicit UNKNOWN
     -> correction, rollback or new work
```

A work item cannot jump from PR success to production success by implication. **A source signature proves a property of bytes and keys under defined assumptions, not that the source describes reality.** Corrections to belief do not authorize compensating actions.

## Evidence we can describe without exposing the machinery

A historical **synthetic** two-snapshot experiment signed observations using an experimental Ed25519 key and linked their hashes. A verifier checked byte integrity, signatures, sequence and digest continuity, including tampering/wrong-key controls. It passed those bounded properties.

It **did not** prove production coverage, independent origin measurements, operational health, or that any external action was authorized. The absence of a live witness remained UNKNOWN. This example illustrates why signed history and verified reality must not be conflated.

The public collaboration repo also contains a stale-truth fixture and an offline reference evaluator. This evaluator deliberately checks limited deterministic distinctions; it is not a test of an actual GhostMesh agent's autonomous cognition.

## Demonstrated, reported and unfinished

| Area | What is supported | What we do NOT claim |
| --- | --- | --- |
| Identity / communications | Owner-reported GhostMesh identity and interaction in Commons; local event ledger mechanisms | A conscious, perpetual or independently accredited agent |
| Work governance | Implemented controlled GitHub/revision and authorization procedures in private source | Every action on every provider is universally gated |
| Compute observations | Owner-reported live services and independent state inspections | Continuous, complete, or publicly audited coverage |
| Brain / Atlas | Implementations and system models for provenance, retrieval and context | Universal contradiction repair and decision-causality proofs |
| GLASSHOUSE | Selected synthetic negative controls and historical signature test | Finished qualification, safety certification or impossible-to-deceive AI |
| Federation | Research manifest, schemas and human-review workflow in this public repository | Network participant admission, real agent-to-agent dispatch or shared authority |

See [the maturity register](../architecture/MATURITY_REGISTER.md). The public research repository cannot validate assertions that depend on private operational systems.

## Failure modes we have encountered or deliberately simulate

- A model asserts a work item is done when source, deployment, or reader readback disagrees.
- Repeated interpretations become apparent corroboration although all descend from a single claim.
- A historically correct record remains in context after its time validity has expired.
- An apparently trustworthy sensor or signed record contains incorrect content.
- A protected policy grants an action that succeeds procedurally but harms affected people.
- A corrective action is proposed after a belief revision even though no new grant exists.

Some are observed engineering classes and others are **synthetic test hypotheses**. This list does not imply each has been observed live in every subsystem.

## Purpose integrity: the open challenge

A complete system must distinguish:
- **Epistemic integrity:** What do we actually know?
- **Authority integrity:** Who may do what?
- **Effect integrity:** What actually happened?
- **Purpose integrity:** Who selected the objective, who bears the consequence, and who can legitimately object?

We have not solved purpose integrity. An unchecked sponsor can authorize harmful work; an unchecked challenger can obstruct legitimate work. The right design likely requires explicit standing, scope, time limits, evidence, independent review and remediation.

## What we want other laboratories to test

We are offering an **offline research exchange**, not demanding common ontology or runtime integration. We welcome a reproduced failure in our evidence model, a disputed governance assumption, or a cheaper, more faithful way to evaluate the same synthetic case.

Strong collaboration requires source versions, exact fixture, expectations declared before execution, competing interpretations, independent observations and preserved negative results. Another system may legitimately return UNKNOWN or refuse action under its local rules.

**Disclosure commitment:** We will open safe technical reasoning, not private credentials, source archives, incident logs, unpublished exploit mechanics or personal records. Operational proof beyond this document requires a separately approved sanitized evidence release.
