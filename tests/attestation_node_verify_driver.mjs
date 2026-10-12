// Fixed-purpose OFFLINE TEST driver: verify one externally provided synthetic vector.
// Trust records come from its Python test harness and are not accredited trust anchors.
import { readFileSync } from "node:fs";
import { verifySynthetic } from "../tools/verify_synthetic_attestation.mjs";

try {
  const request = JSON.parse(readFileSync(0, "utf8"));
  const record = request.trust;
  const trust = new Map([[record.key_id, {
    publicKeyRaw: Buffer.from(record.public_key_raw_hex, "hex"),
    issuer: record.issuer, role: record.role, audiences: record.audiences,
    status: record.status, notBefore: record.not_before, notAfter: record.not_after,
  }]]);
  const observed = verifySynthetic(Buffer.from(request.envelope_b64, "base64url"),
    trust, { expectedAudience: request.expected_audience, now: request.now, replaySeen: new Set() });
  process.stdout.write(JSON.stringify(observed) + "\n");
} catch {
  process.stdout.write(JSON.stringify({ status: "REJECTED", category: "SYNTHETIC_VALIDATION" }) + "\n");
  process.exitCode = 1;
}
