from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.app.database import get_db
from backend.app.config import settings
from backend.app.services.crypto_service import get_or_create_ed25519_keypair

router = APIRouter(prefix="/health", tags=["Health"])

@router.head("", include_in_schema=False)
async def health_check_head():
    return Response(status_code=200)

@router.get("")
def health_check(db: Session = Depends(get_db)):
    # Test DB
    db_ok = False
    try:
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception as e:
        db_error = str(e)

    # Test Ed25519 keypair
    crypto_ok = False
    try:
        priv, pub = get_or_create_ed25519_keypair()
        crypto_ok = True
    except Exception:
        pass

    return {
        "status": "healthy" if db_ok and crypto_ok else "degraded",
        "product": "Inkloom Sentinel",
        "tagline": "Version. Test. Approve. Protect.",
        "team": "ShortKut (Krish Arora & Sanchita Sharma)",
        "organization": "NexaPay Technologies India",
        "database_connected": db_ok,
        "crypto_engine_ready": crypto_ok,
        "ai_provider": f"Gemini 3.8 Flash (Cloud - {settings.GEMINI_MODEL})" if settings.GEMINI_API_KEY else "Local Deterministic & Contextual Engine (Active)",
        "environment": "Production Ready"
    }
