# AUTH-001B | Authorization under concurrency and failure

**Status: source candidate only. Not peer reviewed, not ratified, not integrated, not released.**
**Sponsor:** Tony Malott / GhostMesh Lab. **Preregistration:** [AUTH-001B #29](https://github.com/ghostmesh-lab/ghostmesh-collaboration/issues/29).
**Origin:** [AUTH-001 #27](https://github.com/ghostmesh-lab/ghostmesh-collaboration/issues/27), [draft PR #28](https://github.com/ghostmesh-lab/ghostmesh-collaboration/pull/28), and Dennis/NOVA's [October 16 challenge](https://ghostmesh.slack.com/archives/C0C6KV5SMGT/p1792194665275909).

## Bounded question

Can a grant's claimed actor, resource, content digest and policy version remain bound through *synthetic authorization redemption*, even when two callers compete, delegation changes, or the caller misses a response?

This is a deliberately simplified **SQLite-based toy authorization reference**, not the GhostMesh broker, Hestia, a safe general path resolver, an operating system process executor or physical-effect witness. It never runs a script. Its 'COMMITTED' state means **authorization redemption committed in SQLite only**. No network, credentials, production data, private code or agent dispatch are used.

## Method and falsifiers

- Each attempt opens its own connection to one local synthetic SQLite file. `BEGIN IMMEDIATE` serializes competing grant state updates in this example. The honest single-use invariant expects exactly one `BOUND_MATCH` and one `GRANT_COMMITTED` for two racing attempts on the same grant; separate grants must both pass.
- Compare wrong actor, resource, selected input bytes and policy version against the exact grant. Failed attempts must not consume a still-issued grant. Test normal operation as a positive control.
- Revocation before redemption prevents use; revocation after a **synthetic authorization commit** does not reinterpret historical authorization. This is a chosen local rule, not universal governance.
- Simulate lost acknowledgement after the database commit. The caller receives `ACK_LOST_EFFECT_UNKNOWN`, while replay is denied. A spent authorization **cannot establish that any real-world effect happened** and does not guarantee exactly-once effects.

Use:

```sh
python3 -m unittest tests.test_auth001b_reference -v
python3 -m unittest discover -s tests -p 'test_*.py'
python3 tools/verify_bundle.py
python3 tools/check_publication.py
```

Record exact tested commit, Python/SQLite versions, fixture/tool SHA-256, test outputs, nondeterministic schedules and failures. The unit tests are author-written and unblinded; pass counts only establish the behaviors of this model. For external cross-platform reproduction or operational claims, require separately scoped approval and independently preserved evidence.

## Counterexamples still required

- Fault injection *inside* a real atomic commit and crash/recovery on disk, not merely losing the response after a successful transaction.
- Actual execution of immutable checked bytes, multi-component path walks, kernel-level race handling, process identity binding, and external effect verification.
- Revocation and redemption competing truly concurrently, policy version update ordering, multiple replicas, queue retries, partial failures and false-denial rates at scale.
- Naive reference controls, property-based fuzzing, external peer implementations, independent outcome witnesses and signed source custody.

**Risks, containment and rollback:** This branch/PR is review-only public synthetic C1. No live grant, credentials, private data, operational code change, deployments or cross-system permission. Owner can close or revert candidate without Production rollback; public copies cannot be recalled. Formal release, contribution licenses and independent reviewer gates remain open.

**Scientific posture:** Seek flaws in both GhostMesh and Web4/Hestia assumptions. No leaderboard or claim that a particular AI is smarter.
