#!/usr/bin/env python3
"""Read-only PR metadata admissions. Labels are review state, not authority."""
import json
import os

FAMILIES=("type:","area:","status:","risk:","priority:")
ALLOWED_RISK={"risk:C0-public-read","risk:C1-repo-change"}
def validate(event):
    pull=event.get("pull_request")
    if not pull:
        return ["Missing pull request object"]
    labels={x.get("name","") for x in pull.get("labels",[])}
    errors=[]
    for prefix in FAMILIES:
        group=[name for name in labels if name.startswith(prefix)]
        if len(group)!=1:
            errors.append(f"Expected exactly one {prefix} label; found {len(group)}")
    if not (labels & ALLOWED_RISK):
        errors.append("Public repository PR must be C0 or C1")
    body=pull.get("body") or ""
    if len(body.strip())<150:
        errors.append("PR requires substantive scope/evidence/disclosure explanation")
    for section in ("disclosure","review","check"):
        if section not in body.lower():
            errors.append("PR description missing discussion of "+section)
    return errors

def main():
    if os.environ.get("GITHUB_EVENT_NAME")!="pull_request":
        print("PASS: PR metadata gate not applicable to non-PR event")
        return
    raw=os.environ.get("GH_PR_METADATA_JSON")
    if not raw:
        raise SystemExit("BLOCK: required PR metadata was not supplied")
    event={"pull_request": json.loads(raw)}
    issues=validate(event)
    for issue in issues:
        print("BLOCK:",issue)
    if issues:
        raise SystemExit(1)
    print("PASS: PR labeling, public consequence class and required review description")
    print("LIMITATION: metadata does not attest authorship, safety or authority")

if __name__=="__main__":
    main()
