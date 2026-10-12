// Fixed-purpose OFFLINE TEST vector generator. No external identity or authority.
import { readFileSync } from "node:fs";
import { generateKeyPairSync, sign } from "node:crypto";
import { canonicalJson, signingBytes } from "../tools/verify_synthetic_attestation.mjs";

try {
  const request = JSON.parse(readFileSync(0, "utf8"));
  const { privateKey, publicKey } = generateKeyPairSync("ed25519");
  const payload = request.payload;
  const keyId = "ephemeral-lab-key";
  const sig = sign(null, signingBytes(keyId, payload), privateKey);
  const envelope = canonicalJson({
    payload,
    signature: { algorithm: "Ed25519", key_id: keyId, value: sig.toString("base64url") },
  });
  const spki = publicKey.export({ type: "spki", format: "der" });
  process.stdout.write(JSON.stringify({
    status: "TEST_VECTOR_ONLY",
    envelope_b64: envelope.toString("base64url"),
    public_key_raw_hex: spki.subarray(-32).toString("hex"),
  }) + "\n");
} catch {
  process.stdout.write(JSON.stringify({ status: "REJECTED", category: "SYNTHETIC_VECTOR" }) + "\n");
  process.exitCode = 1;
}
