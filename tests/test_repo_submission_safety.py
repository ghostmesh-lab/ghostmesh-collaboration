#!/usr/bin/env python3
"""Static adversarial checks for unsafe repository submission patterns."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SecurityWorkflow(unittest.TestCase):
    def test_no_privileged_pr_workflow(self):
        for path in (ROOT / ".github/workflows").glob("*.yml"):
            content = path.read_text(encoding="utf-8")
            self.assertNotIn("pull_request_target:", content, str(path))
            self.assertNotIn("workflow_run:", content, str(path))
            self.assertNotIn("id-token: write", content, str(path))
            self.assertNotIn("contents: write", content, str(path))

    def test_sha_pinned_actions(self):
        for path in (ROOT / ".github/workflows").glob("*.yml"):
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip().startswith("- uses:"):
                    action = line.partition("uses:")[2].strip()
                    self.assertRegex(action, r"^actions/[a-z-]+@[a-f0-9]{40}$")

    def test_synthetic_only_interchange(self):
        import json
        manifest = json.loads((ROOT / "federation.manifest.json").read_text())
        self.assertFalse(manifest["live_federation"])
        self.assertFalse(manifest["authority_grants"])
        self.assertIsNone(manifest["execution_endpoint"])
        self.assertIsNone(manifest["enrollment_endpoint"])

    def test_owner_contract_present(self):
        self.assertTrue((ROOT / ".github/CODEOWNERS").is_file())
        self.assertTrue((ROOT / "SECURITY.md").is_file())
        self.assertTrue((ROOT / "AGENTS.md").is_file())


if __name__ == "__main__":
    unittest.main()
