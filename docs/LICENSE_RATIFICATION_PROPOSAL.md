# Contribution rights: precise options for owner decision

**Status: proposal only.** Do not publish a `LICENSE` file or accept substantive third-party copyrighted contributions under assumed terms until an authorized owner explicitly ratifies exact texts and scope.

The aim is to support reuse without making independent collaborators silently surrender rights or import incompatible materials.

## Proposed matrix

| Original artifact | Candidate license | Rationale and open issue |
| --- | --- | --- |
| GhostMesh Lab's original executable research code and reusable validation scripts | **AGPL-3.0-only** | Dennis proposed AGPLv3. Source availability including network-service use may support transparent research, but reciprocal requirements can constrain reusers. Confirm owner owns every contributed line. |
| Original explanatory text, diagrams, technical briefs and research proposals | **CC BY 4.0** | Clear reuse with attribution, including derivatives. It is not the recommended default for executable code. Check trademarks and third-party references separately. |
| Wholly synthetic, independently created benchmark fixtures and result datasets with clear rights | **CC0 1.0** | Broad experiment portability; cannot waive rights one doesn't own, and may be inappropriate for results incorporating external confidential or copyrighted material. |
| External references or collaborator materials | **Their existing licenses, or links only** | Attribution and link do not confer redistribution rights. A project's public availability is not blanket permission to relicense it. |
| GhostMesh name, mark, and partner badges | **Separate trademark/brand permission** | Copyright and open data licenses do not grant implied endorsement or trademark use. |

AGPLv3 and the CC licenses have distinct legal effects. This is a recommendation for discussion, not a legal opinion.

## Explicit ratification decisions

1. Confirm owner rights for each present file and generated code origin.
2. Decide code license (AGPL-3.0-only vs alternative) and notice location.
3. Decide document license (CC BY 4.0 vs alternative) and attribution method.
4. Decide dataset license (CC0-1.0 vs alternative), including restrictions imposed by source ownership.
5. Decide inbound contribution process: submitter ownership/authority representation, license compatibility, third-party notices, and no assumed assignment of all IP.
6. Decide license effective scope and handling of previously published files or outside contributors' independent work.
7. Record owner-approved exact SPDX and versioned license texts in a separate protected PR.

The repository may publish this **proposal** and accept discussion now, but license status remains OPEN_UNRATIFIED until those choices are made.
