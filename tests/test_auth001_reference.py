#!/usr/bin/env python3
"""AUTH-001: bounded, executable, synthetic approval-binding controls.

This measures deliberately naive and guarded *reference implementations*, not
Hardbound, Hestia, or deployed GhostMesh. No external files/credentials/actions.
Uses only stdlib and temporary canaries.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest

CAP = 220

def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()

def preview_grant(command: bytes) -> str:
    """Deliberately flawed: an authorization keyed on a truncated preview."""
    return digest(command[:CAP])

def bound_grant(command: bytes) -> str:
    """Reference binding of full canonical act bytes."""
    return digest(command)

def read_naive(root: Path, relative: str) -> bytes:
    """Deliberately flawed: follows aliases and re-resolves the root name."""
    return (root / relative).read_bytes()

def read_guarded(root_fd: int, name: str) -> bytes:
    """Single-component POSIX reference: pin root FD, prohibit final symlinks."""
    if not name or name in (".", "..") or "/" in name or "\0" in name:
        raise PermissionError("unapproved pathname")
    fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=root_fd)
    try:
        with os.fdopen(fd, "rb", closefd=False) as f:
            return f.read()
    finally:
        os.close(fd)

def read_bound_bytes(path: Path, grant_digest: str) -> bytes:
    """Read once from one file descriptor; check exactly the bytes returned."""
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        with os.fdopen(fd, "rb", closefd=False) as f:
            content = f.read()
    finally:
        os.close(fd)
    if digest(content) != grant_digest:
        raise PermissionError("content does not match approved digest")
    return content

class TestApprovalBindings(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="ghostmesh-auth001-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "approved"
        self.root.mkdir()
        self.other = self.base / "outside"
        self.other.mkdir()
        (self.root / "notes.txt").write_bytes(b"SYNTHETIC_APPROVED\n")
        (self.other / "canary.txt").write_bytes(b"SYNTHETIC_OUTSIDE_CANARY\n")
        self.dirfd = os.open(self.root, os.O_RDONLY | os.O_DIRECTORY)
        self.addCleanup(os.close, self.dirfd)

    def test_01_baseline_naive_allows_real_file(self):
        self.assertEqual(read_naive(self.root, "notes.txt"), b"SYNTHETIC_APPROVED\n")

    def test_02_baseline_guarded_allows_real_file(self):
        self.assertEqual(read_guarded(self.dirfd, "notes.txt"), b"SYNTHETIC_APPROVED\n")

    def test_03_symlink_naive_crosses_boundary(self):
        (self.root / "alias.txt").symlink_to(self.other / "canary.txt")
        self.assertEqual(read_naive(self.root, "alias.txt"), b"SYNTHETIC_OUTSIDE_CANARY\n")

    def test_04_symlink_guarded_denies(self):
        (self.root / "alias.txt").symlink_to(self.other / "canary.txt")
        with self.assertRaises(OSError):
            read_guarded(self.dirfd, "alias.txt")

    def test_05_swapped_root_naive_follows_new_directory(self):
        replacement = self.other / "notes.txt"
        replacement.write_bytes(b"SYNTHETIC_DIFFERENT_ROOT\n")
        self.root.rename(self.base / "approved-moved")
        self.root.symlink_to(self.other, target_is_directory=True)
        self.assertEqual(read_naive(self.root, "notes.txt"), b"SYNTHETIC_DIFFERENT_ROOT\n")

    def test_06_swapped_root_guarded_preserves_approved_fd(self):
        (self.other / "notes.txt").write_bytes(b"SYNTHETIC_DIFFERENT_ROOT\n")
        self.root.rename(self.base / "approved-moved")
        self.root.symlink_to(self.other, target_is_directory=True)
        self.assertEqual(read_guarded(self.dirfd, "notes.txt"), b"SYNTHETIC_APPROVED\n")

    def test_07_changed_script_naive_path_returns_new_bytes(self):
        file = self.root / "script.txt"
        file.write_bytes(b"APPROVED_SYNTHETIC_SCRIPT_V1\n")
        file.write_bytes(b"UNAPPROVED_SYNTHETIC_SCRIPT_V2\n")
        self.assertEqual(read_naive(self.root, "script.txt"), b"UNAPPROVED_SYNTHETIC_SCRIPT_V2\n")

    def test_08_changed_script_bound_read_denies(self):
        file = self.root / "script.txt"
        file.write_bytes(b"APPROVED_SYNTHETIC_SCRIPT_V1\n")
        approved_digest = digest(file.read_bytes())
        file.write_bytes(b"UNAPPROVED_SYNTHETIC_SCRIPT_V2\n")
        with self.assertRaises(PermissionError):
            read_bound_bytes(file, approved_digest)

    def test_09_unchanged_script_bound_read_succeeds(self):
        file = self.root / "script.txt"
        file.write_bytes(b"APPROVED_SYNTHETIC_SCRIPT_V1\n")
        self.assertEqual(read_bound_bytes(file, digest(file.read_bytes())),
                         b"APPROVED_SYNTHETIC_SCRIPT_V1\n")

    def test_10_preview_collision_replays_naive_grant(self):
        command_a = b"SAFE_SYNTHETIC " + b"X" * 220 + b" ACT_A"
        command_b = b"SAFE_SYNTHETIC " + b"X" * 220 + b" ACT_B"
        self.assertNotEqual(command_a, command_b)
        self.assertEqual(preview_grant(command_a), preview_grant(command_b))

    def test_11_full_act_binding_rejects_preview_collision(self):
        command_a = b"SAFE_SYNTHETIC " + b"X" * 220 + b" ACT_A"
        command_b = b"SAFE_SYNTHETIC " + b"X" * 220 + b" ACT_B"
        self.assertNotEqual(bound_grant(command_a), bound_grant(command_b))

    def test_12_masked_preview_does_not_define_identity(self):
        a = b"--token SYNTHETIC_ONE"
        b = b"--token SYNTHETIC_TWO"
        self.assertEqual(b"--token [REDACTED]", b"--token [REDACTED]")
        self.assertNotEqual(bound_grant(a), bound_grant(b))

    def test_13_different_revision_must_be_new_grant(self):
        action_a = json.dumps({"op":"read","scope":"sandbox","rev":"R1"},sort_keys=True).encode()
        action_b = json.dumps({"op":"read","scope":"sandbox","rev":"R2"},sort_keys=True).encode()
        self.assertNotEqual(bound_grant(action_a), bound_grant(action_b))

    def test_14_identical_act_has_stable_identity(self):
        action = b'{"op":"read","scope":"sandbox","rev":"R1"}'
        self.assertEqual(bound_grant(action), bound_grant(action))

    def test_15_symlink_path_component_rejected(self):
        with self.assertRaises(PermissionError):
            read_guarded(self.dirfd, "../outside/canary.txt")

    def test_16_absent_path_is_not_success(self):
        with self.assertRaises(FileNotFoundError):
            read_guarded(self.dirfd, "missing.txt")

    def test_17_reported_success_is_not_independent_effect(self):
        synthetic = {"policy":"allow", "reported_success":True,
                     "independent_effect_witness":None}
        self.assertIsNone(synthetic["independent_effect_witness"])

    def test_18_skipped_security_checks_remain_unobserved(self):
        synthetic = {"ci":"success","sandbox_checks":{"passed":0,"skipped":5}}
        self.assertEqual(synthetic["sandbox_checks"]["passed"],0)
        self.assertEqual(synthetic["sandbox_checks"]["skipped"],5)

    def test_19_valid_allow_still_works_after_positive_ref(self):
        before = read_guarded(self.dirfd, "notes.txt")
        after = read_guarded(self.dirfd, "notes.txt")
        self.assertEqual(before,after)

    def test_20_approval_does_not_inherit_different_actor(self):
        a = json.dumps({"actor":"operator-1","op":"read"},sort_keys=True).encode()
        b = json.dumps({"actor":"operator-2","op":"read"},sort_keys=True).encode()
        self.assertNotEqual(bound_grant(a),bound_grant(b))

if __name__ == "__main__":
    unittest.main(verbosity=2)
