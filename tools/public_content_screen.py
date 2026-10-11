#!/usr/bin/env python3
"""Fail-closed public-content screening for known sensitive patterns.
Heuristic only: not a guarantee of confidentiality, authorization or complete PII detection.
"""
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
ALLOW_PUBLIC_EMAIL = {"ghostmesh@malott.ai"}
MAX_TEXT_BYTES = 1_000_000

# Keep these narrow enough that docs explaining threats remain valid.
PATTERNS = {
    "private-key-header": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github-token": re.compile(r"(?:gh[pousr]_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{35,})"),
    "slack-token": re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}"),
    "aws-key-id": re.compile(r"(?:AKIA|ASIA)[A-Z0-9]{16}"),
    "openai-key": re.compile(r"sk-(?:proj-)?[A-Za-z0-9_-]{24,}"),
    "bearer-token": re.compile(r"(?i)authorization\s*[:=]\s*bearer\s+[A-Za-z0-9._~+/-]{20,}"),
    "password-assignment": re.compile(r"(?i)\b(?:password|api[_-]?key|client[_-]?secret|access[_-]?token)\b\s*[:=]\s*['\"][A-Za-z0-9._+/=-]{15,}['\"]"),
    "private-absolute-path": re.compile(r"(?:/Users/[A-Za-z0-9._-]+/|/home/(?!runner/)[A-Za-z0-9._-]+/|C:\\Users\\[A-Za-z0-9._-]+\\)"),
    "ssn-format": re.compile(r"\b(?!000|666|9\d\d)\d{3}-(?!00)\d{2}-(?!0000)\d{4}\b"),
}
EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")

def scan(text):
    found = []
    for name, expression in PATTERNS.items():
        if expression.search(text):
            found.append(name)
    if any(match.group(0).lower() not in ALLOW_PUBLIC_EMAIL
           for match in EMAIL.finditer(text)):
        found.append("unreviewed-email-address")
    return found

def main():
    tracked = subprocess.check_output(["git", "-C", str(ROOT), "ls-files", "-z"])
    files = [x.decode() for x in tracked.split(b"\0") if x]
    failures = []
    for name in files:
        path = ROOT / name
        if not path.is_file():
            continue
        payload = path.read_bytes()
        if len(payload) > MAX_TEXT_BYTES:
            failures.append((name, "oversize-public-file"))
            continue
        if b"\0" in payload:
            failures.append((name, "binary-content-requires-human-review"))
            continue
        try:
            data = payload.decode("utf-8")
        except UnicodeDecodeError:
            failures.append((name, "non-utf8-content"))
            continue
        for issue in scan(data):
            failures.append((name, issue))
    for name, issue in failures:
        print("BLOCK:", name, issue)
    if failures:
        sys.exit(1)
    print("PASS: heuristic public-content screening (" + str(len(files)) + " tracked files).")
    print("LIMITATION: false negatives are possible; no PII or secret-prevention guarantee.")

if __name__ == "__main__":
    main()
