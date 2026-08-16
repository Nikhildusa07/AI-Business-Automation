import os
import smtplib
from email.message import EmailMessage


def send_notification(
    recipient_email: str,
    subject: str,
    message: str
):
    """
    Send email notification using Gmail SMTP.
    """

    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    sender_email = os.getenv("NOTIFICATION_FROM", smtp_user)

    # Validate SMTP configuration
    if not smtp_user or not smtp_password:
        print("EMAIL ERROR: SMTP credentials are missing.")

        return {
            "status": "FAILED",
            "message": "SMTP credentials are missing."
        }

    if not recipient_email:
        print("EMAIL ERROR: Recipient email is missing.")

        return {
            "status": "FAILED",
            "message": "Recipient email is missing."
        }

    try:
        email = EmailMessage()

        email["From"] = sender_email
        email["To"] = recipient_email
        email["Subject"] = subject

        email.set_content(message)

        # Gmail SMTP SSL
        with smtplib.SMTP_SSL(
            smtp_host,
            smtp_port,
            timeout=30
        ) as server:

            server.login(
                smtp_user,
                smtp_password
            )

            server.send_message(email)

        print(f"EMAIL SENT SUCCESSFULLY: {recipient_email}")

        return {
            "status": "SENT",
            "message": "Notification sent successfully."
        }

    except Exception as e:

        print(f"EMAIL ERROR: {repr(e)}")

        return {
            "status": "FAILED",
            "message": str(e)
        }