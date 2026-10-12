// Independent Node.js implementation of the restricted GhostMesh synthetic Ed25519 profile.
// TEST ONLY. No production identity, authority, trust roots, or durable replay storage.
import { createPublicKey, verify as verifySignature } from "node:crypto";

export class AttestationRejected extends Error {}
const DOMAIN = Buffer.from("ghostmesh-lab.synthetic-attestation.v0.1\0", "ascii");
const SPKI_PREFIX = Buffer.from("302a300506032b6570032100", "hex");
const MAX_BYTES = 4096;
const MAX_SAFE = Number.MAX_SAFE_INTEGER;
const EVENT_ROLES = Object.freeze({
  "synthetic.observation": "synthetic-observer",
  "synthetic.harness-report": "synthetic-reporter",
});
const PAYLOAD_FIELDS = ["audience", "claim", "event_type", "expires_at", "issued_at", "issuer",
  "nonce", "policy_version", "schema", "sequence", "subject"];
const ENVELOPE_FIELDS = ["payload", "signature"];
const SIG_FIELDS = ["algorithm", "key_id", "value"];
const actorRx = /^[a-z][a-z0-9-]{2,63}$/;
const nonceRx = /^[0-9a-f]{32}$/;
const keyRx = /^[a-z][a-z0-9-]{2,63}$/;
const sigRx = /^[A-Za-z0-9_-]{86}$/;

