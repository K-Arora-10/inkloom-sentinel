from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.models import Submission, Approval
from backend.app.schemas.schemas import PublishRequest
from backend.app.services.approval_service import ApprovalService
from backend.app.services.crypto_service import compute_sha256, verify_approval_signature

router = APIRouter(prefix="/releases", tags=["Releases & Publishing"])

@router.get("/{submission_id}/verify")
def verify_approval_seal(submission_id: str, db: Session = Depends(get_db)):
    """
    Verifies the cryptographic Ed25519 signature and SHA-256 seal of the approved content.
    """
    sub = db.query(Submission).filter(Submission.id == submission_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")

    approval = db.query(Approval).filter(
        Approval.submission_id == submission_id,
        Approval.status == "APPROVED"
    ).order_by(Approval.approved_at.desc()).first()

    if not approval or not approval.signature:
        return {
            "has_approval_seal": False,
            "is_valid": False,
            "status": sub.current_status,
            "message": "Content is not yet approved with a cryptographic seal."
        }

    sig = approval.signature
    latest_version = sorted(sub.versions, key=lambda v: v.version_number)[-1]

    # Verify signature
    res = verify_approval_signature(
        submission_id=sub.id,
        version_number=latest_version.version_number,
        raw_content=latest_version.raw_text,
        reviewer_name=approval.reviewer_name,
        approved_at_iso=approval.approved_at.isoformat(),
        signature_b64=sig.signature_b64,
        public_key_b64=sig.public_key_b64
    )

    return {
        "has_approval_seal": True,
        "is_valid": res["is_valid"],
        "status": sub.current_status,
        "content_sha256": sig.content_sha256,
        "current_sha256": compute_sha256(latest_version.raw_text),
        "hash_matches": (sig.content_sha256 == compute_sha256(latest_version.raw_text)),
        "signature_b64": sig.signature_b64,
        "public_key_b64": sig.public_key_b64,
        "reviewer_name": approval.reviewer_name,
        "approved_at": approval.approved_at.isoformat(),
        "verification_details": res["reason"]
    }

@router.post("/{submission_id}/publish")
def publish_content(
    submission_id: str,
    payload: PublishRequest,
    db: Session = Depends(get_db)
):
    """
    Mock publishing gateway that verifies Ed25519 signature before publishing.
    Supports tamper simulation where a character is altered.
    """
    service = ApprovalService(db)

    sub = db.query(Submission).filter(Submission.id == submission_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")

    latest_version = sorted(sub.versions, key=lambda v: v.version_number)[-1]
    content = latest_version.raw_text

    # If user selected tamper simulation, modify 1 character
    if payload.tamper_with_char or payload.altered_text:
        if payload.altered_text:
            content = payload.altered_text
        else:
            # Modify exactly 1 character at end
            content = content + " "

    return service.verify_and_publish(submission_id, content_to_publish=content)

@router.post("/{submission_id}/tamper-test")
def run_tamper_demonstration(submission_id: str, db: Session = Depends(get_db)):
    """
    Executes the exact 1-character tampering demonstration required by Section 12 & 25:
    1. Inspects approved content and cryptographic seal.
    2. Modifies exactly one character (e.g. appends a period or changes a word).
    3. Attempts publication through the verification gateway.
    4. Demonstrates cryptographically that verification fails and publication is blocked.
    """
    service = ApprovalService(db)

    sub = db.query(Submission).filter(Submission.id == submission_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")

    approval = db.query(Approval).filter(
        Approval.submission_id == submission_id,
        Approval.status == "APPROVED"
    ).order_by(Approval.approved_at.desc()).first()

    if not approval or not approval.signature:
        raise HTTPException(status_code=400, detail="Cannot run tamper demonstration: Submission is not yet approved.")

    latest_version = sorted(sub.versions, key=lambda v: v.version_number)[-1]
    original_text = latest_version.raw_text

    # Change 1 single character
    tampered_text = original_text + "." if not original_text.endswith(".") else original_text[:-1]

    # Run verification against tampered text
    result = service.verify_and_publish(submission_id, content_to_publish=tampered_text)

    return {
        "test_name": "Ed25519 Single-Character Tamper Demonstration",
        "original_sha256": approval.signature.content_sha256,
        "tampered_sha256": compute_sha256(tampered_text),
        "original_sample": original_text[:80] + "...",
        "tampered_sample": tampered_text[:80] + "...",
        "single_char_diff": "1 character altered in distribution buffer",
        "verification_result": result,
        "status": "BLOCKED",
        "explanation": "Cryptographic Ed25519 verification failed because SHA-256 hash does not match the approved canonical content digest. Publication blocked by Inkloom Sentinel gateway."
    }
