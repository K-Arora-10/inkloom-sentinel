# SYSTEM ARCHITECTURE — INKLOOM SENTINEL

## 1. High-Level Architecture
Inkloom Sentinel is built with a decoupled client-server architecture:
- **Frontend Layer:** React (JavaScript, Vite, Tailwind CSS, Lucide React). Strict Editorial Minimalist aesthetic without flashy dark-navy AI SaaS tropes.
- **API & Governance Layer:** Python FastAPI with Pydantic request validation and typed domain schemas.
- **Review Pipeline:** Multi-stage audit engine coordinating text boundary parsing, deterministic rule matching, fact comparison, and AI contextual analysis.
- **Cryptographic Security Authority:** SHA-256 canonical digest computation and asymmetric Ed25519 digital signature sealing.
- **Data Persistence:** SQLAlchemy ORM with dual-engine support (PostgreSQL Neon in production, SQLite zero-config local development default).

## 2. Component Diagram
```
+-----------------------------------------------------------+
|               Inkloom Sentinel Frontend (React)           |
|  - Overview  - Brand Vault  - Content Studio              |
|  - Review Workspace  - Approval Hub  - Release Gateway    |
+-----------------------------+-----------------------------+
                              | REST JSON / Multipart
                              v
+-----------------------------------------------------------+
|                 FastAPI Application Server                |
|  +---------------------+   +---------------------------+  |
|  |  Extraction Service |   |  Review Pipeline Engine   |  |
|  |  (PyMuPDF / docx)   |   |  - Deterministic Rules    |  |
|  +---------------------+   |  - Fact Verification      |  |
|  +---------------------+   |  - Claim Passports        |  |
|  | Cryptographic Engine|   |  - AI Contextual Engine   |  |
|  | (SHA-256 / Ed25519) |   +---------------------------+  |
|  +---------------------+                                  |
+-----------------------------+-----------------------------+
                              | SQLAlchemy
                              v
+-----------------------------------------------------------+
|              Database (PostgreSQL / SQLite)               |
|  - Documents  - Rules  - Facts  - Claims  - Signatures    |
+-----------------------------------------------------------+
```
