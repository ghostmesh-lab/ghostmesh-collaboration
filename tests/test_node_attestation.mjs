import test from "node:test";
import assert from "node:assert/strict";
import { generateKeyPairSync, sign } from "node:crypto";
import { canonicalJson, signingBytes, verifySynthetic, AttestationRejected }
  from "../tools/verify_synthetic_attestation.mjs";

const NOW = 1000000;
const ID = "ephemeral-lab-key";
const AUDIENCE = "synthetic-lab-beta";
const ISSUER = "synthetic-lab-alpha";

function caseFile(overrides = {}) {
  const { privateKey, publicKey } = generateKeyPairSync("ed25519");
  const payload = {
    schema: "ghostmesh.synthetic-attestation/v0.1",
    event_type: "synthetic.observation",
    issuer: ISSUER, subject: "synthetic-service", audience: AUDIENCE,
    policy_version: "synthetic-policy-v1",
    issued_at: NOW-30, expires_at: NOW+300,
    nonce: "00112233445566778899aabbccddeeff",
    sequence: 1, claim: "A synthetic service appears healthy", ...overrides,
  };
  const signature = sign(null, signingBytes(ID, payload), privateKey).toString("base64url");
  const raw = canonicalJson({ payload,
    signature: { algorithm: "Ed25519", key_id: ID, value: signature } });
  const publicKeyRaw = publicKey.export({ type: "spki", format: "der" }).subarray(-32);
  const trust = new Map([[ID, { publicKeyRaw, issuer: ISSUER, role: "synthetic-observer",
    audiences: [AUDIENCE], notBefore: NOW-1000, notAfter: NOW+2000, status: "active" }]]);
  return { raw, trust };
}

test("Node verifier accepts an ephemeral synthetic signature", () => {
  const { raw, trust } = caseFile();
  const result = verifySynthetic(raw, trust, { expectedAudience: AUDIENCE, now: NOW, replaySeen: new Set() });
  assert.equal(result.status, "CRYPTO_VERIFIED_SYNTHETIC_ONLY");
  assert.equal(result.real_world_authority, "NONE");
  assert.equal(result.actual_effect, "UNKNOWN");
  assert.equal(result.independent_witness_verified, false);
});
test("Node verifier refuses second use of the same nonce/sequence", () => {
  const { raw, trust } = caseFile();
  const replaySeen = new Set();
  verifySynthetic(raw, trust, { expectedAudience: AUDIENCE, now: NOW, replaySeen });
  assert.throws(() => verifySynthetic(raw, trust, { expectedAudience: AUDIENCE, now: NOW, replaySeen }),
    AttestationRejected);
});
test("Node verifier refuses revoked trust", () => {
  const { raw, trust } = caseFile();
  trust.get(ID).status = "revoked";
  assert.throws(() => verifySynthetic(raw, trust, {
    expectedAudience: AUDIENCE, now: NOW, replaySeen: new Set() }), AttestationRejected);
});
test("Node verifier refuses wrong audience", () => {
  const { raw, trust } = caseFile();
  assert.throws(() => verifySynthetic(raw, trust, {
    expectedAudience: "synthetic-other-lab", now: NOW, replaySeen: new Set() }), AttestationRejected);
});
test("Node verifier refuses wrong key material", () => {
  const first = caseFile(), second = caseFile();
  first.trust.get(ID).publicKeyRaw = second.trust.get(ID).publicKeyRaw;
  assert.throws(() => verifySynthetic(first.raw, first.trust, {
    expectedAudience: AUDIENCE, now: NOW, replaySeen: new Set() }), AttestationRejected);
});
test("Node verifier refuses unsigned edits", () => {
  const { raw, trust } = caseFile();
  const edited = JSON.parse(raw.toString("ascii"));
  edited.payload.claim = "Synthetic false assertion after an unauthorized change";
  assert.throws(() => verifySynthetic(canonicalJson(edited), trust, {
    expectedAudience: AUDIENCE, now: NOW, replaySeen: new Set() }), AttestationRejected);
});
test("Node verifier refuses extra authority fields", () => {
  const { raw, trust } = caseFile();
  const edited = JSON.parse(raw.toString("ascii"));
  edited.payload.production_grant = "none";
  assert.throws(() => verifySynthetic(canonicalJson(edited), trust, {
    expectedAudience: AUDIENCE, now: NOW, replaySeen: new Set() }), AttestationRejected);
});
test("Node canonicalizer refuses non-ASCII, controls, and floats", () => {
  for (const bad of ["café", "a\nb", 1.5, Number.MAX_SAFE_INTEGER + 1]) {
    assert.throws(() => canonicalJson({ claim: bad }), AttestationRejected);
  }
});
test("Node canonical encoding refuses duplicated JSON fields", () => {
  const { raw, trust } = caseFile();
  const duplicate = Buffer.from(raw.toString("ascii").replace('{"payload":', '{"payload":null,"payload":'), "ascii");
  assert.throws(() => verifySynthetic(duplicate, trust, {
    expectedAudience: AUDIENCE, now: NOW, replaySeen: new Set() }), AttestationRejected);
});
