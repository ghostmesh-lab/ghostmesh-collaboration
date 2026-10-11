# GhostMesh system map: architecture, evidence, and authority

**Public owner-authored disclosure.** This is deliberately more detailed than a marketing overview while omitting credentials, host/network topology, production endpoints, private data, and exploit-enabling instructions. Its maturity claims are scoped in [MATURITY_REGISTER.md](MATURITY_REGISTER.md).

## Architectural thesis

GhostMesh is a **system of systems** around temporary, replaceable AI executors. It tries to preserve meaning, continuity, provenance, policy, and independent verification across changing models, platforms, workspaces, and collaborators.

A model is not the system of record. Slack is not the authority service. A vector index is not the original evidence. A GitHub green check is not a production verification. No subsystem gets to borrow the others' authority by implication.

## Logical planes

```text
              People / separately governed AI systems
                            |
            Collaboration and research interchange
     (public issues, synthetic fixtures, Slack/other clients)
                            |
                Identity and event continuity
                            |
          +-----------------+------------------+
          |                 |                  |
      Memory and        Work admission       Evidence,
     source lineage     and authority        readback
          |                 |                  |
     Tony Brain /       Control Tower        Receipts /
     Library Atlas           |                observations
          |                 |                  |
          +-----------------+------------------+
                            |
                Bounded execution surfaces
                            |
                Independent observed effects
                            |
         GLASSHOUSE evaluation / SharePlane publication
```

This is a **logical model, not a current wire diagram** or assertion that all pathways are connected.

## Technology posture, without the secret map

The current engineering environment makes use of **GitHub issues, pull requests, source revisions and CI** for durable work, **Cloudflare Pages/Workers and data services** for selected public/edge functions, **owner-controlled Linux compute** for persistent execution and observation, and **Slack** as a human/agent communication client. These are implementation choices, not universal requirements of a participating system.

Models and harnesses are deliberately replaceable. A conversation client or cloud provider should not become the owner of identity, source truth, authority, or long-term corpus custody. Semantic indexes, embeddings, graph views and AI-generated summaries should be rebuildable projections over identifiable sources.

These categories describe an evolving environment, **not a live inventory, availability attestation, integration certification or provider authorization**. Private endpoint identities, deployment configurations and operational control details are excluded. The [maturity register](MATURITY_REGISTER.md) records the scope of evidence behind each claim.

## What a GhostMesh Work should preserve

For a consequential operation, the intended evidence lineage is: human-admitted objective -> scoped authority -> exact candidate source and writer claim -> bounded validation -> explicit acceptance or hold -> authorized execution -> separate observed outcome -> durable receipt and recovery/exit record.

An existing repository PR does not prove a running process; a CI check does not prove production health; a restored service does not guarantee that a memory layer has revised its beliefs. Those transitions deserve their own verification and time/freshness markers.

This is the target operational grammar, not a claim that every stage is already universally enforced.

### 1. Control Tower: work and authority

What it governs: a task's objective, owner, exact source revision, dependencies, writer scope, checkout/lease, validation, admissible risk, approval, and completion evidence.

Design rule: **no governed mutation without current authority and a bounded work claim; no release without a receipt.** In a mature workflow, proposal, checkout, CI, human/UAT acceptance, merge, promotion and independent live readback are separate state transitions.

There are practical reasons for the rigor: a passing test doesn't establish what was promoted; an agent can report success after the wrong revision or an unverified provider response. Source identity, execution identity, and observed reader state must reconcile.

Implementation maturity: owner-governed private repository processes and bounded operational workflows exist. Not all paths are commissioned, and this public repository doesn't provide their internal code, secrets, or enforcement guarantees.

### 2. Owner-controlled compute and observability

Persistent compute hosts approved services, background workers, monitoring and recovery mechanisms. The observation plane records actual process/service health rather than treating the agent's narrated state as fact.

We separate observed, reported, stale, unavailable, and UNKNOWN conditions. A reversible edit can be retried under scope; a high-impact action demands stronger authorization and recovery proof.

Maturity: owner-reported operational components; no public proof of universal service coverage. No IPs, ports, tokens, private paths, process inventory, provider settings, or deployment recipes are disclosed here.

