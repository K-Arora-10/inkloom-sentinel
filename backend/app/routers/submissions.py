import shutil
from pathlib import Path
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.models import (
    Submission, SubmissionVersion, AuditLog
)
from backend.app.schemas.schemas import (
    SubmissionRead, SubmissionCreate, SubmissionUpdate
)
from backend.app.services.crypto_service import compute_sha256
from backend.app.services.extraction_service import extract_content
from backend.app.services.review_pipeline import ReviewPipeline
from backend.app.config import settings

router = APIRouter(prefix="/submissions", tags=["Submissions"])

@router.get("", response_model=List[SubmissionRead])
def list_submissions(db: Session = Depends(get_db)):
    return db.query(Submission).order_by(Submission.created_at.desc()).all()

@router.post("", response_model=SubmissionRead)
def create_submission(sub_in: SubmissionCreate, db: Session = Depends(get_db)):
    if not sub_in.raw_text.strip():
        raise HTTPException(status_code=400, detail="Content body cannot be empty.")

    submission = Submission(
        title=sub_in.title,
        content_type=sub_in.content_type,
        target_audience=sub_in.target_audience,
        objective=sub_in.objective,
        campaign_name=sub_in.campaign_name,
        current_status="UNDER_REVIEW"
    )
    db.add(submission)
    db.flush()

    raw_text = sub_in.raw_text.strip()
    sub_ver = SubmissionVersion(
        submission_id=submission.id,
        version_number=1,
        raw_text=raw_text,
        file_format="PLAIN_TEXT",
        content_hash=compute_sha256(raw_text),
        created_by=sub_in.author_name or "Krish Arora (Creator)"
    )
    db.add(sub_ver)
    db.flush()

    # Automatically execute the review pipeline on creation
    pipeline = ReviewPipeline(db)
    review = pipeline.run_review(sub_ver)

    db.add(AuditLog(
        action="SUBMISSION_CREATED",
        actor_name=sub_in.author_name or "Creator",
        actor_role="CREATOR",
        target_type="SUBMISSION",
        target_id=submission.id,
        details=f"Created submission '{sub_in.title}'. Review generated {review.findings_count} findings."
    ))
    db.commit()
    db.refresh(submission)
    return submission

@router.get("/{submission_id}", response_model=SubmissionRead)
def get_submission(submission_id: str, db: Session = Depends(get_db)):
    sub = db.query(Submission).filter(Submission.id == submission_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    return sub

@router.post("/upload-extract")
def upload_and_extract_text(file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower()
    if ext not in [".pdf", ".docx", ".txt", ".md"]:
        raise HTTPException(status_code=400, detail="Unsupported file format. Please upload PDF, DOCX, TXT, or MD.")

    save_path = Path(settings.UPLOADS_DIR) / f"temp_{file.filename}"
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        extracted_text, detected_format = extract_content(str(save_path), file.filename)
        return {
            "filename": file.filename,
            "format": detected_format,
            "extracted_text": extracted_text,
            "character_count": len(extracted_text)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text extraction failed: {str(e)}")
    finally:
        if save_path.exists():
            try:
                save_path.unlink()
            except Exception:
                pass

@router.post("/{submission_id}/update-text", response_model=SubmissionRead)
def update_submission_text(submission_id: str, payload: SubmissionUpdate, db: Session = Depends(get_db)):
    sub = db.query(Submission).filter(Submission.id == submission_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")

    new_text = payload.raw_text.strip()
    if not new_text:
        raise HTTPException(status_code=400, detail="Content body cannot be empty.")

    # Determine next version number
    current_versions = sorted(sub.versions, key=lambda v: v.version_number)
    next_ver_num = (current_versions[-1].version_number + 1) if current_versions else 1

    new_ver = SubmissionVersion(
        submission_id=sub.id,
        version_number=next_ver_num,
        raw_text=new_text,
        file_format="PLAIN_TEXT",
        content_hash=compute_sha256(new_text),
        created_by="Creator (Manual Revision)"
    )
    db.add(new_ver)
    db.flush()

    # Re-run review on new version
    pipeline = ReviewPipeline(db)
    review = pipeline.run_review(new_ver)

    sub.current_status = "UNDER_REVIEW"

    db.add(AuditLog(
        action="VERSION_CREATED_MANUAL_EDIT",
        actor_name="Krish Arora",
        actor_role="CREATOR",
        target_type="SUBMISSION_VERSION",
        target_id=new_ver.id,
        details=f"Updated to version {next_ver_num}. New review findings: {review.findings_count}."
    ))

    db.commit()
    db.refresh(sub)
    return sub
