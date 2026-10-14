# ST-001: independent peer-run preparation v0.1

**State: REVIEW CANDIDATE, NOT RATIFIED OR EXECUTED BY AN INDEPENDENT LAB.**
**Sponsor:** Tony Malott, GhostMesh Lab. **Governance:** issue [#2](https://github.com/ghostmesh-lab/ghostmesh-collaboration/issues/2); [SAGE #432](https://github.com/dp-web4/SAGE/issues/432) is an independent voluntary participant track.

## Why this change

The frozen source fixture embeds `evaluation_expectations` and answer-bearing event fields. A participant shown those annotations can repeat the answer without independently classifying evidence. A second derived input suppresses those fields and two revealing event-type labels. The source fixture, reference evaluator, unsigned bundle and the published nine evaluation questions remain unchanged.

**This is answer-suppressed partial blinding, not a secret blind or held-out benchmark.** The public original fixture and reference output remain discoverable. Prior exposure, intentional or accidental, must be disclosed. Published event relationships such as `derived_from`, action correlation and reported harness success are still visible. No claim of independent cognitive competence follows from a correct static analysis.

## Source and derivation binding

- Source repository: `ghostmesh-lab/ghostmesh-collaboration`.
- Source `main` commit inspected before preparation: `374b8d3f38aa8357b39716c20d42c17440e689ef`.
- Frozen input: `fixtures/v0.1/stale-truth.json`.
- Expected original fixture SHA-256: `ea1a9a443e3b80d7140dacd8f4869af90e6945c7546ad6cf39dbcb2b89ffbf5d` (also recorded in the unsigned ST-001 bundle).
- Derivation program: `tools/prepare_st001_peer_input.py`; reject a source-byte mismatch rather than silently processing an updated fixture.
- Derived answer-suppressed input SHA-256 from candidate tool: `b1da69893a20143b6db8a396ffd0cb69e88df6197f1402c408382b1f2f08bc98` (1957 bytes). The reported hash is not an external signature.

## Reproduce locally, offline

From a checkout pinned to the reviewed commit of this candidate PR:

```sh
python3 -m unittest tests/test_st001_peer_input.py -v
python3 tools/prepare_st001_peer_input.py > /tmp/st001-peer-input.json
shasum -a 256 /tmp/st001-peer-input.json
python3 tools/verify_bundle.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 tools/check_publication.py
```

All operations are local and synthetic; do not run service restart commands or provide operational credentials. `tools/evaluate_stale_truth.py` demonstrates a deterministic reference and **must not be used as an independent evaluator**.

## Pre-registered tracks

**Track A: annotated reproduction.** Inspect and reproduce the unchanged public source and deterministic evaluator. Score byte fidelity and correct description of limits only. Not independent evidence discovery.

**Track B: answer-suppressed peer interpretation.** A separately operated participant receives the derived JSON and [the nine frozen questions](ROUND_ONE_EXPERIMENT.md), without the annotated source or reference result in its submitted prompt. Report any preexisting exposure. If no independent or suitably uncontaminated evaluator exists, report `NOT_RUN` or `UNKNOWN`, not PASS.

The event labels `O1`, `O2`, `C1`, `A1`, `P1`, `E1`, `O3` and `N1` are preserved. The derivation hides original `evaluation_expectations`, `truth_at_time`, `confidence`, `new_independent_observation`, `independently_verified`, `is_a_live_grant`; it maps `inherited_claim` to `claim` and `negative_control_observation` to `observation`. This does **not** establish source truth or conceal source ancestry.

## Peer result contract

Use the [research-result v0.1 schema](../schemas/research-result.v0.1.schema.json) where appropriate. Publish exact source and derived-input hashes, model and tool versions, sponsor and claimed actor identity, exact question/prompt, tool and reference access, prior reference exposure, evaluation configuration, local start/end times, cost and latency if known, and independent review status.

Return event-by-event and question-by-question conclusions and evidence IDs; separate historical validity, current evidence, inherited ancestry, permission, execution report, independently observed outcome, causation and remediation authority. Explicitly retain the N1 still-applicable historical-information control. Include raw disagreement, false promotions, unsupported confidence, abstention and `UNKNOWN`. No aggregate benchmark score without the per-case trace.

**Maturity states must remain distinct:** planned, coded, locally tested, reviewed, merged, externally run and independently reproduced. A model response and a schema-valid report do not prove physical effects, legitimate external authority or persistent belief repair.

## Separate experiments and responsibilities

- [FG-001 / SAGE #438](https://github.com/dp-web4/SAGE/issues/438) is **separate**, not a mutation of ST-001. Its matched nonintervention cases (no jurisdiction, discretionary refusal, breached obligation, ineffective intervention) require an independently frozen fixture and review.
- Hestia synthetic correlated and broken-correlation receipts belong in Hestia, not duplicated here. Authority-lifetime and persistent belief-repair tests require separate fixtures and evidence standards.
- GhostMesh/Tony owns review of this public candidate and disclosure scope; Dennis and SAGE are **invited**, not assigned, to contribute an independent run in their own repo. Guillaume or another external reviewer may independently examine methodological assumptions if they choose.
- The [license issue #1](https://github.com/ghostmesh-lab/ghostmesh-collaboration/issues/1) and [formal release gate #14](https://github.com/ghostmesh-lab/ghostmesh-collaboration/issues/14) remain open. Link to third-party work instead of copying copyrighted content or implementation code.

## Containment, rollback and stopping conditions

**No Production, secrets, private evidence, shared memory, cross-system dispatch, repo permission changes, real-world actuation, or agent enrollment.** If fixture hashes differ, authorship/rights cannot be established, a runner saw the answer key without disclosure, output leaves the public synthetic boundary, or source review fails, stop and label the result unqualified. Rollback is reverting this candidate branch/PR; the original fixture and unsigned bundle remain intact.
