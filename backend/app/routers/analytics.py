from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.models import Submission, AuditLog, Finding
from backend.app.schemas.schemas import AnalyticsOverviewResponse, AuditLogRead

router = APIRouter(prefix="/analytics", tags=["Analytics & Overview"])

@router.get("", response_model=AnalyticsOverviewResponse)
def get_analytics_overview(db: Session = Depends(get_db)):
    total = db.query(Submission).count()
    pending = db.query(Submission).filter(Submission.current_status.in_(["DRAFT", "UNDER_REVIEW", "CHANGES_REQUESTED"])).count()
    approved = db.query(Submission).filter(Submission.current_status == "APPROVED").count()
    blocked = db.query(Submission).filter(Submission.current_status == "BLOCKED").count()
    resolved_findings = db.query(Finding).filter(Finding.is_resolved == True).count()

    recent_logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(15).all()

    return AnalyticsOverviewResponse(
        total_submissions=total,
        pending_reviews=pending,
        approved_content=approved,
        blocked_submissions=blocked,
        total_findings_resolved=resolved_findings,
        recent_activity=recent_logs
    )
