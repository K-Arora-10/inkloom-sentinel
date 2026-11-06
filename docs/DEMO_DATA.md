# DEMO DATA & NEXAPAY CONTEXT — INKLOOM SENTINEL

> **DISCLOSURE:** NexaPay is a fictional digital payments organization created as a synthetic demonstration environment for CodeNexus India 2026. All facts, documents, and pricing parameters are synthetic.

## The 7 NexaPay Brand Documents
1. **Brand Guidelines v1.0:** Identity, mission, audience, tone of voice, writing style, acceptable and prohibited content examples.
2. **Brand Glossary:** Controlled terminology table (Guaranteed returns -> Prohibited, 100% secure -> Prohibited, Amazing deal -> Discouraged, etc.).
3. **Approved Facts Register:** Certified single source of truth (Domain: Digital payments, Active Fee: ₹399, Historical Fee: ₹499 superseded, Delivery threshold: ₹499).
4. **Claim Passports Register:** Audit registry of public promotional claims (CLAIM-001 approved delivery, CLAIM-002 unsupported "India's safest payment platform", CLAIM-003 approved transaction fee ₹399).
5. **Visual Identity Guide:** SVG wordmark and emblem, primary colors (#405746, #F8F7F4, #242522, #E8E6DF), clear space specifications.
6. **Content and Advertising Policy:** Superlative restrictions, financial disclosures, required disclaimers, escalation rules.
7. **Historical Brand Updates:** Log of superseded parameters (₹499 fee lowered to ₹399 on 2025-10-01).

## 3 Test Scenarios Built into the UI
- **Scenario A: Social Media Ad**
  - Input: *"NexaPay is India's safest payment platform for everyday payments. Get started today with our amazing ₹299 transaction fee. Guaranteed secure transactions for everyone!"*
  - Flags: Unsupported superlative, incorrect fee (₹299 vs approved ₹399), prohibited guarantee ("Guaranteed secure"), discouraged wording ("amazing").
- **Scenario B: Product Brochure**
  - Input: *"Historical notice: Standard transaction fee was previously INR 499 (superseded). Under our revised pricing schedule, the active transaction fee is INR 399. NexaPay is India's safest payment platform for high volume checkout."*
  - Flags: Outdated ₹499 fee citation, fee conflict, unsupported superlative claim.
- **Scenario C: Brand Communication**
  - Input: *"Hey folks!!! Our deal is absolutely insane. NexaPay is 100% secure and guarantees the best payment experience in India."*
  - Flags: Informal slang ("Hey folks"), hyperbolic punctuation ("!!!"), sensationalism ("insane"), prohibited term ("100% secure"), prohibited guarantee ("guarantees the best").
