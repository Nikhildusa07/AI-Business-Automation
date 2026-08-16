import os
import smtplib
from dotenv import load_dotenv

load_dotenv()

smtp_host = os.getenv("SMTP_HOST")
smtp_port = int(os.getenv("SMTP_PORT", "587"))
smtp_user = os.getenv("SMTP_USER")
smtp_password = os.getenv("SMTP_PASSWORD")

print("SMTP_HOST:", smtp_host)
print("SMTP_PORT:", smtp_port)
print("SMTP_USER:", smtp_user)
print("SMTP_PASSWORD loaded:", bool(smtp_password))
print("SMTP_PASSWORD length:", len(smtp_password) if smtp_password else 0)

try:
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)

    print("SMTP LOGIN SUCCESS")

except Exception as e:
    print("SMTP LOGIN FAILED")
    print(repr(e))