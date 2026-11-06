# SECURITY & CRYPTOGRAPHY SPECIFICATION — INKLOOM SENTINEL

## 1. Cryptographic Approval Seal
When an authorized Reviewer approves content:
1. **Canonicalization:** Content is stripped of trailing whitespaces and normalized to `\n` line endings (`canonicalize_content`).
2. **SHA-256 Hashing:** Generates a 64-character hex digest of the canonical string.
3. **Signed Manifest:**
   ```json
   {
     "submission_id": "...",
     "version_number": 1,
     "content_sha256": "...",
     "reviewer_name": "Sanchita Sharma (Reviewer)",
     "approved_at": "2026-11-05T12:00:00",
     "issuer": "Inkloom Sentinel — NexaPay Security Authority"
   }
   ```
4. **Ed25519 Asymmetric Digital Signature:**
   - Private key is stored server-side in `data/ed25519_key.pem` (never exposed to frontend).
   - If not found on boot, a persistent keypair is generated and persisted to disk.
   - Signs the canonical JSON manifest with the private key.
   - Public key is published with the signature certificate in Base64 format.

## 2. Publish Gateway Verification & Tamper Detection
Before publication to distribution channels:
1. Canonical content is re-hashed.
2. The hash is compared with `content_sha256` recorded in the approval signature.
3. The Ed25519 public key verifies the signature over the manifest bytes.
4. **Tamper Detection:** Modifying even a single character changes the SHA-256 hash completely (avalanche effect) and invalidates the Ed25519 cryptographic signature. The gateway immediately blocks release.

## 3. Server-Side Role Enforcement
- Permissions (`can_approve`, `can_request_changes`) are enforced in FastAPI backend routers using HTTP headers (`x-user-role`).
- Attempting to approve content with role `CREATOR` returns `403 Forbidden`.
