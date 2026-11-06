import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, Integer, Boolean, DateTime, ForeignKey, Index
)
from sqlalchemy.orm import relationship
from backend.app.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Organization(Base):
    __tablename__ = "organisations"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(200), nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    users = relationship("User", back_populates="organization")
    documents = relationship("Document", back_populates="organization")
    submissions = relationship("Submission", back_populates="organization")


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    role = Column(String(50), nullable=False, default="CREATOR")  # CREATOR, REVIEWER, ADMIN
    org_id = Column(String, ForeignKey("organisations.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    organization = relationship("Organization", back_populates="users")
    comments = relationship("Comment", back_populates="user")


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=generate_uuid)
    org_id = Column(String, ForeignKey("organisations.id"), nullable=True)
    title = Column(String(255), nullable=False)
    doc_type = Column(String(50), nullable=False)  # GUIDELINE, GLOSSARY, POLICY, VISUAL, FACT_SHEET
    category = Column(String(100), nullable=True)
    current_version = Column(String(50), default="1.0")
    status = Column(String(50), default="ACTIVE")  # ACTIVE, ARCHIVED, DRAFT
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    organization = relationship("Organization", back_populates="documents")
    versions = relationship("DocumentVersion", back_populates="document", cascade="all, delete-orphan")


class DocumentVersion(Base):
    __tablename__ = "document_versions"

    id = Column(String, primary_key=True, default=generate_uuid)
    document_id = Column(String, ForeignKey("documents.id"), nullable=False)
    version_number = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    extracted_text = Column(Text, nullable=True)
    file_path = Column(String(500), nullable=True)
    file_format = Column(String(20), default="MARKDOWN")  # MARKDOWN, PDF, DOCX, TXT
    created_by = Column(String(100), default="SYSTEM")
    created_at = Column(DateTime, default=datetime.utcnow)

    document = relationship("Document", back_populates="versions")


class BrandRule(Base):
    __tablename__ = "brand_rules"

    id = Column(String, primary_key=True, default=generate_uuid)
    rule_code = Column(String(50), unique=True, nullable=False)
    category = Column(String(100), nullable=False)  # TERMINOLOGY, CLAIMS, TONE, FACT_ACCURACY, REGULATORY
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String(20), nullable=False, default="WARNING")  # CRITICAL, WARNING, INFO
    rule_type = Column(String(50), nullable=False)  # PROHIBITED_TERM, DISCOURAGED_TERM, EXACT_MISMATCH, SUPERLATIVE, GUARANTEE, REQUIRED_DISCLAIMER, TONE_VIOLATION
    pattern = Column(String(500), nullable=False)  # Regex or exact phrase
    replacement = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    version = Column(String(20), default="1.0")
    created_at = Column(DateTime, default=datetime.utcnow)


