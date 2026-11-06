# INKLOOM SENTINEL
> **Version. Test. Approve. Protect.**
> An AI-assisted brand-governance and cryptographic release platform for enterprise communications.
> Production-ready implementation by **Team ShortKut** (Krish Arora & Sanchita Sharma).

---

## 1. Problem Statement
Organizations publish content across dozens of distributed employees, external creative agencies, and generative AI tools. This creates brand erosion, inconsistent terminology, misleading promotional claims, factual contradictions, and regulatory non-compliance.

Inkloom Sentinel solves this not by generating more content or acting as a simple grammar checker, but by serving as an **explainable brand-integrity gatekeeper**. It audits submitted content against approved brand guidelines, facts, and claim passports, suggests minimal corrections preserving creator intent, requires authorized human sign-off, and cryptographically seals releases with Ed25519 digital signatures to prevent silent tampering.

---

## 2. Team Contributions (Team ShortKut)
- **Krish Arora**:
  - Backend architecture, FastAPI REST design, and database schema.
  - Multi-stage review engine (deterministic rules, fact comparisons, and Claim Passport lookups).
  - Retrieval engine, Gemini API integration, and zero-downtime local fallback contextual engine.
  - Fix Assistant backend logic, version bumping, and re-verification pipeline.
  - Cryptographic approval authority (SHA-256 canonical hashing + Ed25519 digital signing) and publishing gateway.
- **Sanchita Sharma**:
  - Frontend architecture (React, Vite, pure JavaScript, Tailwind CSS).
  - Editorial Minimalist design system implementation (#F8F7F4, #405746, #242522, #E8E6DF).
  - Content Studio with plain text and PDF/DOCX file intake with live text extraction preview.
  - Document-centric split Review Workspace with interactive sentence highlight overlays and finding navigation.
  - Human Approval Hub with role-based sign-off and threaded governance comments.
  - Interactive Cryptographic Tamper-Resistance verification interface and Review History archive.
- **Shared**:
  - Architecture decisions, API contracts, NexaPay brand documentation, end-to-end integration testing, deployment configuration, and documentation.

---

## 3. Technology Stack
- **Frontend**: React 19, Vite, JavaScript (pure JS, no TypeScript), Tailwind CSS, React Router, Lucide React icons.
- **Backend**: Python 3.13, FastAPI, Pydantic v2, SQLAlchemy 2.0, Uvicorn, PyMuPDF (fitz), python-docx, cryptography, psycopg2-binary.
- **Database**: PostgreSQL compatible (Neon / Render / Supabase / AWS target) with SQLite local development default.
- **AI & Retrieval**: Google Gemini API (configurable model) with structured JSON output and a robust local deterministic contextual fallback engine.
- **Security**: SHA-256 canonical content hashing + Ed25519 digital signatures for release integrity and tamper detection.

---

## 4. NexaPay Enterprise Brand Vault
The application comes pre-configured with the complete enterprise brand repository for **NexaPay Technologies India** across 7 primary documentation resources:
1. `Brand Guidelines v1.0` (Identity, personality, tone of voice, acceptable/prohibited content)
2. `Brand Glossary` (Controlled vocabulary: Guaranteed returns [Prohibited], 100% secure [Prohibited], Amazing deal [Discouraged])
3. `Approved Facts Register` (Approved transaction fee: ₹399, historical fee: ₹499 superseded, delivery threshold: ₹499)
4. `Claim Passports Register` (CLAIM-001 delivery [Approved], CLAIM-002 "safest platform" [Unsupported], CLAIM-003 transaction fee [Approved])
5. `Visual Identity Guide` (Original SVG brand mark, clear space, brand color palette)
6. `Content and Advertising Policy` (Superlative restrictions, financial disclosures, escalation rules)
7. `Historical Brand Updates` (Audit log of superseded parameters and fee changes)

---

## 5. Quick Start Instructions (Local Development)

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### Backend Setup
```bash
# 1. Navigate to project root
cd inkloom-sentinel

# 2. Install backend dependencies
pip install -r backend/requirements.txt

# 3. Run automated tests (15 test suites)
python -m pytest backend/tests/test_backend.py -v

# 4. Start FastAPI server
uvicorn backend.app.main:app --reload --port 8000
```
Backend starts on `http://localhost:8000`. Database auto-initializes on startup!
Interactive API documentation: `http://localhost:8000/docs`.

### Frontend Setup
```bash
# 1. In a separate terminal, navigate to frontend
cd frontend

# 2. Install dependencies (if not already installed)
npm install

# 3. Start Vite dev server
npm run dev
```
Frontend starts on `http://localhost:5173`.

---

## 6. Environment Variables

### Backend (`backend/.env`)
```ini
DATABASE_URL=sqlite:///data/inkloom.db
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash
ED25519_PRIVATE_KEY=
FRONTEND_URL=http://localhost:5173
ENVIRONMENT=production
```
*(Note: If `GEMINI_API_KEY` is omitted, the application runs its guaranteed local deterministic contextual engine with zero downtime).*

### Frontend (`frontend/.env`)
```ini
VITE_API_BASE_URL=http://localhost:8000
```

---

## 7. Recommended End-to-End Verification Sequence
Follow this standard enterprise governance workflow:
1. Open the application at `http://localhost:5173`.
2. Land on the **Overview** dashboard displaying verified database metrics and the system audit trail.
3. Open **Brand Vault** in the left sidebar; inspect the 7 NexaPay brand documents, glossary table, and facts register.
4. Note that the active transaction fee is **₹399**, while the historical fee was **₹499**.
5. Navigate to **Content Studio** (New Review) and click **Template 1: Promotional Ad**.
6. Inspect the input containing the unsupported superlative "safest", unapproved fee "₹299", and prohibited guarantee.
7. Click **Initiate Sentinel Review**.
8. In the **Review Workspace**: Left panel shows highlighted problematic sentences; Right panel details explainable findings citing Brand Vault sources.
9. Click **Accept Fix** on the pricing violation; watch the content update, version bump to `v2`, and the review engine automatically re-verify the text.
10. Click **Submit for Human Approval**.
11. Navigate to **Approval Hub**; use the role switcher to activate **Sanchita Sharma (Reviewer)**.
12. Inspect the submission in the queue, add decision notes, and click **Approve & Sign Release**.
13. Observe the server generate a cryptographic **Ed25519 digital signature** and **SHA-256 seal**.
14. Navigate to the **Release Gateway** (or click "Verify Seal & Publish").
15. Click **Verify & Publish to Distribution** to confirm the digital certificate passes verification.
16. Click **Execute Tamper-Resistance Verification**.
17. Watch the publishing gateway immediately **BLOCK** publication, showing the exact SHA-256 hash mismatch.
18. Open **Review History** to inspect the chronological version archive and seal records.
19. Open **Product Roadmap** to review scheduled enterprise capabilities.
20. Check `/api/health` and `/docs` for API transparency.

---

## 8. Production Cloud Deployment
See [docs/DEPLOYMENT_GUIDE.md](file:///docs/DEPLOYMENT_GUIDE.md) for 1-click Render blueprint, Vercel frontend, Neon PostgreSQL, and Docker container instructions.

---

## 9. AI Assistance Disclosure
- Google Gemini API is utilized for contextual brand tone analysis when an API key is provided.
- An autonomous coding assistant was utilized for pair-programming and scaffolding.
- All business logic, deterministic rule evaluation, database schemas, cryptographic sealing, and test suites are genuine, functional software.
