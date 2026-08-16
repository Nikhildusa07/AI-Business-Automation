def make_decision(priority: str, confidence_score: float):

    priority = priority.upper()

    # Low AI confidence → Human Review
    if confidence_score < 0.70:
        return {
            "decision": "ESCALATE",
            "action": "HUMAN_REVIEW",
            "reason": "AI confidence is below the required threshold."
        }

    # High priority → Human Review
    if priority == "HIGH":
        return {
            "decision": "ESCALATE",
            "action": "HUMAN_REVIEW",
            "reason": "High-priority request requires human attention."
        }

    # Medium priority → Customer Follow-Up
    if priority == "MEDIUM":
        return {
            "decision": "FOLLOW_UP",
            "action": "CUSTOMER_FOLLOW_UP",
            "reason": "Medium-priority request requires follow-up."
        }

    # Low priority → Automated Response
    return {
        "decision": "AUTO_PROCESS",
        "action": "AUTOMATED_RESPONSE",
        "reason": "Low-priority request can be processed automatically."
    }