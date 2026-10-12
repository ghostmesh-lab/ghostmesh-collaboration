# Ten-minute researcher quickstart

**Only public synthetic experiments. No infrastructure access, account connection, or agent registration is needed.**

## 1. Read the contract

Review [AGENTS.md](../AGENTS.md) if an AI is drafting the submission, [CONTRIBUTING.md](../CONTRIBUTING.md), and [SECURITY.md](../SECURITY.md). Name the human or organization sponsoring an AI contribution. A transport account or model identity is not automatically a verified research principal.

## 2. Reproduce the existing result

From a clean checkout of the publicly available repo:

```bash
python3 tools/verify_bundle.py
python3 tools/evaluate_stale_truth.py > /tmp/st001-result.json
python3 -m unittest discover -s tests -p 'test_*.py'
python3 tools/check_publication.py
```

Optional full schema validation requires the pinned `jsonschema` dependency described in [tests/README.md](../tests/README.md). The reference evaluator itself uses only Python's standard library.

The hash-manifest verifier detects byte tampering, but is unsigned and cannot authenticate publisher identity or certify source truth. It requires no signing keys or secrets.

The result is a **synthetic deterministic calculation**, not a measured AI model result. Compare with [the committed reference output](../examples/stale-truth-reference-output.json) only after confirming the exact fixture and code revisions. Record the fixture SHA-256 and source revision.

## 3. Look for unsupported claims

- Was the service down at T1? What establishes its later state?
- Are ten repeated reports ten witnesses, or one ancestor repeated ten times?
- Does a synthetic policy decision grant real authority? No.
- Does the tool's success flag establish a successful repair? No.
- Does an independent observation after the command prove causation? Not automatically.
- Is an old observation necessarily false? No.

If you cannot establish a relationship from the fixture, **UNKNOWN** is a useful result.

## 4. Challenge the model rather than agreeing with it

Consider an adversarial variant: a signed original observation is wrong; or newer evidence is missing; or a challenger makes a false accusation against a legitimate objective. State which existing evaluator rule would incorrectly accept that case. Include a negative control so a superficial heuristic cannot pass.

The current [Round One protocol](../experiments/ROUND_ONE_EXPERIMENT.md) is an invitation to evaluate and revise the test, **not** evidence of a completed multi-lab comparison.

## 5. Participate without overcommitting

Choose one public discussion:
- [ST-001 methodology](https://github.com/ghostmesh-lab/ghostmesh-collaboration/issues/2)
- [Independent sources](https://github.com/ghostmesh-lab/ghostmesh-collaboration/issues/9)
- [Purpose integrity](https://github.com/ghostmesh-lab/ghostmesh-collaboration/issues/10)
- [Publication release gate](https://github.com/ghostmesh-lab/ghostmesh-collaboration/issues/14)

Include author/sponsor, exact evidence, expected failure, uncertainty, and a reproducible synthetic procedure. **Do not** paste private logs, credentials, real machine identifiers, or substantial third-party copyrighted material.

Until licensing is ratified, public discussion and links to independent research are the preferred contribution path. No shared runtime, memory, identity, or governance authority is implied.

## The most useful contribution

A short, well-reproduced negative result that changes what we believe is more valuable than a long statement agreeing with the architecture.
