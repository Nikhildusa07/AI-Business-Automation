import os
import smtplib
from email.message import EmailMessage


def send_notification(
    recipient_email: str,
    subject: str,
    message: str
):
    """
    Send an email notification.

    SMTP configuration is loaded from environment variables.
    """

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    sender_email = os.getenv("NOTIFICATION_FROM", smtp_user)

    if not all([
        smtp_host,
        smtp_user,
        smtp_password,
        sender_email
    ]):
        return {
            "status": "SKIPPED",
            "message": "SMTP configuration is not available."
        }

    try:
        email = EmailMessage()

        email["From"] = sender_email
        email["To"] = recipient_email
        email["Subject"] = subject

        email.set_content(message)

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(email)

        return {
            "status": "SENT",
            "message": "Notification sent successfully."
        }

    except Exception as e:
        return {
            "status": "FAILED",
            "message": str(e)
        }