from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Request as RequestModel, ActivityLog, ReviewQueue
from .reviews import approve_review, reject_review


router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------
@router.get("/dashboard/")
def dashboard(
    request: Request,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # AUTHENTICATION CHECK
    # -----------------------------------------------------

    if not request.session.get("admin_logged_in"):
        return RedirectResponse(
            url="/auth/login",
            status_code=303
        )

    # -----------------------------------------------------
    # DASHBOARD METRICS
    # -----------------------------------------------------

    total_requests = (
        db.query(RequestModel).count()
    )

    successful_automations = (
        db.query(ActivityLog)
        .filter(
            ActivityLog.action == "ACTION_EXECUTED",
            ActivityLog.status == "SUCCESS"
        )
        .count()
    )

    failed_automations = (
        db.query(ActivityLog)
        .filter(
            ActivityLog.status == "FAILED"
        )
        .count()
    )

    pending_reviews_count = (
        db.query(ReviewQueue)
        .filter(
            ReviewQueue.status == "pending"
        )
        .count()
    )

    high_priority = (
        db.query(RequestModel)
        .filter(
            RequestModel.priority == "HIGH"
        )
        .count()
    )

    completed_requests = (
        db.query(RequestModel)
        .filter(
            RequestModel.status == "completed"
        )
        .count()
    )

    # -----------------------------------------------------
    # RECENT REQUESTS
    # -----------------------------------------------------

    recent_requests = (
        db.query(RequestModel)
        .order_by(
            RequestModel.created_at.desc()
        )
        .limit(10)
        .all()
    )

    # -----------------------------------------------------
    # PENDING HUMAN REVIEWS
    # -----------------------------------------------------

    pending_reviews = (
        db.query(
            ReviewQueue,
            RequestModel
        )
        .join(
            RequestModel,
            ReviewQueue.request_id == RequestModel.request_id
        )
        .filter(
            ReviewQueue.status == "pending"
        )
        .order_by(
            RequestModel.created_at.desc()
        )
        .all()
    )

    # -----------------------------------------------------
    # RECENT ACTIVITY
    # -----------------------------------------------------

    recent_activity = (
        db.query(ActivityLog)
        .order_by(
            ActivityLog.created_at.desc()
        )
        .limit(10)
        .all()
    )

    # -----------------------------------------------------
    # RENDER DASHBOARD
    # -----------------------------------------------------

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "total_requests": total_requests,
            "successful_automations": successful_automations,
            "failed_automations": failed_automations,
            "pending_reviews": pending_reviews_count,
            "high_priority": high_priority,
            "completed_requests": completed_requests,
            "recent_requests": recent_requests,
            "pending_review_items": pending_reviews,
            "recent_activity": recent_activity,
            "success_message": request.query_params.get(
                "success"
            ),
            "error_message": request.query_params.get(
                "error"
            )
        }
    )


# ---------------------------------------------------------
# DASHBOARD APPROVE
# ---------------------------------------------------------

@router.post("/dashboard/review/{request_id}/approve")
def dashboard_approve(
    request: Request,
    request_id: str,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # AUTHENTICATION CHECK
    # -----------------------------------------------------

    if not request.session.get("admin_logged_in"):
        return RedirectResponse(
            url="/auth/login",
            status_code=303
        )

    try:

        approve_review(
            request_id=request_id,
            db=db
        )

        return RedirectResponse(
            url="/dashboard/?success=Request+approved+successfully",
            status_code=303
        )

    except HTTPException as e:

        return RedirectResponse(
            url=f"/dashboard/?error={e.detail}",
            status_code=303
        )


# ---------------------------------------------------------
# DASHBOARD REJECT
# ---------------------------------------------------------

@router.post("/dashboard/review/{request_id}/reject")
def dashboard_reject(
    request: Request,
    request_id: str,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # AUTHENTICATION CHECK
    # -----------------------------------------------------

    if not request.session.get("admin_logged_in"):
        return RedirectResponse(
            url="/auth/login",
            status_code=303
        )

    try:

        reject_review(
            request_id=request_id,
            db=db
        )

        return RedirectResponse(
            url="/dashboard/?success=Request+rejected+successfully",
            status_code=303
        )

    except HTTPException as e:

        return RedirectResponse(
            url=f"/dashboard/?error={e.detail}",
            status_code=303
        )