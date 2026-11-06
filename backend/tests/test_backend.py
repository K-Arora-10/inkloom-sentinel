import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database import SessionLocal, Base, engine
from backend.app.seed.seed_data import seed_database
from backend.app.services.crypto_service import (
    compute_sha256, sign_approval_payload, verify_approval_signature, get_or_create_ed25519_keypair
)
from backend.app.services.extraction_service import extract_text_from_pdf, extract_text_from_docx

client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed_database(db)
    db.close()
    yield

# 1. Health endpoint
def test_1_health_endpoint():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] in ["healthy", "degraded"]
    assert "Inkloom Sentinel" in data["product"]
    assert data["organization"] == "NexaPay Technologies India"
    assert data["database_connected"] is True

# 2. Brand Vault retrieval
def test_2_brand_vault_retrieval():
    # Documents
    docs_res = client.get("/api/brand-vault/documents")
    assert docs_res.status_code == 200
    docs = docs_res.json()
    assert len(docs) >= 7

    # Rules
    rules_res = client.get("/api/brand-vault/rules")
    assert rules_res.status_code == 200
    rules = rules_res.json()
    assert len(rules) >= 4

    # Facts
    facts_res = client.get("/api/brand-vault/facts")
    assert facts_res.status_code == 200
    facts = facts_res.json()
    assert any("₹399" in f["approved_value"] for f in facts)

    # Claims
    claims_res = client.get("/api/brand-vault/claims")
    assert claims_res.status_code == 200
    claims = claims_res.json()
    assert any(c["claim_code"] == "CLAIM-002" for c in claims)

    # Glossary
    gloss_res = client.get("/api/brand-vault/glossary")
    assert gloss_res.status_code == 200
    gloss = gloss_res.json()
    assert any(g["term"].lower() == "guaranteed returns" for g in gloss)

# 3. Rule evaluation
def test_3_rule_evaluation():
    # Submit text with prohibited term and hyperbolic punctuation
    payload = {
        "title": "Rule Evaluation Test",
        "content_type": "SOCIAL_MEDIA",
        "raw_text": "Hey folks!!! NexaPay is 100% secure and guarantees returns."
    }
    res = client.post("/api/submissions", json=payload)
    assert res.status_code == 200
    sub = res.json()
    latest_review = sub["versions"][-1]["reviews"][-1]
    findings = latest_review["findings"]
    assert len(findings) >= 2
    # Verify categories
    categories = [f["category"] for f in findings]
    assert "TERMINOLOGY" in categories or "CLAIMS" in categories

# 4. Fact verification
def test_4_fact_verification():
    # Submit incorrect fee ₹299
    payload = {
        "title": "Fact Accuracy Test",
        "content_type": "ADVERTISEMENT",
        "raw_text": "Sign up today with our transaction fee of ₹299."
    }
    res = client.post("/api/submissions", json=payload)
    assert res.status_code == 200
    sub = res.json()
    findings = sub["versions"][-1]["reviews"][-1]["findings"]
    fact_findings = [f for f in findings if f["category"] == "FACT_ACCURACY"]
    assert len(fact_findings) >= 1
    assert "₹299" in fact_findings[0]["what_went_wrong"]
    assert "₹399" in fact_findings[0]["supporting_evidence"]

# 5. Unsupported claim detection
def test_5_unsupported_claim_detection():
    payload = {
        "title": "Unsupported Claim Test",
        "content_type": "MARKETING_COPY",
        "raw_text": "NexaPay is India's safest payment platform for online commerce."
    }
    res = client.post("/api/submissions", json=payload)
    assert res.status_code == 200
    sub = res.json()
    findings = sub["versions"][-1]["reviews"][-1]["findings"]
    unsupported = [f for f in findings if f["classification"] == "UNSUPPORTED_BY_EVIDENCE"]
    assert len(unsupported) >= 1
    assert "CLAIM-002" in unsupported[0]["supporting_evidence"] or "safest" in unsupported[0]["what_went_wrong"].lower()

# 6. PDF extraction
def test_6_pdf_extraction():
    fixture_path = Path(__file__).parent / "fixtures" / "scenario_b_brochure.pdf"
    assert fixture_path.exists()
    text = extract_text_from_pdf(str(fixture_path))
    assert "NexaPay Enterprise Payment Brochure" in text
    assert "499" in text
    assert "399" in text

# 7. DOCX extraction
def test_7_docx_extraction():
    fixture_path = Path(__file__).parent / "fixtures" / "sample_policy.docx"
    assert fixture_path.exists()
    text = extract_text_from_docx(str(fixture_path))
    assert "NexaPay Internal Communication Draft" in text
    assert "insane" in text

# 8. Review creation
def test_8_review_creation():
    payload = {
        "title": "Scenario A Review Test",
        "content_type": "ADVERTISEMENT",
        "raw_text": "NexaPay is India's safest payment platform for everyday payments. Get started today with our amazing ₹299 transaction fee. Guaranteed secure transactions for everyone!"
    }
    res = client.post("/api/submissions", json=payload)
    assert res.status_code == 200
    sub = res.json()
    sub_id = sub["id"]
    version = sub["versions"][0]
    review = version["reviews"][0]
    assert review["status"] == "COMPLETED"
    assert review["findings_count"] >= 3
    assert review["critical_count"] >= 2

