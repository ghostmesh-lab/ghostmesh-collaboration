#!/usr/bin/env python3
"""Validate ST-001 byte hashes and bundle boundaries; NOT a digital signature.

A matching unsigned manifest plus files establishes INTERNAL consistency only.
It does not authenticate the publisher, establish source truth, or authorize actions.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "bundles/st001/manifest.json"
SHA256 = re.compile(r"^[0-9a-f]{64}$")
REV = re.compile(r"^[0-9a-f]{40}$")
ALLOWED_FILES = {
    "fixture": "fixtures/v0.1/stale-truth.json",
    "evaluator": "tools/evaluate_stale_truth.py",
    "reference_output": "examples/stale-truth-reference-output.json",
    "preregistration": "experiments/ROUND_ONE_EXPERIMENT.md",
}
ALLOWED_ROLES = set(ALLOWED_FILES)
MAX_FILE = 1_000_000
ALLOWED_MANIFEST_FIELDS = {
    "schema", "bundle_id", "classification", "source_commit",
    "signature_status", "independently_reproduced", "grants_external_authority",
    "digest_algorithm", "claim", "files", "known_limitations",
}
ALLOWED_RECORD_FIELDS = {"path", "role", "sha256", "size_bytes"}


def verify(manifest: dict, root: Path) -> list[str]:
    problems: list[str] = []
    if set(manifest) != ALLOWED_MANIFEST_FIELDS:
        problems.append("unreviewed or missing manifest fields")
    if manifest.get("digest_algorithm") != "SHA-256":
        problems.append("unsupported hash algorithm")
    if manifest.get("bundle_id") != "ST-001-RESEARCH-REFERENCE-v0.1":
        problems.append("unexpected bundle identity")
    if manifest.get("schema") != "ghostmesh.unsigned-research-bundle/v0.1":
        problems.append("unknown bundle schema")
    if manifest.get("classification") != "PUBLIC_SYNTHETIC":
        problems.append("bundle cannot reference restricted data")
    if manifest.get("signature_status") != "UNSIGNED_HASH_MANIFEST":
        problems.append("unverified signature status or misleading attestation")
    if manifest.get("grants_external_authority") is not False:
        problems.append("bundle cannot grant external authority")
    if manifest.get("independently_reproduced") is not False:
        problems.append("bundle cannot claim independent reproduction")
    if not REV.fullmatch(str(manifest.get("source_commit", ""))):
        problems.append("missing exact Git source revision")
    files = manifest.get("files")
    if not isinstance(files, list) or not files or len(files) > 15:
        return problems + ["missing or excessive bundle file records"]
    root = root.resolve()
    seen_paths: set[str] = set()
    seen_roles: set[str] = set()
    for i, record in enumerate(files):
        if not isinstance(record, dict):
            problems.append("malformed record")
            continue
        if set(record) != ALLOWED_RECORD_FIELDS:
            problems.append(f"record {i}: unreviewed or missing file fields")
            continue
        name = record.get("path")
        role = record.get("role")
        expected = record.get("sha256")
        expected_size = record.get("size_bytes")
        if (not isinstance(name, str) or not name or "\\" in name
            or not re.fullmatch(r"[A-Za-z0-9_.\/-]+", name)):
            problems.append(f"record {i}: invalid relative file path")
            continue
        pure = PurePosixPath(name)
        if pure.is_absolute() or pure.as_posix() != name or any(part in ("..", ".") for part in name.split("/")):
            problems.append(f"record {i}: path traversal")
            continue
        if name in seen_paths:
            problems.append(f"record {i}: duplicate file")
            continue
        seen_paths.add(name)
        if role not in ALLOWED_ROLES or role in seen_roles:
            problems.append(f"record {i}: invalid or duplicate role")
            continue
        seen_roles.add(role)
        if name != ALLOWED_FILES[role]:
            problems.append(f"record {i}: file not approved for its evidence role")
            continue
        if not SHA256.fullmatch(str(expected)):
            problems.append(f"record {i}: invalid sha256 digest")
            continue
        if not isinstance(expected_size, int) or isinstance(expected_size, bool) or not 0 < expected_size <= MAX_FILE:
            problems.append(f"record {i}: invalid size")
            continue
        # Only a fixed, explicitly reviewed path for each role may be opened.
        original = root / ALLOWED_FILES[role]
        if original.is_symlink() or any(parent.is_symlink() for parent in original.parents if parent != root):
            problems.append(f"record {i}: symlink forbidden")
            continue
        candidate = original.resolve()
        if not candidate.is_relative_to(root) or not candidate.is_file():
            problems.append(f"record {i}: file unavailable or escapes root")
            continue
        payload = candidate.read_bytes()
        if len(payload) != expected_size or hashlib.sha256(payload).hexdigest() != expected:
            problems.append(f"record {i}: byte length or digest mismatch")
    if seen_roles != ALLOWED_ROLES:
        problems.append("missing one or more required evidence roles")
    return problems


def main() -> None:
    manifest = json.loads(BUNDLE.read_text(encoding="utf-8"))
    problems = verify(manifest, ROOT)
    if problems:
        for problem in problems:
            print("BLOCK:", problem)
        raise SystemExit(1)
    print(f"PASS: {len(manifest['files'])} ST-001 files match published SHA-256 commitments")
    print("PROVEN: internal exact-byte consistency against this manifest")
    print("NOT PROVEN: independent custody, publisher identity, actual source truth, executed effects, or authorization")
    print("AUTHENTICATION: separate trusted Git revision or external signature must be established by relying party")


if __name__ == "__main__":
    main()
