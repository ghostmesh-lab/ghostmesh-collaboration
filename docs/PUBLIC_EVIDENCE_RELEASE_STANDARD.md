# Public evidence release standard

**Draft review policy.** A secure collaboration depends on sharing enough to test claims without sharing what can compromise people or systems.

## Release categories

- **OPEN:** Original public specifications, synthetic examples, non-sensitive architecture and author-approved results.
- **REVIEW:** Sanitized operational excerpt or sensitive research conclusion requiring owner and subject-matter disclosure review.
- **RESTRICTED:** Keys, tokens, live infrastructure details, private corpora, raw operational logs, personal records, non-public research and any material whose release would expose a participant. Do not submit here.
- **UNKNOWN:** Classification uncertain; stop publication pending a responsible owner decision.

## Minimum proof-package manifest

An independently usable public claim should include:
1. Exact claim and the scope of what was tested.
2. Source revision(s) and hash of actual public artifacts.
3. Producer/sponsor identity, authorship and any known independent reviewer.
4. Observation timestamp **and** recorded/reported timestamp, with provenance.
5. Author-reported vs independently reproduced status and its coverage denominator.
6. Test method, expected outputs, negative controls, and failure conditions.
7. Results that include FAILURE, INCONCLUSIVE and UNKNOWN, not just success.
8. Privacy/license review record, exclusions, and correction route.

A raw hash does not establish truthful source content. A signed report is still a report. A working service observed at one instant says nothing universal about all times.

## Sanitization requirements

Use synthetic identities and public, fictional case data. Strip personal names or third-party contact details unless publicly relevant and permitted. Omit actual networks, internal systems, host IDs, PIDs, operational timestamps tied to private incidents, IP addresses, private filenames, secrets, high-risk attack recipes and cross-tenant identifiers.

Review filenames, commit metadata, embedded image metadata, encoded payloads, prompts, and URLs as well as visible prose. Public PR CI runs *after the submission is already public*, so sensitive data must be removed **before** upload.

## Claim grades

- `PROPOSED`: a conjecture or intended method.
- `AUTHOR_REPORTED`: assertion by the producing team, not externally repeated.
- `BOUNDED_TESTED`: explicit test passed under bounded inputs.
- `INDEPENDENTLY_REPRODUCED`: a separate party repeated the stated test and reported methods.
- `UNKNOWN`: missing or insufficient evidence for that aspect.
- `DISPUTED`: material conflicting evidence or interpretation.

Do not silently upgrade an author-reported claim to independent proof because several agents repeat it.

## First release

The existing public ST-001 fixture and a deterministic, purely synthetic evaluator are eligible as research examples. A **sanitized real GhostMesh operational receipt** is a separate future release requiring exact source revision, human owner review and proof that no privileged context is embedded.