class GlossaryTerm(Base):
    __tablename__ = "glossary_terms"

    id = Column(String, primary_key=True, default=generate_uuid)
    term = Column(String(150), unique=True, nullable=False)
    status = Column(String(50), nullable=False)  # APPROVED, PROHIBITED, DISCOURAGED, CONTEXTUAL
    preferred_alternative = Column(String(255), nullable=True)
    context_note = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ApprovedFact(Base):
    __tablename__ = "approved_facts"

    id = Column(String, primary_key=True, default=generate_uuid)
    fact_code = Column(String(50), nullable=False)
    fact_name = Column(String(255), nullable=False)
    approved_value = Column(String(500), nullable=False)
    supporting_source = Column(String(255), nullable=False)
    owner = Column(String(100), nullable=False)
    effective_date = Column(String(50), nullable=False)
    expiry_date = Column(String(50), nullable=True)
    version = Column(String(20), default="1.0")
    status = Column(String(50), default="ACTIVE")  # ACTIVE, EXPIRED, SUPERSEDED
    is_historical = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class ClaimPassport(Base):
    __tablename__ = "claim_passports"

    id = Column(String, primary_key=True, default=generate_uuid)
    claim_code = Column(String(50), unique=True, nullable=False)
    claim_text = Column(Text, nullable=False)
    evidence = Column(Text, nullable=False)
    source_document = Column(String(255), nullable=False)
    owner = Column(String(100), nullable=False)
    expiry_date = Column(String(50), nullable=True)
    approval_status = Column(String(50), default="APPROVED")  # APPROVED, UNSUPPORTED, CONDITIONAL, REJECTED
    linked_fact_codes = Column(String(255), nullable=True)  # Comma separated
    created_at = Column(DateTime, default=datetime.utcnow)


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(String, primary_key=True, default=generate_uuid)
    org_id = Column(String, ForeignKey("organisations.id"), nullable=True)
    title = Column(String(255), nullable=False)
    content_type = Column(String(100), nullable=False)  # SOCIAL_MEDIA, ADVERTISEMENT, MARKETING_COPY, EMAIL, PRODUCT_DESCRIPTION, PRESS_RELEASE, GENERAL
    target_audience = Column(String(200), nullable=True)
    objective = Column(Text, nullable=True)
    campaign_name = Column(String(200), nullable=True)
    created_by_user_id = Column(String, ForeignKey("users.id"), nullable=True)
    current_status = Column(String(50), default="DRAFT")  # DRAFT, UNDER_REVIEW, CHANGES_REQUESTED, APPROVED, PUBLISHED, BLOCKED
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    organization = relationship("Organization", back_populates="submissions")
    versions = relationship("SubmissionVersion", back_populates="submission", cascade="all, delete-orphan", order_by="SubmissionVersion.version_number")
    comments = relationship("Comment", back_populates="submission", cascade="all, delete-orphan")
    approvals = relationship("Approval", back_populates="submission", cascade="all, delete-orphan")


class SubmissionVersion(Base):
    __tablename__ = "submission_versions"

    id = Column(String, primary_key=True, default=generate_uuid)
    submission_id = Column(String, ForeignKey("submissions.id"), nullable=False)
    version_number = Column(Integer, nullable=False, default=1)
    raw_text = Column(Text, nullable=False)
    file_path = Column(String(500), nullable=True)
    file_format = Column(String(50), default="PLAIN_TEXT")  # PLAIN_TEXT, PDF, DOCX
    content_hash = Column(String(64), nullable=False)  # SHA-256 of raw_text
    created_by = Column(String(100), default="Krish Arora (Creator)")
    created_at = Column(DateTime, default=datetime.utcnow)

    submission = relationship("Submission", back_populates="versions")
    reviews = relationship("Review", back_populates="submission_version", cascade="all, delete-orphan")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(String, primary_key=True, default=generate_uuid)
    submission_version_id = Column(String, ForeignKey("submission_versions.id"), nullable=False)
    status = Column(String(50), default="COMPLETED")  # PENDING, COMPLETED, FAILED
    findings_count = Column(Integer, default=0)
    critical_count = Column(Integer, default=0)
    warning_count = Column(Integer, default=0)
    info_count = Column(Integer, default=0)
    summary = Column(Text, nullable=True)
    review_duration_ms = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    submission_version = relationship("SubmissionVersion", back_populates="reviews")
    findings = relationship("Finding", back_populates="review", cascade="all, delete-orphan")


class Finding(Base):
    __tablename__ = "findings"

    id = Column(String, primary_key=True, default=generate_uuid)
    review_id = Column(String, ForeignKey("reviews.id"), nullable=False)
    rule_id = Column(String, ForeignKey("brand_rules.id"), nullable=True)
    rule_code = Column(String(50), nullable=True)
    original_text = Column(Text, nullable=False)
    start_char = Column(Integer, default=-1)
    end_char = Column(Integer, default=-1)
    category = Column(String(100), nullable=False)  # TERMINOLOGY, CLAIMS, TONE, FACT_ACCURACY, REGULATORY
    severity = Column(String(20), nullable=False)  # CRITICAL, WARNING, INFO
    classification = Column(String(50), nullable=False)  # RULE_BREACH, UNSUPPORTED_BY_EVIDENCE, POTENTIAL_RISK, NEEDS_HUMAN_JUDGEMENT
    what_went_wrong = Column(Text, nullable=False)
    why_it_matters = Column(Text, nullable=False)
    supporting_evidence = Column(Text, nullable=False)
    source_document = Column(String(255), nullable=False)
    suggested_correction = Column(Text, nullable=True)
    confidence_signal = Column(String(50), default="High (Deterministic Match)")
    needs_human_judgment = Column(Boolean, default=False)
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    review = relationship("Review", back_populates="findings")
    fixes = relationship("SuggestedFix", back_populates="finding", cascade="all, delete-orphan")
    evidence_refs = relationship("EvidenceReference", back_populates="finding", cascade="all, delete-orphan")


