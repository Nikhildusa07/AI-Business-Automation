import json
import os
import time

from typing import Any, Dict

from dotenv import load_dotenv
from google import genai


load_dotenv()


# =========================================================
# AVAILABLE BUSINESS TOOLS
# =========================================================

TOOLS = {

    "business_hours":
        "Retrieve official business operating hours.",

    "payment_support":
        "Retrieve payment/refund support information.",

    "profile_support":
        "Retrieve routine customer profile support information.",

    "general_support":
        "Retrieve general business support information.",
}


# =========================================================
# GEMINI CLIENT
# =========================================================

def _client():

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    return genai.Client(
        api_key=api_key
    )


# =========================================================
# DETERMINISTIC TOOL SELECTION
# =========================================================

def _fallback_tool_selection(
    input_text: str,
    intent: str
) -> Dict[str, Any]:

    lower = (
        f"{input_text} {intent}"
    ).lower()

    # -----------------------------------------------------
    # BUSINESS HOURS
    # -----------------------------------------------------

    if any(
        word in lower
        for word in (
            "hour",
            "hours",
            "open",
            "close",
            "opening",
            "closing",
            "operating",
            "working hours",
        )
    ):

        return {
            "tool": "business_hours",
            "reason": (
                "Request contains business-hours "
                "or operating-time information."
            ),
            "fallback": True,
        }

    # -----------------------------------------------------
    # PAYMENT SUPPORT
    # -----------------------------------------------------

    if any(
        word in lower
        for word in (
            "payment",
            "refund",
            "charge",
            "charged",
            "billing",
            "invoice",
            "transaction",
            "money",
        )
    ):

        return {
            "tool": "payment_support",
            "reason": (
                "Request relates to payment, "
                "billing, transaction, or refund support."
            ),
            "fallback": True,
        }

    # -----------------------------------------------------
    # PROFILE SUPPORT
    # -----------------------------------------------------

    if any(
        word in lower
        for word in (
            "profile",
            "account",
            "address",
            "email",
            "phone",
            "name",
            "update my",
            "change my",
            "subscription",
            "plan",
        )
    ):

        return {
            "tool": "profile_support",
            "reason": (
                "Request relates to customer profile, "
                "account, or subscription information."
            ),
            "fallback": True,
        }

    # -----------------------------------------------------
    # GENERAL SUPPORT
    # -----------------------------------------------------

    return {
        "tool": "general_support",
        "reason": (
            "Request does not match a specialized "
            "business tool, so general support was selected."
        ),
        "fallback": True,
    }


# =========================================================
# TOOL SELECTION
# =========================================================

def select_tool(
    input_text: str,
    intent: str
) -> Dict[str, Any]:

    """
    AI agent selects the most appropriate internal
    business tool/API.

    Gemini is attempted ONCE.

    If Gemini is unavailable or quota exhausted,
    deterministic tool selection is used.
    """

    prompt = f"""
You are the tool-selection agent
in a business operations automation system.

Available tools:

{json.dumps(TOOLS, indent=2)}

Request:

{input_text}

Detected intent:

{intent}

Select the most appropriate tool.

Return ONLY valid JSON:

{{
    "tool":
        "business_hours|payment_support|profile_support|general_support",

    "reason":
        "short reason for selecting the tool"
}}
"""

    try:

        response = _client().models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        text = response.text.strip()

        if text.startswith("```"):

            text = (
                text
                .replace(
                    "```json",
                    "",
                    1
                )
                .replace(
                    "```",
                    ""
                )
                .strip()
            )

        result = json.loads(
            text
        )

        tool = result.get(
            "tool"
        )

        if tool not in TOOLS:

            raise ValueError(
                "Agent selected an unsupported tool."
            )

        return {

            "tool": tool,

            "reason": str(
                result.get(
                    "reason",
                    "Tool selected by AI agent."
                )
            ),

            "fallback": False,
        }

    except Exception as exc:

        error_text = str(exc)

        if (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
            or "quota" in error_text.lower()
            or "rate limit" in error_text.lower()
        ):

            print(
                "Gemini agent quota exhausted. "
                "Using deterministic tool selection."
            )

        else:

            print(
                f"AI tool selection unavailable: {error_text}"
            )

        fallback = _fallback_tool_selection(
            input_text,
            intent
        )

        fallback["fallback_reason"] = error_text

        return fallback


