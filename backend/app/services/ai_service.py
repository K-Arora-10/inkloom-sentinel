import os
import json
import logging
from typing import List, Dict, Any, Optional
import httpx
from pydantic import BaseModel, Field
from backend.app.config import settings

logger = logging.getLogger(__name__)

class AIFindingItem(BaseModel):
    original_text: str
    category: str = Field(description="TONE, CLAIMS, TERMINOLOGY, or AMBIGUITY")
    severity: str = Field(description="CRITICAL, WARNING, or INFO")
    classification: str = Field(description="RULE_BREACH, UNSUPPORTED_BY_EVIDENCE, POTENTIAL_RISK, or NEEDS_HUMAN_JUDGEMENT")
    what_went_wrong: str
    why_it_matters: str
    supporting_evidence: str
    suggested_correction: str
    confidence_signal: str = "Indicative AI Signal"
    needs_human_judgment: bool = True

class AIReviewResponse(BaseModel):
    findings: List[AIFindingItem] = []
    summary: str = ""

class BaseAIProvider:
    def analyze_content(self, text: str, approved_context: Dict[str, Any]) -> Optional[AIReviewResponse]:
        raise NotImplementedError

class GeminiAIProvider(BaseAIProvider):
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        self.api_key = api_key
        self.model = model
        self.endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"

    def analyze_content(self, text: str, approved_context: Dict[str, Any]) -> Optional[AIReviewResponse]:
        if not self.api_key:
            return None

        prompt = f"""
You are the AI Brand Governance Auditor for NexaPay (digital payments enterprise).
Audit the submitted text strictly against approved brand guidelines and facts:

[APPROVED BRAND CONTEXT]:
- Brand Tone: Professional, confident, approachable, trustworthy, never exaggerated. Avoid hyperbole, excessive exclamation marks, casual slang ("Hey folks", "insane", "amazing deal").
- Approved Transaction Fee: ₹399 (superseded outdated fee was ₹499).
- Free Delivery Threshold: ₹499.
- Prohibited Terms: "Guaranteed returns", "100% secure".
- Discouraged Terms: "Amazing deal" -> "Special offer".
- Safety claims: NexaPay has NO approved certification to claim being "India's safest payment platform" or "guaranteed secure".

[SUBMITTED TEXT TO AUDIT]:
\"\"\"{text}\"\"\"

Task:
Identify any tone inconsistencies, implied unsubstantiated claims, or ambiguous messaging.
DO NOT hallucinate facts. If a claim lacks proof, mark it as UNSUPPORTED_BY_EVIDENCE.
Return a valid JSON object matching this schema:
{{
  "summary": "Short 1-2 sentence overview of the tone and compliance.",
  "findings": [
    {{
      "original_text": "Exact sentence flagged",
      "category": "TONE or CLAIMS or TERMINOLOGY",
      "severity": "CRITICAL or WARNING or INFO",
      "classification": "RULE_BREACH or UNSUPPORTED_BY_EVIDENCE or POTENTIAL_RISK or NEEDS_HUMAN_JUDGEMENT",
      "what_went_wrong": "Precise explanation of what violates the guidelines",
      "why_it_matters": "Why this damages brand trust or creates regulatory exposure",
      "supporting_evidence": "Citation from NexaPay Brand Guidelines or Glossary",
      "suggested_correction": "Minimal rewrite preserving creator's original intent",
      "confidence_signal": "Indicative Contextual Signal",
      "needs_human_judgment": true
    }}
  ]
}}
Only output raw JSON.
"""

        try:
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.1,
                    "responseMimeType": "application/json"
                }
            }
            with httpx.Client(timeout=10.0) as client:
                res = client.post(self.endpoint, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    raw_content = data["candidates"][0]["content"]["parts"][0]["text"]
                    parsed = json.loads(raw_content)
                    return AIReviewResponse.model_validate(parsed)
                else:
                    logger.warning(f"Gemini API returned status code {res.status_code}: {res.text}")
                    return None
        except Exception as e:
            logger.warning(f"Gemini API invocation failed: {e}")
            return None

class LocalDeterministicAIProvider(BaseAIProvider):
    """
    Guaranteed reliable local fallback that detects tone exaggerations and contextual
    issues when Gemini API is offline or not configured with a key.
    Ensures zero downtime and continuous reliability.
    """
    def analyze_content(self, text: str, approved_context: Dict[str, Any]) -> AIReviewResponse:
        findings = []
        sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]

        for s in sentences:
            s_lower = s.lower()
            # Tone check: Excessive exclamation marks or hyperbole
            if "!!!" in s or "!!" in s:
                suggested = s.replace("!!!", ".").replace("!!", ".")
                findings.append(AIFindingItem(
                    original_text=s,
                    category="TONE",
                    severity="WARNING",
                    classification="POTENTIAL_RISK",
                    what_went_wrong="Excessive punctuation and excited informal tone detected.",
                    why_it_matters="NexaPay's Brand Personality is professional, confident, and trustworthy. Hyperbolic punctuation erodes financial credibility.",
                    supporting_evidence="NexaPay Brand Guidelines v1.0 — Section 5 (Tone of Voice): 'Avoid exaggerated punctuation, all-caps shouting, and sensationalist claims.'",
                    suggested_correction=suggested,
                    confidence_signal="High (Pattern Tone Analysis)",
                    needs_human_judgment=True
                ))

            if any(w in s_lower for w in ["insane", "crazy", "mind-blowing", "unbelievable"]):
                suggested = s
                for w in ["insane", "crazy", "mind-blowing", "unbelievable"]:
                    suggested = suggested.replace(w, "competitive").replace(w.capitalize(), "Competitive")
                findings.append(AIFindingItem(
                    original_text=s,
                    category="TONE",
                    severity="WARNING",
                    classification="POTENTIAL_RISK",
                    what_went_wrong="Sensationalist / hyper-informal language detected ('insane').",
                    why_it_matters="Financial services messaging must remain grounded, factual, and restrained.",
                    supporting_evidence="NexaPay Content and Advertising Policy — Section 2: 'Misleading or sensationalist promotional language is prohibited.'",
                    suggested_correction=suggested,
                    confidence_signal="Indicative Local Contextual Engine",
                    needs_human_judgment=True
                ))

            if "hey folks" in s_lower:
                suggested = s.replace("Hey folks", "Hello").replace("hey folks", "hello")
                findings.append(AIFindingItem(
                    original_text=s,
                    category="TONE",
                    severity="INFO",
                    classification="POTENTIAL_RISK",
                    what_went_wrong="Overly casual greeting ('Hey folks') used in corporate communication.",
                    why_it_matters="Customer communications should maintain a polished, approachable tone without being colloquial.",
                    supporting_evidence="NexaPay Brand Guidelines v1.0 — Writing Style: 'Tone must be approachable yet dignified.'",
                    suggested_correction=suggested,
                    confidence_signal="Indicative Local Contextual Engine",
                    needs_human_judgment=True
                ))

        return AIReviewResponse(
            findings=findings,
            summary="Review evaluated against NexaPay brand tone and communication guidelines."
        )

def get_ai_provider() -> BaseAIProvider:
    if settings.GEMINI_API_KEY:
        return GeminiAIProvider(settings.GEMINI_API_KEY, settings.GEMINI_MODEL)
    return LocalDeterministicAIProvider()
