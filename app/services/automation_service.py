from datetime import datetime
import os

from ..models import ReviewQueue, AutomationAction
from .notification_service import send_notification


def execute_action(decision, request_id, db, customer_email):

    action = decision["action"]

    # =========================================================
    # HIGH PRIORITY / LOW CONFIDENCE → HUMAN REVIEW
    # =========================================================
    if action == "HUMAN_REVIEW":

        # -----------------------------------------------------
        # Prevent duplicate review queue entries
        # -----------------------------------------------------

        existing_review = (
            db.query(ReviewQueue)
            .filter(
                ReviewQueue.request_id == request_id,
                ReviewQueue.status == "pending"
            )
            .first()
        )

        if not existing_review:

            review_item = ReviewQueue(
                request_id=request_id,
                reason=decision["reason"],
                status="pending"
            )

            db.add(review_item)

        # -----------------------------------------------------
        # Notify reviewer
        # -----------------------------------------------------

        reviewer_email = os.getenv("REVIEWER_EMAIL")

        reviewer_notification = {
            "status": "SKIPPED",
            "message": "Reviewer email is not configured."
        }

        if reviewer_email:

            try:

                reviewer_notification = send_notification(
                    recipient_email=reviewer_email,
                    subject=f"Human Review Required - {request_id}",
                    message=(
                        "A business request requires human review.\n\n"
                        f"Request ID: {request_id}\n"
                        f"Reason: {decision['reason']}\n\n"
                        "Please review the request from the dashboard "
                        "and approve or reject it."
                    )
                )

            except Exception as e:

                reviewer_notification = {
                    "status": "FAILED",
                    "message": f"Reviewer notification failed: {str(e)}"
                }

        # -----------------------------------------------------
        # Notify customer
        # -----------------------------------------------------

        customer_notification = {
            "status": "SKIPPED",
            "message": "Customer email is not configured."
        }

        if customer_email:

            try:

                customer_notification = send_notification(
                    recipient_email=customer_email,
                    subject=f"Request Received - {request_id}",
                    message=(
                        "Thank you for contacting us.\n\n"
                        "Your request has been received successfully.\n\n"
                        f"Request ID: {request_id}\n\n"
                        "Your request requires additional human review. "
                        "Our team will review it and get back to you "
                        "with the next steps.\n\n"
                        "Please keep your request ID for reference."
                    )
                )

            except Exception as e:

                customer_notification = {
                    "status": "FAILED",
                    "message": f"Customer notification failed: {str(e)}"
                }

        return {
            "action": "HUMAN_REVIEW",
            "status": "PENDING",
            "notification": {
                "reviewer": reviewer_notification,
                "customer": customer_notification
            },
            "message": (
                "Request has been added to the human review queue."
            )
        }

    # =========================================================
    # MEDIUM PRIORITY → CUSTOMER FOLLOW-UP
    # =========================================================

    elif action == "CUSTOMER_FOLLOW_UP":

        follow_up = AutomationAction(
            request_id=request_id,
            action_type="CUSTOMER_FOLLOW_UP",
            status="completed",
            message="Customer follow-up action has been created.",
            completed_at=datetime.utcnow()
        )

        db.add(follow_up)

        # -----------------------------------------------------
        # Customer notification
        # -----------------------------------------------------

        customer_notification = {
            "status": "SKIPPED",
            "message": "Customer email is not configured."
        }

        if customer_email:

            try:

                customer_notification = send_notification(
                    recipient_email=customer_email,
                    subject=f"Follow-Up Required - {request_id}",
                    message=(
                        "Thank you for contacting us.\n\n"
                        "We have received your request and it requires "
                        "additional follow-up.\n\n"
                        f"Request ID: {request_id}\n\n"
                        "Our team will review your request and contact "
                        "you with the next steps.\n\n"
                        "Thank you for your patience."
                    )
                )

            except Exception as e:

                customer_notification = {
                    "status": "FAILED",
                    "message": f"Customer notification failed: {str(e)}"
                }

        return {
            "action": "CUSTOMER_FOLLOW_UP",
            "status": "SUCCESS",
            "notification": customer_notification,
            "message": (
                "Customer follow-up action has been created."
            )
        }

    # =========================================================
    # LOW PRIORITY → AUTOMATED RESPONSE
    # =========================================================

    elif action == "AUTOMATED_RESPONSE":

        automated_action = AutomationAction(
            request_id=request_id,
            action_type="AUTOMATED_RESPONSE",
            status="completed",
            message="Automated response action has been created.",
            completed_at=datetime.utcnow()
        )

        db.add(automated_action)

        # -----------------------------------------------------
        # Customer notification
        # -----------------------------------------------------

        customer_notification = {
            "status": "SKIPPED",
            "message": "Customer email is not configured."
        }

        if customer_email:

            try:

                customer_notification = send_notification(
                    recipient_email=customer_email,
                    subject=f"Request Processed - {request_id}",
                    message=(
                        "Thank you for contacting us.\n\n"
                        "Your request has been processed automatically.\n\n"
                        f"Request ID: {request_id}\n\n"
                        "No further action is required at this time.\n\n"
                        "Thank you for contacting us."
                    )
                )

            except Exception as e:

                customer_notification = {
                    "status": "FAILED",
                    "message": f"Customer notification failed: {str(e)}"
                }

        return {
            "action": "AUTOMATED_RESPONSE",
            "status": "SUCCESS",
            "notification": customer_notification,
            "message": (
                "Request has been processed automatically."
            )
        }

    # =========================================================
    # UNKNOWN ACTION
    # =========================================================

    return {
        "action": "UNKNOWN",
        "status": "FAILED",
        "notification": {
            "status": "FAILED",
            "message": "Unknown automation action."
        },
        "message": "Unknown automation action."
    }