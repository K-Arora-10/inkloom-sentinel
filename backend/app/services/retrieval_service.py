import re
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.app.models.models import (
    ApprovedFact, ClaimPassport, GlossaryTerm, BrandRule, Document, DocumentVersion
)

class RetrievalService:
    def __init__(self, db: Session):
        self.db = db

    def get_active_facts(self) -> List[ApprovedFact]:
        return self.db.query(ApprovedFact).filter(
            ApprovedFact.status == "ACTIVE",
            ApprovedFact.is_historical == False
        ).all()

    def get_historical_facts(self) -> List[ApprovedFact]:
        return self.db.query(ApprovedFact).filter(
            (ApprovedFact.is_historical == True) | (ApprovedFact.status == "SUPERSEDED")
        ).all()

    def get_all_claim_passports(self) -> List[ClaimPassport]:
        return self.db.query(ClaimPassport).all()

    def get_active_glossary_terms(self) -> List[GlossaryTerm]:
        return self.db.query(GlossaryTerm).filter(GlossaryTerm.is_active == True).all()

    def get_active_rules(self) -> List[BrandRule]:
        return self.db.query(BrandRule).filter(BrandRule.is_active == True).all()

    def find_relevant_sources_for_claim(self, claim_text: str) -> Dict[str, Any]:
        """
        Retrieves matching facts, claim passports, and glossary entries
        for a candidate statement or claim.
        """
        claim_lower = claim_text.lower()
        matched_facts = []
        matched_historical = []
        matched_passports = []
        matched_glossary = []

        # Check Active Facts
        for fact in self.get_active_facts():
            # Keyword or value match
            if (fact.approved_value.lower() in claim_lower or 
                any(w in claim_lower for w in fact.fact_name.lower().split() if len(w) > 3)):
                matched_facts.append(fact)

        # Check Historical Facts
        for h_fact in self.get_historical_facts():
            if h_fact.approved_value.lower() in claim_lower:
                matched_historical.append(h_fact)

        # Check Claim Passports
        for passport in self.get_all_claim_passports():
            # Match if key phrases match
            keywords = [w for w in re.findall(r'\b\w+\b', passport.claim_text.lower()) if len(w) > 4]
            overlap = sum(1 for kw in keywords if kw in claim_lower)
            if overlap >= 2 or passport.claim_text.lower() in claim_lower:
                matched_passports.append(passport)

        # Check Glossary
        for term in self.get_active_glossary_terms():
            if term.term.lower() in claim_lower:
                matched_glossary.append(term)

        return {
            "matched_facts": matched_facts,
            "matched_historical": matched_historical,
            "matched_passports": matched_passports,
            "matched_glossary": matched_glossary
        }
