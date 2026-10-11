#!/usr/bin/env python3
"""Red-team synthetic input checks. No real secrets or personal information."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("publicscreen", ROOT / "tools/public_content_screen.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def expect_flag(name, candidate):
    result = mod.scan(candidate)
    if not result:
        raise AssertionError("Expected a safe synthetic detection: " + name)
    print("BLOCKED:", name, ",".join(result))

def main():
    expect_flag("fake-code-host-token", "gh" + "p_" + "A" * 30)
    expect_flag("fake-slack-token", "xo" + "xb-" + "A" * 25)
    expect_flag("synthetic-secret-key-header", "-----BEGIN " + "OPENSSH PRIVATE KEY-----")
    expect_flag("synthetic-password-assignment", "password" + " = " + "'" + ("M" * 25) + "'")
    expect_flag("synthetic-personal-email", "person" + "@example.com")
    expect_flag("synthetic-id-number", "123" + "-45-" + "6789")
    expect_flag("synthetic-home-path", "/home/" + "fictionaluser/private.log")
    if mod.scan("Research based on public synthetic observations. Contact ghostmesh@malott.ai."):
        raise AssertionError("Allowed public project contact unexpectedly rejected")
    print("PASS: synthetic screening negative tests and approved project address")

if __name__ == "__main__":
    main()
