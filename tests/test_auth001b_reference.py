"""Executable synthetic AUTH-001B checks, no service actions or network I/O."""
import sys
import tempfile
import threading
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from auth001b_reference import GrantStore


class AuthorizationFaultTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = GrantStore(Path(self.temp.name) / "grant.sqlite3")
        self.raw = b"synthetic-action-v1"
        self.store.issue("g", "a", "resource-A", self.raw, "law-v1")

    def attempt(self, **overrides):
        p = dict(grant_id="g", actor="a", resource="resource-A",
                 executed_bytes=self.raw, policy="law-v1")
        p.update(overrides)
        return self.store.redeem(**p)

    def test_honest_unchanged_operation_allowed(self):
        self.assertEqual(self.attempt(), "BOUND_MATCH")
        self.assertEqual(self.store.grant_state("g"), "COMMITTED")

    def test_one_grant_two_concurrent_executors(self):
        barrier = threading.Barrier(3)
        results = []
        lock = threading.Lock()
        def contender():
            barrier.wait()
            reply = self.attempt()
            with lock:
                results.append(reply)
        a = threading.Thread(target=contender)
        b = threading.Thread(target=contender)
        a.start(); b.start()
        barrier.wait()
        a.join(timeout=10); b.join(timeout=10)
        self.assertFalse(a.is_alive() or b.is_alive())
        self.assertCountEqual(results, ["BOUND_MATCH", "GRANT_COMMITTED"])
        self.assertEqual(len(self.store.records("g")), 2)

    def test_two_separate_grants_positive_control(self):
        self.store.issue("g2", "b", "resource-B", b"other", "law-v1")
        self.assertEqual(self.attempt(), "BOUND_MATCH")
        self.assertEqual(self.store.redeem("g2", "b", "resource-B", b"other", "law-v1"),
                         "BOUND_MATCH")

    def test_wrong_actor_does_not_consume_grant(self):
        self.assertEqual(self.attempt(actor="b"), "WRONG_ACTOR")
        self.assertEqual(self.store.grant_state("g"), "ISSUED")
        self.assertEqual(self.attempt(), "BOUND_MATCH")

    def test_wrong_resource_rejected(self):
        self.assertEqual(self.attempt(resource="resource-B"), "WRONG_RESOURCE")
        self.assertEqual(self.store.grant_state("g"), "ISSUED")

    def test_bytes_substitution_rejected(self):
        self.assertEqual(self.attempt(executed_bytes=b"synthetic-action-v2"),
                         "WRONG_CONTENT")
        self.assertEqual(self.attempt(), "BOUND_MATCH")

    def test_old_policy_version_rejected(self):
        self.assertEqual(self.attempt(policy="law-v2"), "WRONG_POLICY")
        self.assertEqual(self.attempt(), "BOUND_MATCH")

    def test_revocation_before_redeem_denies(self):
        self.assertEqual(self.store.revoke("g"), "REVOKED")
        self.assertEqual(self.attempt(), "GRANT_REVOKED")

    def test_revocation_after_commit_not_retroactive(self):
        self.assertEqual(self.attempt(), "BOUND_MATCH")
        self.assertEqual(self.store.revoke("g"), "NO_RETROACTIVE_CHANGE")
        self.assertEqual(self.attempt(), "GRANT_COMMITTED")

    def test_lost_ack_must_not_claim_known_effect(self):
        self.assertEqual(self.attempt(lose_ack=True),
                         "ACK_LOST_EFFECT_UNKNOWN")
        self.assertEqual(self.store.grant_state("g"), "COMMITTED")
        self.assertEqual(self.attempt(), "GRANT_COMMITTED")
        # No independent effect measurement is supplied by the reference.
        self.assertNotIn("EFFECT_OBSERVED", str(self.store.records("g")))

    def test_unknown_grant_does_not_create_authority(self):
        self.assertEqual(self.attempt(grant_id="never-issued"), "UNKNOWN_GRANT")
        self.assertEqual(self.store.grant_state("never-issued"), "UNKNOWN_GRANT")


if __name__ == "__main__":
    unittest.main()