class EvidenceReference(Base):
    __tablename__ = "evidence_references"

    id = Column(String, primary_key=True, default=generate_uuid)
    finding_id = Column(String, ForeignKey("findings.id"), nullable=False)
    source_type = Column(String(50), nullable=False)  # FACT, CLAIM, DOCUMENT, RULE, GLOSSARY
    source_id = Column(String(100), nullable=True)
    title = Column(String(255), nullable=False)
    snippet = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    finding = relationship("Finding", back_populates="evidence_refs")


class SuggestedFix(Base):
    __tablename__ = "suggested_fixes"

    id = Column(String, primary_key=True, default=generate_uuid)
    finding_id = Column(String, ForeignKey("findings.id"), nullable=False)
    original_sentence = Column(Text, nullable=False)
    suggested_sentence = Column(Text, nullable=False)
    explanation = Column(Text, nullable=False)
    status = Column(String(50), default="PENDING")  # PENDING, ACCEPTED, REJECTED, MODIFIED
    applied_at = Column(DateTime, nullable=True)

    finding = relationship("Finding", back_populates="fixes")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(String, primary_key=True, default=generate_uuid)
    submission_id = Column(String, ForeignKey("submissions.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    author_name = Column(String(100), nullable=False)
    author_role = Column(String(50), nullable=False)
    comment_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    submission = relationship("Submission", back_populates="comments")
    user = relationship("User", back_populates="comments")


class Approval(Base):
    __tablename__ = "approvals"

    id = Column(String, primary_key=True, default=generate_uuid)
    submission_id = Column(String, ForeignKey("submissions.id"), nullable=False)
    submission_version_id = Column(String, ForeignKey("submission_versions.id"), nullable=False)
    reviewer_id = Column(String, ForeignKey("users.id"), nullable=True)
    reviewer_name = Column(String(100), nullable=False, default="Sanchita Sharma (Reviewer)")
    status = Column(String(50), nullable=False)  # APPROVED, CHANGES_REQUESTED, REJECTED
    decision_notes = Column(Text, nullable=True)
    approved_at = Column(DateTime, default=datetime.utcnow)

    submission = relationship("Submission", back_populates="approvals")
    signature = relationship("ApprovalSignature", uselist=False, back_populates="approval", cascade="all, delete-orphan")


class ApprovalSignature(Base):
    __tablename__ = "approval_signatures"

    id = Column(String, primary_key=True, default=generate_uuid)
    approval_id = Column(String, ForeignKey("approvals.id"), nullable=False, unique=True)
    submission_version_id = Column(String, ForeignKey("submission_versions.id"), nullable=False)
    canonical_content = Column(Text, nullable=False)
    content_sha256 = Column(String(64), nullable=False)
    signature_b64 = Column(Text, nullable=False)
    public_key_b64 = Column(Text, nullable=False)
    signed_at = Column(DateTime, default=datetime.utcnow)
    is_valid = Column(Boolean, default=True)

    approval = relationship("Approval", back_populates="signature")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, default=generate_uuid)
    action = Column(String(100), nullable=False)
    actor_id = Column(String(100), nullable=True)
    actor_name = Column(String(100), nullable=False)
    actor_role = Column(String(50), nullable=False)
    target_type = Column(String(50), nullable=False)  # SUBMISSION, REVIEW, APPROVAL, FACT, RULE, PUBLISH
    target_id = Column(String(100), nullable=False)
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Asset(Base):
    __tablename__ = "assets"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(200), nullable=False)
    asset_type = Column(String(50), nullable=False)  # LOGO_PRIMARY, LOGO_SECONDARY, COLOR_PALETTE, TYPOGRAPHY
    specs = Column(Text, nullable=True)
    svg_content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
