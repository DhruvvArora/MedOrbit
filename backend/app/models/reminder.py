from datetime import datetime, timedelta
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey

from app.models.base import Base

class Reminder(Base):
    """
    Physical tracker for patient action items spawned from the VisitReport.
    """
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    visit_id = Column(String(36), ForeignKey("visits.id"), nullable=False)
    patient_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    source_report_id = Column(Integer, ForeignKey("visit_reports.id"), nullable=False)
    
    title = Column(String, nullable=False)
    status = Column(String, default="PENDING", nullable=False) # 'PENDING', 'COMPLETED', 'SKIPPED'
    
    # Simple default due_at scheduler (+1 day from generation for MVP)
    due_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
