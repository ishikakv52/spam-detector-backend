"""
Gemini integration — the only place in the backend that talks to Google's AI.
Kept deliberately simple: one prompt, one JSON response, no chat history,
no fine-tuning, no custom ML.
"""
import json
import logging

from google import genai
from django.conf import settings

from .constants import Category

logger = logging.getLogger(__name__)

ANALYSIS_PROMPT = """You are a spam-detection assistant. Analyze the following message and
decide whether it is SPAM or NOT SPAM.

Message:
\"\"\"{message}\"\"\"

Respond with ONLY a raw JSON object (no markdown, no code fences, no extra text) in exactly
this shape:

{{
  "classification": "spam" or "not_spam",
  "category": one of {categories},
  "explanation": "short 1-2 sentence explanation of why",
  "suspicious_indicators": ["short phrase", "short phrase"],
  "safety_suggestion": "one short practical safety tip for the user"
}}

Rules:
- "suspicious_indicators" should be an empty list if the message is not spam and has none.
- Never claim 100% certainty in the explanation — this is an assistive classification, not a guarantee.
- Keep "explanation" and "safety_suggestion" short and in plain English.
"""


class GeminiAnalysisError(Exception):
    """Raised when Gemini cannot be reached or returns something unusable."""


def _get_client():
    if not settings.GEMINI_API_KEY:
        raise GeminiAnalysisError("GEMINI_API_KEY is not configured on the server.")
    return genai.Client(api_key=settings.GEMINI_API_KEY)


def _fallback_category(raw_category: str) -> str:
    raw_category = (raw_category or "").strip().lower().replace(" ", "_").replace("/", "_")
    return raw_category if raw_category in Category.VALID_VALUES else Category.OTHER


def analyze_message(message_text: str) -> dict:
    """
    Sends `message_text` to Gemini and returns a normalized dict:
    {classification, category, explanation, suspicious_indicators, safety_suggestion}
    Raises GeminiAnalysisError on any failure so the view can turn it into a clean 502.
    """
    client = _get_client()
    prompt = ANALYSIS_PROMPT.format(
        message=message_text,
        categories=[c[0] for c in Category.CHOICES],
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        raw_text = (response.text or "").strip()
    except Exception as exc:  # network errors, quota errors, etc.
        logger.exception("Gemini API call failed")
        raise GeminiAnalysisError("Could not reach the AI analysis service.") from exc

    # Gemini sometimes wraps JSON in ```json fences despite instructions — strip them.
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.replace("json\n", "", 1).replace("json", "", 1)

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        logger.error("Gemini returned non-JSON response: %s", raw_text)
        raise GeminiAnalysisError("The AI service returned an unexpected response.") from exc

    classification = "spam" if str(data.get("classification", "")).lower().startswith("spam") else "not_spam"
    indicators = data.get("suspicious_indicators") or []
    if not isinstance(indicators, list):
        indicators = [str(indicators)]

    return {
        "classification": classification,
        "category": _fallback_category(data.get("category", "")),
        "explanation": str(data.get("explanation", "")).strip(),
        "suspicious_indicators": [str(i).strip() for i in indicators if str(i).strip()],
        "safety_suggestion": str(data.get("safety_suggestion", "")).strip(),
    }
