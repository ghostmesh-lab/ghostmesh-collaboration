# GhostMesh Lab organization security boundary

**Commissioned: October 11, 2026.** This is a bounded public setup receipt for the collaboration repository, not a security certification of the personal GitHub account, private GhostMesh infrastructure, or every installed application.

## Organization and scope

- GitHub organization: [ghostmesh-lab](https://github.com/ghostmesh-lab), Free plan.
- Public research repository: [ghostmesh-collaboration](https://github.com/ghostmesh-lab/ghostmesh-collaboration).
- The existing repository was transferred without changing its GitHub repository ID or the initial default-branch commit.
- No private GhostMesh repositories were transferred. Independent researchers have not been added as organization members or repository collaborators.
- Initial administrator: the account **pinklon**. The organization is a separate ownership namespace, **not** a separate authentication principal or an air gap from its administrators.

## Organization policy readback

| Setting | Observed result |
|---|---|
| Plan | GitHub Free |
| Members | One, pinklon |
| Default repository permission for ordinary members | None |
| Member creation of repositories | Disabled |
| Member creation of Pages sites | Disabled |
| Member forking of private organization repositories | Disabled |
| Deploy key creation for organization repositories | Disabled |
| Enforced organization-wide 2FA | Not yet verified or activated |
| Additional organization owners, teams, and outside collaborators | None provisioned as part of this commissioning |

Some member controls, such as authority to invite collaborators, delete repositories or change visibility, are managed separately by GitHub and need further manual verification in organization settings before future non-owner members are invited. **Do not presume that default permission None disables every administrative feature.**

## Research repository protections

The public repo retained the protected `main` branch, required public contract checks, signed commits, no force push, no deletion, linear history, required PR entry and resolved conversations. GitHub Actions is restricted to selected GitHub-owned SHA-pinned actions with read-only workflow permissions and outside-fork workflow approval.

Secret scanning and push protection required reenabling after the organization transfer; both were restored. CodeQL default setup was also restored using the extended queries for Python and GitHub Actions, and its restored initial scan completed successfully. These are point-in-time reports, not perpetual attestations.

## Not proof of account isolation

The owner controls the organization through the same personal GitHub login. A compromised login or broad-scope machine token could still affect other repositories it can reach. Repo branch rules and file scanners do not prevent every form of unauthorized account access.

The existing machine authentication posture is outside the authority of this public repository. Do not paste personal tokens into issues or attempt to rotate credentials from collaboration requests. Moving to a repo-scoped GitHub App or fine-grained token requires separately enumerating existing integrations, then owner approval and staged replacement.

## Collaboration access

Independent human and AI researchers may read public content, open discussions, create issues, and propose pull requests under GitHub's public contribution model. Doing so does **not** grant membership in GhostMesh Lab, repository write access, signing keys, credentials, system-operator roles, private repository access, or execution rights.

Keep substantive contributors at public discussion and fork-PR level until a separate maintainer policy, privacy checks, and independent review arrangements are approved. Never assume a GitHub identity is proof of autonomous-agent identity.

## Preservation and migration notes

The old owner/repository URL automatically redirects, but it is not canonical. Public documents, the research manifest, examples, and issue templates should refer to this organization namespace. Avoid creating a new repository at the old location, which can destroy redirects.

See [REPOSITORY_OPERATING_MODEL.md](REPOSITORY_OPERATING_MODEL.md), [SECURITY.md](../SECURITY.md), and [GOVERNANCE.md](../GOVERNANCE.md) for local operating policies.

## Remaining gates

1. Confirm account phishing-resistant 2FA, recovery codes, security keys, authorized sessions, and third-party OAuth/GitHub App grants in GitHub account settings.
2. Reconcile or replace any broadly scoped token only after all current users of that credential are identified, then use scoped credentials appropriate to each system.
3. Verify member privileges that could not be fully controlled with the available authenticated API.
4. Assign any future independent PR reviewer through an explicit human decision, not automatically because a researcher contributed an issue.
5. Continue monitored secret scanning, CodeQL, disclosure review, and historical provenance checks. **Zero matches in a heuristic scan does not establish absence of PII or secrets.**
