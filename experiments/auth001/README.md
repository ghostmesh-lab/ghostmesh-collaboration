# AUTH-001 | Approval-to-execution identity, synthetic reference study

**State:** owner-authored public-synthetic experiment candidate. **Executed locally; not independently reproduced, not integrated with GhostMesh, not a security certification.**

## The question

Can an apparently valid approval be reused for a materially different target, filesystem object, content digest, or actor between decision and use? Can a narrowly bound mechanism reject the substitution **without denying an unchanged authorized action**?

This study follows [Dennis's October 15 public Commons challenge](https://ghostmesh.slack.com/archives/C0C6KV5SMGT/p1792083799355889) and the related public [SAGE #454](https://github.com/dp-web4/SAGE/issues/454), [Hestia #627](https://github.com/dp-web4/hestia/issues/627), [Hestia #1229](https://github.com/dp-web4/hestia/issues/1229), and [Hestia #1290](https://github.com/dp-web4/hestia/issues/1290) findings. **No Hardbound private code, screenshot, trace, or confidential material is copied into this study.**

## Experiment

Run `python3 -m unittest tests.test_auth001_reference -v` from repository root, or `python3 tests/test_auth001_reference.py`. All filesystem data are disposable generated canaries in a temporary directory. Tests do not execute scripts, access real credentials, modify policies, touch production services or communicate with other agents.

| Paired case | Intentionally naive reference | Guarded reference | Observable criterion |
| --- | --- | --- | --- |
| Symlink to out-of-scope resource | Read by pathname follows symlink and returns artificial outside canary | Single-component `open(dir_fd=..., O_NOFOLLOW)` | Denial, while ordinary in-scope file succeeds |
| Directory-root substitution | Late pathname resolution follows replaced symlink root | Previously opened directory descriptor remains bound to original inode | Different observed bytes from naive path; approved content from handle |
| Changed content after approval | Name/path-only access reads new bytes | Read exact bytes once and compare SHA-256 to approved digest | Changed digest denied; unchanged bytes still available |
| Preview/masked approval collision | Authorization identity hashes only a 220-byte preview | Hash complete canonical operation bytes, including relevant principal/revision | Naive collision; distinct full hashes |

Additional tests separately preserve the absence of evidence of physical effects, distinguish skipped from successful security checks, and confirm basic legitimate-allow controls.

### Reproducibility and scoring

The 20 named tests are human-authored, **unblinded deterministic reference assertions**. The entire code is both the mechanism under test and the test oracle, so passing the suite verifies those sample rules, not external agent cognition or actual authority enforcement. This initial work was designed and executed before formal GitHub publication, **not prospectively preregistered**.

A first local execution on owner Mac Studio Python 3.14.7 passed **20/20 tests**. See `RUN_LOG.txt` and `SHA256SUMS.txt` for exact bytes. Hosted exact-head CI and independent review must be checked separately.

### Important limitations

- Guarded `O_NOFOLLOW` example deliberately permits only a single filename component, with an already-approved directory handle. It is not a general-purpose secure path resolver and does not prove multi-component sandbox containment.
- A digest comparison alone does **not** make authorization and effects atomic. Real execution must use the same immutable/safely opened object whose content and context were validated, without reopening a mutable name after the check.
- Complete approval identity in a production system requires more than a command digest: principal, action type, exact parameters, target object identity, content or revision commitments, jurisdiction, evidence/policy version, delegation validity, single-use consumption and commit boundary need explicit semantics.
- An approval rejection may be wrong, too. Legitimate positive cases and false-denial metrics are required.
- No concurrency-race stress, privilege escape, runtime integration, multi-agent execution, production deployment, cross-platform assurance or independent reproduced result is claimed.

## What should follow

1. **AUTH-001B:** Extend exact-byte synthetic fixtures with policy/source revisions, multiple path components, symlink swaps during lookup, revoked grants, one-time redemption and mismatched owner grants. Add Linux `openat2` scoped-path checks on a qualified runner where possible. Preserve expected false denials.
2. **AUTH-001C:** Audit GhostMesh's actual broker/publisher/compute dispatch *privately*. Do not equate this toy test with real protection. Report only sanitized failures/proofs with explicit approval.
3. **AUTH-001D:** Invite independent Web4/Hestia reviewers to reproduce the same source SHA and report disagreements, including tests skipped because the host cannot enforce a primitive.

Owner review and release licensing remain open under [license #1](https://github.com/ghostmesh-lab/ghostmesh-collaboration/issues/1) and [release #14](https://github.com/ghostmesh-lab/ghostmesh-collaboration/issues/14). Do not merge or grant operational access solely on the basis of passing toy tests.

**Doctrine:** An approval is a grant bound to a specific act, not a persuasive description of an act.
