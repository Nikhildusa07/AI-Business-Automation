from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
import os

from ..database import get_db
from ..models import Request, ActivityLog, ReviewQueue, AutomationAction
from ..schemas import RequestCreate
from ..services.ai_service import analyze_request
from ..services.agent_service import run_agent_workflow
from ..services.decision_service import make_decision
from ..services.automation_service import execute_action
from ..services.notification_service import send_notification


router = APIRouter(
    prefix="/api/requests",
    tags=["Requests"]
)


def _safe_human_review_fallback(
    request_id: str,
    customer_email: str,
    reason: str,
    db: Session,
):
    """Create a safe human-review fallback when an automated step fails."""

    existing = (
        db.query(ReviewQueue)
        .filter(
            ReviewQueue.request_id == request_id,
            ReviewQueue.status == "pending"
        )
        .first()
    )

    if not existing:
        db.add(
            ReviewQueue(
                request_id=request_id,
                reason=reason,
                status="pending"
            )
        )

    reviewer_email = os.getenv("REVIEWER_EMAIL")
    reviewer_notification = {"status": "SKIPPED", "message": "Reviewer email is not configured."}

    if reviewer_email:
        reviewer_notification = send_notification(
            recipient_email=reviewer_email,
            subject=f"Human Review Required - {request_id}",
            message=(
                "An automated workflow could not safely complete.\n\n"
                f"Request ID: {request_id}\n"
                f"Reason: {reason}\n\n"
                "Please review this request from the dashboard."
            )
        )

    customer_notification = {"status": "SKIPPED", "message": "Customer email is not configured."}

    if customer_email:
        customer_notification = send_notification(
            recipient_email=customer_email,
            subject=f"Request Received - {request_id}",
            message=(
                "Your request has been received successfully.\n\n"
                f"Request ID: {request_id}\n\n"
                "The automated workflow requires additional human review. "
                "Our team will review it and contact you with the next steps."
            )
        )

    return {
        "reviewer": reviewer_notification,
        "customer": customer_notification,
    }


def _verify_action(request_id: str, action: str, status: str, db: Session):
    """Verify that the selected action actually produced the expected state."""

    if action == "HUMAN_REVIEW":
        review = (
            db.query(ReviewQueue)
            .filter(
                ReviewQueue.request_id == request_id,
                ReviewQueue.status == "pending"
            )
            .first()
        )
        return bool(review), "Human review queue entry verified."

    action_record = (
        db.query(AutomationAction)
        .filter(
            AutomationAction.request_id == request_id,
            AutomationAction.action_type == action,
            AutomationAction.status == "completed"
        )
        .order_by(AutomationAction.id.desc())
        .first()
    )

    if status == "SUCCESS" and action_record:
        return True, "Automation action record verified."

    return False, "Expected automation action record was not found."


