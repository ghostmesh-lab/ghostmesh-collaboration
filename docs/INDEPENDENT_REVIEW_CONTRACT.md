# Independent human review: admission without account compromise

**Status: proposed process.** Only `pinklon` has collaborator rights now; mandatory independent approvals are **not** enabled.

## Roles

- **Public contributor:** may read, discuss and propose PRs, under GitHub's existing public visibility. No organization membership required.
- **Independent scientific reviewer:** evaluates reproducibility and methodology. A review can be submitted in a public issue without granting repository write permission or exposing private data.
- **Security reviewer:** assesses threat boundaries, disclosure and PR workflow changes. Must not request credentials, account tokens or source outside the public repo.
- **Release approver:** a named, legitimately appointed human with explicitly scoped repository rights. Only after a separate owner decision and verified GitHub settings.

An AI may assist any of the above but may not secretly impersonate independent human approval.

## Reviewer record

A meaningful review states: public author identity, source commit, exact tested files, reproducible method, observed vs inferred results, competing interpretation, disclosure/privacy status, requested correction and reviewer independence. The reviewer need not endorse GhostMesh's goals.

## Immediate safe path

Request **public issue-based independent critique** first. A named person does not become a maintainer or release approver merely because they comment. When licensing and governance have been accepted, the owner can appoint a reviewer with the least necessary role and then enable one required approval/code-owner review in GitHub. Test solo-owner recovery before enforcing a configuration that could deadlock.

## Independence isn't a cryptographic checkbox

Signed Git commits establish narrowly defined historical integrity and key-authorship assumptions. They do not establish a reviewer has no conflicts, independently ran the experiment, or that an agent's declared sponsor is authentic. Reviewer independence depends on organizational separation, actual method, disclosures and adjudication, as well as cryptography when proof of authorship is needed.

## Existing blockers

- No authorized external reviewer.
- No accepted contribution license for substantial outside source.
- No independently reproduced ST-001 result.
- Broad owner-side machine token dependencies unresolved; no public app can fix them.

No invitation or access grant is implied by this document.
