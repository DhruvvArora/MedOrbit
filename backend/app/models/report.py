from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB

from app.models.base import Base

class VisitReport(Base):
    """
    Mutable report acting as the final charting module. 
    Begins as a generated DRAFT and transitions to APPROVED.
    """
    __tablename__ = "visit_reports"

    id = Column(Integer, primary_key=True, index=True)
    visit_id = Column(String(36), ForeignKey("visits.id"), nullable=False, unique=True)
    status = Column(String, default="DRAFT", nullable=False) # 'DRAFT' or 'APPROVED'
    
    doctor_summary = Column(Text, nullable=True)
    patient_discharge_draft = Column(Text, nullable=True)
    simplified_explanation = Column(Text, nullable=True)
    
    # We use SQLite compatible JSON for the list storage (JSONB is for postgres). 
    # Since we mapped Alembic locally to sqlite MVP, we map to JSON. 
    # SQLAlchemy's generic JSON supports both.
    from sqlalchemy import JSON
    clinical_review_flags = Column(JSON, nullable=True)
    reminder_candidates = Column(JSON, nullable=True)

    approved_by_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
