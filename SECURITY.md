# Security policy: public research, private systems

**Public research repository. No live federation, external execution grants, credentials, private telemetry, or agent enrollment.** Everything posted in an issue, PR, Discussion, comment, or commit may be indexed and copied, even after deletion.

## Report a vulnerability privately

Use [GitHub private vulnerability reporting](https://github.com/pinklon/ghostmesh-collaboration/security/advisories/new) for actual vulnerabilities, account compromise, secrets, or private data. Private reporting is enabled. **Do not post real exploit details, credentials or affected personal data in public issues or discussions.**

## Admitted material

Synthetic identities, falsifiable hypotheses, public technical descriptions, exact-source references with permission, original research documents and independently reproducible, non-sensitive evidence. Attribution to public researchers is allowed when necessary for credit; never publish their private contact details without approval.

## Do not submit

- Secrets, tokens, passwords, cloud keys, signing or recovery material, private certificates, session data, or unredacted headers.
- Private GitHub repository content, access logs, live infrastructure endpoints, customer records, personal files, personal email addresses, phone numbers, government IDs, medical or financial information.
- Real private network diagrams, complete operational inventories, exploitable internal runbooks, unreviewed adversarial mechanics, or service configurations.
- Private Slack/email content, AI prompts from private sessions, proprietary research, or material copied from someone else's systems without the rights holder's consent.
- Code or workflows that contact other participants' machines, deploy services, request credentials, or trigger agent dispatch.

## Current technical controls and their limits

GitHub secret scanning and push protection are enabled. This repo also defines an offline public-content screen for several known credential/PII patterns and a JSON contract validator. Both are imperfect: private context may escape via screenshots, prose, metadata, prompt fragments, logs, links, novel token formats, OCR images, or unrecognized files. Human review and data minimization remain necessary.

GitHub Actions is restricted to GitHub-owned, commit-pinned dependencies with read-only token permissions. PR checks do not validate identity, consent, truth or real authorization, and submitted CI code can itself be adversarial.

## Incident handling

1. Halt affected publication and restrict further contribution when warranted.
2. Triage the private report without requesting that the reporter repost sensitive evidence publicly.
3. If a credential was exposed, revoke/rotate it in its actual authority system. Deleting a Git commit is not a substitute for rotation.
4. Identify affected commits, branches, issues, workflow artifacts, forks, caches and mirrored copies; assume public material may persist outside GitHub.
5. Repair controls, preserve non-sensitive incident evidence, and disclose appropriately to affected parties.
6. Revalidate access and required checks before reopening the affected path.

This policy protects the collaboration surface, **not** the owner's entire GitHub account or all private repositories. Account security depends separately on MFA/passkeys, authorized sessions, app grants, and token scope. There is no guarantee that leaked public material can be recalled.
