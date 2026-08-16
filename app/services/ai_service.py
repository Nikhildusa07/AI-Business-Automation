import os
import json
from typing import Dict, Any

from dotenv import load_dotenv
from google import genai


load_dotenv()


# =========================================================
# GEMINI CLIENT
# =========================================================

def _get_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    return genai.Client(api_key=api_key)


# =========================================================
# CLEAN JSON RESPONSE
# =========================================================

def _clean_json(text: str) -> str:
    text = text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "", 1)
        text = text.replace("```", "")
        text = text.strip()

    return text


# =========================================================
# LOCAL FALLBACK ANALYSIS
# =========================================================

def _fallback_analysis(input_text: str) -> Dict[str, Any]:
    """
    Deterministic fallback used when Gemini is unavailable.

    This prevents the entire business workflow from stopping
    because of an external AI quota/API problem.
    """

    text = input_text.lower().strip()

    # -----------------------------------------------------
    # HIGH PRIORITY
    # -----------------------------------------------------

    high_keywords = [
        "hacked",
        "fraud",
        "fraudulent",
        "unauthorized transaction",
        "unauthorized payment",
        "account compromised",
        "security breach",
        "data breach",
        "double charged",
        "charged twice",
        "money deducted",
        "money stolen",
        "payment failed",
        "payment failure",
        "refund not received",
        "urgent refund",
        "service down",
        "system down",
        "cannot access account",
        "account locked",
        "critical",
        "emergency",
    ]

    if any(keyword in text for keyword in high_keywords):

        if any(
            keyword in text
            for keyword in [
                "refund",
                "charged",
                "charge",
                "payment",
                "money",
                "transaction",
            ]
        ):
            intent = "Payment Issue / Refund Request"

        elif any(
            keyword in text
            for keyword in [
                "hacked",
                "fraud",
                "security",
                "compromised",
            ]
        ):
            intent = "Security / Account Issue"

        else:
            intent = "Critical Support Request"

        return {
            "intent": intent,
            "priority": "HIGH",
            "confidence_score": 0.92,
            "summary": (
                "The request requires urgent attention due to "
                "a potentially critical business or customer issue."
            ),
            "analysis_source": "LOCAL_FALLBACK",
        }

    # -----------------------------------------------------
    # MEDIUM PRIORITY
    # -----------------------------------------------------

    medium_keywords = [
        "subscription",
        "plan",
        "upgrade",
        "downgrade",
        "billing",
        "invoice",
        "profile",
        "account update",
        "change email",
        "change phone",
        "change address",
        "update account",
        "cancel subscription",
        "renewal",
        "payment method",
        "customer support",
        "follow up",
        "follow-up",
    ]

    if any(keyword in text for keyword in medium_keywords):

        if any(
            keyword in text
            for keyword in [
                "subscription",
                "plan",
                "upgrade",
                "downgrade",
                "renewal",
                "cancel subscription",
            ]
        ):
            intent = "Subscription Plan Management"

        elif any(
            keyword in text
            for keyword in [
                "profile",
                "account update",
                "change email",
                "change phone",
                "change address",
                "update account",
            ]
        ):
            intent = "Profile Update"

        elif any(
            keyword in text
            for keyword in [
                "billing",
                "invoice",
                "payment method",
            ]
        ):
            intent = "Billing Support"

        else:
            intent = "Customer Support Request"

        return {
            "intent": intent,
            "priority": "MEDIUM",
            "confidence_score": 0.88,
            "summary": (
                "The request requires normal customer-support "
                "processing and follow-up."
            ),
            "analysis_source": "LOCAL_FALLBACK",
        }

    # -----------------------------------------------------
    # LOW PRIORITY
    # -----------------------------------------------------

    low_keywords = [
        "business hours",
        "business hour",
        "opening hours",
        "opening time",
        "closing time",
        "when are you open",
        "when do you open",
        "when do you close",
        "working hours",
        "operating hours",
        "location",
        "where are you located",
        "general information",
        "information request",
        "hello",
        "hi",
        "help",
    ]

    if any(keyword in text for keyword in low_keywords):

        if any(
            keyword in text
            for keyword in [
                "hour",
                "open",
                "close",
                "working",
                "operating",
            ]
        ):
            intent = "Business Hours Inquiry"
        else:
            intent = "General Information Request"

        return {
            "intent": intent,
            "priority": "LOW",
            "confidence_score": 0.90,
            "summary": (
                "The request is a routine informational enquiry "
                "that can normally be handled automatically."
            ),
            "analysis_source": "LOCAL_FALLBACK",
        }

    # -----------------------------------------------------
    # DEFAULT
    # -----------------------------------------------------

    return {
        "intent": "General Business Request",
        "priority": "LOW",
        "confidence_score": 0.75,
        "summary": (
            "The request appears to be a routine business enquiry "
            "that can be processed through the standard workflow."
        ),
        "analysis_source": "LOCAL_FALLBACK",
    }


