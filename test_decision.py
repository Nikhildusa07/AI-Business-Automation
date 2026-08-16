from app.services.decision_service import make_decision


tests = [
    ("HIGH", 0.98),
    ("MEDIUM", 0.90),
    ("LOW", 0.85),
    ("LOW", 0.40)
]

for priority, confidence in tests:
    result = make_decision(priority, confidence)

    print(
        f"Priority={priority}, "
        f"Confidence={confidence} → "
        f"{result}"
    )