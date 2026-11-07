from contextlib import asynccontextmanager
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import settings
from backend.app.database import engine, Base, SessionLocal
from backend.app.seed.seed_data import seed_database
from backend.app.routers import (
    health, brand_vault, submissions, reviews, approvals, releases, history, analytics, demo
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables
    Base.metadata.create_all(bind=engine)
    # Seed database with NexaPay resources
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    yield

app = FastAPI(
    title="Inkloom Sentinel API",
    description="Enterprise brand integrity and governance platform for NexaPay",
    version=settings.VERSION,
    lifespan=lifespan
)

# CORS configuration
origins = [
    settings.FRONTEND_URL,
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:4173",
    "http://127.0.0.1:4173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(health.router, prefix=settings.API_PREFIX)
app.include_router(brand_vault.router, prefix=settings.API_PREFIX)
app.include_router(submissions.router, prefix=settings.API_PREFIX)
app.include_router(reviews.router, prefix=settings.API_PREFIX)
app.include_router(approvals.router, prefix=settings.API_PREFIX)
app.include_router(releases.router, prefix=settings.API_PREFIX)
app.include_router(history.router, prefix=settings.API_PREFIX)
app.include_router(analytics.router, prefix=settings.API_PREFIX)
app.include_router(demo.router, prefix=settings.API_PREFIX)

@app.head("/api/health", include_in_schema=False)
@app.head("/health", include_in_schema=False)
async def health_check_head():
    return Response(status_code=200)

@app.get("/")
def root():
    return {
        "product": "Inkloom Sentinel",
        "tagline": "Version. Test. Approve. Protect.",
        "team": "ShortKut (Krish Arora & Sanchita Sharma)",
        "docs_url": "/docs",
        "health_check": "/api/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
