from datetime import datetime
from typing import Dict, List, Literal, Optional

from pydantic import BaseModel


class DoctorVisitListItem(BaseModel):
    id: str
    title: Optional[str] = None
    status: str
    type: str
    patient_name: str
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    created_at: datetime
    transcript_chunk_count: int = 0
    transcript_ready: bool = False
    report_status: Literal["none", "draft", "approved"] = "none"
    last_activity_at: Optional[datetime] = None


class DoctorDashboardSummaryResponse(BaseModel):
    doctor_id: str
    doctor_name: str
    counts: Dict[str, int]
    visits: List[DoctorVisitListItem]


class TranscriptStatsView(BaseModel):
    total_chunks: int = 0
    speaker_breakdown: Dict[str, int] = {}
    source_breakdown: Dict[str, int] = {}
    first_chunk_at: Optional[str] = None
    last_chunk_at: Optional[str] = None
    total_characters: int = 0


class TranscriptChunkView(BaseModel):
    id: str
    sequence_number: int
    speaker_role: str
    speaker_label: Optional[str] = None
    text: str
    source_type: str
    created_at: datetime


class ReportStatusSummary(BaseModel):
    exists: bool
    status: Literal["none", "draft", "approved"]
    approved_at: Optional[datetime] = None
    approved_by_id: Optional[str] = None
    reminder_candidates_count: int = 0


class ConsultationWorkspaceResponse(BaseModel):
    visit: DoctorVisitListItem
    transcript_stats: TranscriptStatsView
    transcript_chunks: List[TranscriptChunkView]
    report_status: ReportStatusSummary
    report_preview: Optional[dict] = None
    available_actions: List[str]