function reject(reason) { throw new AttestationRejected(reason); }
function exactFields(obj, fields) {
  return obj !== null && typeof obj === "object" && !Array.isArray(obj) &&
    Object.keys(obj).length === fields.length &&
    fields.every(k => Object.hasOwn(obj, k));
}
function printableAscii(value) {
  return typeof value === "string" && /^[\x20-\x7E]*$/.test(value);
}
export function canonicalJson(value) {
  function walk(item, depth) {
    if (depth > 4) reject("canonicalization depth");
    if (item === null || typeof item === "boolean") return item;
    if (typeof item === "number") {
      if (!Number.isSafeInteger(item)) reject("unsafe or fractional JSON number");
      return item;
    }
    if (typeof item === "string") {
      if (!printableAscii(item)) reject("non-printable ASCII / Unicode unsupported");
      return item;
    }
    if (Array.isArray(item)) return item.map(v => walk(v, depth + 1));
    if (item && typeof item === "object") {
      const copy = {};
      for (const key of Object.keys(item).sort()) {
        if (!printableAscii(key)) reject("bad JSON key");
        Object.defineProperty(copy, key, {
          value: walk(item[key], depth + 1), enumerable: true, configurable: true, writable: true,
        });
      }
      return copy;
    }
    reject("unsupported JSON type");
  }
  const out = Buffer.from(JSON.stringify(walk(value, 0)), "ascii");
  if (out.length > MAX_BYTES) reject("oversize data");
  return out;
}
export function signingBytes(keyId, payload) {
  if (typeof keyId !== "string" || !keyRx.test(keyId)) reject("invalid signing key id");
  return Buffer.concat([DOMAIN, canonicalJson({ key_id: keyId, payload })]);
}
function decodeExact(raw) {
  if (!Buffer.isBuffer(raw) || raw.length > MAX_BYTES) reject("invalid envelope bytes");
  let data;
  try { data = JSON.parse(raw.toString("utf8")); } catch { reject("bad JSON envelope"); }
  if (!raw.equals(canonicalJson(data))) reject("noncanonical envelope");
  return data; // Duplicate-key strings cannot match reserialized canonical bytes.
}
function safeTime(n) { return typeof n === "number" && Number.isSafeInteger(n); }
function validatePayload(p, expectedAudience, now) {
  if (!exactFields(p, PAYLOAD_FIELDS)) reject("invalid payload fields");
  if (p.schema !== "ghostmesh.synthetic-attestation/v0.1") reject("unknown schema");
  if (!Object.hasOwn(EVENT_ROLES, p.event_type)) reject("unknown event type");
  if (p.policy_version !== "synthetic-policy-v1") reject("unrecognized policy version");
  for (const k of ["issuer", "subject", "audience"]) {
    if (typeof p[k] !== "string" || !actorRx.test(p[k])) reject("invalid actor");
  }
  if (p.audience !== expectedAudience) reject("wrong audience");
  if (typeof p.nonce !== "string" || !nonceRx.test(p.nonce)) reject("invalid nonce");
  if (!safeTime(p.sequence) || p.sequence < 1) reject("invalid sequence");
  if (!safeTime(p.issued_at) || !safeTime(p.expires_at)) reject("invalid validity");
  if (p.issued_at > now + 60 || p.expires_at <= now || p.expires_at <= p.issued_at)
    reject("expired or future statement");
  if (p.expires_at - p.issued_at > 3600) reject("excessive lifetime");
  if (typeof p.claim !== "string" || p.claim.length < 10 || p.claim.length > 240)
    reject("invalid claim");
  canonicalJson(p);
}
export function verifySynthetic(raw, trust, { expectedAudience, now, replaySeen }) {
  if (!safeTime(now) || !(trust instanceof Map) || !(replaySeen instanceof Set))
    reject("invalid local verification context");
  const env = decodeExact(raw);
  if (!exactFields(env, ENVELOPE_FIELDS) || !exactFields(env.signature, SIG_FIELDS))
    reject("unexpected signature envelope");
  const sig = env.signature;
  if (sig.algorithm !== "Ed25519" || typeof sig.key_id !== "string" || !keyRx.test(sig.key_id))
    reject("unsupported signature type or key ID");
  const record = trust.get(sig.key_id);
  if (!record || record.status !== "active") reject("unknown or revoked key");
  validatePayload(env.payload, expectedAudience, now);
  const p = env.payload;
  if (p.issuer !== record.issuer || p.audience !== expectedAudience ||
      !record.audiences.includes(p.audience)) reject("issuer or audience not trusted");
  if (record.role !== EVENT_ROLES[p.event_type]) reject("role disallowed for event");
  if (!safeTime(record.notBefore) || !safeTime(record.notAfter) ||
      !(record.notBefore <= p.issued_at && p.issued_at < record.notAfter &&
        record.notBefore <= now && now < record.notAfter)) reject("key invalid at event time");
  if (typeof sig.value !== "string" || !sigRx.test(sig.value))
    reject("signature encoding rejected");
  const signature = Buffer.from(sig.value, "base64url");
  if (signature.length !== 64 || signature.toString("base64url") !== sig.value)
    reject("signature encoding not canonical");
  if (!Buffer.isBuffer(record.publicKeyRaw) || record.publicKeyRaw.length !== 32)
    reject("invalid Ed25519 trust key bytes");
  let key;
  try { key = createPublicKey({ key: Buffer.concat([SPKI_PREFIX, record.publicKeyRaw]),
    format: "der", type: "spki" }); }
  catch { reject("invalid trust public key"); }
  if (!verifySignature(null, signingBytes(sig.key_id, p), key, signature))
    reject("invalid cryptographic signature");
  const tokenN = `${sig.key_id}:nonce:${p.nonce}`;
  const tokenS = `${sig.key_id}:sequence:${p.sequence}`;
  if (replaySeen.has(tokenN) || replaySeen.has(tokenS)) reject("replay or reused sequence");
  replaySeen.add(tokenN);
  replaySeen.add(tokenS);
  return {
    status: "CRYPTO_VERIFIED_SYNTHETIC_ONLY",
    signing_key_id: sig.key_id,
    issuer: p.issuer,
    event_type: p.event_type,
    identity_accepted_within_supplied_synthetic_trust_map: true,
    source_truth_verified: false,
    independent_witness_verified: false,
    real_world_authority: "NONE",
    actual_effect: "UNKNOWN",
  };
}
