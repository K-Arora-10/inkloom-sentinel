import time
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from backend.app.models.models import (
    Submission, SubmissionVersion, Review, Finding, EvidenceReference, SuggestedFix
)
from backend.app.services.extraction_service import extract_sentences_with_offsets
from backend.app.services.rules_engine import DeterministicRulesEngine
from backend.app.services.retrieval_service import RetrievalService
from backend.app.services.ai_service import get_ai_provider

class ReviewPipeline:
    def __init__(self, db: Session):
        self.db = db
        self.rules_engine = DeterministicRulesEngine(db)
        self.retrieval_service = RetrievalService(db)
        self.ai_provider = get_ai_provider()

    def run_review(self, submission_version: SubmissionVersion) -> Review:
        start_time = time.time()
        raw_text = submission_version.raw_text

        # Stage 1: Extraction & Sentence parsing
        sentences = extract_sentences_with_offsets(raw_text)

        # Stage 2: Deterministic checks
        deterministic_findings = self.rules_engine.evaluate_content(raw_text)

        # Stage 3: Approved-source retrieval context
        approved_context = {
            "active_facts": [f.approved_value for f in self.retrieval_service.get_active_facts()],
            "historical_facts": [f.approved_value for f in self.retrieval_service.get_historical_facts()],
            "glossary": [g.term for g in self.retrieval_service.get_active_glossary_terms()]
        }

        # Stage 4: AI contextual analysis (with automatic graceful fallback)
        ai_response = None
        try:
            ai_response = self.ai_provider.analyze_content(raw_text, approved_context)
        except Exception:
            ai_response = None

        all_findings_raw = list(deterministic_findings)

        if ai_response and ai_response.findings:
            for ai_f in ai_response.findings:
                # Avoid duplicate findings on the same sentence
                if not any(df["original_text"] == ai_f.original_text and df["category"] == ai_f.category for df in deterministic_findings):
                    # Find offsets if possible
                    start_char = raw_text.find(ai_f.original_text)
                    end_char = start_char + len(ai_f.original_text) if start_char != -1 else -1

                    all_findings_raw.append({
                        "rule_code": f"AI-{ai_f.category}",
                        "original_text": ai_f.original_text,
                        "start_char": start_char,
                        "end_char": end_char,
                        "category": ai_f.category,
                        "severity": ai_f.severity,
                        "classification": ai_f.classification,
                        "what_went_wrong": ai_f.what_went_wrong,
                        "why_it_matters": ai_f.why_it_matters,
                        "supporting_evidence": ai_f.supporting_evidence,
                        "source_document": "NexaPay Brand Guidelines & AI Context Review",
                        "suggested_correction": ai_f.suggested_correction,
                        "confidence_signal": ai_f.confidence_signal,
                        "needs_human_judgment": ai_f.needs_human_judgment,
                        "evidence_type": "DOCUMENT",
                        "evidence_id": "GUIDELINES-AI"
                    })

        # Calculate counts
        critical_count = sum(1 for f in all_findings_raw if f["severity"] == "CRITICAL")
        warning_count = sum(1 for f in all_findings_raw if f["severity"] == "WARNING")
        info_count = sum(1 for f in all_findings_raw if f["severity"] == "INFO")

        duration_ms = int((time.time() - start_time) * 1000)

        # Stage 5: Create Review Record and Findings in DB
        review = Review(
            submission_version_id=submission_version.id,
            status="COMPLETED",
            findings_count=len(all_findings_raw),
            critical_count=critical_count,
            warning_count=warning_count,
            info_count=info_count,
            summary=f"Found {len(all_findings_raw)} items ({critical_count} critical, {warning_count} warnings, {info_count} info) requiring review.",
            review_duration_ms=duration_ms
        )
        self.db.add(review)
        self.db.flush()

        # Insert findings and linked evidence & fixes
        for f_data in all_findings_raw:
            finding = Finding(
                review_id=review.id,
                rule_code=f_data.get("rule_code"),
                original_text=f_data["original_text"],
                start_char=f_data.get("start_char", -1),
                end_char=f_data.get("end_char", -1),
                category=f_data["category"],
                severity=f_data["severity"],
                classification=f_data["classification"],
                what_went_wrong=f_data["what_went_wrong"],
                why_it_matters=f_data["why_it_matters"],
                supporting_evidence=f_data["supporting_evidence"],
                source_document=f_data["source_document"],
                suggested_correction=f_data.get("suggested_correction"),
                confidence_signal=f_data.get("confidence_signal", "High"),
                needs_human_judgment=f_data.get("needs_human_judgment", False),
                is_resolved=False
            )
            self.db.add(finding)
            self.db.flush()

            # Add Evidence Reference
            ev_ref = EvidenceReference(
                finding_id=finding.id,
                source_type=f_data.get("evidence_type", "RULE"),
                source_id=str(f_data.get("evidence_id", "REF-01")),
                title=f_data["source_document"],
                snippet=f_data["supporting_evidence"]
            )
            self.db.add(ev_ref)

            # Add Suggested Fix if correction available
            if f_data.get("suggested_correction"):
                fix = SuggestedFix(
                    finding_id=finding.id,
                    original_sentence=f_data["original_text"],
                    suggested_sentence=f_data["suggested_correction"],
                    explanation=f"Preserves original intent while complying with {f_data['source_document']}.",
                    status="PENDING"
                )
                self.db.add(fix)

        self.db.commit()
        self.db.refresh(review)
        return review
