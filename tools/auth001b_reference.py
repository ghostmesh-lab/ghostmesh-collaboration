#!/usr/bin/env python3
"""Offline AUTH-001B toy grant-redemption reference, NOT an execution engine.

SQLite transaction semantics are tested, not a production grant or external effect.
All actors/resources/content and evidence in this reference are synthetic.
"""
from __future__ import annotations

import hashlib
import sqlite3
from contextlib import contextmanager
from pathlib import Path


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


class GrantStore:
    def __init__(self, path: str | Path):
        self.path = str(path)
        with self._connect() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS grants (
                    grant_id TEXT PRIMARY KEY,
                    actor TEXT NOT NULL,
                    resource TEXT NOT NULL,
                    content_sha256 TEXT NOT NULL,
                    policy TEXT NOT NULL,
                    state TEXT NOT NULL CHECK (state IN ('ISSUED','REVOKED','COMMITTED'))
                );
                CREATE TABLE IF NOT EXISTS decisions (
                    seq INTEGER PRIMARY KEY AUTOINCREMENT,
                    grant_id TEXT NOT NULL,
                    actor TEXT NOT NULL,
                    verdict TEXT NOT NULL,
                    reason TEXT NOT NULL
                );
            """)

    @contextmanager
    def _connect(self):
        db = sqlite3.connect(self.path, timeout=10, isolation_level=None)
        try:
            yield db
        finally:
            db.close()

    def issue(self, grant_id: str, actor: str, resource: str,
              content: bytes, policy: str) -> None:
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            db.execute(
                "INSERT INTO grants VALUES (?,?,?,?,?,?)",
                (grant_id, actor, resource, digest(content), policy, "ISSUED"),
            )
            db.commit()

    def revoke(self, grant_id: str) -> str:
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT state FROM grants WHERE grant_id=?", (grant_id,)
            ).fetchone()
            if row is None:
                result = "UNKNOWN_GRANT"
            elif row[0] == "ISSUED":
                db.execute(
                    "UPDATE grants SET state='REVOKED' WHERE grant_id=?", (grant_id,)
                )
                result = "REVOKED"
            else:
                result = "NO_RETROACTIVE_CHANGE"
            db.commit()
        return result

    def redeem(self, grant_id: str, actor: str, resource: str,
               executed_bytes: bytes, policy: str, *, lose_ack: bool = False) -> str:
        # A bytes argument models exact data selected for a synthetic operation.
        # It does NOT prove a later real executor used these bytes.
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT actor,resource,content_sha256,policy,state "
                "FROM grants WHERE grant_id=?", (grant_id,)
            ).fetchone()
            if row is None:
                verdict, reason = "DENIED", "UNKNOWN_GRANT"
            elif row[4] != "ISSUED":
                verdict, reason = "DENIED", "GRANT_" + row[4]
            elif row[0] != actor:
                verdict, reason = "DENIED", "WRONG_ACTOR"
            elif row[1] != resource:
                verdict, reason = "DENIED", "WRONG_RESOURCE"
            elif row[2] != digest(executed_bytes):
                verdict, reason = "DENIED", "WRONG_CONTENT"
            elif row[3] != policy:
                verdict, reason = "DENIED", "WRONG_POLICY"
            else:
                db.execute(
                    "UPDATE grants SET state='COMMITTED' WHERE grant_id=?", (grant_id,)
                )
                verdict, reason = "COMMITTED_AUTHORIZATION", "BOUND_MATCH"
            db.execute(
                "INSERT INTO decisions(grant_id,actor,verdict,reason) VALUES(?,?,?,?)",
                (grant_id, actor, verdict, reason),
            )
            db.commit()  # Simulates durable authorization commit, NOT effect.
        return "ACK_LOST_EFFECT_UNKNOWN" if lose_ack and verdict == "COMMITTED_AUTHORIZATION" else reason

    def grant_state(self, grant_id: str) -> str:
        with self._connect() as db:
            row = db.execute(
                "SELECT state FROM grants WHERE grant_id=?", (grant_id,)
            ).fetchone()
            return row[0] if row else "UNKNOWN_GRANT"

    def records(self, grant_id: str) -> list[tuple]:
        with self._connect() as db:
            return db.execute(
                "SELECT actor,verdict,reason FROM decisions WHERE grant_id=? ORDER BY seq",
                (grant_id,),
            ).fetchall()
