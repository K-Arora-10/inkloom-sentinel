# AGENTS.md — INKLOOM SENTINEL

## Project Context
- **Product:** Inkloom Sentinel
- **Tagline:** Version. Test. Approve. Protect.
- **Competition:** CodeNexus India 2026 (Round 2 — The Build)
- **Team:** ShortKut (Krish Arora & Sanchita Sharma)
- **Organization Context:** Fictional synthetic digital payments enterprise **NexaPay**

## Architectural Guidelines
1. **Frontend:** Pure JavaScript with React, Vite, Tailwind CSS, Lucide React icons, and React Router. No TypeScript.
2. **Backend:** Python FastAPI, Pydantic, SQLAlchemy, PyMuPDF, python-docx, cryptography.
3. **Database:** PostgreSQL compatible schema with SQLite zero-config local development fallback. Auto-seeding on initial setup.
4. **Security & Cryptography:** SHA-256 canonical hashing + Ed25519 asymmetric signatures for approval sealing and publish tamper-detection. Server-side private key persistence.
5. **AI Integration:** Google Gemini API with provider abstraction and a complete deterministic review fallback engine when no API key is provided or when offline.
6. **Design System:** Editorial Minimalism (warm off-white `#F8F7F4`, white surfaces `#FFFFFF`, near-black `#242522`, forest green accent `#405746`, warm grey borders `#E8E6DF`).
7. **Quality:** Zero fake mockups, actual REST APIs, database persistence, working end-to-end review, fix application, human approval, cryptographic signing, and tamper detection.
