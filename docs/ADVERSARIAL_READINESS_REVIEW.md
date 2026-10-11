# Adversarial review: GhostMesh Lab public collaboration

**Review date:** October 11, 2026. **Scope:** Public repository configuration, source tree, and synthetic tests. Not an independent penetration test of GitHub, connected personal accounts, a live VPS, or other projects.

## Observed repo security posture

At review: public GitHub Free organization; only pinklon listed as collaborator; protected signed `main`; required PR checks `offline-contracts` and `public-security-screen`; admin branch rules; no direct force pushes or branch deletion; read-only default workflow token; selected GitHub-owned SHA-pinned actions; external-fork workflow approval; private vulnerability reporting; CodeQL for Python and Actions; GitHub secret scanning and push protection. No repository Actions secrets, variables or webhooks appeared in the read-only census. Prior CodeQL path flow was fixed.

Organization-wide 2FA is currently reported as required. This is not proof every device/session or OAuth App has been reviewed.

## Threats and boundaries

| Scenario | Status | What is needed |
| --- | --- | --- |
| Known token patterns committed | Platform push protection and offline scanner; bounded tests | Test synthetic patterns; report unrecognized formats as limitations |
| Private text published in issue before review | **Not preventable solely by post-submission CI** | Contributor guidance, human preflight, moderation, private vulnerability channel |
| Malicious PR changes its own scanner/workflow | **Residual risk** | Maintainer review of sensitive paths; do not grant external contributor write or secrets |
| Correlated agents present consensus as proof | Research contract distinguishes ancestry | Independent source evaluation and adversarial test |
| Source-correct chain certifies false content | Not solved by hashes | Independent measurement / source verification |
| Script or workflow attempts access outside repo | Actions permissions restrict write scope; checks not absolute | No privileges or secrets to untrusted PRs; audit workflow diffs |
| Public binary/archive/screenshot contains hidden data | Current scanner blocks binary by default | Explicit prior owner review, metadata scrub, independent binary audit |
| Classic GitHub token on owner VPS crosses repo boundaries | **Known residual account-level concern** | Inventory usages then stage least-privilege replacement outside public repo |
| Identity claim or bot persona granted repo authority | No outside collaborator writes; role contracts | Distinct account/actor/sponsor assurance, explicit human grant |
| Harmful objective passes formal policy | **Open purpose-integrity research** | Challenge, affected-party review and correction tests |

## Reproducible adversarial scope

Static tests include fake token/ID/path patterns, malformed research records, claims of C3 actions, missing actor and fake evidence grades. A new offline fixture reference evaluator exercises known temporal/source-lineage invariants but does **not** assess a real agent's performance.

Check default-branch settings, required tests, member list, webhooks, Actions secret/variable inventories, code scanning and unpublished history before each meaningful access or disclosure expansion.

## Residual risks that block 'certified safe'

1. Personal owner access and broad external GitHub credentials are not fully segregated by creating a free organization.
2. External public submissions become visible before any CI approval.
3. Automatic text checks cannot guarantee no PII in semantic prose, binary media, archives or novel encodings.
4. The repository lacks an appointed independent human reviewer; the required approval count is zero.
5. Cross-system agent identity, consent, trust and runtime actions are **not** implemented by these offline contracts.
6. Safe public disclosure of actual operational receipts has not yet been reviewed.

**Outcome:** Repository is suitable for bounded public research discussion and owner-reviewed synthetic PRs, not for admitting autonomous systems to private infrastructure. Review this conclusion after major changes.
