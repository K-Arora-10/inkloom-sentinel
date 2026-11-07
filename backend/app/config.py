import os
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv

# Load .env if present
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
KEY_FILE_PATH = DATA_DIR / "ed25519_key.pem"
UPLOADS_DIR = DATA_DIR / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

def get_database_url() -> str:
    raw_url = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR / 'inkloom.db'}")
    if raw_url.startswith("postgres://"):
        return raw_url.replace("postgres://", "postgresql://", 1)
    return raw_url

class Settings(BaseModel):
    PROJECT_NAME: str = "Inkloom Sentinel"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    # Database
    DATABASE_URL: str = get_database_url()
    
    # Gemini AI
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    
    # Cryptographic keys
    ED25519_PRIVATE_KEY_HEX: str = os.getenv("ED25519_PRIVATE_KEY", "")
    KEY_PATH: str = str(KEY_FILE_PATH)
    
    # CORS
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")

settings = Settings()