# 9. Suggested fixes
def test_9_suggested_fixes():
    subs = client.get("/api/submissions").json()
    latest_sub = subs[0]
    sub_id = latest_sub["id"]
    detail = client.get(f"/api/submissions/{sub_id}").json()
    review = detail["versions"][-1]["reviews"][-1]
    finding_with_fix = next((f for f in review["findings"] if f["fixes"]), None)
    assert finding_with_fix is not None
    fix = finding_with_fix["fixes"][0]
    assert fix["suggested_sentence"] is not None
    assert len(fix["suggested_sentence"]) > 0

# 10. Re-verification (Applying fix)
def test_10_re_verification_and_fix_application():
    # Create submission with fixable issue
    payload = {
        "title": "Fix Application Flow",
        "content_type": "SOCIAL_MEDIA",
        "raw_text": "Get started today with our amazing ₹299 transaction fee."
    }
    sub = client.post("/api/submissions", json=payload).json()
    sub_id = sub["id"]
    review = sub["versions"][0]["reviews"][0]
    fix = review["findings"][0]["fixes"][0]

    # Apply fix
    apply_res = client.post(
        f"/api/reviews/{review['id']}/fixes/{fix['id']}/apply",
        json={"fix_id": fix["id"]}
    )
    assert apply_res.status_code == 200
    updated_sub = apply_res.json()
    # Confirm version bumped to 2
    assert len(updated_sub["versions"]) == 2
    assert updated_sub["versions"][-1]["version_number"] == 2
    # Confirm new review was automatically run on version 2
    assert len(updated_sub["versions"][-1]["reviews"]) == 1

# 11. Approval workflow
def test_11_approval_workflow():
    payload = {
        "title": "Workflow Test Submission",
        "content_type": "PRESS_RELEASE",
        "raw_text": "NexaPay provides digital payments for enterprises across India."
    }
    sub = client.post("/api/submissions", json=payload).json()
    sub_id = sub["id"]

    # Submit for review
    submit_res = client.post(f"/api/approvals/{sub_id}/submit")
    assert submit_res.status_code == 200
    assert submit_res.json()["current_status"] == "UNDER_REVIEW"

    # Request changes as Reviewer
    change_res = client.post(
        f"/api/approvals/{sub_id}/request-changes",
        json={"notes": "Please verify GST disclosure wording."},
        headers={"x-user-role": "REVIEWER"}
    )
    assert change_res.status_code == 200
    assert change_res.json()["current_status"] == "CHANGES_REQUESTED"

    # Approve as Reviewer
    appr_res = client.post(
        f"/api/approvals/{sub_id}/approve",
        json={"notes": "Approved for final distribution."},
        headers={"x-user-role": "REVIEWER"}
    )
    assert appr_res.status_code == 200
    appr_data = appr_res.json()
    assert appr_data["status"] == "APPROVED"
    assert appr_data["signature"] is not None

# 12. SHA-256 canonical hashing
def test_12_sha256_canonical_hashing():
    text1 = "NexaPay   is secure.  \r\n"
    text2 = "NexaPay   is secure."
    hash1 = compute_sha256(text1)
    hash2 = compute_sha256(text2)
    assert hash1 == hash2
    assert len(hash1) == 64

# 13. Ed25519 digital signature generation and verification
def test_13_ed25519_signature():
    content = "NexaPay standard transaction fee is ₹399."
    sub_id = "test-sub-123"
    ver_num = 1
    reviewer = "Sanchita Sharma"
    now_iso = "2026-11-05T12:00:00"

    signed_payload = sign_approval_payload(
        submission_id=sub_id,
        version_number=ver_num,
        raw_content=content,
        reviewer_name=reviewer,
        approved_at_iso=now_iso
    )
    assert "signature_b64" in signed_payload
    assert "public_key_b64" in signed_payload

    # Verify signature
    verify_res = verify_approval_signature(
        submission_id=sub_id,
        version_number=ver_num,
        raw_content=content,
        reviewer_name=reviewer,
        approved_at_iso=now_iso,
        signature_b64=signed_payload["signature_b64"],
        public_key_b64=signed_payload["public_key_b64"]
    )
    assert verify_res["is_valid"] is True
    assert verify_res["hash_matches"] is True

# 14. Tampered-content rejection
def test_14_tampered_content_rejection():
    # Create submission and approve it
    payload = {
        "title": "Tamper Test Subject",
        "content_type": "GENERAL",
        "raw_text": "NexaPay standard transaction fee is ₹399."
    }
    sub = client.post("/api/submissions", json=payload).json()
    sub_id = sub["id"]

    client.post(
        f"/api/approvals/{sub_id}/approve",
        json={"notes": "Approved"},
        headers={"x-user-role": "REVIEWER"}
    )

    # Run tamper test endpoint
    tamper_res = client.post(f"/api/releases/{sub_id}/tamper-test")
    assert tamper_res.status_code == 200
    t_data = tamper_res.json()
    assert t_data["status"] == "BLOCKED"
    assert t_data["verification_result"]["hash_matches"] is False
    assert "Tampering detected" in t_data["verification_result"]["message"]

# 15. Role-based permissions
def test_15_role_based_permissions():
    payload = {
        "title": "Permission Check",
        "content_type": "GENERAL",
        "raw_text": "Sample text."
    }
    sub = client.post("/api/submissions", json=payload).json()
    sub_id = sub["id"]

    # Attempt to approve as CREATOR -> Expect 403 Forbidden
    res = client.post(
        f"/api/approvals/{sub_id}/approve",
        json={"notes": "Illegal Creator self-approval"},
        headers={"x-user-role": "CREATOR"}
    )
    assert res.status_code == 403
    assert "Only authorized Reviewers" in res.json()["detail"]
