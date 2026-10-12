#!/usr/bin/env python3
"""Purely synthetic signatures, generated in memory. No test keys persisted."""
from __future__ import annotations
import base64
import copy
import importlib.util
import json
import unittest
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("synthetic_attestation", ROOT / "tools/verify_synthetic_attestation.py")
lab = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = lab
spec.loader.exec_module(lab)

NOW = 1_000_000
KEY_ID = "ephemeral-lab-key"
ISSUER = "synthetic-lab-alpha"
AUDIENCE = "synthetic-lab-beta"


class SyntheticAttestationTests(unittest.TestCase):
    def setUp(self):
        self.private = Ed25519PrivateKey.generate()
        self.trust = {KEY_ID: lab.TrustedKey(
            public_key=self.private.public_key(),
            issuer=ISSUER, role="synthetic-observer",
            audiences=frozenset({AUDIENCE}),
            not_before=NOW-1000, not_after=NOW+2000,
        )}
        self.seen = set()
        self.payload = {
            "schema": "ghostmesh.synthetic-attestation/v0.1",
            "event_type": "synthetic.observation",
            "issuer": ISSUER,
            "subject": "synthetic-service",
            "audience": AUDIENCE,
            "policy_version": "synthetic-policy-v1",
            "issued_at": NOW-30,
            "expires_at": NOW+300,
            "nonce": "00112233445566778899aabbccddeeff",
            "sequence": 1,
            "claim": "A synthetic service appears healthy",
        }

    def encode(self, payload=None, private=None, *, key_id=KEY_ID):
        p = copy.deepcopy(payload if payload is not None else self.payload)
        signing_key = private or self.private
        signature = signing_key.sign(lab.signing_bytes(key_id, p))
        envelope = {"payload":p,"signature":{
            "algorithm":"Ed25519","key_id":key_id,
            "value":base64.urlsafe_b64encode(signature).decode().rstrip("="),
        }}
        return lab.canonical_json(envelope)

    def check_rejected(self, **changes):
        altered = copy.deepcopy(self.payload)
        altered.update(changes)
        with self.assertRaises(lab.AttestationRejected):
            lab.verify(self.encode(altered), self.trust, expected_audience=AUDIENCE,
                       now=NOW, replay_seen=self.seen)
        self.assertFalse(self.seen, "invalid verification must not consume replay state")

    def test_good_synthetic_attestation(self):
        out = lab.verify(self.encode(), self.trust, expected_audience=AUDIENCE,
                         now=NOW, replay_seen=self.seen)
        self.assertEqual(out["status"], "CRYPTO_VERIFIED_SYNTHETIC_ONLY")
        self.assertFalse(out["source_truth_verified"])
        self.assertFalse(out["independent_witness_verified"])
        self.assertEqual(out["real_world_authority"], "NONE")
        self.assertEqual(out["actual_effect"], "UNKNOWN")
        self.assertEqual(len(self.seen), 2)

    def test_tampered_claim_detected(self):
        parsed = json.loads(self.encode())
        parsed["payload"]["claim"] = "A fabricated unhealthy service claim"
        with self.assertRaises(lab.AttestationRejected):
            lab.verify(lab.canonical_json(parsed), self.trust, expected_audience=AUDIENCE,
                       now=NOW, replay_seen=self.seen)

    def test_wrong_trust_root_detected(self):
        other = Ed25519PrivateKey.generate()
        trust = {KEY_ID: lab.TrustedKey(other.public_key(), ISSUER, "synthetic-observer",
                    frozenset({AUDIENCE}), NOW-1000, NOW+2000)}
        with self.assertRaises(lab.AttestationRejected):
            lab.verify(self.encode(), trust, expected_audience=AUDIENCE, now=NOW,
                       replay_seen=self.seen)

    def test_unknown_signing_key_detected(self):
        with self.assertRaises(lab.AttestationRejected):
            lab.verify(self.encode(), {}, expected_audience=AUDIENCE, now=NOW,
                       replay_seen=self.seen)

    def test_revocation_detected(self):
        self.trust[KEY_ID] = lab.TrustedKey(self.private.public_key(), ISSUER, "synthetic-observer",
                          frozenset({AUDIENCE}), NOW-1000, NOW+2000, "revoked")
        with self.assertRaises(lab.AttestationRejected):
            lab.verify(self.encode(), self.trust, expected_audience=AUDIENCE, now=NOW,
                       replay_seen=self.seen)

    def test_expired_trust_anchor_detected(self):
        self.trust[KEY_ID] = lab.TrustedKey(self.private.public_key(), ISSUER, "synthetic-observer",
                          frozenset({AUDIENCE}), NOW-2000, NOW-1)
        with self.assertRaises(lab.AttestationRejected):
            lab.verify(self.encode(), self.trust, expected_audience=AUDIENCE, now=NOW,
                       replay_seen=self.seen)

    def test_issuer_mismatch_with_authentic_signature(self):
        self.check_rejected(issuer="synthetic-lab-gamma")

    def test_role_mismatch_with_authentic_signature(self):
        self.check_rejected(event_type="synthetic.harness-report")

    def test_event_type_substitution(self):
        self.check_rejected(event_type="production.action-authorized")

    def test_policy_substitution(self):
        self.check_rejected(policy_version="production-policy-v1")

    def test_wrong_audience(self):
        self.check_rejected(audience="synthetic-lab-gamma")

    def test_expired_attestation(self):
        self.check_rejected(expires_at=NOW-1)

    def test_excessive_validity(self):
        self.check_rejected(expires_at=NOW+10_000)

    def test_future_issued_at(self):
        self.check_rejected(issued_at=NOW+120)

    def test_replayed_nonce_detected(self):
        lab.verify(self.encode(), self.trust, expected_audience=AUDIENCE,
                   now=NOW, replay_seen=self.seen)
        with self.assertRaises(lab.AttestationRejected):
            lab.verify(self.encode(), self.trust, expected_audience=AUDIENCE,
                       now=NOW, replay_seen=self.seen)

    def test_reused_sequence_with_fresh_nonce(self):
        lab.verify(self.encode(), self.trust, expected_audience=AUDIENCE,
                   now=NOW, replay_seen=self.seen)
        alternate = copy.deepcopy(self.payload)
        alternate["nonce"] = "ffeeddccbbaa99887766554433221100"
        with self.assertRaises(lab.AttestationRejected):
            lab.verify(self.encode(alternate), self.trust, expected_audience=AUDIENCE,
                       now=NOW, replay_seen=self.seen)

    def test_signing_key_alias_substitution_fails_even_same_public_key(self):
        self.trust["another-lab-key"] = self.trust[KEY_ID]
        envelope = json.loads(self.encode())
        envelope["signature"]["key_id"] = "another-lab-key"
        with self.assertRaises(lab.AttestationRejected):
            lab.verify(lab.canonical_json(envelope), self.trust, expected_audience=AUDIENCE,
                       now=NOW, replay_seen=self.seen)

    def test_signature_algorithm_downgrade(self):
        envelope = json.loads(self.encode())
        envelope["signature"]["algorithm"] = "none"
        with self.assertRaises(lab.AttestationRejected):
            lab.verify(lab.canonical_json(envelope), self.trust, expected_audience=AUDIENCE,
                       now=NOW, replay_seen=self.seen)

    def test_noncanonical_spacing_rejected(self):
        envelope = json.loads(self.encode())
        noncanonical = json.dumps(envelope, indent=2).encode("ascii")
        with self.assertRaises(lab.AttestationRejected):
            lab.verify(noncanonical, self.trust, expected_audience=AUDIENCE,
                       now=NOW, replay_seen=self.seen)

    def test_duplicate_field_rejected(self):
        canonical = self.encode()
        mutated = canonical.replace(b'{"payload":', b'{"payload":null,"payload":', 1)
        with self.assertRaises(lab.AttestationRejected):
            lab.verify(mutated, self.trust, expected_audience=AUDIENCE,
                       now=NOW, replay_seen=self.seen)

    def test_non_ascii_and_floats_rejected(self):
        altered = copy.deepcopy(self.payload)
        altered["claim"] = "Caf\u00e9 is healthy"
        with self.assertRaises(lab.AttestationRejected):
            self.encode(altered)
        altered = copy.deepcopy(self.payload)
        altered["sequence"] = 1.0
        with self.assertRaises(lab.AttestationRejected):
            self.encode(altered)

    def test_invalid_signature_encoding(self):
        envelope = json.loads(self.encode())
        envelope["signature"]["value"] = "!" * 86
        with self.assertRaises(lab.AttestationRejected):
            lab.verify(lab.canonical_json(envelope), self.trust, expected_audience=AUDIENCE,
                       now=NOW, replay_seen=self.seen)

    def test_authentic_but_false_claim_not_truth(self):
        misleading = copy.deepcopy(self.payload)
        misleading["claim"] = "Synthetic service is healthy, but the synthetic monitor is compromised"
        result = lab.verify(self.encode(misleading), self.trust,
                            expected_audience=AUDIENCE, now=NOW, replay_seen=self.seen)
        self.assertFalse(result["source_truth_verified"])
        self.assertEqual(result["actual_effect"], "UNKNOWN")

    def test_signed_success_is_not_independently_verified_effect(self):
        record = lab.TrustedKey(self.private.public_key(), ISSUER, "synthetic-reporter",
                       frozenset({AUDIENCE}), NOW-1000, NOW+2000)
        self.trust[KEY_ID] = record
        payload = copy.deepcopy(self.payload)
        payload["event_type"] = "synthetic.harness-report"
        payload["claim"] = "Synthetic harness reports success, but independent effect check failed"
        output = lab.verify(self.encode(payload), self.trust,
                             expected_audience=AUDIENCE, now=NOW, replay_seen=self.seen)
        self.assertFalse(output["independent_witness_verified"])
        self.assertEqual(output["actual_effect"], "UNKNOWN")

    def test_extra_event_grant_not_accepted(self):
        modified = copy.deepcopy(self.payload)
        modified["live_authority_granted"] = True
        with self.assertRaises(lab.AttestationRejected):
            lab.verify(self.encode(modified), self.trust, expected_audience=AUDIENCE,
                       now=NOW, replay_seen=self.seen)


if __name__ == "__main__":
    unittest.main()
