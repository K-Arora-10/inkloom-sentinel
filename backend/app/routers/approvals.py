from typing import List
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.models import (
    Submission, Approval, Comment, AuditLog
)
from backend.app.schemas.schemas import (
    SubmissionRead, ApprovalRead, ApprovalActionRequest, ChangesActionRequest, CommentCreate, CommentRead
)
from backend.app.services.approval_service import ApprovalService

router = APIRouter(prefix="/approvals", tags=["Approvals"])

@router.post("/{submission_id}/submit", response_model=SubmissionRead)
def submit_for_review(
    submission_id: str,
    x_user_name: str = Header(default="Krish Arora (Creator)"),
    x_user_role: str = Header(default="CREATOR"),
    db: Session = Depends(get_db)
):
    service = ApprovalService(db)
    return service.submit_for_review(submission_id, x_user_name, x_user_role)

@router.post("/{submission_id}/approve", response_model=ApprovalRead)
def approve_submission(
    submission_id: str,
    payload: ApprovalActionRequest,
    x_user_name: str = Header(default="Sanchita Sharma (Reviewer)"),
    x_user_role: str = Header(default="REVIEWER"),
    db: Session = Depends(get_db)
):
    service = ApprovalService(db)
    return service.approve_submission(
        submission_id=submission_id,
        notes=payload.notes or "Approved for release.",
        reviewer_name=x_user_name,
        reviewer_role=x_user_role
    )

@router.post("/{submission_id}/request-changes", response_model=SubmissionRead)
def request_changes(
    submission_id: str,
    payload: ChangesActionRequest,
    x_user_name: str = Header(default="Sanchita Sharma (Reviewer)"),
    x_user_role: str = Header(default="REVIEWER"),
    db: Session = Depends(get_db)
):
    service = ApprovalService(db)
    return service.request_changes(
        submission_id=submission_id,
        notes=payload.notes,
        reviewer_name=x_user_name,
        reviewer_role=x_user_role
    )

@router.post("/{submission_id}/comments", response_model=CommentRead)
def add_comment(
    submission_id: str,
    payload: CommentCreate,
    x_user_name: str = Header(default="Krish Arora"),
    x_user_role: str = Header(default="CREATOR"),
    db: Session = Depends(get_db)
):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    comment = Comment(
        submission_id=submission.id,
        author_name=x_user_name,
        author_role=x_user_role,
        comment_text=payload.comment_text
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment
