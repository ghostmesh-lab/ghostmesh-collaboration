# Publication readiness: public research, not a production federation

**Status:** CANDIDATE_NOT_RELEASED. The repository's source is already publicly readable. This gate controls whether we formally advertise a release, certify an experiment, or invite broader contribution. This is not an audit of private GhostMesh production.

## What can be published now

- Owner-authored North Star, GhostMesh architectural description, definitions of epistemic/authority/effect/purpose integrity.
- Machine-readable **offline** research proposal with no live enrollment, dispatch, identity proof or authority grant.
- Synthetic ST-001 fixture, deterministic reference evaluator and its narrow negative tests.
- Privacy policy, threat model, provenance limitations, and public issue/discussion process.
- Exact repo-commit citation plus public methods for a reader to reproduce the synthetic result.

## Release checklist

| Gate | Present state | What changes it |
| --- | --- | --- |
| Public architecture and provenance description | Present | Owner approves disclosure and corrects overstatements |
| Offline tests and protected-branch CI | Configured | Green checks for exact proposed revision |
| Public link integrity | Automated local check | Broken paths fixed, external targets separately reviewed |
| Secret scanning, push protection, CodeQL | Enabled at last live review | Must refresh API status when releasing |
| License for code/docs/fixtures | **OPEN** | Record owner decision in [issue #1](https://github.com/ghostmesh-lab/ghostmesh-collaboration/issues/1), check inbound rights and commit applicable licenses |
| Independent reviewer | **NOT CONFIGURED** | Explicitly appoint appropriately limited reviewer or adopt owner-ratified equivalent, then enforce it |
| Independently reproduced real operational evidence | **NOT DONE** | Release only a sanitized, scoped, separately verified package via [issue #12](https://github.com/ghostmesh-lab/ghostmesh-collaboration/issues/12) |
| Personal/VPS GitHub authorization separation | **OPEN outside repository** | Credential inventory, least-privilege replacement with rollback |
| Human release approval | **REQUIRED** | Explicit owner release decision after reading exact diff and cited evidence |

**Do not convert a green static test into evidence that a live network, an agent identity, a production outcome, or a safe objective has been verified.**

## Integrity model for future release packages

A qualifying release should freeze source revision, fixture hash, evaluator identity/version, negative-control cases, independent reviewer, what it proves, what it cannot establish, and how later corrections are recorded. When a claim depends on privately owned systems, disclose a distinct independently reviewed sanitized artifact; never publish raw production receipts, source paths, credentials or private messages here.

## Publication threat model

- **Before CI:** issues, PRs and comments become publicly visible before automated scanning. Require local review prior to submission.
- **During CI:** PR-controlled code can change its own tests or workflows. Maintain independent human review of sensitive changes; do not infer immutable execution controls from a PASS result alone.
- **After publication:** deleting content does not erase forks, archives or mirror copies. An exposed credential must be revoked at its issuing authority.
- **Outside this repo:** organization ownership does not isolate a compromised personal admin account or classic multi-repo token.
- **Shared research:** a model-generated response, signature or multiple repeated agents is not independent evidence.

## Concretely next

1. Resolve licensing and contribution policy first. This is a human rights/ownership decision, not a CI flag.
2. Approve a safe independent review mechanism for public code and security contract changes.
3. Independently reproduce the first synthetic comparison against a pinned commit.
4. Prepare one genuinely sanitized real GhostMesh observation/decision/receipt package, with private-side screening before upload.
5. Once all gates are satisfied, cut an annotated research release that calls out experimental status and no operational federation.

[Machine-readable readiness record](../publication-readiness.json). This file is not an authorization system, and its gates must be rechecked against live GitHub state at publication time.
