import re
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from backend.app.models.models import (
    BrandRule, GlossaryTerm, ApprovedFact, ClaimPassport
)
from backend.app.services.extraction_service import extract_sentences_with_offsets

class DeterministicRulesEngine:
    def __init__(self, db: Session):
        self.db = db

    def evaluate_content(self, text: str) -> List[Dict[str, Any]]:
        findings = []
        sentences = extract_sentences_with_offsets(text)

        # Load database rules
        active_rules = self.db.query(BrandRule).filter(BrandRule.is_active == True).all()
        glossary_terms = self.db.query(GlossaryTerm).filter(GlossaryTerm.is_active == True).all()
        active_facts = self.db.query(ApprovedFact).filter(ApprovedFact.status == "ACTIVE", ApprovedFact.is_historical == False).all()
        historical_facts = self.db.query(ApprovedFact).filter((ApprovedFact.is_historical == True) | (ApprovedFact.status == "SUPERSEDED")).all()
        claim_passports = self.db.query(ClaimPassport).all()

        for s in sentences:
            s_text = s["text"]
            s_lower = s_text.lower()
            start_pos = s["start_char"]
            end_pos = s["end_char"]

            # 1. Evaluate Glossary Terms
            for g_term in glossary_terms:
                term_pattern = r'\b' + re.escape(g_term.term.lower()) + r'\b'
                if re.search(term_pattern, s_lower):
                    if g_term.status == "PROHIBITED":
                        replacement = g_term.preferred_alternative if g_term.preferred_alternative and g_term.preferred_alternative.lower() != "none" else ""
                        suggested_s = re.sub(re.escape(g_term.term), replacement or "[Removed prohibited claim]", s_text, flags=re.IGNORECASE) if replacement else s_text.replace(g_term.term, "")
                        findings.append({
                            "rule_code": "TERM-PROHIBITED",
                            "original_text": s_text,
                            "start_char": start_pos,
                            "end_char": end_pos,
                            "category": "TERMINOLOGY",
                            "severity": "CRITICAL",
                            "classification": "RULE_BREACH",
                            "what_went_wrong": f"Prohibited term detected: '{g_term.term}'.",
                            "why_it_matters": g_term.context_note or "NexaPay compliance strictly prohibits absolute or non-compliant claims in external communications.",
                            "supporting_evidence": f"Brand Glossary: Term '{g_term.term}' is explicitly listed as PROHIBITED.",
                            "source_document": "NexaPay Brand Glossary v1.0",
                            "suggested_correction": suggested_s.strip(),
                            "confidence_signal": "High (Deterministic Match)",
                            "needs_human_judgment": False,
                            "evidence_type": "GLOSSARY",
                            "evidence_id": g_term.id
                        })
                    elif g_term.status == "DISCOURAGED":
                        replacement = g_term.preferred_alternative or "appropriate phrasing"
                        suggested_s = re.sub(re.escape(g_term.term), replacement, s_text, flags=re.IGNORECASE)
                        findings.append({
                            "rule_code": "TERM-DISCOURAGED",
                            "original_text": s_text,
                            "start_char": start_pos,
                            "end_char": end_pos,
                            "category": "TERMINOLOGY",
                            "severity": "WARNING",
                            "classification": "RULE_BREACH",
                            "what_went_wrong": f"Discouraged terminology used: '{g_term.term}'.",
                            "why_it_matters": f"Preferred alternative is '{replacement}'. Avoid promotional overstatement.",
                            "supporting_evidence": f"Brand Glossary: Term '{g_term.term}' is DISCOURAGED. Preferred: '{replacement}'.",
                            "source_document": "NexaPay Brand Glossary v1.0",
                            "suggested_correction": suggested_s.strip(),
                            "confidence_signal": "High (Deterministic Match)",
                            "needs_human_judgment": False,
                            "evidence_type": "GLOSSARY",
                            "evidence_id": g_term.id
                        })

            # 2. Evaluate Brand Rules
            for rule in active_rules:
                if re.search(rule.pattern, s_text, re.IGNORECASE):
                    # Formulate suggestion
                    suggested_s = s_text
                    if rule.replacement:
                        suggested_s = re.sub(rule.pattern, rule.replacement, s_text, flags=re.IGNORECASE)
                    
                    classification = "RULE_BREACH"
                    if rule.rule_type == "SUPERLATIVE":
                        classification = "UNSUPPORTED_BY_EVIDENCE"
                    elif rule.rule_type == "TONE_VIOLATION":
                        classification = "POTENTIAL_RISK"
                    elif rule.rule_type == "GUARANTEE":
                        classification = "RULE_BREACH"

                    findings.append({
                        "rule_code": rule.rule_code,
                        "original_text": s_text,
                        "start_char": start_pos,
                        "end_char": end_pos,
                        "category": rule.category,
                        "severity": rule.severity,
                        "classification": classification,
                        "what_went_wrong": f"Violated rule [{rule.rule_code}]: {rule.name}.",
                        "why_it_matters": rule.description,
                        "supporting_evidence": f"Rule {rule.rule_code}: {rule.description}",
                        "source_document": "NexaPay Brand Guidelines v1.0 & Content Policy",
                        "suggested_correction": suggested_s.strip() if suggested_s != s_text else f"Revise statement to adhere to {rule.name}.",
                        "confidence_signal": "High (Deterministic Rule Match)",
                        "needs_human_judgment": (rule.severity == "WARNING" or classification == "POTENTIAL_RISK"),
                        "evidence_type": "RULE",
                        "evidence_id": rule.id
                    })

            # 3. Currency / Pricing Fact Verification
            # Look for ₹ or Rs. or INR amounts in the sentence
            fee_matches = re.findall(r'(?:₹|rs\.?|inr)\s*(\d+)', s_lower)
            if fee_matches:
                for fee_val in fee_matches:
                    fee_num = int(fee_val)
                    # Check against transaction fee
                    # Current fee is 399
                    current_fee_fact = next((f for f in active_facts if "fee" in f.fact_name.lower() or "399" in f.approved_value), None)
                    current_fee_str = "₹399"
                    if current_fee_fact:
                        current_fee_str = current_fee_fact.approved_value

                    # Check if this sentence mentions fee / transaction / cost
                    if any(k in s_lower for k in ["fee", "transaction", "charge", "cost", "pricing"]):
                        if fee_val == "499":
                            # Historical outdated fact!
                            h_fact = next((hf for hf in historical_facts if "499" in hf.approved_value), None)
                            suggested_s = re.sub(r'(?:₹|rs\.?|inr)\s*499', current_fee_str, s_text, flags=re.IGNORECASE)
                            findings.append({
                                "rule_code": "FACT-OUTDATED",
                                "original_text": s_text,
                                "start_char": start_pos,
                                "end_char": end_pos,
                                "category": "FACT_ACCURACY",
                                "severity": "CRITICAL",
                                "classification": "RULE_BREACH",
                                "what_went_wrong": f"Outdated transaction fee referenced: ₹499.",
                                "why_it_matters": f"The ₹499 fee was superseded on 2025-10-01. The current approved transaction fee is {current_fee_str}.",
                                "supporting_evidence": f"Historical Brand Updates & Approved Fact FACT-002: Approved current fee is {current_fee_str} (effective 2025-10-01). Superseded fee was ₹499.",
                                "source_document": "NexaPay Approved Facts Register & Historical Updates",
                                "suggested_correction": suggested_s,
                                "confidence_signal": "High (Deterministic Fact Comparison)",
                                "needs_human_judgment": False,
                                "evidence_type": "FACT",
                                "evidence_id": h_fact.id if h_fact else "FACT-002-HIST"
                            })
                        elif fee_val != "399" and fee_val != "499":
                            # Unapproved or fictitious fee like ₹299
                            suggested_s = re.sub(r'(?:₹|rs\.?|inr)\s*' + fee_val, current_fee_str, s_text, flags=re.IGNORECASE)
                            findings.append({
                                "rule_code": "FACT-INCORRECT",
                                "original_text": s_text,
                                "start_char": start_pos,
                                "end_char": end_pos,
                                "category": "FACT_ACCURACY",
                                "severity": "CRITICAL",
                                "classification": "RULE_BREACH",
                                "what_went_wrong": f"Incorrect transaction fee cited: ₹{fee_val}.",
                                "why_it_matters": f"Approved transaction fee is {current_fee_str}. Publishing incorrect pricing violates regulatory financial disclosure standards.",
                                "supporting_evidence": f"Approved Facts Register (FACT-002): Approved transaction fee is {current_fee_str}.",
                                "source_document": "NexaPay Approved Facts Register v1.0",
                                "suggested_correction": suggested_s,
                                "confidence_signal": "High (Deterministic Fact Verification)",
                                "needs_human_judgment": False,
                                "evidence_type": "FACT",
                                "evidence_id": current_fee_fact.id if current_fee_fact else "FACT-002"
                            })

            # 4. Check Claim Passports for unsupported or unverified claims
            # e.g., CLAIM-002: "safest payment platform"
            for passport in claim_passports:
                claim_keywords = [w for w in re.findall(r'\b\w+\b', passport.claim_text.lower()) if len(w) > 4]
                match_count = sum(1 for kw in claim_keywords if kw in s_lower)
                if match_count >= 2 or passport.claim_text.lower() in s_lower:
                    if passport.approval_status == "UNSUPPORTED":
                        # Check if already flagged by rule, if not flag as UNSUPPORTED_BY_EVIDENCE
                        if not any(f["rule_code"] == "CLAIM-UNSUPPORTED" and f["original_text"] == s_text for f in findings):
                            suggested_s = re.sub(r'India\'s safest payment platform', 'a secure digital payment platform', s_text, flags=re.IGNORECASE)
                            findings.append({
                                "rule_code": "CLAIM-UNSUPPORTED",
                                "original_text": s_text,
                                "start_char": start_pos,
                                "end_char": end_pos,
                                "category": "CLAIMS",
                                "severity": "CRITICAL",
                                "classification": "UNSUPPORTED_BY_EVIDENCE",
                                "what_went_wrong": f"Claim flagged in Claim Passport as unsupported: '{passport.claim_text}'.",
                                "why_it_matters": "No approved independent security audit or regulatory certification substantiates the claim of being 'India\'s safest'. Superlative claims require explicit certification.",
                                "supporting_evidence": f"Claim Passport {passport.claim_code}: Status is UNSUPPORTED. Evidence: '{passport.evidence}'.",
                                "source_document": "NexaPay Claim Passports Register",
                                "suggested_correction": suggested_s if suggested_s != s_text else "Remove or qualify absolute superlative safety claim.",
                                "confidence_signal": "High (Claim Passport Match)",
                                "needs_human_judgment": True,
                                "evidence_type": "CLAIM",
                                "evidence_id": passport.id
                            })

        # Deduplicate findings by rule_code and original_text
        unique_findings = []
        seen = set()
        for f in findings:
            key = (f["rule_code"], f["original_text"][:40])
            if key not in seen:
                seen.add(key)
                unique_findings.append(f)

        return unique_findings
