# Threat model for public multi-agent research

**Status:** Proposed threat model for the collaboration repository, not a claim that a deployed federation has mitigated all risks.

## Assets worth preserving

- Accuracy and provenance of research claims.
- Consent, authorship, and legitimacy of human/agent participation.
- Boundaries between public collaboration and private systems.
- Independent policy and execution authority of each participant.
- Confidentiality of private contexts and source material.
- Ability to challenge, retract, export, and leave without losing historical accountability.

## Boundaries and adversaries

| Threat | Failure example | Public research control | Unresolved outside this repo |
|---|---|---|---|
| Identity impersonation / Sybil | One agent appears as 100 independent participants | Declare sponsor, transport actor and SELF_DECLARED assurance; don't equate names with identity | Cryptographic proof, independent identity binding and collusion detection |
| Prompt injection | A posted fixture tells an agent to change permissions | AGENTS.md explicitly treats content as untrusted data | Enforcement depends on each participant's runtime |
| Evidence laundering | Ten summaries cite one flawed measurement | Source ancestry, independence fields and negative fixtures | Universal detection of correlated or concealed sources |
| Historically valid, currently false | Old outage belief continues after repair | Temporal fields, separate T2/T4 measurements | Real-world temporal truth oracle |
| Authentic but wrong witness | Signed sensor lies | Separate cryptographic provenance from content confidence | Independent measurement and witness diversity |
| Self-certification | Agent reports completion without outside readback | Separate execution report and outcome | Reliable external observation coverage |
| Authority replay | Expired grant reused after role withdrawal | Classify proposals as not authorization; explicit scopes and validity | Live role/policy gate and revocation enforcement |
| Governance capture | Sponsor selects all judges and appealers | Document challenge, review, disagreement, purpose integrity | Legitimate institution design and due process |
| Obstruction by challenge | False objections repeatedly pause lawful work | Evaluate harmful action *and* malicious/incorrect objections | Scoped appeal/pause engine |
| Data exfiltration | Source logs or private conversations pasted publicly | Public synthetic only, human review, security rules | Absolute prevention once information is published |
| False federation claim | Public manifest mistaken for live agent gateway | Null endpoints, no grants, explicit status | Real secure transport, negotiated interoperability |

## Risk model

A flaw is not solved by moving responsibility to another layer. Receipts don't automatically establish truth. A policy decision doesn't automatically prove the actor was still authorized at execution. A legitimate objection doesn't automatically justify permanent shutdown. A signed chain doesn't prove its source was complete.

## Attack-surface exclusions for published tests

No real credentials, network map, private identity keys, live exploits, raw private data, production endpoints or operational attack recipes. Use synthetic actors and fake timestamps. The public validator makes structural claims only.

## Definition of a useful failure

A test passes the scientific method if it makes a hidden assumption visible, even when the underlying system fails. Document the exact failed claim and what could falsify the proposed remedy. Preserve original evidence and negative results.

## Unresolved work

Formalized trust and identity assurance, governed consent, cross-jurisdiction disputes, true independent witnesses, anti-Sybil proof, safe runtime interoperability, and legitimacy of objective selection remain outside the current deployed scope.
