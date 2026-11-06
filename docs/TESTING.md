# TESTING & QUALITY ASSURANCE — INKLOOM SENTINEL

The test suite validates the 15 required core criteria using `pytest`:

```bash
python -m pytest backend/tests/test_backend.py -v
```

## The 15 Automated Test Cases
1. `test_1_health_endpoint`: Validates health status, database connectivity, and cryptographic engine readiness.
2. `test_2_brand_vault_retrieval`: Asserts that all 7 brand documents, rules, facts, claims, and glossary terms are retrieved.
3. `test_3_rule_evaluation`: Evaluates deterministic matching on prohibited terms and punctuation.
4. `test_4_fact_verification`: Confirms that incorrect fees (e.g. ₹299) are flagged against approved fee ₹399.
5. `test_5_unsupported_claim_detection`: Verifies detection of unsupported superlative claims (CLAIM-002 "safest").
6. `test_6_pdf_extraction`: Tests PyMuPDF extraction on actual PDF brochure test fixture.
7. `test_7_docx_extraction`: Tests python-docx extraction on actual DOCX communication draft test fixture.
8. `test_8_review_creation`: Validates multi-stage review execution and finding count generation.
9. `test_9_suggested_fixes`: Confirms Fix Assistant generates minimal replacements.
10. `test_10_re_verification_and_fix_application`: Verifies fix acceptance, automatic content modification, version bump (v1 -> v2), and re-verification.
11. `test_11_approval_workflow`: Validates state transitions (Draft -> Under Review -> Changes Requested -> Approved).
12. `test_12_sha256_canonical_hashing`: Tests canonical normalization and SHA-256 hash invariance.
13. `test_13_ed25519_signature`: Tests asymmetric keypair signing and verification over the canonical manifest.
14. `test_14_tampered_content_rejection`: Demonstrates that altering even a single character causes cryptographic verification failure and blocks publication.
15. `test_15_role_based_permissions`: Enforces server-side permission checks (Creators cannot self-approve, Reviewers can approve).
