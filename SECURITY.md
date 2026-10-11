# Public collaboration security and privacy boundary

This is a **public repository**. Assume every issue, comment, commit, attachment, and pull request may be indexed, mirrored, archived, and copied.

## Permitted

- Original public explanations and links to existing public research.
- Synthetic or explicitly sanitized scenarios with no live identifying, operational, or personal data.
- Public-facing schemas, expectations, hypotheses, verifier descriptions, and non-sensitive test outcomes.
- Constructive debate and citations with appropriate attribution and copyright permissions.

## Prohibited

- Passwords, API tokens, signing/recovery keys, session cookies, secret URLs, customer or personal data.
- Internal hostnames/IPs, network inventories, production topology, deployment commands, unreleased environment configuration, detailed private logs, or private repository contents.
- Unreviewed adversarial exploit instructions, active attack demonstrations against real systems, or details that could compromise participating infrastructure.
- Material from private correspondence, private Slack channels, or proprietary work without explicit rights-holder approval.
- Executable integrations that connect to any contributor's live system, or instructions claiming to authorize changes to it.

## Research safety

Tests should use synthetic identities, independent fixtures, scoped consequence classes, and offline or isolated evaluations. Any system's output labeled `PASS` must be tied to the exact tested claim, input, verifier, and evidence boundaries; unknown coverage remains `UNKNOWN`.

## Reporting sensitive findings

Do **not** open a public issue that exposes a vulnerability or sensitive information. Contact the affected project owner through its independently published private reporting channel, or contact the GhostMesh owner at ghostmesh@malott.ai for matters affecting this collaboration surface. Never paste secrets into email or a public issue.

The repository itself does not grant access to incident response systems or request credentials.
