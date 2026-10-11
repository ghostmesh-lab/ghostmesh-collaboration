# First comparison proposal: evidence -> belief -> authority -> effect -> repair

**Status: proposed; not a ratified shared benchmark or completed cross-system run.**

This project proposes an exchange of static, entirely synthetic artifacts so independent systems can confront the same evidence without integrating runtimes or sharing credentials.

## Initial fixture

[stale-truth.json](../fixtures/v0.1/stale-truth.json) describes a service outage that was genuinely observed at T1, resolved at T2, and incorrectly carried into a decision at T3. T4 captures a separate later measurement. An older still-valid evidence item is included as a **negative control**, preventing the trivial heuristic that every old observation must be rejected.

## Candidate evaluation criteria

1. Preserve original source ancestry; ten repetitions from one source are not independent corroboration.
2. Keep the observation's **time of truth** separate from the time it was recorded, replayed, or interpreted.
3. Identify which facts are independently observed, actor-reported, inferred, disputed, or **UNKNOWN**.
4. Distinguish an authorized and executed command from a verified outcome.
5. State whether evidence **supported** a belief versus whether it **caused** the decision.
6. Preserve that belief correction does not itself grant authority for remediation.
7. Record valid disagreement and abstention, not only affirmative answers.
8. Preserve independent system sovereignty; no live integration required.

## Proposed next cases

- Duplicated misinformation from a single inherited observation.
- Signed, authentic but false observation from a compromised source.
- An execution receipt reporting success when the service remains down.
- Revocation or role change between decision and execution.
- A legitimate objective wrongly challenged, and a harmful objective properly authorized.

Any future tests should fix the exact source revision, evaluator, expected distinctions, negative controls, time/compute costs, and data classification **before** comparative execution. Results are not pre-certified by this proposal.
