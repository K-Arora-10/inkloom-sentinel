from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.app.models.models import (
    Submission, SubmissionVersion, Approval, ApprovalSignature, AuditLog, Comment, SuggestedFix, Finding
)
from backend.app.services.crypto_service import (
    compute_sha256, sign_approval_payload, verify_approval_signature, canonicalize_content
)

class ApprovalService:
    def __init__(self, db: Session):
        self.db = db

    def submit_for_review(self, submission_id: str, user_name: str, user_role: str) -> Submission:
        submission = self.db.query(Submission).filter(Submission.id == submission_id).first()
        if not submission:
            raise HTTPException(status_code=404, detail="Submission not found")
        
        submission.current_status = "UNDER_REVIEW"
        self.db.add(AuditLog(
            action="SUBMITTED_FOR_REVIEW",
            actor_name=user_name,
            actor_role=user_role,
            target_type="SUBMISSION",
            target_id=submission_id,
            details="Creator submitted content version for formal brand approval."
        ))
        self.db.commit()
        self.db.refresh(submission)
        return submission

    def request_changes(self, submission_id: str, notes: str, reviewer_name: str, reviewer_role: str) -> Submission:
        if reviewer_role not in ["REVIEWER", "ADMIN"]:
            raise HTTPException(status_code=403, detail="Only authorized Reviewers can request changes.")

        submission = self.db.query(Submission).filter(Submission.id == submission_id).first()
        if not submission:
            raise HTTPException(status_code=404, detail="Submission not found")

        latest_version = sorted(submission.versions, key=lambda v: v.version_number)[-1]

        approval = Approval(
            submission_id=submission.id,
            submission_version_id=latest_version.id,
            reviewer_name=reviewer_name,
            status="CHANGES_REQUESTED",
            decision_notes=notes,
            approved_at=datetime.utcnow()
        )
        self.db.add(approval)
        submission.current_status = "CHANGES_REQUESTED"

        # Also add comment
        self.db.add(Comment(
            submission_id=submission.id,
            author_name=reviewer_name,
            author_role=reviewer_role,
            comment_text=f"Changes requested: {notes}"
        ))

        self.db.add(AuditLog(
            action="CHANGES_REQUESTED",
            actor_name=reviewer_name,
            actor_role=reviewer_role,
            target_type="SUBMISSION",
            target_id=submission_id,
            details=f"Reviewer requested modifications: {notes}"
        ))

        self.db.commit()
        self.db.refresh(submission)
        return submission

    def approve_submission(self, submission_id: str, notes: str, reviewer_name: str, reviewer_role: str) -> Approval:
        if reviewer_role not in ["REVIEWER", "ADMIN"]:
            raise HTTPException(status_code=403, detail="Only authorized Reviewers can approve content.")

        submission = self.db.query(Submission).filter(Submission.id == submission_id).first()
        if not submission:
            raise HTTPException(status_code=404, detail="Submission not found")

        latest_version = sorted(submission.versions, key=lambda v: v.version_number)[-1]

        now_iso = datetime.utcnow().isoformat()

        # Generate Ed25519 digital signature and SHA-256 seal
        crypto_payload = sign_approval_payload(
            submission_id=submission.id,
            version_number=latest_version.version_number,
            raw_content=latest_version.raw_text,
            reviewer_name=reviewer_name,
            approved_at_iso=now_iso
        )

        approval = Approval(
            submission_id=submission.id,
            submission_version_id=latest_version.id,
            reviewer_name=reviewer_name,
            status="APPROVED",
            decision_notes=notes or "Approved for publication in accordance with NexaPay brand integrity standards.",
            approved_at=datetime.utcnow()
        )
        self.db.add(approval)
        self.db.flush()

        signature_record = ApprovalSignature(
            approval_id=approval.id,
            submission_version_id=latest_version.id,
            canonical_content=crypto_payload["canonical_content"],
            content_sha256=crypto_payload["content_sha256"],
            signature_b64=crypto_payload["signature_b64"],
            public_key_b64=crypto_payload["public_key_b64"],
            signed_at=datetime.utcnow(),
            is_valid=True
        )
        self.db.add(signature_record)

        submission.current_status = "APPROVED"

        self.db.add(AuditLog(
            action="CONTENT_APPROVED_AND_SEALED",
            actor_name=reviewer_name,
            actor_role=reviewer_role,
            target_type="APPROVAL",
            target_id=approval.id,
            details=f"Content cryptographically signed with Ed25519 (SHA-256: {crypto_payload['content_sha256'][:16]}...)"
        ))

        self.db.commit()
        self.db.refresh(approval)
        return approval

    def verify_and_publish(self, submission_id: str, content_to_publish: Optional[str] = None) -> Dict[str, Any]:
        submission = self.db.query(Submission).filter(Submission.id == submission_id).first()
        if not submission:
            raise HTTPException(status_code=404, detail="Submission not found")

        # Find approval record
        approval = self.db.query(Approval).filter(
            Approval.submission_id == submission_id,
            Approval.status == "APPROVED"
        ).order_by(Approval.approved_at.desc()).first()

        if not approval or not approval.signature:
            raise HTTPException(
                status_code=400,
                detail="Submission cannot be published: No valid cryptographic approval seal found."
            )

        sig = approval.signature
        latest_version = sorted(submission.versions, key=lambda v: v.version_number)[-1]

        # Content to verify is either submitted payload or current version raw text
        test_content = content_to_publish if content_to_publish is not None else latest_version.raw_text

        # Verify signature and SHA-256 hash
        verification_result = verify_approval_signature(
            submission_id=submission.id,
            version_number=latest_version.version_number,
            raw_content=test_content,
            reviewer_name=approval.reviewer_name,
            approved_at_iso=approval.approved_at.isoformat(),
            signature_b64=sig.signature_b64,
            public_key_b64=sig.public_key_b64
        )

        expected_hash = sig.content_sha256
        actual_hash = compute_sha256(test_content)
        hash_matches = (expected_hash == actual_hash)

        if verification_result["is_valid"] and hash_matches:
            submission.current_status = "PUBLISHED"
            self.db.add(AuditLog(
                action="CONTENT_PUBLISHED",
                actor_name="Mock Publishing Gateway",
                actor_role="SYSTEM",
                target_type="SUBMISSION",
                target_id=submission_id,
                details=f"Publish verification successful. SHA-256: {actual_hash[:16]}..."
            ))
            self.db.commit()
            return {
                "status": "APPROVED",
                "message": "Cryptographic approval seal verified. Content published successfully to NexaPay distribution channels.",
                "hash_matches": True,
                "signature_valid": True,
                "expected_hash": expected_hash,
                "verified_hash": actual_hash,
                "reviewer": approval.reviewer_name,
                "approved_at": approval.approved_at.isoformat(),
                "published_at": datetime.utcnow().isoformat(),
                "public_key": sig.public_key_b64[:32] + "..."
            }
        else:
            submission.current_status = "BLOCKED"
            self.db.add(AuditLog(
                action="PUBLISH_BLOCKED_TAMPER_DETECTED",
                actor_name="Mock Publishing Gateway",
                actor_role="SYSTEM",
                target_type="SUBMISSION",
                target_id=submission_id,
                details=f"Publish blocked: Hash mismatch! Expected {expected_hash[:12]}, got {actual_hash[:12]}"
            ))
            self.db.commit()
            return {
                "status": "BLOCKED",
                "message": "Tampering detected: The content submitted for publication does NOT match the cryptographically signed approved version.",
                "hash_matches": False,
                "signature_valid": False,
                "expected_hash": expected_hash,
                "verified_hash": actual_hash,
                "reason": "Hash mismatch detected. Even a 1-character modification invalidates the Ed25519 approval signature."
            }
