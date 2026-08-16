import os
import requests


def send_notification(
    recipient_email: str,
    subject: str,
    message: str
):
    """
    Send email notification using Brevo HTTP API.
    """

    api_key = os.getenv("BREVO_API_KEY")
    sender_email = os.getenv("BREVO_SENDER_EMAIL")

    if not api_key or not sender_email:
        print("EMAIL ERROR: Brevo configuration is missing.")

        return {
            "status": "FAILED",
            "message": "Brevo configuration is missing."
        }

    if not recipient_email:
        print("EMAIL ERROR: Recipient email is missing.")

        return {
            "status": "FAILED",
            "message": "Recipient email is missing."
        }

    try:
        url = "https://api.brevo.com/v3/smtp/email"

        headers = {
            "accept": "application/json",
            "api-key": api_key,
            "content-type": "application/json"
        }

        data = {
            "sender": {
                "email": sender_email
            },
            "to": [
                {
                    "email": recipient_email
                }
            ],
            "subject": subject,
            "textContent": message
        }

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=30
        )

        if response.status_code in (200, 201, 202):
            print(f"EMAIL SENT SUCCESSFULLY: {recipient_email}")

            return {
                "status": "SENT",
                "message": "Notification sent successfully."
            }

        print(f"EMAIL ERROR: {response.status_code} - {response.text}")

        return {
            "status": "FAILED",
            "message": response.text
        }

    except Exception as e:

        print(f"EMAIL ERROR: {repr(e)}")

        return {
            "status": "FAILED",
            "message": str(e)
        }