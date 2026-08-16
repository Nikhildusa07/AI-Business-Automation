import os
import smtplib
from email.message import EmailMessage


def send_notification(
    recipient_email: str,
    subject: str,
    message: str
):
    """
    Send an email notification using Gmail SMTP.

    Configuration:
        SMTP_HOST
        SMTP_PORT
        SMTP_USER
        SMTP_PASSWORD
        NOTIFICATION_FROM
    """

    smtp_host = os.getenv(
        "SMTP_HOST",
        "smtp.gmail.com"
    )

    smtp_port = int(
        os.getenv("SMTP_PORT", "465")
    )

    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    sender_email = os.getenv(
        "NOTIFICATION_FROM",
        smtp_user
    )

    # ---------------------------------------------------------
    # Validate SMTP configuration
    # ---------------------------------------------------------

    if not smtp_user:
        print("EMAIL ERROR: SMTP_USER is missing.")

        return {
            "status": "FAILED",
            "message": "SMTP_USER is not configured."
        }

    if not smtp_password:
        print("EMAIL ERROR: SMTP_PASSWORD is missing.")

        return {
            "status": "FAILED",
            "message": "SMTP_PASSWORD is not configured."
        }

    if not sender_email:
        print("EMAIL ERROR: NOTIFICATION_FROM is missing.")

        return {
            "status": "FAILED",
            "message": "Sender email is not configured."
        }

    if not recipient_email:
        print("EMAIL ERROR: Recipient email is missing.")

        return {
            "status": "FAILED",
            "message": "Recipient email is required."
        }

    # ---------------------------------------------------------
    # Create email
    # ---------------------------------------------------------

    email = EmailMessage()

    email["From"] = sender_email
    email["To"] = recipient_email
    email["Subject"] = subject

    email.set_content(message)

    # ---------------------------------------------------------
    # Send email
    # ---------------------------------------------------------

    try:

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

        print(
            f"EMAIL SENT SUCCESSFULLY: {recipient_email}"
        )

        return {
            "status": "SENT",
            "message": "Notification sent successfully."
        }

    except smtplib.SMTPAuthenticationError as e:

        print(
            f"EMAIL AUTHENTICATION ERROR: {repr(e)}"
        )

        return {
            "status": "FAILED",
            "message": "SMTP authentication failed."
        }

    except smtplib.SMTPConnectError as e:

        print(
            f"EMAIL CONNECTION ERROR: {repr(e)}"
        )

        return {
            "status": "FAILED",
            "message": "Could not connect to SMTP server."
        }

    except smtplib.SMTPException as e:

        print(
            f"EMAIL SMTP ERROR: {repr(e)}"
        )

        return {
            "status": "FAILED",
            "message": str(e)
        }

    except Exception as e:

        print(
            f"EMAIL ERROR: {repr(e)}"
        )

        return {
            "status": "FAILED",
            "message": str(e)
        }