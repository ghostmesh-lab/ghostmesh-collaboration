#!/usr/bin/env python3
"""Lab-only Ed25519 verifier. NO real identity, authority, or operating keys.

Canonicalization is a bounded ASCII/integer JSON profile, NOT full RFC 8785.
Test keys are created in memory by the test suite and are never persisted.
"""
from __future__ import annotations

import base64
import json
import re
from dataclasses import dataclass
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

DOMAIN = b"ghostmesh-lab.synthetic-attestation.v0.1\x00"
FIELDS = {
    "schema", "event_type", "issuer", "subject", "audience", "policy_version",
    "issued_at", "expires_at", "nonce", "sequence", "claim",
}
ENVELOPE_FIELDS = {"payload", "signature"}
SIGN_FIELDS = {"algorithm", "key_id", "value"}
KEY_ID = re.compile(r"^[a-z][a-z0-9-]{2,63}$")
ACTOR = re.compile(r"^[a-z][a-z0-9-]{2,63}$")
NONCE = re.compile(r"^[0-9a-f]{32}$")
SIG_B64 = re.compile(r"^[A-Za-z0-9_-]{86}$")
MAX_BYTES = 4096
MAX_LIFETIME = 3600
CLOCK_SKEW = 60

EVENT_ROLES = {
    "synthetic.observation": "synthetic-observer",
    "synthetic.harness-report": "synthetic-reporter",
}


class AttestationRejected(ValueError):
    """A synthetic attestation does not satisfy this profile."""


@dataclass(frozen=True)
class TrustedKey:
    """Locally supplied synthetic trust record; never loaded from signed payload."""
    public_key: Ed25519PublicKey
    issuer: str
    role: str
    audiences: frozenset[str]
    not_before: int
    not_after: int
    status: str = "active"


def canonical_json(obj: Any) -> bytes:
    """Narrow deterministic ASCII subset; no floats, Unicode, NaN or excess depth.

    Contract uses sorted ASCII keys and Python's fixed JSON escaping behavior.
    It is intentionally NOT an RFC 8785 implementation. Do not claim universal
    interoperable JCS signatures or use for C2/C3 production.
    """
    def check(value: Any, depth: int = 0) -> None:
        if depth > 4:
            raise AttestationRejected("canonicalization depth exceeded")
        if isinstance(value, dict):
            if not all(isinstance(k, str) for k in value):
                raise AttestationRejected("non-string object key")
            for k, v in value.items():
                try: k.encode("ascii")
                except UnicodeEncodeError as exc:
                    raise AttestationRejected("non-ascii JSON key") from exc
                check(v, depth + 1)
        elif isinstance(value, list):
            for entry in value: check(entry, depth + 1)
        elif isinstance(value, str):
            try: value.encode("ascii")
            except UnicodeEncodeError as exc:
                raise AttestationRejected("non-ascii JSON string") from exc
        elif value is None or type(value) in (bool, int):
            if type(value) is int and abs(value) > 2**53 - 1:
                raise AttestationRejected("oversize integer")
        else:
            raise AttestationRejected("unsupported JSON type")
    check(obj)
    encoded = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                         allow_nan=False).encode("ascii")
    if len(encoded) > MAX_BYTES:
        raise AttestationRejected("oversize attestation")
    return encoded


def signing_bytes(key_id: str, payload: dict) -> bytes:
    """Domain-separate the signature and bind both key ID and synthetic claim."""
    if not isinstance(key_id, str) or not KEY_ID.fullmatch(key_id):
        raise AttestationRejected("invalid signing key identifier")
    return DOMAIN + canonical_json({"key_id": key_id, "payload": payload})


def _reject_duplicates(pairs: list[tuple[str, Any]]) -> dict:
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise AttestationRejected("duplicate JSON key")
        obj[key] = value
    return obj


def decode_exact(raw: bytes) -> dict:
    if not isinstance(raw, bytes) or len(raw) > MAX_BYTES:
        raise AttestationRejected("invalid encoded envelope")
    try:
        obj = json.loads(raw.decode("ascii"), object_pairs_hook=_reject_duplicates,
                         parse_constant=lambda _: (_ for _ in ()).throw(
                             AttestationRejected("nonfinite JSON value")))
    except (UnicodeError, json.JSONDecodeError, TypeError) as exc:
        raise AttestationRejected("invalid JSON envelope") from exc
    if not isinstance(obj, dict) or canonical_json(obj) != raw:
        raise AttestationRejected("envelope is not exact canonical ASCII JSON")
    return obj


