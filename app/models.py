from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from datetime import datetime

from .database import Base


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String(50), unique=True, index=True, nullable=False)

    customer_name = Column(String(100), nullable=False)
    customer_email = Column(String(150), nullable=False)

    input_text = Column(Text, nullable=False)

    intent = Column(String(100), nullable=True)
    priority = Column(String(20), nullable=True)
    confidence_score = Column(Float, nullable=True)
    ai_summary = Column(Text, nullable=True)

    status = Column(String(50), default="received")
    action_taken = Column(Text, nullable=True)

    error_message = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)

    request_id = Column(String(50), nullable=False, index=True)

    action = Column(String(100), nullable=False)

    status = Column(String(30), nullable=False)

    message = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

class ReviewQueue(Base):
    __tablename__ = "review_queue"

    id = Column(Integer, primary_key=True, index=True)

    request_id = Column(String(50), nullable=False, index=True)

    reason = Column(Text, nullable=False)

    status = Column(String(30), default="pending")

    reviewer_note = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    reviewed_at = Column(DateTime, nullable=True)

class AutomationAction(Base):
    __tablename__ = "automation_actions"

    id = Column(Integer, primary_key=True, index=True)

    request_id = Column(String(50), nullable=False, index=True)

    action_type = Column(String(50), nullable=False)

    status = Column(String(30), default="pending")

    message = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    completed_at = Column(DateTime, nullable=True)