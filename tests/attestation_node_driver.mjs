// Test-only Node driver. Requests come from local Python unit tests via stdin.
// Inputs are supplied synthetic trust records, NOT independently accredited roots.
import { readFileSync } from "node:fs";
import { generateKeyPairSync, sign } from "node:crypto";
import { canonicalJson, signingBytes, verifySynthetic } from "../tools/verify_synthetic_attestation.mjs";

function run() {
  const request = JSON.parse(readFileSync(0, "utf8"));
  if (request.operation === "issue_ephemeral_test") {
    const { privateKey, publicKey } = generateKeyPairSync("ed25519");
    const payload = request.payload;
    const keyId = "ephemeral-lab-key";
    const sig = sign(null, signingBytes(keyId, payload), privateKey);
    const envelope = canonicalJson({
      payload,
      signature: { algorithm: "Ed25519", key_id: keyId, value: sig.toString("base64url") },
    });
    const spki = publicKey.export({ type: "spki", format: "der" });
    return { status: "TEST_VECTOR_ONLY", envelope_b64: envelope.toString("base64url"),
      public_key_raw_hex: spki.subarray(-32).toString("hex") };
  }
  if (request.operation === "verify") {
    const record = request.trust;
    const trust = new Map([[record.key_id, {
      publicKeyRaw: Buffer.from(record.public_key_raw_hex, "hex"),
      issuer: record.issuer, role: record.role, audiences: record.audiences,
      status: record.status, notBefore: record.not_before, notAfter: record.not_after,
    }]]);
    const observed = verifySynthetic(Buffer.from(request.envelope_b64, "base64url"),
      trust, { expectedAudience: request.expected_audience, now: request.now, replaySeen: new Set() });
    return observed;
  }
  throw new Error("Unsupported test request");
}
try {
  process.stdout.write(JSON.stringify(run()) + "\n");
} catch (error) {
  process.stdout.write(JSON.stringify({ status: "REJECTED", category: "SYNTHETIC_VALIDATION" }) + "\n");
  process.exitCode = 1;
}
