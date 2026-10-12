#!/usr/bin/env python3
"""Deterministic local publication contract checks. Does not call GitHub or certify safety."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]+)\)")
PUBLIC_OWNER = "https://github.com/ghostmesh-lab/ghostmesh-collaboration"
FORBIDDEN_OLD_OWNER = "https://github.com/pinklon/ghostmesh-collaboration"
REQUIRED = (
    "README.md", "START_HERE.md", "AGENTS.md", "SECURITY.md",
    "GOVERNANCE.md", "CONTRIBUTING.md", "LICENSE-DECISION.md",
    "docs/NORTH_STAR.md", "architecture/GHOSTMESH_SYSTEM_MAP.md",
    "docs/GHOSTMESH_TECHNICAL_DISCLOSURE_V0_3.md",
    "docs/PUBLIC_EVIDENCE_RELEASE_STANDARD.md",
    "docs/ADVERSARIAL_READINESS_REVIEW.md",
    "docs/COLLABORATOR_KICKOFF.md", "experiments/ROUND_ONE_EXPERIMENT.md",
    "tools/evaluate_stale_truth.py", "examples/stale-truth-reference-output.json",
    "docs/PUBLICATION_READINESS.md", "publication-readiness.json",
    "docs/CRYPTOGRAPHIC_ASSURANCE_POLICY.md", "docs/LICENSE_RATIFICATION_PROPOSAL.md",
    "docs/INDEPENDENT_REVIEW_CONTRACT.md",
    "bundles/st001/README.md", "bundles/st001/manifest.json", "tools/verify_bundle.py",
    "docs/ARCHITECTURE_AT_A_GLANCE.md", "docs/RESEARCHER_QUICKSTART.md",
    "examples/README.md", "schemas/research-result.v0.1.schema.json",
    "examples/research-result-template.v0.1.json",
)


def check_link(source: Path, href: str, root: Path = ROOT) -> str | None:
    href = href.strip().split(" \"", 1)[0].split(" '", 1)[0]
    if not href:
        return "empty link target"
    if href.startswith("#"):
        return None  # Anchor-specific verification not performed.
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc:
        if parsed.scheme not in {"http", "https", "mailto"}:
            return "unexpected link scheme"
        return None  # External reachability is explicitly unverified.
    if href.startswith("/") or href.startswith("\\"):
        return "absolute local path"
    local_path = unquote(parsed.path)
    if not local_path:
        return None
    candidate_before_resolve = source.parent / local_path
    if candidate_before_resolve.is_symlink():
        return "symlink target prohibited"
    candidate = candidate_before_resolve.resolve()
    resolved_root = root.resolve()
    if not candidate.is_relative_to(resolved_root):
        return "path escapes repository"
    if not candidate.exists():
        return "broken relative link"
    return None


def check_readiness(package: dict) -> list[str]:
    errors = []
    if package.get("status") != "CANDIDATE_NOT_RELEASED":
        errors.append("must remain CANDIDATE_NOT_RELEASED until separately approved")
    if package.get("repository") != PUBLIC_OWNER:
        errors.append("manifest repository must be canonical GhostMesh Lab")
    gates = package.get("release_gates", {})
    for name in ("license", "owner_disclosure_review", "independent_human_review",
                 "independent_external_reproduction", "vps_credentials"):
        if name not in gates:
            errors.append("missing explicit release gate: " + name)
    if not package.get("unresolved"):
        errors.append("cannot declare release readiness without recording blockers")
    if gates.get("cryptographic_artifact_integrity") != "BOUNDED_HASH_MANIFEST_ONLY_UNSIGNED":
        errors.append("unsigned bundle cannot be promoted into signed external attestation")
    if package.get("agent_authority_granted") is not False:
        errors.append("release manifest may not grant agent authority")
    if package.get("live_federation") is not False:
        errors.append("release manifest may not claim deployed federation")
    return errors


def scan(root: Path = ROOT) -> tuple[int, list[str]]:
    errors: list[str] = []
    for relative in REQUIRED:
        if not (root / relative).is_file():
            errors.append(f"missing required publication artifact: {relative}")
    try:
        package = json.loads((root / "publication-readiness.json").read_text(encoding="utf-8"))
        errors.extend(check_readiness(package))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append("readiness manifest unavailable or invalid: " + type(exc).__name__)
    tracked = subprocess.check_output(["git", "-C", str(root), "ls-files", "-z"])
    paths = sorted({p.decode() for p in tracked.split(b"\0") if p})
    count = 0
    for relative in paths:
        file = root / relative
        if file.suffix.lower() not in {".md", ".markdown", ".json", ".yml", ".yaml"}:
            continue
        if not file.is_file() or file.is_symlink():
            errors.append(f"{relative}: missing file or symlink")
            continue
        text = file.read_text(encoding="utf-8")
        count += 1
        if FORBIDDEN_OLD_OWNER in text:
            errors.append(f"{relative}: stale repository-owner link")
        if file.suffix.lower() not in {".md", ".markdown"}:
            continue
        for match in LINK.finditer(text):
            error = check_link(file, match.group(1), root)
            if error:
                errors.append(f"{relative}: {error}")
    return count, sorted(set(errors))


def main() -> None:
    count, errors = scan()
    for error in errors:
        print("BLOCK:", error)
    if errors:
        raise SystemExit(1)
    print(f"PASS: offline publication contract ({count} structured files) and explicit open release gates")
    print("LIMITS: no external link, private credential, real operational evidence, or human-approval verification")


if __name__ == "__main__":
    main()
