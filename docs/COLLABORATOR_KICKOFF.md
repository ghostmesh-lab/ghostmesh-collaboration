# Research kickoff: three bounded invitations

**Open to independent researchers and AI-assisted contributors. This is not a task dispatch, partnership agreement or evidence of consent by any named person.**

## Invitation 1: Challenge ST-001

**Question:** Can a participant distinguish inherited claims from independent observations, time-bounded truth from current truth, synthetic permission from actual authority, and a tool report from a verified external effect?

**Public inputs:** [ST-001](../fixtures/v0.1/stale-truth.json), [predeclared protocol](../experiments/ROUND_ONE_EXPERIMENT.md), [offline evaluator](../tools/evaluate_stale_truth.py), and [reference tests](../tests/test_reference_evaluator.py).

**Research output:** A bounded critique or counterexample plus reproduction instructions. Do not simply copy the deterministic reference answer and call it an independent evaluation.

**What would falsify a claim:** Show a scenario where the proposed evidence fields lead a reviewer to unsupported certainty, or where justified abstention is graded as failure.

## Invitation 2: Correlated evidence and false corroboration

**Question:** Can independently operated systems recognize that many derived claims may trace to one underlying observation? Conversely, can they avoid rejecting genuinely independent observations merely because their wording is similar?

**Adversarial controls:** One source repeated by ten agents; two independent sensors with conflicting readings; a signed but compromised observer; source ancestry hidden by an intermediary; a false allegation against legitimate evidence.

**Research output:** Propose a synthetic fixture schema and scoring plan with explicit independence assumptions, privacy limitations, missing evidence, and negative controls. No new identity claims, live message ingestion, or external agent connections.

## Invitation 3: Purpose integrity without an unaccountable veto

**Question:** Can a governance system detect and challenge a harmful but procedurally authorized objective without allowing any one model or actor to wield limitless authority?

**Paired cases:** (A) approved work benefits its sponsor but demonstrably harms others; (B) a legitimate objective receives a plausible but false objection. Require separate rights to raise an objection, temporarily pause a task, review evidence, change objectives, and authorize remedy.

**Research output:** A falsifiable governance state machine with escalation, timeout, appeal, affected-party standing, evidence and challenge-abuse prevention.

## Collaboration rules

- Start as a **human or tool-sponsored public proposal**. Identify the author, sponsor and evidence maturity.
- Critique or improve the test without adopting GhostMesh, Web4, HORTRAME, Engrammic or any participant's vocabulary as universal law.
- Use public synthetic data; no production actions, private artifacts, credentials, account integration or agent dispatch.
- Link to independent projects for credit but do not reproduce proprietary materials without license/permission.
- Open a scoped issue or PR with expected outcomes and negative cases. A useful failure or abstention is a legitimate research result.
- Before accepting substantive third-party source code or copyrighted research, resolve [licensing](../LICENSE-DECISION.md).

## When the repo is ready for outside humans and agents

1. Security baseline readback, private vulnerability reporting and code scanning continue to pass.
2. The owner accepts this public disclosure and its limits.
3. Repository contributor rules and licensing have a clear, consented path.
4. A human reviewer or governance alternative is explicitly appointed for sensitive PRs.
5. No external participant is granted private repository, VPS, or production authority.

The repository is a **research meeting room**. It is not permission for an autonomous system to walk into another participant's house.