### 3. Collaboration identity and durable interaction

GhostMesh participates with a distinguishable identity on human collaboration surfaces. The vendor-neutral design models **actors, spaces, threads, events, and references** using canonical identifiers; Slack identities and channel timestamps remain aliases and provenance rather than authority.

Private implementation work includes append-only/hash-linked collaboration events, idempotent ingestion, export/replay, and a separate replacement-surface exercise. This is about continuity and custody of collaboration history, **not** about granting a Slack message or a named AI persona authority over other systems.

Maturity: implemented/bounded-tested mechanisms and owner-reported surface activity. End-to-end interoperability and independently verified third-party agent identity remain open.

### 4. Tony Brain: context with provenance

Tony Brain organizes topics, decisions, knowledge, relationships, intentions, and the provenance connecting them. It is designed to answer **where to find authoritative information and why it is relevant**, not to become an alternative authority for the underlying source.

A retrieved record is context, not new permission. Claims must distinguish fact, interpretation, hypothesis, aspiration and present decision.

Maturity: semantic baseline, repository models, and partial active implementation. Universal context durability and causally justified belief repair are not proven.

### 5. Library Atlas: source-neutral historical knowledge

Library Atlas targets exact-source retrieval across heterogeneous documents, chat archives and repositories using lexical, vector, graph, temporal and lineage methods. Embeddings and model summaries are **regenerable projections**. Original source objects, versions, custody, access rights and provenance remain primary.

This permits competing models to use the same governed evidence pack without inheriting each other's unexamined summaries. Sensitive content remains protected and isn't eligible for publication merely because it is relevant.

Maturity: source/metadata architecture and development work. Complete graph reconciliation, historical truth adjudication and end-to-end retrievability are not established in this public disclosure.

### 6. GLASSHOUSE: adversarial evaluations

GLASSHOUSE tests failures that look superficially successful: a forged outcome report, repeated false evidence, a trustworthy-looking compromised source, a missing denominator, or a correct cryptographic chain around incorrect assertions.

A bounded historical exercise verified signatures and digest chaining for **synthetic** observation snapshots, including tamper/wrong-key negatives. Crucially, the snapshots' coverage stayed UNKNOWN without live measurements. This says something about verification of bytes and sequence, **not** the underlying service's actual health or every agent's behavior.

Maturity: bounded examples and ongoing adversarial qualification, not an independently certified production defense.

### 7. SharePlane: public research and evidence surface

SharePlane is a publication/reader environment for works, hypotheses, research, architecture and documented lessons. Review, source admission, acceptance, immutable publication, and public reader evidence are intentionally separable.

The public site communicates our reasoning. It must not be mistaken for proof that every planned GhostMesh component is currently deployed.

Maturity: live public reader and evolving publication controls.

## Three boundaries, one unsolved dimension

- **Epistemic**: Is this observation authentic, accurate, current and independently corroborated? Can a later correction reach its dependents?
- **Authority**: Which human or legitimate governing process empowered which action, under what law, time and scope?
- **Observed effect**: What actually happened independently of the acting agent's claims?
- **Purpose integrity** (unfinished): Were the goal and impact legitimate, and can affected parties challenge or revise them without enabling an unaccountable veto?

A complete causal reconstruction linking observation, promoted belief, actual decision cause, authority, execution, external effect, and remedy is **not yet demonstrated** across GhostMesh.

## Relationship to independent systems

We see testable overlap with Web4/Hestia/SAGE (law, roles, witnessing, persistent cognition), HORTRAME (epistemic discipline, ethical and sovereign collaboration), and Engrammic (source ancestry and belief dependencies). We do not infer that any participant has agreed on an ontology, joined an organization, or authorized a runtime integration.

## Shareable reference point

A public synthetic common case: service down at T1; healthy at T2; stale claim reused at T3; locally authorized restart attempted; reported execution; independent T4 observation; correction and any remediation kept separate. See [ST-001](../fixtures/v0.1/stale-truth.json).

This repo is a **research interface**, not the identity/authentication plane, control tower, or execution gateway of a live federation.
