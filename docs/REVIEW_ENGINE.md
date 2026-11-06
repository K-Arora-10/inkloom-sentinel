# REVIEW ENGINE PIPELINE — INKLOOM SENTINEL

Inkloom Sentinel's review engine is a 5-stage pipeline designed to eliminate hallucinations, enforce hard business rules, and provide explainable evidence citations.

## Stage 1: Content Extraction & Sentence Offsets
- Parses raw text, PDF (PyMuPDF), or DOCX (python-docx).
- Normalizes character encodings and line endings.
- Segments text into discrete sentences with `start_char` and `end_char` offsets.

## Stage 2: Deterministic Rule Evaluation
- Queries active `BrandRule` and `GlossaryTerm` tables from the database.
- Evaluates regex patterns against every sentence:
  - Prohibited terminology: Identifies terms like "Guaranteed returns", "100% secure".
  - Discouraged terminology: Replaces sensationalist words ("Amazing deal" -> "Special offer").
  - Absolute superlatives: Flags unsupported claims like "India's safest payment platform".
  - Tone patterns: Flags exclamation clusters ("!!!") and casual slang ("Hey folks").
  - Numerical pricing: Extracts currency values and verifies them against the `ApprovedFact` table (detecting outdated ₹499 fees or fictional ₹299 fees vs approved ₹399).

## Stage 3: Approved-Source Retrieval
- Matches candidate statements against current active facts, historical facts, and Claim Passports.
- Excludes expired and superseded records from active approval decisions, but cites them to explain why a statement is outdated.

## Stage 4: AI Contextual Analysis (Provider Abstraction)
- Uses Google Gemini API when configured (`GEMINI_API_KEY`).
- Injects grounded approved context into Gemini system instructions.
- Validates structured JSON response with Pydantic (`AIReviewResponse`).
- **Local Fallback Engine:** If the Gemini API is unconfigured or times out, the local deterministic contextual engine continues evaluation without failure. Never fabricates AI responses.

## Stage 5: Finding Explanations & Evidence Linking
Every finding generates:
1. What went wrong (precise violation description).
2. Why it matters (regulatory/brand damage explanation).
3. Supporting evidence citation (exact reference to Brand Vault document, rule code, or fact ID).
4. Suggested minimal fix (preserving creator intent while complying with guidelines).
5. Confidence signal (e.g., "High (Deterministic Match)").