# =========================================================
# AI ANALYSIS
# =========================================================

def analyze_request(input_text: str) -> Dict[str, Any]:
    """
    Analyze a business request using Gemini.

    If Gemini is unavailable, rate-limited, or returns invalid
    data, the system safely falls back to deterministic analysis.

    IMPORTANT:
    We intentionally DO NOT retry 429 quota errors.
    Retrying a quota-exhausted request only creates more failures.
    """

    if not input_text or not input_text.strip():
        raise ValueError("Business request cannot be empty.")

    prompt = f"""
You are an AI business operations assistant.

Analyze the following business request.

Return ONLY valid JSON.

Required JSON structure:

{{
    "intent": "short classification of the request",
    "priority": "HIGH, MEDIUM, or LOW",
    "confidence_score": 0.0,
    "summary": "short summary of the request"
}}

Priority rules:

HIGH:
- Fraud
- Unauthorized transactions
- Security problems
- Critical payment problems
- Account compromise
- Urgent operational failures

MEDIUM:
- Subscription changes
- Profile/account updates
- Billing questions
- Normal customer support
- Refund requests that are not clearly urgent

LOW:
- Business hours
- General information
- Routine enquiries

Business request:

{input_text}
"""

    try:

        client = _get_client()

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        result_text = response.text.strip()

        result_text = _clean_json(result_text)

        result = json.loads(result_text)

        # -------------------------------------------------
        # VALIDATE RESULT
        # -------------------------------------------------

        intent = str(
            result.get(
                "intent",
                "General Business Request"
            )
        ).strip()

        priority = str(
            result.get(
                "priority",
                "LOW"
            )
        ).upper().strip()

        confidence = float(
            result.get(
                "confidence_score",
                0.75
            )
        )

        summary = str(
            result.get(
                "summary",
                "Business request analyzed successfully."
            )
        ).strip()

        # -------------------------------------------------
        # NORMALIZE PRIORITY
        # -------------------------------------------------

        if priority not in {
            "HIGH",
            "MEDIUM",
            "LOW"
        }:
            priority = "LOW"

        # -------------------------------------------------
        # NORMALIZE CONFIDENCE
        # -------------------------------------------------

        confidence = max(
            0.0,
            min(
                1.0,
                confidence
            )
        )

        return {
            "intent": intent,
            "priority": priority,
            "confidence_score": confidence,
            "summary": summary,
            "analysis_source": "GEMINI",
        }

    except Exception as exc:

        error_text = str(exc)

        # -------------------------------------------------
        # 429 / QUOTA ERROR
        # -------------------------------------------------

        is_quota_error = (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
            or "quota" in error_text.lower()
            or "rate limit" in error_text.lower()
        )

        if is_quota_error:

            print(
                "Gemini quota exhausted. "
                "Using deterministic local analysis fallback."
            )

        else:

            print(
                f"Gemini analysis unavailable: {error_text}"
            )

        # -------------------------------------------------
        # SAFE FALLBACK
        # -------------------------------------------------

        fallback = _fallback_analysis(input_text)

        fallback["fallback_reason"] = (
            "Gemini quota/API unavailable; "
            "local deterministic analysis was used."
        )

        return fallback