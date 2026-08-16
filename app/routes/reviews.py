from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import ReviewQueue, Request as RequestModel, ActivityLog
from ..services.notification_service import send_notification


router = APIRouter(
    prefix="/api/reviews",
    tags=["Human Review"]
)


# =========================================================
# AUTHENTICATION HELPER
# =========================================================

def require_admin(request: Request):
    """
    Verify that the admin is authenticated.
    Used to protect review API endpoints.
    """

    if not request.session.get("admin_logged_in"):
        raise HTTPException(
            status_code=401,
            detail="Authentication required."
        )


# =========================================================
# GET PENDING REVIEWS
# =========================================================

@router.get("/pending")
def get_pending_reviews(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Return all pending human review requests.
    Admin authentication required.
    """

    require_admin(request)

    reviews = (
        db.query(ReviewQueue)
        .filter(
            ReviewQueue.status == "pending"
        )
        .order_by(
            ReviewQueue.created_at.desc()
        )
        .all()
    )

    return [
        {
            "id": review.id,
            "request_id": review.request_id,
            "reason": review.reason,
            "status": review.status,
            "created_at": review.created_at
        }
        for review in reviews
    ]


# =========================================================
# APPROVE REVIEW - INTERNAL BUSINESS LOGIC
# =========================================================

def approve_review(
    request_id: str,
    db: Session
):
    """
    Approve a pending review.

    This function is intentionally kept independent
    of HTTP Request authentication because it is also
    called internally by the dashboard route.
    """

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

    business_request = (
        db.query(RequestModel)
        .filter(
            RequestModel.request_id == request_id
        )
        .first()
    )

    if not business_request:
        raise HTTPException(
            status_code=404,
            detail="Request not found."
        )

    # -----------------------------------------------------
    # Update review status
    # -----------------------------------------------------

    review.status = "approved"
    review.reviewed_at = __import__("datetime").datetime.utcnow()

    # -----------------------------------------------------
    # Update request status
    # -----------------------------------------------------

    business_request.status = "completed"
    business_request.action_taken = "REFUND_APPROVED"

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
        recipient_email=business_request.customer_email,
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
    db.refresh(business_request)

    # -----------------------------------------------------
    # Return response
    # -----------------------------------------------------

    return {
        "message": "Request approved successfully.",
        "request_id": request_id,
        "status": business_request.status,
        "action": business_request.action_taken,
        "notification": notification
    }


# =========================================================
# APPROVE REVIEW - API ENDPOINT
# =========================================================

@router.post("/{request_id}/approve")
def approve_review_api(
    request: Request,
    request_id: str,
    db: Session = Depends(get_db)
):
    """
    API endpoint for approving a review.
    Admin authentication required.
    """

    require_admin(request)

    return approve_review(
        request_id=request_id,
        db=db
    )


# =========================================================
# REJECT REVIEW - INTERNAL BUSINESS LOGIC
# =========================================================

def reject_review(
    request_id: str,
    db: Session
):
    """
    Reject a pending review.

    This function is intentionally kept independent
    of HTTP Request authentication because it is also
    called internally by the dashboard route.
    """

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

    business_request = (
        db.query(RequestModel)
        .filter(
            RequestModel.request_id == request_id
        )
        .first()
    )

    if not business_request:
        raise HTTPException(
            status_code=404,
            detail="Request not found."
        )

    # -----------------------------------------------------
    # Update review status
    # -----------------------------------------------------

    review.status = "rejected"
    review.reviewed_at = __import__("datetime").datetime.utcnow()

    # -----------------------------------------------------
    # Update request status
    # -----------------------------------------------------

    business_request.status = "completed"
    business_request.action_taken = "REQUEST_REJECTED"

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
        recipient_email=business_request.customer_email,
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
    db.refresh(business_request)

    # -----------------------------------------------------
    # Return response
    # -----------------------------------------------------

    return {
        "message": "Request rejected successfully.",
        "request_id": request_id,
        "status": business_request.status,
        "action": business_request.action_taken,
        "notification": notification
    }


# =========================================================
# REJECT REVIEW - API ENDPOINT
# =========================================================

@router.post("/{request_id}/reject")
def reject_review_api(
    request: Request,
    request_id: str,
    db: Session = Depends(get_db)
):
    """
    API endpoint for rejecting a review.
    Admin authentication required.
    """

    require_admin(request)

    return reject_review(
        request_id=request_id,
        db=db
    )