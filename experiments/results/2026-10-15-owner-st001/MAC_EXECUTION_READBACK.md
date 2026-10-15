# Owner Mac Studio ST-001 exact-head readback (2026-10-15)

**Research maturity:** verified local test execution, not cross-lab validation or Production deployment.

- Checkout: detached Git commit `7e69235d385d1578cb6312f25aa02752f7387ede` of `ghostmesh-lab/ghostmesh-collaboration`, the still-open PR #25.
- Canonical source SHA-256: `ea1a9a443e3b80d7140dacd8f4869af90e6945c7546ad6cf39dbcb2b89ffbf5d`.
- Derived input SHA-256: `b1da69893a20143b6db8a396ffd0cb69e88df6197f1402c408382b1f2f08bc98`.
- Python 3.14.7. Fresh temporary environment initially lacked `jsonschema`, leading to an import error during full test discovery. This failed attempt was not called PASS.
- After isolated installation of `jsonschema==4.23.0` and `cryptography==46.0.5`: **91/91 Python tests PASS**.
- Focused PR #25 peer-input tests: **6/6 PASS**.
- Unsigned four-file evidence manifest exact hashes: PASS.
- Offline publication checker: PASS; outstanding approval and licensing gates remain open.
- Log file SHA-256 (stored in owner-controlled Mac repository of research receipts):
  - `focused-tests.log`: `7755b455aaed302287d4046e4b4f8fed393f604f4fa128ee88f8a4877794c0f4`
  - `all-tests-venv.log`: `7ebae7f28774b534aa3e8d03aa5686f4bcd62352891aaad22312cda80e7198b0`
  - `bundle.log`: `3b50e891e9e2c540a261fac043365c5e3858c116a63fdce473a50e9b0197f3ac`
  - `publication.log`: `1e8eba2d2b064bf4acd35356fd9794bc616c3bb01276dd72f9cfb2be08470e71`

The native log files are retained on the owner Mac, **not independently accessible in this public branch** unless separately copied and verified. This is an attributed local execution record, not an externally authenticated audit receipt. It must not be cited as scientific reproduction of McNugget or proof of deployed cognitive behavior.
