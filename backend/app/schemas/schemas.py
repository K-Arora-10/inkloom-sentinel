from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

# Organization & User
class OrganizationRead(BaseModel):
    id: str
    name: str
    code: str
    description: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True

class UserRead(BaseModel):
    id: str
    name: str
    email: str
    role: str
    created_at: datetime
    class Config:
        from_attributes = True

class RoleSwitchRequest(BaseModel):
    role: str  # CREATOR or REVIEWER

# Brand Vault
class DocumentVersionRead(BaseModel):
    id: str
    version_number: str
    content: str
    file_format: str
    created_by: str
    created_at: datetime
    class Config:
        from_attributes = True

class DocumentRead(BaseModel):
    id: str
    title: str
    doc_type: str
    category: Optional[str] = None
    current_version: str
    status: str
    summary: Optional[str] = None
    versions: List[DocumentVersionRead] = []
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class BrandRuleRead(BaseModel):
    id: str
    rule_code: str
    category: str
    name: str
    description: str
    severity: str
    rule_type: str
    pattern: str
    replacement: Optional[str] = None
    is_active: bool
    version: str
    class Config:
        from_attributes = True

class GlossaryTermRead(BaseModel):
    id: str
    term: str
    status: str
    preferred_alternative: Optional[str] = None
    context_note: Optional[str] = None
    is_active: bool
    class Config:
        from_attributes = True

class ApprovedFactRead(BaseModel):
    id: str
    fact_code: str
    fact_name: str
    approved_value: str
    supporting_source: str
    owner: str
    effective_date: str
    expiry_date: Optional[str] = None
    version: str
    status: str
    is_historical: bool
    class Config:
        from_attributes = True

class ClaimPassportRead(BaseModel):
    id: str
    claim_code: str
    claim_text: str
    evidence: str
    source_document: str
    owner: str
    expiry_date: Optional[str] = None
    approval_status: str
    linked_fact_codes: Optional[str] = None
    class Config:
        from_attributes = True

# Findings & Fixes
class EvidenceRefRead(BaseModel):
    id: str
    source_type: str
    source_id: Optional[str] = None
    title: str
    snippet: str
    class Config:
        from_attributes = True

class SuggestedFixRead(BaseModel):
    id: str
    original_sentence: str
    suggested_sentence: str
    explanation: str
    status: str
    applied_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class FindingRead(BaseModel):
    id: str
    rule_code: Optional[str] = None
    original_text: str
    start_char: int
    end_char: int
    category: str
    severity: str
    classification: str
    what_went_wrong: str
    why_it_matters: str
    supporting_evidence: str
    source_document: str
    suggested_correction: Optional[str] = None
    confidence_signal: str
    needs_human_judgment: bool
    is_resolved: bool
    evidence_refs: List[EvidenceRefRead] = []
    fixes: List[SuggestedFixRead] = []
    class Config:
        from_attributes = True

class ReviewRead(BaseModel):
    id: str
    submission_version_id: str
    status: str
    findings_count: int
    critical_count: int
    warning_count: int
    info_count: int
    summary: Optional[str] = None
    review_duration_ms: int
    created_at: datetime
    findings: List[FindingRead] = []
    class Config:
        from_attributes = True

# Submissions
class SubmissionVersionRead(BaseModel):
    id: str
    submission_id: str
    version_number: int
    raw_text: str
    file_format: str
    content_hash: str
    created_by: str
    created_at: datetime
    reviews: List[ReviewRead] = []
    class Config:
        from_attributes = True

class CommentRead(BaseModel):
    id: str
    author_name: str
    author_role: str
    comment_text: str
    created_at: datetime
    class Config:
        from_attributes = True

class ApprovalSignatureRead(BaseModel):
    id: str
    canonical_content: str
    content_sha256: str
    signature_b64: str
    public_key_b64: str
    signed_at: datetime
    is_valid: bool
    class Config:
        from_attributes = True

class ApprovalRead(BaseModel):
    id: str
    submission_id: str
    submission_version_id: str
    reviewer_name: str
    status: str
    decision_notes: Optional[str] = None
    approved_at: datetime
    signature: Optional[ApprovalSignatureRead] = None
    class Config:
        from_attributes = True

class SubmissionRead(BaseModel):
    id: str
    title: str
    content_type: str
    target_audience: Optional[str] = None
    objective: Optional[str] = None
    campaign_name: Optional[str] = None
    current_status: str
    created_at: datetime
    updated_at: datetime
    versions: List[SubmissionVersionRead] = []
    comments: List[CommentRead] = []
    approvals: List[ApprovalRead] = []
    class Config:
        from_attributes = True

class SubmissionCreate(BaseModel):
    title: str
    content_type: str = "SOCIAL_MEDIA"
    target_audience: Optional[str] = "General Audience"
    objective: Optional[str] = "Brand Communication"
    campaign_name: Optional[str] = None
    raw_text: str
    author_name: Optional[str] = "Krish Arora (Creator)"

class SubmissionUpdate(BaseModel):
    raw_text: str

class FixApplyRequest(BaseModel):
    fix_id: str
    custom_sentence: Optional[str] = None

class ApprovalActionRequest(BaseModel):
    notes: Optional[str] = "Approved in accordance with NexaPay brand integrity standards."
    reviewer_name: Optional[str] = "Sanchita Sharma (Reviewer)"

class ChangesActionRequest(BaseModel):
    notes: str
    reviewer_name: Optional[str] = "Sanchita Sharma (Reviewer)"

class CommentCreate(BaseModel):
    comment_text: str
    author_name: Optional[str] = "Krish Arora"
    author_role: Optional[str] = "CREATOR"

class PublishRequest(BaseModel):
    tamper_with_char: Optional[bool] = False
    altered_text: Optional[str] = None

class AuditLogRead(BaseModel):
    id: str
    action: str
    actor_name: str
    actor_role: str
    target_type: str
    target_id: str
    details: Optional[str] = None
    timestamp: datetime
    class Config:
        from_attributes = True

class AnalyticsOverviewResponse(BaseModel):
    total_submissions: int
    pending_reviews: int
    approved_content: int
    blocked_submissions: int
    total_findings_resolved: int
    recent_activity: List[AuditLogRead]
