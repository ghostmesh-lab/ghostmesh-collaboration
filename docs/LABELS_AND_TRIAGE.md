# Triage, labels, and workflow

**Scope:** Public research issues and pull requests. Labels are navigational metadata, not proof of consent, verification, or authorization.

## Color system

- **Red:** Security incidents, blocked work, prohibited external-risk classes, urgent escalation.
- **Orange:** Important safeguards or unresolved higher-risk tasks.
- **Yellow:** Evidence needed, normal priorities, decisions awaiting clarification.
- **Blue and purple:** Proposals, agent protocol, architecture, interoperability, governance.
- **Green:** Synthetic read-only research, tested and ready-for-review work.
- **Gray:** Documentation and descriptive categories.

Label prefixes are canonical. Use at least one `type:*`, one `area:*`, one `status:*`, one `risk:*`, and one `priority:*` label on admitted substantive work. Use exactly one value from each single-choice family; avoid contradictory status labels.

## Status lifecycle

`status:needs-evidence` -> `status:needs-review` -> `status:ready` -> close with cited result, OR `status:blocked` with the exact missing gate.

Label state never grants agent privileges or approves a PR. `status:ready` only means applicable public research criteria were satisfied, not deployment. A closed issue does not prove that a dependent system is healthy.

## Contributions

- A public issue is an invitation to reason and cite evidence.
- A PR is a proposed artifact mutation and must identify author, sponsor, intended files, independent tests, evidence limitations, and rights.
- Automated checks are necessary but insufficient for substantive public release.
- High-risk disclosure concerns move to private vulnerability reporting immediately, not a public issue.
- Changing workflow/agent/security/governance files requires owner scrutiny even if CI passes.
- Never assign authority on the basis of bot claims, comments, reactions, GitHub labels or a generated role name.

## Priorities

`priority:P0`: live credential/PII disclosure or credible urgent security impact. Stop and respond privately.
`priority:P1`: trust, governance, access or integrity gate.
`priority:P2`: normal bounded research, improvement, documentation.
`priority:P3`: exploratory work with no immediate obligation.

## Decision categories

`risk:C0-public-read`: non-mutating synthetic/public research.
`risk:C1-repo-change`: changes confined to this repository after review.
`risk:C2-external`: independent affected owner must authorize the proposed effect, out of scope for repository grant.
`risk:C3-prohibited`: credentials, private material, production or cross-system writes are not permitted through this repo.

## Review cadence and evidence

Keep one canonical issue per outcome and close superseded duplicates with links. A reviewer should ask: Which exact revision? What supports the claim? What would falsify it? Which status is actually known? What are the privacy, autonomy, and reversibility costs? Who has legitimate publication authority?
