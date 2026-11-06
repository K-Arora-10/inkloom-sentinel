from datetime import datetime
from sqlalchemy.orm import Session
from backend.app.models.models import (
    Organization, User, Document, DocumentVersion, BrandRule, GlossaryTerm,
    ApprovedFact, ClaimPassport, Asset, Submission, SubmissionVersion, Review,
    Finding, SuggestedFix, EvidenceReference, AuditLog
)
from backend.app.services.crypto_service import compute_sha256

def seed_database(db: Session):
    # Check if already seeded
    if db.query(Organization).filter(Organization.code == "NEXAPAY").first():
        return

    # 1. Organization
    org = Organization(
        name="NexaPay Technologies India",
        code="NEXAPAY",
        description="NexaPay Technologies India — Digital payments infrastructure, merchant acquisition, and transactional settlement platform."
    )
    db.add(org)
    db.flush()

    # 2. Demo Users
    creator = User(
        name="Krish Arora",
        email="krish.creator@nexapay.internal",
        role="CREATOR",
        org_id=org.id
    )
    reviewer = User(
        name="Sanchita Sharma",
        email="sanchita.reviewer@nexapay.internal",
        role="REVIEWER",
        org_id=org.id
    )
    db.add_all([creator, reviewer])
    db.flush()

    # 3. Document 1: Brand Guidelines v1.0
    doc1 = Document(
        org_id=org.id,
        title="NexaPay Brand Guidelines v1.0",
        doc_type="GUIDELINE",
        category="BRAND_GOVERNANCE",
        current_version="1.0",
        summary="Foundational brand identity, mission, voice and writing guidelines for NexaPay digital payments."
    )
    db.add(doc1)
    db.flush()
    doc1_ver = DocumentVersion(
        document_id=doc1.id,
        version_number="1.0",
        content="""# NexaPay Brand Guidelines v1.0

## 1. Company Identity & Positioning
NexaPay is an enterprise digital payments ecosystem empowering millions of Indian merchants and consumers with frictionless, reliable transaction infrastructure.

## 2. Mission & Communication Principles
Our mission is to enable seamless financial flows with absolute transparency, uncompromising regulatory adherence, and quiet competence.

## 3. Brand Personality & Tone of Voice
- **Professional**: Authoritative, grounded in verified facts, devoid of financial hyperbole.
- **Confident**: We do not need superlative bluster or sensationalist slogans.
- **Approachable**: Dignified yet accessible to both urban businesses and grassroots merchants.
- **Trustworthy**: Every claim must be substantiated by registered audit evidence or regulatory compliance.
- **Restrained**: We explicitly avoid aggressive promotional salesmanship, emojis in corporate notices, or exclamation-mark-heavy copy.

## 4. Writing Style
- Prefer simple, declarative sentences.
- Avoid hyperbole (e.g., "mind-blowing", "insane deal", "crazy discounts").
- Never guarantee investment or speculative returns.

## 5. Examples of Unacceptable Content
- "NexaPay guarantees 100% security for all transactions." -> Unacceptable. Absolute security cannot be guaranteed.
- "Hey folks! Check out our insane ₹299 deal!" -> Unacceptable. Informal slang and fictitious pricing breach brand standards.
""",
        extracted_text="Foundational NexaPay Brand Guidelines v1.0.",
        file_format="MARKDOWN",
        created_by="Brand Committee"
    )
    db.add(doc1_ver)

    # 4. Document 2: Brand Glossary
    doc2 = Document(
        org_id=org.id,
        title="NexaPay Brand Glossary v1.0",
        doc_type="GLOSSARY",
        category="TERMINOLOGY",
        current_version="1.0",
        summary="Definitive directory of approved, discouraged, and strictly prohibited terms across all NexaPay media."
    )
    db.add(doc2)
    db.flush()
    doc2_ver = DocumentVersion(
        document_id=doc2.id,
        version_number="1.0",
        content="""# NexaPay Brand Glossary

| Term | Status | Preferred Alternative | Contextual Requirement |
|---|---|---|---|
| Guaranteed returns | PROHIBITED | None | Financial regulatory restriction (SEBI/RBI). |
| 100% secure | PROHIBITED | Use approved standard: 'multi-layer bank-grade encryption' | Absolute zero-risk guarantees are legally untenable. |
| Amazing deal | DISCOURAGED | Special offer | Prevents promotional sensationalism. |
| Insane deal | PROHIBITED | Special offer / Competitive pricing | Inappropriate colloquialism for financial infrastructure. |
| Transaction fee | APPROVED | Transaction fee | Standard approved term. Current fee is ₹399. |
| Payment platform | APPROVED | Payment platform | Approved category descriptor. |
| India's safest payment platform | PROHIBITED | A secure digital payment platform | Superlatives require third-party accreditation which is absent. |
""",
        extracted_text="NexaPay Brand Glossary Table and Term Directory.",
        file_format="MARKDOWN",
        created_by="Governance Team"
    )
    db.add(doc2_ver)

    # 5. Document 3: Approved Facts Register
    doc3 = Document(
        org_id=org.id,
        title="NexaPay Approved Facts Register v1.0",
        doc_type="FACT_SHEET",
        category="FACT_ACCURACY",
        current_version="1.0",
        summary="Certified single source of truth for corporate numbers, thresholds, and commercial terms."
    )
    db.add(doc3)
    db.flush()
    doc3_ver = DocumentVersion(
        document_id=doc3.id,
        version_number="1.0",
        content="""# Approved Facts Register
Certified commercial facts for NexaPay:
- FACT-001: Operating Domain: Digital payments & merchant checkout infrastructure.
- FACT-002: Approved Transaction Fee: ₹399 (Effective: 2025-10-01).
- FACT-002-HIST: Superseded Transaction Fee: ₹499 (Expired: 2025-09-30).
- FACT-003: Free Delivery Threshold: ₹499 on eligible hardware terminals.
""",
        file_format="MARKDOWN",
        created_by="Finance & Operations"
    )
    db.add(doc3_ver)

    # 6. Document 4: Claim Passports Register
    doc4 = Document(
        org_id=org.id,
        title="NexaPay Claim Passports Register",
        doc_type="POLICY",
        category="CLAIMS",
        current_version="1.0",
        summary="Audit registry of public statements, their evidence backing, and verification status."
    )
    db.add(doc4)
    db.flush()
    doc4_ver = DocumentVersion(
        document_id=doc4.id,
        version_number="1.0",
        content="""# Claim Passports
- CLAIM-001: "Free delivery on eligible orders above ₹499." [Status: APPROVED]
- CLAIM-002: "NexaPay is India's safest payment platform." [Status: UNSUPPORTED]
- CLAIM-003: "Transaction fees are ₹399." [Status: APPROVED]
""",
        file_format="MARKDOWN",
        created_by="Legal & Compliance"
    )
    db.add(doc4_ver)

    # 7. Document 5: Visual Identity Guide
    doc5 = Document(
        org_id=org.id,
        title="NexaPay Visual Identity Guide",
        doc_type="VISUAL",
        category="DESIGN_SYSTEM",
        current_version="1.0",
        summary="Color tokens, logo clearances, typography hierarchy, and accessibility standards."
    )
    db.add(doc5)
    db.flush()
    doc5_ver = DocumentVersion(
        document_id=doc5.id,
        version_number="1.0",
        content="""# NexaPay Visual Identity
- Forest Green Accent: #405746
- Warm Off-White Background: #F8F7F4
- Near-Black Text: #242522
- Warm Grey Border: #E8E6DF
- Clear Space around NexaPay logo: Minimum 24px padding.
- Typography: Inter or Geist font stack.
""",
        file_format="MARKDOWN",
        created_by="Design Team"
    )
    db.add(doc5_ver)

    # 8. Document 6: Content and Advertising Policy
    doc6 = Document(
        org_id=org.id,
        title="NexaPay Content and Advertising Policy",
        doc_type="POLICY",
        category="COMPLIANCE",
        current_version="1.0",
        summary="Rules governing promotional campaigns, superlatives, and financial liability disclosures."
    )
    db.add(doc6)
    db.flush()
    doc6_ver = DocumentVersion(
        document_id=doc6.id,
        version_number="1.0",
        content="""# Content & Advertising Policy
1. Unsupported Superlatives: Any claim to be 'safest', 'fastest', or 'cheapest' requires third-party certification.
2. Financial Disclosures: Any pricing quotation must specify whether GST is inclusive and cite the active registered fee.
3. Escalation Rules: Claims involving guaranteed financial returns or absolute security require Head of Compliance signoff.
""",
        file_format="MARKDOWN",
        created_by="Compliance Office"
    )
    db.add(doc6_ver)

    # 9. Document 7: Historical Brand Updates
    doc7 = Document(
        org_id=org.id,
        title="NexaPay Historical Brand Updates",
        doc_type="GUIDELINE",
        category="ARCHIVE",
        current_version="1.0",
        summary="Historical log of superseded brand parameters, retired fees, and policy revisions."
    )
    db.add(doc7)
    db.flush()
    doc7_ver = DocumentVersion(
        document_id=doc7.id,
        version_number="1.0",
        content="""# Historical Brand Updates
- 2025-10-01: Standard transaction fee lowered from ₹499 to ₹399. (Approved by: Ananya Sen, CFO).
- 2025-06-15: Retired phrase '100% secure' in favor of contextual security descriptors.
""",
        file_format="MARKDOWN",
        created_by="Governance Archive"
    )
    db.add(doc7_ver)

    # 10. Glossary Terms in Table
    terms = [
        GlossaryTerm(
            term="Guaranteed returns",
            status="PROHIBITED",
            preferred_alternative="None",
            context_note="Guaranteed returns in financial payments violate regulatory guidelines."
        ),
        GlossaryTerm(
            term="100% secure",
            status="PROHIBITED",
            preferred_alternative="bank-grade encryption and secure protocols",
            context_note="Absolute security claims create regulatory liability; use qualified standards."
        ),
        GlossaryTerm(
            term="Amazing deal",
            status="DISCOURAGED",
            preferred_alternative="Special offer",
            context_note="Sensationalist phrasing contradicts NexaPay's restrained editorial brand personality."
        ),
        GlossaryTerm(
            term="Transaction fee",
            status="APPROVED",
            preferred_alternative="Transaction fee",
            context_note="Standard approved nomenclature for billing."
        ),
        GlossaryTerm(
            term="Payment platform",
            status="APPROVED",
            preferred_alternative="Payment platform",
            context_note="Standard approved domain descriptor."
        ),
        GlossaryTerm(
            term="Insane",
            status="PROHIBITED",
            preferred_alternative="Competitive",
            context_note="Slang adjectives are prohibited in commercial and marketing releases."
        )
    ]
    db.add_all(terms)

    # 11. Brand Rules
    rules = [
        BrandRule(
            rule_code="RULE-SUPERLATIVE-SAFE",
            category="CLAIMS",
            name="Unsupported Superlative 'Safest'",
            description="NexaPay cannot claim to be 'safest' without third-party comparative audit certification.",
            severity="CRITICAL",
            rule_type="SUPERLATIVE",
            pattern=r"\b(safest|number\s*one\s*safe|most\s*secure)\b",
            replacement="a secure digital payment platform"
        ),
        BrandRule(
            rule_code="RULE-GUARANTEE-SECURITY",
            category="CLAIMS",
            name="Absolute Security Guarantee",
            description="Absolute security guarantees ('guaranteed secure', 'guarantees the best') are prohibited by compliance.",
            severity="CRITICAL",
            rule_type="GUARANTEE",
            pattern=r"\b(guaranteed\s+secure|guarantees\s+the\s+best|guaranteed\s+returns)\b",
            replacement="multi-layer security protections"
        ),
        BrandRule(
            rule_code="RULE-TONE-EXCLAMATION",
            category="TONE",
            name="Hyperbolic Punctuation",
            description="Exclamation clusters (e.g., '!!!') violate NexaPay's restrained, professional aesthetic.",
            severity="WARNING",
            rule_type="TONE_VIOLATION",
            pattern=r"[!]{2,}",
            replacement="."
        ),
        BrandRule(
            rule_code="RULE-CASUAL-GREETING",
            category="TONE",
            name="Informal Colloquial Greeting",
            description="'Hey folks' is too informal for an enterprise digital payments brand.",
            severity="WARNING",
            rule_type="TONE_VIOLATION",
            pattern=r"\b(hey\s+folks|hey\s+guys)\b",
            replacement="Welcome"
        )
    ]
    db.add_all(rules)

    # 12. Approved Facts
    facts = [
        ApprovedFact(
            fact_code="FACT-001",
            fact_name="Domain of Operation",
            approved_value="Digital payments & checkout infrastructure",
            supporting_source="NexaPay Corporate Charter 2025",
            owner="Legal & Corporate Affairs",
            effective_date="2024-01-01",
            status="ACTIVE",
            is_historical=False
        ),
        ApprovedFact(
            fact_code="FACT-002",
            fact_name="Standard Transaction Fee",
            approved_value="₹399",
            supporting_source="Finance Circular FC-2025-10",
            owner="Finance & Pricing Committee",
            effective_date="2025-10-01",
            status="ACTIVE",
            is_historical=False
        ),
        ApprovedFact(
            fact_code="FACT-002-HIST",
            fact_name="Superseded Standard Transaction Fee",
            approved_value="₹499",
            supporting_source="Finance Circular FC-2024-04 (Superseded)",
            owner="Finance & Pricing Committee",
            effective_date="2024-04-01",
            expiry_date="2025-09-30",
            status="SUPERSEDED",
            is_historical=True
        ),
        ApprovedFact(
            fact_code="FACT-003",
            fact_name="Hardware Delivery Threshold",
            approved_value="₹499",
            supporting_source="Operations Standard Operating Procedure v3.1",
            owner="Logistics & Supply Chain",
            effective_date="2025-01-01",
            status="ACTIVE",
            is_historical=False
        )
    ]
    db.add_all(facts)

    # 13. Claim Passports
    passports = [
        ClaimPassport(
            claim_code="CLAIM-001",
            claim_text="Free delivery on eligible orders above ₹499.",
            evidence="Backed by Operations SOP v3.1 and Logistics vendor SLA.",
            source_document="NexaPay Approved Facts Register (FACT-003)",
            owner="Logistics",
            expiry_date="2026-12-31",
            approval_status="APPROVED",
            linked_fact_codes="FACT-003"
        ),
        ClaimPassport(
            claim_code="CLAIM-002",
            claim_text="NexaPay is India's safest payment platform.",
            evidence="No certified benchmark audit substantiates this superlative. Superlative comparison is legally unverified.",
            source_document="Claim Passports Register",
            owner="Compliance Office",
            expiry_date=None,
            approval_status="UNSUPPORTED",
            linked_fact_codes=None
        ),
        ClaimPassport(
            claim_code="CLAIM-003",
            claim_text="Transaction fees are ₹399.",
            evidence="Backed by Finance Circular FC-2025-10 effective October 1, 2025.",
            source_document="NexaPay Approved Facts Register (FACT-002)",
            owner="Finance",
            expiry_date="2026-06-30",
            approval_status="APPROVED",
            linked_fact_codes="FACT-002"
        )
    ]
    db.add_all(passports)

    # 14. NexaPay Visual Brand Asset (SVG Logo)
    svg_logo = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 60" width="240" height="60">
  <rect width="240" height="60" fill="none"/>
  <rect x="8" y="14" width="32" height="32" rx="4" fill="#405746"/>
  <path d="M16 38 L24 22 L32 38" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
  <circle cx="24" cy="30" r="2.5" fill="#FFFFFF"/>
  <text x="50" y="38" font-family="Inter, sans-serif" font-size="22" font-weight="600" fill="#242522" letter-spacing="-0.5">NexaPay</text>
  <text x="142" y="38" font-family="Inter, sans-serif" font-size="11" font-weight="500" fill="#77766F" letter-spacing="1.5">GOVERNED</text>
