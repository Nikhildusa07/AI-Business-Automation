from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import ReviewQueue, Request, ActivityLog
from ..services.notification_service import send_notification


router = APIRouter(
    prefix="/api/reviews",
    tags=["Human Review"]
)


# ---------------------------------------------------------
# GET PENDING REVIEWS
# ---------------------------------------------------------
@router.get("/pending")
def get_pending_reviews(
    db: Session = Depends(get_db)
):
    reviews = (
        db.query(ReviewQueue)
        .filter(
            ReviewQueue.status == "pending"
        )
        .all()
    )

    return [
        {
            "id": review.id,
            "request_id": review.request_id,
            "reason": review.reason,
            "status": review.status
        }
        for review in reviews
    ]


# ---------------------------------------------------------
# APPROVE REVIEW
# ---------------------------------------------------------
@router.post("/{request_id}/approve")
def approve_review(
    request_id: str,
    db: Session = Depends(get_db)
):
    # -----------------------------------------------------
    # Find pending review
    # -----------------------------------------------------

    review = (
        db.query(ReviewQueue)
        .filter(
            ReviewQueue.request_id == request_id,
            ReviewQueue.status == "pending"
        )
        .first()
    )

    if not review:
        raise HTTPException(
            status_code=404,
            detail="Pending review not found."
        )

    # -----------------------------------------------------
    # Find original request
    # -----------------------------------------------------

    request = (
        db.query(Request)
        .filter(
            Request.request_id == request_id
        )
        .first()
    )

    if not request:
        raise HTTPException(
            status_code=404,
            detail="Request not found."
        )

    # -----------------------------------------------------
    # Update review status
    # -----------------------------------------------------

    review.status = "approved"

    # -----------------------------------------------------
    # Update request status
    # -----------------------------------------------------

    request.status = "completed"
    request.action_taken = "REFUND_APPROVED"

    # -----------------------------------------------------
    # Log human review
    # -----------------------------------------------------

    activity = ActivityLog(
        request_id=request_id,
        action="HUMAN_REVIEW",
        status="SUCCESS",
        message="Human reviewer approved the request."
    )

    db.add(activity)

    # -----------------------------------------------------
    # Send customer notification
    # -----------------------------------------------------

    notification = send_notification(
        recipient_email=request.customer_email,
        subject=f"Request Approved - {request_id}",
        message=(
            "Thank you for contacting us.\n\n"
            f"Your request {request_id} has been reviewed "
            "and approved by our team.\n\n"
            "Your refund/action has been approved successfully.\n\n"
            "Thank you."
        )
    )

    # -----------------------------------------------------
    # Log final action
    # -----------------------------------------------------

    final_activity = ActivityLog(
        request_id=request_id,
        action="REFUND_APPROVED",
        status="SUCCESS",
        message=(
            "Human reviewer approved the request "
            "and customer was notified."
        )
    )

    db.add(final_activity)

    # -----------------------------------------------------
    # Save changes
    # -----------------------------------------------------

    db.commit()
    db.refresh(request)

    # -----------------------------------------------------
    # Return response
    # -----------------------------------------------------

    return {
        "message": "Request approved successfully.",
        "request_id": request_id,
        "status": request.status,
        "action": request.action_taken,
        "notification": notification
    }


# ---------------------------------------------------------
# REJECT REVIEW
# ---------------------------------------------------------
@router.post("/{request_id}/reject")
def reject_review(
    request_id: str,
    db: Session = Depends(get_db)
):
    # -----------------------------------------------------
    # Find pending review
    # -----------------------------------------------------

    review = (
        db.query(ReviewQueue)
        .filter(
            ReviewQueue.request_id == request_id,
            ReviewQueue.status == "pending"
        )
        .first()
    )

    if not review:
        raise HTTPException(
            status_code=404,
            detail="Pending review not found."
        )

    # -----------------------------------------------------
    # Find original request
    # -----------------------------------------------------

    request = (
        db.query(Request)
        .filter(
            Request.request_id == request_id
        )
        .first()
    )

    if not request:
        raise HTTPException(
            status_code=404,
            detail="Request not found."
        )

    # -----------------------------------------------------
    # Update review status
    # -----------------------------------------------------

    review.status = "rejected"

    # -----------------------------------------------------
    # Update request status
    # -----------------------------------------------------

    request.status = "completed"
    request.action_taken = "REQUEST_REJECTED"

    # -----------------------------------------------------
    # Log human review
    # -----------------------------------------------------

    activity = ActivityLog(
        request_id=request_id,
        action="HUMAN_REVIEW",
        status="SUCCESS",
        message="Human reviewer rejected the request."
    )

    db.add(activity)

    # -----------------------------------------------------
    # Send customer notification
    # -----------------------------------------------------

    notification = send_notification(
        recipient_email=request.customer_email,
        subject=f"Request Update - {request_id}",
        message=(
            "Thank you for contacting us.\n\n"
            f"Your request {request_id} has been reviewed "
            "by our team.\n\n"
            "Unfortunately, the request could not be approved "
            "at this time.\n\n"
            "Please contact our support team if you need "
            "further assistance."
        )
    )

    # -----------------------------------------------------
    # Log final rejection
    # -----------------------------------------------------

    final_activity = ActivityLog(
        request_id=request_id,
        action="REQUEST_REJECTED",
        status="SUCCESS",
        message=(
            "Human reviewer rejected the request "
            "and customer was notified."
        )
    )

    db.add(final_activity)

    # -----------------------------------------------------
    # Save changes
    # -----------------------------------------------------

    db.commit()
    db.refresh(request)

    # -----------------------------------------------------
    # Return response
    # -----------------------------------------------------

    return {
        "message": "Request rejected successfully.",
        "request_id": request_id,
        "status": request.status,
        "action": request.action_taken,
        "notification": notification
    }