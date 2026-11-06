# INKLOOM SENTINEL — PRODUCTION DEPLOYMENT GUIDE

This document provides complete, step-by-step instructions to deploy Inkloom Sentinel (Frontend, Backend, and PostgreSQL Database) to production on free-tier, enterprise-grade cloud platforms without requiring credit cards or temporary mockups.

---

## Architecture in Production

```
[ User Browser ]
       |
       v
[ Frontend (Vite / React) ]  -->  Hosted on Render Static Site or Vercel
       |
       | HTTPS API Calls (VITE_API_BASE_URL)
       v
[ Backend (FastAPI / Python) ]  -->  Hosted on Render Web Service
       |
       | Encrypted SSL Connection (DATABASE_URL)
       v
[ Database (PostgreSQL) ]  -->  Hosted on Neon Free PostgreSQL / Render PostgreSQL
```

---

## OPTION 1: 1-Click Blueprint on Render (Recommended — Simplest)

Render can build and host the **Frontend Static Site**, **FastAPI Backend**, and **PostgreSQL Database** in a single automated blueprint using the included `render.yaml`.

### Step 1: Push your Code to GitHub
Ensure all code in your local folder is pushed to your GitHub repository:
```bash
git add .
git commit -m "feat: production deployment configuration"
git push origin master
```

### Step 2: Deploy on Render
1. Go to [https://dashboard.render.com](https://dashboard.render.com).
2. Click **New +** and select **Blueprint**.
3. Connect your GitHub account and choose your `inkloom-sentinel` repository.
4. Render will detect `render.yaml` and configure three managed services:
   - `inkloom-postgres` (Managed PostgreSQL Database)
   - `inkloom-sentinel-api` (FastAPI Python Service with auto-migrated DB)
   - `inkloom-sentinel-ui` (React Vite Static Site)
5. Click **Apply**.
6. Render will automatically build the backend, provision the database, seed the initial brand documentation, build the frontend bundle, and link them together!

---

## OPTION 2: Individual Deployment (Render Backend + Vercel / Netlify Frontend + Neon DB)

If you prefer using **Neon** for PostgreSQL and **Vercel** for the frontend:

### 1. Database (Neon PostgreSQL)
1. Go to [https://neon.tech](https://neon.tech) and create a free project.
2. Copy the connection string. It will look like:
   `postgresql://username:password@ep-xyz.region.neon.tech/neondb?sslmode=require`

### 2. Backend (Render Web Service)
1. In Render, click **New +** $\rightarrow$ **Web Service**.
2. Connect your GitHub repository.
3. Configure settings:
   - **Environment:** Python
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
   - **Health Check Path:** `/api/health`
4. Add Environment Variables:
   - `DATABASE_URL`: *(Paste your Neon PostgreSQL connection string)*
   - `GEMINI_API_KEY`: *(Optional: paste your Google AI Studio API key for cloud LLM tone review)*
   - `ENVIRONMENT`: `production`
5. Click **Create Web Service**.
6. Once deployed, copy your backend URL (e.g. `https://inkloom-sentinel-api.onrender.com`).

### 3. Frontend (Vercel or Render Static Site)
1. In Vercel or Render, create a new Static Site from the same repository.
2. Configure settings:
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
3. Add Environment Variable:
   - `VITE_API_BASE_URL`: `https://inkloom-sentinel-api.onrender.com` *(your deployed backend URL)*
4. Click **Deploy**.
5. Your frontend is live with production backend connectivity!

---

## OPTION 3: Docker Deployment (Railway, Fly.io, or VPS)

A complete production `Dockerfile` and `docker-compose.yml` are provided in the repository:
```bash
# Build and run backend + PostgreSQL with 1 command:
docker compose up -d --build
```
- The backend will start on `http://localhost:8000` with persistent PostgreSQL on port `5432`.

---

## What the System Does Automatically on First Boot
- **Database Tables:** SQLAlchemy automatically creates all 19 relational tables on startup (`Base.metadata.create_all`).
- **Seed Data:** Initializes the NexaPay Brand Vault, Guidelines, Glossary, Facts Register, Claim Passports, and baseline compliance cases.
- **Persistent Cryptographic Key:** If an Ed25519 key does not exist on disk, a persistent server-side keypair is generated and stored in `data/ed25519_key.pem`.
- **Zero-Downtime Fallback:** If `GEMINI_API_KEY` is not provided, the local deterministic contextual engine handles tone and hyperbole detection with 100% uptime.

---

## What You Need to Do Manually
1. **GitHub Repository:** Push this codebase to your own GitHub account.
2. **Cloud Account:** Sign in to Render, Vercel, or Neon (all offer 100% free accounts with no credit card required).
3. **Trigger Deployment:** Connect the GitHub repository in Render/Vercel and click Deploy.
4. If you have an external PostgreSQL database or Gemini API key you would like to test locally right now, you can paste the connection string into `backend/.env`!
