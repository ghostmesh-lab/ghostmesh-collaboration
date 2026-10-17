"""Offline AUTH-001B fault-boundary and false-denial controls.

These tests use generated SQLite databases and a deliberately unsafe toy control.
They do not exercise the GhostMesh broker, Hestia, real authorization or effects.
"""
from __future__ import annotations

import sqlite3
from contextlib import closing
import sys
import tempfile
import threading
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from auth001b_reference import GrantStore


class FaultBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.db_path = Path(self.tmp.name) / "synthetic.sqlite3"
        self.store = GrantStore(self.db_path)
        self.bytes = b"synthetic bytes only"
        self.store.issue("grant", "actor-A", "resource-A", self.bytes, "law-1")

    def redeem(self, *, grant_id="grant", actor="actor-A",
               resource="resource-A", content=None, policy="law-1",
               lose_ack=False):
        return self.store.redeem(grant_id, actor, resource,
                                 self.bytes if content is None else content,
                                 policy, lose_ack=lose_ack)

    def assert_clean_precommit_rollback(self):
        reopened = GrantStore(self.db_path)
        self.assertEqual(reopened.grant_state("grant"), "ISSUED")
        self.assertEqual(reopened.records("grant"), [])
        self.assertEqual(reopened.redeem(
            "grant", "actor-A", "resource-A", self.bytes, "law-1"
        ), "BOUND_MATCH")

    def test_fault_during_state_transition_rolls_back(self):
        with closing(sqlite3.connect(self.db_path)) as con:
            con.executescript("""
                CREATE TRIGGER fail_state BEFORE UPDATE OF state ON grants
                WHEN NEW.state='COMMITTED'
                BEGIN SELECT RAISE(ABORT, 'synthetic pre-commit fault'); END;
            """)
        with self.assertRaises(sqlite3.IntegrityError):
            self.redeem()
        with closing(sqlite3.connect(self.db_path)) as con:
            con.execute("DROP TRIGGER fail_state")
        self.assert_clean_precommit_rollback()

    def test_fault_after_transition_before_audit_rolls_back_both(self):
        with closing(sqlite3.connect(self.db_path)) as con:
            con.executescript("""
                CREATE TRIGGER fail_audit BEFORE INSERT ON decisions
                WHEN NEW.verdict='COMMITTED_AUTHORIZATION'
                BEGIN SELECT RAISE(ABORT, 'synthetic audit fault'); END;
            """)
        with self.assertRaises(sqlite3.IntegrityError):
            self.redeem()
        with closing(sqlite3.connect(self.db_path)) as con:
            con.execute("DROP TRIGGER fail_audit")
        self.assert_clean_precommit_rollback()

    def test_lost_ack_survives_reopen_without_proving_effect(self):
        self.assertEqual(self.redeem(lose_ack=True), "ACK_LOST_EFFECT_UNKNOWN")
        recovered = GrantStore(self.db_path)
        self.assertEqual(recovered.grant_state("grant"), "COMMITTED")
        self.assertEqual(recovered.redeem(
            "grant", "actor-A", "resource-A", self.bytes, "law-1"
        ), "GRANT_COMMITTED")
        self.assertEqual(recovered.records("grant")[0][1],
                         "COMMITTED_AUTHORIZATION")
        # There is no effects table or independent observer in the model.
        with closing(sqlite3.connect(self.db_path)) as con:
            tables = {r[0] for r in con.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )}
        self.assertNotIn("effects", tables)

    def test_two_parallel_valid_grants_do_not_false_deny(self):
        self.store.issue("grant-B", "actor-B", "resource-B", b"other", "law-1")
        barrier = threading.Barrier(3)
        outcomes = []
        errors = []

        def run(args):
            try:
                barrier.wait(timeout=5)
                outcomes.append(self.store.redeem(*args))
            except Exception as exc:
                errors.append(type(exc).__name__)

        args_a = ("grant", "actor-A", "resource-A", self.bytes, "law-1")
        args_b = ("grant-B", "actor-B", "resource-B", b"other", "law-1")
        threads = [threading.Thread(target=run, args=(args,))
                   for args in (args_a, args_b)]
        for t in threads:
            t.start()
        barrier.wait(timeout=5)
        for t in threads:
            t.join(timeout=10)
        self.assertFalse(any(t.is_alive() for t in threads))
        self.assertEqual(errors, [])
        self.assertCountEqual(outcomes, ["BOUND_MATCH", "BOUND_MATCH"])

    def test_racing_revocation_and_redeem_have_valid_serial_orders(self):
        # This samples one schedule per iteration; it does not prove all
        # interleavings, crash models, or distributed linearizability.
        for trial in range(16):
            db = GrantStore(Path(self.tmp.name) / f"race-{trial}.sqlite3")
            db.issue("g", "a", "r", b"x", "p")
            barrier = threading.Barrier(3)
            outcomes = {}
            errors = []

            def redeem():
                try:
                    barrier.wait(timeout=5)
                    outcomes["redeem"] = db.redeem("g", "a", "r", b"x", "p")
                except Exception as exc:
                    errors.append(type(exc).__name__)

            def revoke():
                try:
                    barrier.wait(timeout=5)
                    outcomes["revoke"] = db.revoke("g")
                except Exception as exc:
                    errors.append(type(exc).__name__)

            threads = [threading.Thread(target=redeem),
                       threading.Thread(target=revoke)]
            for t in threads:
                t.start()
            barrier.wait(timeout=5)
            for t in threads:
                t.join(timeout=10)
            self.assertFalse(any(t.is_alive() for t in threads))
            self.assertEqual(errors, [])
            self.assertIn(
                (outcomes["redeem"], outcomes["revoke"]),
                {("BOUND_MATCH", "NO_RETROACTIVE_CHANGE"),
                 ("GRANT_REVOKED", "REVOKED")},
            )
            self.assertIn(db.grant_state("g"), {"REVOKED", "COMMITTED"})

    def test_deliberately_naive_two_executor_reference_double_accepts(self):
        # A counterexample for "check then later set" without an atomic
        # critical section. Not a claim that any deployed code behaves so.
        naive_state = {"state": "ISSUED"}
        both_read = threading.Barrier(2)
        results = []

        def naive_redeem():
            authorized = naive_state["state"] == "ISSUED"
            both_read.wait(timeout=5)
            if authorized:
                naive_state["state"] = "COMMITTED"
                results.append("ACCEPTED")
            else:
                results.append("DENIED")

        a = threading.Thread(target=naive_redeem)
        b = threading.Thread(target=naive_redeem)
        a.start()
        b.start()
        a.join(timeout=10)
        b.join(timeout=10)
        self.assertFalse(a.is_alive() or b.is_alive())
        self.assertEqual(results.count("ACCEPTED"), 2)

    def test_denied_wrong_actor_does_not_consume_valid_grant(self):
        for _ in range(3):
            self.assertEqual(self.redeem(actor="actor-B"), "WRONG_ACTOR")
        self.assertEqual(self.store.grant_state("grant"), "ISSUED")
        self.assertEqual(self.redeem(), "BOUND_MATCH")
        self.assertEqual(len(self.store.records("grant")), 4)


if __name__ == "__main__":
    unittest.main()
