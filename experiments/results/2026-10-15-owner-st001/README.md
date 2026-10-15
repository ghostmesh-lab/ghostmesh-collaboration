# GhostMesh ST-001: Owner-operated execution receipts (2026-10-15)

**Status: PUBLIC RESEARCH CANDIDATE, NOT MERGED, NOT FORMAL RELEASE, NOT INDEPENDENT SCIENTIFIC REPRODUCTION.**

This directory contains executed local tests and raw model outputs, not just a design proposal. This result was prepared and run on owner-operated systems, then publicly disclosed for scrutiny. Reviewer conclusions are *attributed post-hoc interpretations*, not blinded benchmark scores.

## Source and chain of evidence

- Original GhostMesh Lab synthetic ST-001 fixture: `ea1a9a443e3b80d7140dacd8f4869af90e6945c7546ad6cf39dbcb2b89ffbf5d` SHA-256.
- Frozen answer-suppressed derivation code: [PR #25](https://github.com/ghostmesh-lab/ghostmesh-collaboration/pull/25), exact head `7e69235d385d1578cb6312f25aa02752f7387ede` (still unmerged when this candidate was prepared).
- Derived participant input: `b1da69893a20143b6db8a396ffd0cb69e88df6197f1402c408382b1f2f08bc98` SHA-256.
- SAGE's separately sponsored McNugget run: [SAGE #432, raw answers](https://github.com/dp-web4/SAGE/issues/432#issuecomment-6184645543). Our work does **not** claim to reproduce its model/runtime.
- This publication changes **no** frozen ST-001 fixture, reference evaluator, SAGE artifact or production runtime.

## Experiment A: Local model behavior

**Study:** `GM-ST001-LOCALQWEN-20261015-01`, `local_model_protocol.json` generated *before inference*; SHA-256 `f937984d4a8e2bd0871e4f0de03ee2f45287ad69df9fbeea1bc6c9dc6f131c46`.

The existing Qwen2.5 14B local vLLM model was queried with the exact derived input at `temperature=0`, `seed=42`, no tools, no external model API, and no system changes. Conditions were (a) one prompt containing all nine questions; (b) nine isolated stateless prompts, each containing the same evidence and one question.

- Inference: **10/10 HTTP requests returned a response**, not 10/10 correct answers. **9/10** finished normally; isolated **Q6** stopped at its output-token cap.
- Bundled condition: input 975 tokens, output 573 tokens, 12,560 ms.
- Nine isolated requests combined: 7,654 input tokens, 891 output tokens, summed request time 19,142 ms. Inputs were repeated, so totals are not normalized.
- Raw prompts, response text, usage, finish reasons and model identification: [`local_model_raw.json`](local_model_raw.json); exact SHA-256 `71025cf706524adfd0258167fa76131052ab2f768e894b1fe0e36cb69ac8e438`.
- Captured execution script: [`local_model_st001.py`](local_model_st001.py) (environment-specific original, included for source custody).

**Post-hoc evidence-based findings:** E1's `reported_success: true` was promoted to proof of execution in both Q4 conditions, a mistake *of the same kind* as the one in McNugget, not evidence of identical causes. Bundled Q9 retained unknown inferences while isolated Q9 incorrectly declared none. Isolated Q6 mixed a causality warning with unsupported effect narration before truncating. Q1 also revealed ambiguity because the participant-visible event data does not explicitly label a `T4` identifier. Q2, Q5 and Q8 contained useful distinctions. See verbatim responses in JSON; do not infer an accuracy score.

**Study limits:** Single run per condition, no randomization, unequal token exposure and output limits, no longitudinal memory, no calibration, no blinded scoring, and no evidence that the original McNugget run was independently reproduced. No causal conclusion about presentation format.

## Experiment B: Deterministic adversarial controls

**Study:** `GM-ST001-OWNER-20261015-MECH-01`. [`PREREGISTERED_SCOPE.json`](PREREGISTERED_SCOPE.json) SHA-256 `0e4a8bc5643d371c971ac2fab957edcdd4c70639a9ca5c46006fe76763fd7e7e`.

[`ghostmesh_adversarial_controls.py`](ghostmesh_adversarial_controls.py) SHA-256 `ce6df6dae5ad626ee1fe07d8392f8f9aba780a6cf391db7013a28ac30b52160d` is a standalone, standard-library Python suite. Its original execution returned **30/30 PASS**; see [`RUN_LOG.txt`](RUN_LOG.txt).

```sh
cd experiments/results/2026-10-15-owner-st001
python3 ghostmesh_adversarial_controls.py
sha256sum stale-truth.json peer-input.json local_model_raw.json local_model_protocol.json
```

These are authored *deterministic* fixture and lineage assertions, including temporal mutations, missing ancestors/cycles, the still-valid N1 control, source repetition, and reported execution versus independently demonstrated effects. Passing does not prove model competence or deployed agent governance. Counterfactuals do not alter the frozen source.

## Experiment C: Exact-head Mac Studio reproducibility

An owner-controlled, fresh detached checkout at the same PR #25 head yielded 6/6 focused peer-input tests, 91/91 full Python tests after isolated pinned dependencies, a matching four-file unsigned ST-001 manifest, and a passing publication checker with release gates still open. The initial unprepared run had a missing-`jsonschema` import and was not counted as a pass. Mac-native exact test logs and their SHA-256 hashes are stored separately on the owner Mac; see [`MAC_EXECUTION_READBACK.md`](MAC_EXECUTION_READBACK.md). These tests do not validate model reasoning.

## Research conclusions and outstanding checks

1. **Observed model limitation:** Multiple responses mistake a harness report for verified execution. Treat this as an evidence-class promotion failure.
2. **Observed prompt-condition inconsistency:** UNKNOWNs disappear under isolated Q9, while isolated Q6 truncates. No cause assigned.
3. **Fixture-design limitation:** The frozen questions reference T1/T2/T4, while participant-visible JSON does not name T4. Do not retrospectively modify the frozen study.
4. **Important gap:** Nothing here establishes persistent-belief correction, reliable effect witnessing, live credentialed execution or safety.
5. **Next experimental work:** Frozen, repeatedly sampled presentation-factor study; separately preregistered multi-wake belief revision; independent evaluations with known source ancestry and disclosed exposure.

No live infrastructure was touched by these experiments. No third-party authorization, license ratification, independent human review, cross-lab certification or merge approval is implied. Code and results are new owner-generated research material, offered for review while [licensing #1](https://github.com/ghostmesh-lab/ghostmesh-collaboration/issues/1) and [formal release #14](https://github.com/ghostmesh-lab/ghostmesh-collaboration/issues/14) remain unresolved.

For the issue thread and methodology, see [GhostMesh Lab ST-001 #2](https://github.com/ghostmesh-lab/ghostmesh-collaboration/issues/2).
