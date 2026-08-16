from app.database import SessionLocal
from app.services.automation_service import execute_action


db = SessionLocal()

try:
    result = execute_action(
        {
            "decision": "ESCALATE",
            "action": "HUMAN_REVIEW",
            "reason": "High-priority request requires human attention."
        },
        "TEST-REVIEW-001",
        db
    )

    db.commit()

    print(result)

finally:
    db.close()