from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.models import (
    Review, Finding, SuggestedFix, Submission, SubmissionVersion, AuditLog
)
from backend.app.schemas.schemas import (
    ReviewRead, FindingRead, FixApplyRequest, SubmissionRead
)
from backend.app.services.crypto_service import compute_sha256
from backend.app.services.review_pipeline import ReviewPipeline

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.get("/{review_id}", response_model=ReviewRead)
def get_review(review_id: str, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.post("/{review_id}/fixes/{fix_id}/apply", response_model=SubmissionRead)
def apply_fix(
    review_id: str,
    fix_id: str,
    payload: FixApplyRequest,
    db: Session = Depends(get_db)
):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    fix = db.query(SuggestedFix).filter(SuggestedFix.id == fix_id).first()
    if not fix:
        raise HTTPException(status_code=404, detail="Suggested fix not found")

    sub_ver = review.submission_version
    submission = sub_ver.submission

    # Replace original sentence with suggested or custom replacement
    replacement_text = payload.custom_sentence or fix.suggested_sentence
    original_text = fix.original_sentence

    current_text = sub_ver.raw_text
    if original_text in current_text:
        updated_text = current_text.replace(original_text, replacement_text, 1)
    else:
        # Fallback: if case differs
        import re
        updated_text = re.sub(re.escape(original_text), replacement_text, current_text, count=1, flags=re.IGNORECASE)

    # Bump version number
    current_versions = sorted(submission.versions, key=lambda v: v.version_number)
    next_ver_num = current_versions[-1].version_number + 1

    new_ver = SubmissionVersion(
        submission_id=submission.id,
        version_number=next_ver_num,
        raw_text=updated_text,
        file_format=sub_ver.file_format,
        content_hash=compute_sha256(updated_text),
        created_by="Creator (Applied Fix)"
    )
    db.add(new_ver)
    db.flush()

    # Mark fix as ACCEPTED
    fix.status = "ACCEPTED"
    fix.applied_at = datetime.utcnow()
    fix.finding.is_resolved = True

    # Run review pipeline on the new version
    pipeline = ReviewPipeline(db)
    new_review = pipeline.run_review(new_ver)

    db.add(AuditLog(
        action="FIX_ACCEPTED_VERSION_BUMPED",
        actor_name="Krish Arora",
        actor_role="CREATOR",
        target_type="SUBMISSION_VERSION",
        target_id=new_ver.id,
        details=f"Applied fix for rule '{fix.finding.rule_code}'. Created version {next_ver_num}. New review findings count: {new_review.findings_count}."
    ))

    db.commit()
    db.refresh(submission)
    return submission

@router.post("/{review_id}/fixes/{fix_id}/reject")
def reject_fix(review_id: str, fix_id: str, db: Session = Depends(get_db)):
    fix = db.query(SuggestedFix).filter(SuggestedFix.id == fix_id).first()
    if not fix:
        raise HTTPException(status_code=404, detail="Suggested fix not found")

    fix.status = "REJECTED"
    db.commit()
    return {"status": "rejected", "message": "Fix suggestion rejected."}

@router.post("/rerun/{submission_id}", response_model=SubmissionRead)
def rerun_review_for_submission(submission_id: str, db: Session = Depends(get_db)):
    sub = db.query(Submission).filter(Submission.id == submission_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")

    latest_version = sorted(sub.versions, key=lambda v: v.version_number)[-1]
    pipeline = ReviewPipeline(db)
    new_review = pipeline.run_review(latest_version)

    db.add(AuditLog(
        action="REVIEW_RERUN",
        actor_name="Krish Arora",
        actor_role="CREATOR",
        target_type="REVIEW",
        target_id=new_review.id,
        details=f"Re-executed brand review pipeline on version {latest_version.version_number}. Findings count: {new_review.findings_count}."
    ))

    db.commit()
    db.refresh(sub)
    return sub