def validate_payload(payload: dict, expected_audience: str, now: int) -> None:
    if not isinstance(payload, dict) or set(payload) != FIELDS:
        raise AttestationRejected("unexpected payload fields")
    if payload["schema"] != "ghostmesh.synthetic-attestation/v0.1":
        raise AttestationRejected("unknown synthetic attestation schema")
    if payload["event_type"] not in EVENT_ROLES:
        raise AttestationRejected("unsupported event type")
    if payload["policy_version"] != "synthetic-policy-v1":
        raise AttestationRejected("wrong synthetic policy version")
    for field in ("issuer", "subject", "audience"):
        if not isinstance(payload[field], str) or not ACTOR.fullmatch(payload[field]):
            raise AttestationRejected("bad actor identifier")
    if payload["audience"] != expected_audience:
        raise AttestationRejected("wrong audience")
    if not isinstance(payload["nonce"], str) or not NONCE.fullmatch(payload["nonce"]):
        raise AttestationRejected("bad replay nonce")
    if (type(payload["sequence"]) is not int or
        not 1 <= payload["sequence"] <= 2**53 - 1):
        raise AttestationRejected("bad sequence")
    issued, expires = payload["issued_at"], payload["expires_at"]
    if type(issued) is not int or type(expires) is not int:
        raise AttestationRejected("noninteger validity window")
    if issued > now + CLOCK_SKEW or expires <= now or expires <= issued:
        raise AttestationRejected("not yet valid or expired")
    if expires - issued > MAX_LIFETIME:
        raise AttestationRejected("excessive attestation lifetime")
    if (not isinstance(payload["claim"], str) or
        not 10 <= len(payload["claim"]) <= 240):
        raise AttestationRejected("bad synthetic claim")
    canonical_json(payload)


def verify(raw: bytes, trust: dict[str, TrustedKey], *, expected_audience: str,
           now: int, replay_seen: set[tuple[str, str, str | int]]) -> dict:
    """Validate, then consume a replay marker. One-process demonstration only.

    A real replay ledger needs atomic, shared, durable transactions. A caller
    cannot reuse this mutable set across processes without losing protection.
    """
    if type(now) is not int or not isinstance(replay_seen, set):
        raise AttestationRejected("invalid verification context")
    envelope = decode_exact(raw)
    if set(envelope) != ENVELOPE_FIELDS:
        raise AttestationRejected("unknown envelope fields")
    payload, signature = envelope["payload"], envelope["signature"]
    if not isinstance(signature, dict) or set(signature) != SIGN_FIELDS:
        raise AttestationRejected("malformed signature")
    if signature["algorithm"] != "Ed25519":
        raise AttestationRejected("algorithm mismatch")
    key_id = signature["key_id"]
    if not isinstance(key_id, str) or not KEY_ID.fullmatch(key_id):
        raise AttestationRejected("untrusted key identifier")
    record = trust.get(key_id)
    if not isinstance(record, TrustedKey) or record.status != "active":
        raise AttestationRejected("key unavailable or revoked")
    validate_payload(payload, expected_audience, now)
    if payload["issuer"] != record.issuer:
        raise AttestationRejected("issuer is not trust-root-bound")
    if payload["audience"] not in record.audiences:
        raise AttestationRejected("audience not allowed for key")
    if record.role != EVENT_ROLES[payload["event_type"]]:
        raise AttestationRejected("signer role not authorized for event type")
    if not (record.not_before <= payload["issued_at"] < record.not_after and
            record.not_before <= now < record.not_after):
        raise AttestationRejected("signing key outside trusted time window")
    value = signature["value"]
    if not isinstance(value, str) or not SIG_B64.fullmatch(value):
        raise AttestationRejected("invalid signature encoding")
    try:
        raw_signature = base64.urlsafe_b64decode(value + "==")
        if len(raw_signature) != 64 or base64.urlsafe_b64encode(raw_signature).decode().rstrip("=") != value:
            raise AttestationRejected("noncanonical signature encoding")
        record.public_key.verify(raw_signature, signing_bytes(key_id, payload))
    except (ValueError, InvalidSignature) as exc:
        raise AttestationRejected("cryptographic signature rejected") from exc
    nonce_token = (key_id, "nonce", payload["nonce"])
    sequence_token = (key_id, "sequence", payload["sequence"])
    if nonce_token in replay_seen or sequence_token in replay_seen:
        raise AttestationRejected("replay or sequence reuse")
    replay_seen.update((nonce_token, sequence_token))
    return {
        "status": "CRYPTO_VERIFIED_SYNTHETIC_ONLY",
        "signing_key_id": key_id,
        "issuer": payload["issuer"],
        "event_type": payload["event_type"],
        "identity_accepted_within_supplied_synthetic_trust_map": True,
        "source_truth_verified": False,
        "independent_witness_verified": False,
        "real_world_authority": "NONE",
        "actual_effect": "UNKNOWN",
    }
