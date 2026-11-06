# API REFERENCE — INKLOOM SENTINEL

Interactive Swagger documentation is available at `/docs` when the backend is running.

## 1. System & Demo
- `GET /api/health`: Health status, database connection, cryptographic engine, and AI provider status.
- `GET /api/analytics`: Aggregate statistics (submissions, pending, approved, blocked) and recent audit logs.
- `POST /api/demo/switch-role`: Toggles active persona between `CREATOR` and `REVIEWER`.

## 2. Brand Vault
- `GET /api/brand-vault/documents`: Lists all corporate guidelines and policies.
- `GET /api/brand-vault/documents/{id}`: Full document text with version history.
- `POST /api/brand-vault/documents/upload`: Uploads and parses PDF/DOCX policy documents.
- `GET /api/brand-vault/rules`: Lists active deterministic brand rules.
- `GET /api/brand-vault/glossary`: Controlled vocabulary dictionary with alternatives.
- `GET /api/brand-vault/facts`: Active and historical approved corporate facts.
- `GET /api/brand-vault/claims`: Claim Passports with evidence backing.
- `GET /api/brand-vault/assets`: Visual identity tokens and SVG brand marks.

## 3. Submissions & Intake
- `GET /api/submissions`: Lists all submissions.
- `POST /api/submissions`: Creates new content submission and executes Sentinel review pipeline.
- `GET /api/submissions/{id}`: Detailed submission with versions, reviews, comments, and approvals.
- `POST /api/submissions/upload-extract`: Previews text extraction from uploaded PDF/DOCX files.
- `POST /api/submissions/{id}/update-text`: Manually edits content, creates new version, and re-audits.

## 4. Reviews & Fix Assistant
- `GET /api/reviews/{id}`: Fetches review details and findings.
- `POST /api/reviews/{id}/fixes/{fix_id}/apply`: Accepts suggested fix, creates bumped version (e.g. v2), and re-verifies.
- `POST /api/reviews/{id}/fixes/{fix_id}/reject`: Marks fix suggestion as rejected.
- `POST /api/reviews/rerun/{submission_id}`: Re-runs audit engine on latest version.

## 5. Approvals & Workflow
- `POST /api/approvals/{submission_id}/submit`: Submits content for reviewer signoff.
- `POST /api/approvals/{submission_id}/approve`: Approves content and generates Ed25519 digital signature seal (Reviewer only).
- `POST /api/approvals/{submission_id}/request-changes`: Requests changes with reviewer notes.
- `POST /api/approvals/{submission_id}/comments`: Adds internal governance comment.

## 6. Releases & Tamper Protection
- `GET /api/releases/{submission_id}/verify`: Inspects cryptographic Ed25519 signature and SHA-256 seal.
- `POST /api/releases/{submission_id}/publish`: Verifies signature before publishing to distribution.
- `POST /api/releases/{submission_id}/tamper-test`: Executes the 1-character tamper demonstration test.