# =========================================================
# DATA RETRIEVAL
# =========================================================

def retrieve_data(
    tool: str,
    request_text: str
) -> Dict[str, Any]:

    """
    Execute the selected business tool
    and retrieve relevant business data.
    """

    data = {

        "business_hours": {

            "source":
                "Business Operations Knowledge Base",

            "data":
                "Monday-Friday 9:00 AM-6:00 PM; "
                "Saturday 10:00 AM-2:00 PM; "
                "Sunday closed.",
        },

        "payment_support": {

            "source":
                "Payment Support Policy",

            "data":
                "Payment/refund issues require "
                "verification of the transaction "
                "and may require human review.",
        },

        "profile_support": {

            "source":
                "Customer Profile Service",

            "data":
                "Routine profile updates can be "
                "handled automatically after "
                "customer verification.",
        },

        "general_support": {

            "source":
                "Business Support Knowledge Base",

            "data":
                "General requests are routed "
                "according to priority and "
                "AI confidence.",
        },
    }

    if tool not in data:

        raise ValueError(
            f"Unsupported tool: {tool}"
        )

    return data[tool]


# =========================================================
# AI REASONING
# =========================================================

def reason_about_result(
    input_text: str,
    analysis: Dict[str, Any],
    retrieved: Dict[str, Any]
) -> Dict[str, Any]:

    """
    Reason about the retrieved information
    before executing the final action.
    """

    priority = str(
        analysis.get(
            "priority",
            "LOW"
        )
    ).upper()

    confidence = float(
        analysis.get(
            "confidence_score",
            0.0
        )
    )

    # -----------------------------------------------------
    # LOW CONFIDENCE
    # -----------------------------------------------------

    if confidence < 0.70:

        next_step = (
            "Human review because AI "
            "confidence is below the threshold."
        )

    # -----------------------------------------------------
    # HIGH PRIORITY
    # -----------------------------------------------------

    elif priority == "HIGH":

        next_step = (
            "Human review because the "
            "request is high priority."
        )

    # -----------------------------------------------------
    # MEDIUM PRIORITY
    # -----------------------------------------------------

    elif priority == "MEDIUM":

        next_step = (
            "Customer follow-up is required."
        )

    # -----------------------------------------------------
    # LOW PRIORITY
    # -----------------------------------------------------

    else:

        next_step = (
            "Automated response is appropriate "
            "for this routine request."
        )

    return {

        "reasoning": (

            f"Retrieved data from "
            f"{retrieved['source']}. "

            f"The request was classified as "
            f"{priority} with confidence "
            f"{confidence:.2f}. "

            f"{next_step}"
        ),

        "next_step": next_step,
    }


# =========================================================
# COMPLETE AI AGENT WORKFLOW
# =========================================================

def run_agent_workflow(
    input_text: str,
    analysis: Dict[str, Any]
) -> Dict[str, Any]:

    """
    Complete multi-step AI-agent workflow:

    Request
        ↓
    Tool Selection
        ↓
    Data Retrieval
        ↓
    AI Reasoning
        ↓
    Verification Ready

    Gemini failures do not destroy the workflow.
    """

    # -----------------------------------------------------
    # 1. TOOL SELECTION
    # -----------------------------------------------------

    selected = select_tool(
        input_text,
        analysis.get(
            "intent",
            "General Business Request"
        )
    )

    # -----------------------------------------------------
    # 2. DATA RETRIEVAL
    # -----------------------------------------------------

    retrieved = retrieve_data(
        selected["tool"],
        input_text
    )

    # -----------------------------------------------------
    # 3. AI / RULE-BASED REASONING
    # -----------------------------------------------------

    reasoning = reason_about_result(
        input_text,
        analysis,
        retrieved
    )

    # -----------------------------------------------------
    # 4. VERIFICATION
    # -----------------------------------------------------

    verification = {

        "status": "READY",

        "message":
            "Tool selection, data retrieval, "
            "and reasoning completed before "
            "action execution.",
    }

    # -----------------------------------------------------
    # 5. RETURN COMPLETE WORKFLOW
    # -----------------------------------------------------

    return {

        "status": "SUCCESS",

        "tool_selection": selected,

        "data_retrieval": retrieved,

        "reasoning": reasoning,

        "verification": verification,
    }