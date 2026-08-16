from app.database import SessionLocal
from app.services.automation_service import execute_action


db = SessionLocal()

try:
    result = execute_action(
        {
            "decision": "AUTO_PROCESS",
            "action": "AUTOMATED_RESPONSE",
            "reason": "Low-priority request can be processed automatically."
        },
        "TEST-AUTO-001",
        db
    )

    db.commit()

    print(result)

finally:
    db.close()