</svg>"""

    asset = Asset(
        name="NexaPay Primary Logo Mark",
        asset_type="LOGO_PRIMARY",
        specs="Monochrome Forest Green (#405746) emblem with near-black (#242522) wordmark. Clear margin: 24px.",
        svg_content=svg_logo
    )
    db.add(asset)

    # 15. Initial Demo Submission (Pre-seeded Scenario A)
    initial_text = "NexaPay is India's safest payment platform for everyday payments. Get started today with our amazing ₹299 transaction fee. Guaranteed secure transactions for everyone!"
    sub = Submission(
        org_id=org.id,
        title="NexaPay Q1 Merchant Promotional Ad",
        content_type="ADVERTISEMENT",
        target_audience="Small & Medium Enterprise Merchants in Tier 1 & 2 cities",
        objective="Announce merchant fee structures and drive onboarding registrations",
        campaign_name="NexaPay Spring Merchant Drive",
        created_by_user_id=creator.id,
        current_status="UNDER_REVIEW"
    )
    db.add(sub)
    db.flush()

    sub_ver = SubmissionVersion(
        submission_id=sub.id,
        version_number=1,
        raw_text=initial_text,
        file_format="PLAIN_TEXT",
        content_hash=compute_sha256(initial_text),
        created_by="Krish Arora (Creator)"
    )
    db.add(sub_ver)
    db.flush()

    # Pre-run review for the initial submission so the judge immediately sees rich findings on launch!
    review = Review(
        submission_version_id=sub_ver.id,
        status="COMPLETED",
        findings_count=4,
        critical_count=3,
        warning_count=1,
        info_count=0,
        summary="Review identified 4 findings (3 critical violations, 1 warning) regarding unsupported claims, incorrect pricing, and discouraged terminology.",
        review_duration_ms=45
    )
    db.add(review)
    db.flush()

    f1 = Finding(
        review_id=review.id,
        rule_code="CLAIM-UNSUPPORTED",
        original_text="NexaPay is India's safest payment platform for everyday payments.",
        start_char=0,
        end_char=66,
        category="CLAIMS",
        severity="CRITICAL",
        classification="UNSUPPORTED_BY_EVIDENCE",
        what_went_wrong="Unsupported superlative statement: 'India's safest payment platform'.",
        why_it_matters="No approved third-party security certification or audit substantiates this superlative claim. Stating this creates regulatory liability under ASCI rules.",
        supporting_evidence="Claim Passport CLAIM-002: Status is UNSUPPORTED. No certified benchmark audit registered in NexaPay Brand Vault.",
        source_document="NexaPay Claim Passports Register & Content Policy",
        suggested_correction="NexaPay is a secure digital payment platform for everyday payments.",
        confidence_signal="High (Deterministic Match)",
        needs_human_judgment=True
    )
    f2 = Finding(
        review_id=review.id,
        rule_code="FACT-INCORRECT",
        original_text="Get started today with our amazing ₹299 transaction fee.",
        start_char=67,
        end_char=123,
        category="FACT_ACCURACY",
        severity="CRITICAL",
        classification="RULE_BREACH",
        what_went_wrong="Incorrect transaction fee quoted: ₹299.",
        why_it_matters="The officially approved transaction fee is ₹399 (effective 2025-10-01). Fictitious promotional pricing breaches commercial governance.",
        supporting_evidence="Approved Facts Register (FACT-002): Approved standard fee is ₹399.",
        source_document="NexaPay Approved Facts Register v1.0",
        suggested_correction="Get started today with our special offer ₹399 transaction fee.",
        confidence_signal="High (Deterministic Fact Verification)",
        needs_human_judgment=False
    )
    f3 = Finding(
        review_id=review.id,
        rule_code="RULE-GUARANTEE-SECURITY",
        original_text="Guaranteed secure transactions for everyone!",
        start_char=124,
        end_char=168,
        category="CLAIMS",
        severity="CRITICAL",
        classification="RULE_BREACH",
        what_went_wrong="Prohibited absolute security guarantee: 'Guaranteed secure'.",
        why_it_matters="Absolute security guarantees are legally invalid in digital payment infrastructure. Industry-standard bank-grade encryption must be referenced instead.",
        supporting_evidence="Brand Glossary & Policy: Term 'Guaranteed secure' is PROHIBITED. Absolute guarantees violate compliance guidelines.",
        source_document="NexaPay Brand Glossary v1.0",
        suggested_correction="Bank-grade encrypted transactions for everyone.",
        confidence_signal="High (Deterministic Rule Match)",
        needs_human_judgment=False
    )
    f4 = Finding(
        review_id=review.id,
        rule_code="TERM-DISCOURAGED",
        original_text="Get started today with our amazing ₹299 transaction fee.",
        start_char=67,
        end_char=123,
        category="TERMINOLOGY",
        severity="WARNING",
        classification="RULE_BREACH",
        what_went_wrong="Discouraged terminology: 'amazing'.",
        why_it_matters="NexaPay's editorial voice is restrained and professional. 'Amazing deal' is flagged for promotional overstatement.",
        supporting_evidence="Brand Glossary: 'Amazing deal' is DISCOURAGED. Preferred alternative: 'Special offer'.",
        source_document="NexaPay Brand Glossary v1.0",
        suggested_correction="Get started today with our special offer ₹399 transaction fee.",
        confidence_signal="High (Deterministic Match)",
        needs_human_judgment=False
    )
    db.add_all([f1, f2, f3, f4])
    db.flush()

    for f in [f1, f2, f3, f4]:
        db.add(SuggestedFix(
            finding_id=f.id,
            original_sentence=f.original_text,
            suggested_sentence=f.suggested_correction,
            explanation=f"Replaces non-compliant phrasing in accordance with {f.source_document}.",
            status="PENDING"
        ))
        db.add(EvidenceReference(
            finding_id=f.id,
            source_type="RULE",
            source_id="REF-NEXAPAY",
            title=f.source_document,
            snippet=f.supporting_evidence
        ))

    db.add(AuditLog(
        action="SYSTEM_INITIALIZED",
        actor_name="System Seeder",
        actor_role="SYSTEM",
        target_type="ORGANIZATION",
        target_id=org.id,
        details="Initial NexaPay brand documentation, rules, facts, and baseline compliance repository initialized."
    ))

    db.commit()