@router.post("/")
def create_request(
    request_data: RequestCreate,
    db: Session = Depends(get_db)
):
    request_id = f"REQ-{uuid.uuid4().hex[:8].upper()}"

    # =========================================================
    # 1. REQUEST RECEIVED
    # =========================================================
    activity_received = ActivityLog(
        request_id=request_id,
        action="REQUEST_RECEIVED",
        status="SUCCESS",
        message="Business request received successfully."
    )
    db.add(activity_received)

    # =========================================================
    # 2. AI ANALYSIS WITH RETRY / FAILURE FALLBACK
    # =========================================================
    try:
        ai_result = analyze_request(request_data.input_text)

    except Exception as exc:
        error_message = str(exc)

        db.add(ActivityLog(
            request_id=request_id,
            action="AI_ANALYSIS",
            status="FAILED",
            message=error_message
        ))

        new_request = Request(
            request_id=request_id,
            customer_name=request_data.customer_name,
            customer_email=request_data.customer_email,
            input_text=request_data.input_text,
            intent="AI_ANALYSIS_FAILED",
            priority="HIGH",
            confidence_score=0.0,
            ai_summary="AI analysis failed. Request routed to human review.",
            status="pending_review",
            action_taken="HUMAN_REVIEW",
            error_message=error_message
        )
        db.add(new_request)

        decision = {
            "decision": "ESCALATE",
            "action": "HUMAN_REVIEW",
            "reason": "AI analysis failed after retry attempts; safe human-review fallback was activated."
        }

        db.add(ActivityLog(
            request_id=request_id,
            action="DECISION_MADE",
            status="FALLBACK",
            message=decision["reason"]
        ))

        try:
            fallback_notifications = _safe_human_review_fallback(
                request_id=request_id,
                customer_email=request_data.customer_email,
                reason=decision["reason"],
                db=db,
            )
        except Exception as fallback_exc:
            fallback_notifications = {
                "reviewer": {"status": "FAILED", "message": str(fallback_exc)},
                "customer": {"status": "FAILED", "message": str(fallback_exc)},
            }
            db.add(ActivityLog(
                request_id=request_id,
                action="FALLBACK_NOTIFICATION",
                status="FAILED",
                message=str(fallback_exc)
            ))

        db.add(ActivityLog(
            request_id=request_id,
            action="ACTION_EXECUTED",
            status="PENDING",
            message="AI failure safely routed the request to human review."
        ))

        try:
            db.commit()
            db.refresh(new_request)
        except Exception as db_exc:
            db.rollback()
            raise HTTPException(status_code=500, detail="Failed to save fallback request.") from db_exc

        return {
            "message": "Request received and routed to human review.",
            "request_id": request_id,
            "status": "pending_review",
            "ai_analysis": {
                "intent": new_request.intent,
                "priority": new_request.priority,
                "confidence_score": new_request.confidence_score,
                "summary": new_request.ai_summary,
            },
            "decision": decision,
            "automation": {
                "action": "HUMAN_REVIEW",
                "status": "PENDING",
                "message": "AI failure fallback activated.",
                "notification": fallback_notifications,
            },
            "agent_workflow": {
                "status": "FALLBACK",
                "tool_selection": None,
                "data_retrieval": None,
                "reasoning": "AI analysis was unavailable, so the system safely escalated to human review.",
                "verification": {"status": "READY", "message": "Human review fallback was created."},
            },
        }

    # =========================================================
    # 3. SAVE REQUEST AFTER SUCCESSFUL AI ANALYSIS
    # =========================================================
    new_request = Request(
        request_id=request_id,
        customer_name=request_data.customer_name,
        customer_email=request_data.customer_email,
        input_text=request_data.input_text,
        intent=ai_result["intent"],
        priority=ai_result["priority"],
        confidence_score=ai_result["confidence_score"],
        ai_summary=ai_result["summary"],
        status="processing",
        action_taken="AI analysis completed"
    )
    db.add(new_request)

    db.add(ActivityLog(
        request_id=request_id,
        action="AI_ANALYSIS",
        status="SUCCESS",
        message=(
            f"Intent: {ai_result['intent']}, "
            f"Priority: {ai_result['priority']}, "
            f"Confidence: {ai_result['confidence_score']}"
        )
    ))

    # =========================================================
    # 4. ADVANCED AI-AGENT WORKFLOW
    # Request -> Tool Selection -> Data Retrieval -> Reasoning
    # =========================================================
    try:
        agent_workflow = run_agent_workflow(
            request_data.input_text,
            ai_result
        )

        db.add(ActivityLog(
            request_id=request_id,
            action="AGENT_TOOL_SELECTED",
            status="SUCCESS",
            message=(
                f"Tool: {agent_workflow['tool_selection']['tool']}; "
                f"Reason: {agent_workflow['tool_selection']['reason']}"
            )
        ))

        db.add(ActivityLog(
            request_id=request_id,
            action="AGENT_DATA_RETRIEVED",
            status="SUCCESS",
            message=(
                f"Source: {agent_workflow['data_retrieval']['source']}; "
                f"Data: {agent_workflow['data_retrieval']['data']}"
            )
        ))

        db.add(ActivityLog(
            request_id=request_id,
            action="AGENT_REASONING",
            status="SUCCESS",
            message=agent_workflow["reasoning"]["reasoning"]
        ))

    except Exception as exc:
        error_message = str(exc)
        agent_workflow = {
            "status": "FALLBACK",
            "tool_selection": None,
            "data_retrieval": None,
            "reasoning": f"Agent workflow failed: {error_message}",
            "verification": {"status": "PENDING", "message": "Human review fallback required."},
        }

        db.add(ActivityLog(
            request_id=request_id,
            action="AGENT_WORKFLOW",
            status="FAILED",
            message=error_message
        ))

    # =========================================================
    # 5. DECISION
    # =========================================================
    try:
        decision = make_decision(
            ai_result["priority"],
            ai_result["confidence_score"]
        )

        if agent_workflow["status"] == "FALLBACK":
            decision = {
                "decision": "ESCALATE",
                "action": "HUMAN_REVIEW",
                "reason": "Agent workflow failed; safe human-review fallback was activated."
            }

    except Exception as exc:
        error_message = str(exc)
        db.add(ActivityLog(
            request_id=request_id,
            action="DECISION_MADE",
            status="FAILED",
            message=error_message
        ))
        decision = {
            "decision": "ESCALATE",
            "action": "HUMAN_REVIEW",
            "reason": "Decision service failed; safe human-review fallback was activated."
        }

    db.add(ActivityLog(
        request_id=request_id,
        action="DECISION_MADE",
        status="SUCCESS" if decision["action"] != "HUMAN_REVIEW" or ai_result["priority"] == "HIGH" else "SUCCESS",
        message=(
            f"Decision: {decision['decision']}, "
            f"Action: {decision['action']}, "
            f"Reason: {decision['reason']}"
        )
    ))

    # =========================================================
    # 6. ACTION EXECUTION
    # =========================================================
    try:
        automation_result = execute_action(
            decision=decision,
            request_id=request_id,
            db=db,
            customer_email=request_data.customer_email
        )

    except Exception as exc:
        error_message = str(exc)
        db.add(ActivityLog(
            request_id=request_id,
            action="ACTION_EXECUTED",
            status="FAILED",
            message=error_message
        ))

        new_request.error_message = error_message
        new_request.status = "pending_review"
        new_request.action_taken = "HUMAN_REVIEW"

        try:
            fallback_notifications = _safe_human_review_fallback(
                request_id=request_id,
                customer_email=request_data.customer_email,
                reason="Automation execution failed; safe human-review fallback was activated.",
                db=db,
            )
        except Exception as fallback_exc:
            fallback_notifications = {
                "reviewer": {"status": "FAILED", "message": str(fallback_exc)},
                "customer": {"status": "FAILED", "message": str(fallback_exc)},
            }

        automation_result = {
            "action": "HUMAN_REVIEW",
            "status": "PENDING",
            "notification": fallback_notifications,
            "message": "Automation failed and the request was routed to human review."
        }

    # =========================================================
    # 7. UPDATE REQUEST STATUS
    # =========================================================
    new_request.action_taken = automation_result["action"]

    if automation_result["status"] == "PENDING":
        new_request.status = "pending_review"
    elif automation_result["status"] == "SUCCESS":
        new_request.status = "completed"
    else:
        new_request.status = "failed"

    db.add(ActivityLog(
        request_id=request_id,
        action="ACTION_EXECUTED",
        status=automation_result["status"],
        message=automation_result["message"]
    ))

    # Log notification failures without hiding the main workflow result.
    notifications = automation_result.get("notification") or {}
    notification_values = notifications.values() if isinstance(notifications, dict) else []
    for notification in notification_values:
        if isinstance(notification, dict) and notification.get("status") == "FAILED":
            db.add(ActivityLog(
                request_id=request_id,
                action="NOTIFICATION",
                status="FAILED",
                message=notification.get("message", "Notification failed.")
            ))

    # =========================================================
    # 8. COMMIT BEFORE VERIFICATION
    # =========================================================
    try:
        db.commit()
        db.refresh(new_request)
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to save request.") from exc

    # =========================================================
    # 9. VERIFY ACTION
    # =========================================================
    verified, verification_message = _verify_action(
        request_id=request_id,
        action=automation_result["action"],
        status=automation_result["status"],
        db=db
    )

    if verified:
        db.add(ActivityLog(
            request_id=request_id,
            action="ACTION_VERIFICATION",
            status="SUCCESS",
            message=verification_message
        ))
    else:
        new_request.status = "pending_review"
        new_request.action_taken = "HUMAN_REVIEW"
        reason = "Action verification failed; request requires human review."

        fallback_notifications = _safe_human_review_fallback(
            request_id=request_id,
            customer_email=request_data.customer_email,
            reason=reason,
            db=db,
        )

        db.add(ActivityLog(
            request_id=request_id,
            action="ACTION_VERIFICATION",
            status="FAILED",
            message=verification_message
        ))
        db.add(ActivityLog(
            request_id=request_id,
            action="VERIFICATION_FALLBACK",
            status="PENDING",
            message=reason
        ))

        automation_result = {
            "action": "HUMAN_REVIEW",
            "status": "PENDING",
            "notification": fallback_notifications,
            "message": reason,
        }

    db.commit()
    db.refresh(new_request)

    # =========================================================
    # 10. COMPLETE WORKFLOW RESPONSE
    # =========================================================
    agent_workflow["verification"] = {
        "status": "SUCCESS" if verified else "FALLBACK",
        "message": verification_message
    }

    return {
        "message": "Request processed successfully",
        "request_id": request_id,
        "status": new_request.status,
        "ai_analysis": {
            "intent": new_request.intent,
            "priority": new_request.priority,
            "confidence_score": new_request.confidence_score,
            "summary": new_request.ai_summary
        },
        "agent_workflow": agent_workflow,
        "decision": {
            "decision": decision["decision"],
            "action": decision["action"],
            "reason": decision["reason"]
        },
        "automation": {
            "action": automation_result["action"],
            "status": automation_result["status"],
            "message": automation_result["message"],
            "notification": automation_result.get("notification")
        }
    }
