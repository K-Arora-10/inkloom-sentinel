# DATABASE SCHEMA — INKLOOM SENTINEL

The relational schema implements 19 tables in PostgreSQL/SQLite:

1. `organisations`: Multi-tenant organization boundaries (`id`, `name`, `code`, `description`).
2. `users`: System personas (`id`, `name`, `email`, `role` [CREATOR, REVIEWER, ADMIN]).
3. `documents`: Brand Vault documents (`id`, `title`, `doc_type`, `category`, `current_version`, `status`).
4. `document_versions`: Full content revisions (`id`, `document_id`, `version_number`, `content`, `extracted_text`).
5. `brand_rules`: Active deterministic rules (`id`, `rule_code`, `category`, `severity`, `pattern`, `replacement`).
6. `glossary_terms`: Controlled vocabulary (`id`, `term`, `status` [APPROVED, PROHIBITED, DISCOURAGED], `preferred_alternative`).
7. `approved_facts`: Certified single source of truth (`id`, `fact_code`, `approved_value`, `supporting_source`, `status`, `is_historical`).
8. `claim_passports`: Public statements audit registry (`id`, `claim_code`, `claim_text`, `evidence`, `approval_status`).
9. `submissions`: Content drafts and releases (`id`, `title`, `content_type`, `current_status`).
10. `submission_versions`: Content versions (`id`, `submission_id`, `version_number`, `raw_text`, `content_hash`).
11. `reviews`: Review run records (`id`, `submission_version_id`, `status`, `findings_count`, `critical_count`).
12. `findings`: Detailed audit findings (`id`, `review_id`, `rule_code`, `what_went_wrong`, `why_it_matters`, `supporting_evidence`, `suggested_correction`).
13. `evidence_references`: Citations linked to Brand Vault (`id`, `finding_id`, `source_type`, `title`, `snippet`).
14. `suggested_fixes`: Minimal suggested replacements (`id`, `finding_id`, `original_sentence`, `suggested_sentence`, `status`).
15. `comments`: Threaded governance notes (`id`, `submission_id`, `author_name`, `comment_text`).
16. `approvals`: Human sign-off decisions (`id`, `submission_id`, `reviewer_name`, `status`, `decision_notes`).
17. `approval_signatures`: Cryptographic seal manifests (`id`, `approval_id`, `canonical_content`, `content_sha256`, `signature_b64`, `public_key_b64`).
18. `audit_logs`: Immutable action trail (`id`, `action`, `actor_name`, `target_type`, `target_id`, `details`, `timestamp`).
19. `assets`: Visual assets and SVG brand specifications (`id`, `name`, `asset_type`, `svg_content`).
