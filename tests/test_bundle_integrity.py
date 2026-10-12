#!/usr/bin/env python3
"""Adversarial offline tests: internal consistency is not independent attestation."""
import copy
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("bundle_verifier", ROOT / "tools/verify_bundle.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
MANIFEST = json.loads((ROOT / "bundles/st001/manifest.json").read_text(encoding="utf-8"))


class BundleAssurance(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        for relative in mod.ALLOWED_FILES.values():
            source = ROOT / relative
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)

    def verify(self, manifest=None):
        return mod.verify(manifest if manifest is not None else copy.deepcopy(MANIFEST), self.root)

    def test_normal_bundle_matches(self):
        self.assertEqual(self.verify(), [])

    def test_tampered_bytes_rejected(self):
        path = self.root / mod.ALLOWED_FILES["fixture"]
        path.write_bytes(path.read_bytes() + b"\n")
        self.assertTrue(any("mismatch" in error for error in self.verify()))

    def test_tampered_digest_rejected(self):
        mutated = copy.deepcopy(MANIFEST)
        mutated["files"][0]["sha256"] = "0" * 64
        self.assertTrue(self.verify(mutated))

    def test_unreviewed_signature_claim_field_rejected(self):
        mutated = copy.deepcopy(MANIFEST)
        mutated["verified_external_signer"] = "imagined"
        self.assertTrue(self.verify(mutated))

    def test_hash_algorithm_swap_rejected(self):
        mutated = copy.deepcopy(MANIFEST)
        mutated["digest_algorithm"] = "MD5"
        self.assertTrue(self.verify(mutated))

    def test_noncanonical_relative_path_rejected(self):
        mutated = copy.deepcopy(MANIFEST)
        mutated["files"][0]["path"] = "fixtures//v0.1/stale-truth.json"
        self.assertTrue(self.verify(mutated))

    def test_unreviewed_file_claim_field_rejected(self):
        mutated = copy.deepcopy(MANIFEST)
        mutated["files"][0]["external_truth_verified"] = True
        self.assertTrue(self.verify(mutated))

    def test_fake_signature_claim_rejected(self):
        mutated = copy.deepcopy(MANIFEST)
        mutated["signature_status"] = "ED25519_VERIFIED"
        self.assertTrue(self.verify(mutated))

    def test_fake_authority_rejected(self):
        mutated = copy.deepcopy(MANIFEST)
        mutated["grants_external_authority"] = True
        self.assertTrue(self.verify(mutated))

    def test_fake_independent_result_rejected(self):
        mutated = copy.deepcopy(MANIFEST)
        mutated["independently_reproduced"] = True
        self.assertTrue(self.verify(mutated))

    def test_parent_traversal_rejected(self):
        mutated = copy.deepcopy(MANIFEST)
        mutated["files"][0]["path"] = "../../private.txt"
        self.assertTrue(self.verify(mutated))

    def test_unapproved_valid_path_rejected(self):
        mutated = copy.deepcopy(MANIFEST)
        mutated["files"][0]["path"] = "other/not-an-approved-fixture.json"
        self.assertTrue(self.verify(mutated))

    def test_role_substitution_rejected(self):
        mutated = copy.deepcopy(MANIFEST)
        mutated["files"][0]["role"] = "reference_output"
        self.assertTrue(self.verify(mutated))

    def test_duplicate_role_rejected(self):
        mutated = copy.deepcopy(MANIFEST)
        mutated["files"][1]["role"] = "fixture"
        self.assertTrue(self.verify(mutated))

    def test_symlink_rejected(self):
        source = self.root / mod.ALLOWED_FILES["fixture"]
        source.unlink()
        source.symlink_to(self.root / mod.ALLOWED_FILES["evaluator"])
        self.assertTrue(self.verify())


if __name__ == "__main__":
    unittest.main()
