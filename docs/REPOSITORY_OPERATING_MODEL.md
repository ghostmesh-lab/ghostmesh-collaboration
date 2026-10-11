# Repository operating model and protection register

**Owner-verified snapshot: 2026-10-11.** This is a disclosure of the public research repository's governance state, not an audit or guarantee of the owner's entire GitHub account. Recheck live settings after changes.

## Separation of concerns

This public repository stores shareable research, agent-readable contracts, synthetic fixtures, discussion, and review history. It does **not** host a runtime federation, control private GhostMesh systems, hold secrets, or issue delegated authority to outside humans or agents.

An outside collaborator may read, comment, and propose through GitHub's normal public permissions. Repo participation does not confer write access, main merge rights, access to the owner's account, or any authority over private systems.

## GitHub protections verified

| Control | State |
|---|---|
| Visibility | Public |
| Maintainer/collaborators | Owner account only at commissioning |
| Default branch | `main` |
| Change entry | PR required; force pushes and deletion disabled |
| Branch admin bypass | Administrators covered by protection |
| Required checks | `offline-contracts`, `public-security-screen` |
| History | Linear and signed commits required |
| PR conversations | Resolution required before merge |
| Required independent reviewer approvals | **0**: no second reviewer appointed; limitation is explicit |
| CODEOWNERS | `@pinklon` at repository scope; attribution, not a separate independent approval |
| GitHub Actions | Read-only token; selected GitHub-owned actions; full commit SHA pinning |
| Untrusted fork contributions | Workflow approval required from maintainers |
| Security | Secret scanning and push protection; private vulnerability reporting |
| Code scanning | CodeQL Python and GitHub Actions, extended suite |
| Repository-hosted Actions secrets, variables, webhooks | None observed at commissioning |

The status checks validate public contract structure, PR classification, known sensitive-pattern screening, and synthetic adversarial cases. These checks do **not** prove private-data absence, factual truth, human consent, or agent identity. CodeQL may find implementation defects requiring separate review.

## Contribution workflow

1. Public research discussion: use a GitHub Discussion, or a scoped issue with attributed sponsorship and a falsifiable question.
2. Categorize with one `type:`, `area:`, `status:`, `risk:`, and `priority:` label. The [taxonomy](LABELS_AND_TRIAGE.md) explains color meanings.
3. Propose a bounded PR. Use the template to state file scope, rights, negative controls, evidence, uncertainty, and disclosure decision.
4. Wait for required CI and the appropriate human review. Label presence does not authorize anything.
5. The owner or an explicitly appointed maintainer may merge after policy gates. A merge is **not** permission to deploy or connect an agent.
6. Record the conclusion in a linked issue; failures, disputes and unknowns remain first-class results.

Only the owner can approve changes to protected files for now. GitHub cannot provide independent approval by the same person who authored a change. Requiring a second reviewer will need a trusted, specifically authorized repository collaborator or separately governed review mechanism.

## Safety and privacy

See [SECURITY.md](../SECURITY.md) and use GitHub's **private vulnerability reporting** for sensitive findings. Every public issue/PR can be mirrored permanently. Public text checkers and platform scanning only catch recognized patterns. Human disclosure review is required for anything copied from external research, logs or private sources.

The named owner account remains visible on GitHub because this repository is owned by that account. Stronger identity separation would require a dedicated organization or another repository owner and a repo-scoped installation. That would be a separate consented migration, not an automatic consequence of joining this lab.

## Board and workflow organization

Two GitHub milestones organize the work: security/agent admission commissioning and independent synthetic research. Color-coded status labels can be filtered directly in Issues and PRs. A native GitHub Projects board is not required for safe contribution and has not been commissioned here. Never broaden GitHub account token scopes merely to create a board.

## Adversarial evidence, bounded

- Offline validator checks schema fields, examples, negative controls, and absence of live endpoints or grants.
- Synthetic DLP tests exercise credential-like strings, personal email and identifier patterns without using real credentials.
- A historical reachability scan inspected public Git blobs for recognized sensitive patterns; it is heuristic only.
- CodeQL identified a path-flow concern in the first PR metadata gate; a new reviewed PR removed the path-based read.
- Neither checks nor branch protection can prevent a human from intentionally pasting confidential prose into a public comment before a reviewer can see it.

## Unresolved decisions

- [Licensing and contribution rights](https://github.com/pinklon/ghostmesh-collaboration/issues/1).
- [First shared benchmark ratification](https://github.com/pinklon/ghostmesh-collaboration/issues/2).
- [Repository governance and future independent review](https://github.com/pinklon/ghostmesh-collaboration/issues/3).
- Separate organizational identity and least-privilege automation credentials if the owner decides to go beyond personal account ownership.

**Review baseline:** Reassess these settings, collaborators, webhooks, installed actions, security alerts and any new repository secrets before admitting external agent automation.
