#!/usr/bin/env python3
"""Cross-language synthetic Ed25519 vectors: Python and independently coded Node.

No files contain test signing secrets. Ephemeral keys exist only in process memory.
Node receives synthetic public-key trust records over stdin, NOT real trust roots.
"""
import base64
import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from verify_synthetic_attestation import TrustedKey, AttestationRejected, signing_bytes, canonical_json, verify

KEY_ID = "ephemeral-lab-key"
ISSUER = "synthetic-lab-alpha"
AUDIENCE = "synthetic-lab-beta"
NOW = 1_000_000
VERIFY_DRIVER = str(ROOT / "tests/attestation_node_verify_driver.mjs")
ISSUE_DRIVER = str(ROOT / "tests/attestation_node_issue_driver.mjs")


def run_node(request, *, success=True, driver=VERIFY_DRIVER):
    result = subprocess.run(["node", driver], input=json.dumps(request),
                            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            timeout=12, check=False)
    if success and result.returncode != 0:
        raise AssertionError("independent Node checker unexpectedly rejected synthetic case")
    if not success and result.returncode == 0:
        raise AssertionError("independent Node checker unexpectedly accepted synthetic attack")
    return json.loads(result.stdout)


class CrossLanguageAttestation(unittest.TestCase):
    def setUp(self):
        self.private = Ed25519PrivateKey.generate()
        self.pub = self.private.public_key()
        self.payload = {
            "schema": "ghostmesh.synthetic-attestation/v0.1",
            "event_type": "synthetic.observation",
            "issuer": ISSUER, "subject": "synthetic-service", "audience": AUDIENCE,
            "policy_version": "synthetic-policy-v1",
            "issued_at": NOW-30, "expires_at": NOW+300,
            "nonce": "00112233445566778899aabbccddeeff",
            "sequence": 1, "claim": "A synthetic service appears healthy",
        }
        self.record = {
            "key_id": KEY_ID,
            "public_key_raw_hex": self.pub.public_bytes(Encoding.Raw, PublicFormat.Raw).hex(),
            "issuer": ISSUER, "role": "synthetic-observer", "audiences": [AUDIENCE],
            "not_before": NOW-1000, "not_after": NOW+2000, "status": "active",
        }

    def issue_python(self, payload=None):
        p = copy.deepcopy(payload if payload is not None else self.payload)
        sig = base64.urlsafe_b64encode(self.private.sign(signing_bytes(KEY_ID, p))).decode().rstrip("=")
        raw = canonical_json({"payload": p, "signature": {"algorithm": "Ed25519", "key_id": KEY_ID, "value": sig}})
        return base64.urlsafe_b64encode(raw).decode().rstrip("=")

    def node_verify(self, *, envelope_b64=None, trust=None, audience=AUDIENCE, now=NOW, success=True):
        request = {"envelope_b64": envelope_b64 or self.issue_python(),
                   "trust": trust or self.record, "expected_audience": audience, "now": now}
        return run_node(request, success=success)

    def test_python_signed_node_verified(self):
        result = self.node_verify()
        self.assertEqual(result["status"], "CRYPTO_VERIFIED_SYNTHETIC_ONLY")
        self.assertEqual(result["real_world_authority"], "NONE")
        self.assertFalse(result["source_truth_verified"])

    def test_node_signed_python_verified(self):
        case = run_node({"payload": self.payload}, driver=ISSUE_DRIVER)
        self.assertEqual(case["status"], "TEST_VECTOR_ONLY")
        raw = base64.urlsafe_b64decode(case["envelope_b64"] + "==")
        pkey = Ed25519PublicKey.from_public_bytes(bytes.fromhex(case["public_key_raw_hex"]))
        trust = {KEY_ID: TrustedKey(pkey, ISSUER, "synthetic-observer",
                    frozenset([AUDIENCE]), NOW-1000, NOW+2000)}
        result = verify(raw, trust, expected_audience=AUDIENCE, now=NOW, replay_seen=set())
        self.assertEqual(result["status"], "CRYPTO_VERIFIED_SYNTHETIC_ONLY")
        self.assertEqual(result["actual_effect"], "UNKNOWN")

    def test_key_alias_substitution_rejected(self):
        env = json.loads(base64.urlsafe_b64decode(self.issue_python() + "=="))
        env["signature"]["key_id"] = "substitute-lab-key"
        altered = base64.urlsafe_b64encode(canonical_json(env)).decode().rstrip("=")
        record = dict(self.record, key_id="substitute-lab-key")
        self.node_verify(envelope_b64=altered, trust=record, success=False)

    def test_signer_role_substitution_rejected(self):
        self.node_verify(trust=dict(self.record, role="synthetic-reporter"), success=False)

    def test_wrong_audience_rejected(self):
        self.node_verify(audience="synthetic-lab-gamma", success=False)

    def test_revoked_key_rejected(self):
        self.node_verify(trust=dict(self.record, status="revoked"), success=False)

    def test_expired_signature_rejected(self):
        self.node_verify(now=NOW+400, success=False)

    def test_wrong_trust_root_rejected(self):
        other = Ed25519PrivateKey.generate().public_key()
        rec = dict(self.record,
                   public_key_raw_hex=other.public_bytes(Encoding.Raw, PublicFormat.Raw).hex())
        self.node_verify(trust=rec, success=False)

    def test_noncanonical_padding_rejected(self):
        raw = base64.urlsafe_b64decode(self.issue_python() + "==")
        altered = base64.urlsafe_b64encode(raw + b" ").decode().rstrip("=")
        self.node_verify(envelope_b64=altered, success=False)

    def test_byte_tampering_rejected(self):
        env = json.loads(base64.urlsafe_b64decode(self.issue_python() + "=="))
        env["payload"]["claim"] = "The monitor falsely reports the service failed"
        altered = base64.urlsafe_b64encode(canonical_json(env)).decode().rstrip("=")
        self.node_verify(envelope_b64=altered, success=False)

    def test_printable_ascii_shared_profile(self):
        payload = dict(self.payload, claim='ASCII quoting: "test" and backslash \\ with signs !?')
        self.assertEqual(
            self.node_verify(envelope_b64=self.issue_python(payload))["status"],
            "CRYPTO_VERIFIED_SYNTHETIC_ONLY"
        )

    def test_nonprintable_python_rejected(self):
        bad = dict(self.payload, claim="A synthetic\nnewline is not accepted")
        with self.assertRaises(AttestationRejected):
            self.issue_python(bad)

    def test_still_not_independent_measurement(self):
        p = dict(self.payload, claim="A signed synthetic report that makes a knowingly false assertion")
        result = self.node_verify(envelope_b64=self.issue_python(p))
        self.assertFalse(result["source_truth_verified"])
        self.assertFalse(result["independent_witness_verified"])
        self.assertEqual(result["actual_effect"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
