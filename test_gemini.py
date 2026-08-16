import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print("API key exists:", bool(api_key))

client = genai.Client(api_key=api_key)

print("Sending request...")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Reply with exactly: Gemini connection successful"
)

print("Response:")
print(response.text)