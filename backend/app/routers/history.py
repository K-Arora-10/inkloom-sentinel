from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.models import Submission
from backend.app.schemas.schemas import SubmissionRead

router = APIRouter(prefix="/history", tags=["Review History"])

@router.get("", response_model=List[SubmissionRead])
def get_review_history(db: Session = Depends(get_db)):
    return db.query(Submission).order_by(Submission.updated_at.desc()).all()
