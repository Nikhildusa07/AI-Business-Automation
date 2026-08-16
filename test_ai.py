from app.services.ai_service import analyze_request


result = analyze_request(
    "My payment failed and I need help immediately."
)

print(result)