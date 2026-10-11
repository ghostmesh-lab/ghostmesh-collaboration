# Example artifacts and limits

This directory provides **illustrative** records and a deterministic fixture-specific result. Neither is an independent model benchmark, real observation, identity proof, or executable permit.

## ST-001 fixture and reference output

- Input: [stale-truth.json](../fixtures/v0.1/stale-truth.json)
- Local deterministic implementation: [evaluate_stale_truth.py](../tools/evaluate_stale_truth.py)
- Example output: [stale-truth-reference-output.json](stale-truth-reference-output.json)
- Research rules: [Round One preregistration](../experiments/ROUND_ONE_EXPERIMENT.md)

You can reproduce the output with:

```bash
python3 tools/evaluate_stale_truth.py
```

The output includes `fixture_sha256`. If you change the input fixture, the hash and potentially the interpretation change. Explicit `UNKNOWN` fields preserve information the input never established.

**Do not mistake matching the reference output for an independent AI result.** The fixture, expectations and reference evaluator originate from the same research team. Independent reproduction requires a separately operated method and transparent report of differences.

## Research result interchange (not an attestation)

A separate [research-result schema](../schemas/research-result.v0.1.schema.json) and [non-executed template](research-result-template.v0.1.json) distinguish an illustrative placeholder, an author-reported result, and an independently reproduced result. The template's claims are marked NOT_EVALUATED. Validation checks structure and fixture digest, but it cannot establish honesty, independent identity, or scientific quality.

## Proposed research envelope

- [Schema](../schemas/research-envelope.v0.2.schema.json)
- [Sample proposal](research-proposal.v0.2.json)
- [Agent/human protocol](../protocol/INTERACTION_CONTRACT_V0_2.md)

The envelope describes who claims to speak, who sponsors them, what they propose, and what evidence grade they assert. The repo cannot verify a real actor's identity or authority simply by parsing JSON.

Please use [security reporting](../SECURITY.md) if you discover protected information. This directory is public and must contain only owner-reviewed safe synthetic samples.
