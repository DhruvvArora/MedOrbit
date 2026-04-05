export type VisitStatus = "scheduled" | "active" | "completed" | "cancelled";
export type VisitType = "virtual" | "in_person";
export type ReportStatus = "none" | "draft" | "approved";

export interface DoctorVisitListItem {
  id: string;
  title?: string | null;
  status: VisitStatus;
  type: VisitType;
  patient_name: string;
  started_at?: string | null;
  ended_at?: string | null;
  created_at: string;
  transcript_chunk_count: number;
  transcript_ready: boolean;
  report_status: ReportStatus;
  last_activity_at?: string | null;
}

export interface DoctorDashboardSummary {
  doctor_id: string;
  doctor_name: string;
  counts: Record<string, number>;
  visits: DoctorVisitListItem[];
}

export interface TranscriptChunk {
  id: string;
  sequence_number: number;
  speaker_role: "doctor" | "patient" | "system";
  speaker_label?: string | null;
  text: string;
  source_type: "manual" | "transcribed" | "simulated";
  created_at: string;
}

export interface TranscriptStatsView {
  total_chunks: number;
  speaker_breakdown: Record<string, number>;
  source_breakdown: Record<string, number>;
  first_chunk_at?: string | null;
  last_chunk_at?: string | null;
  total_characters: number;
}

export interface ReportPreview {
  doctor_summary?: string | null;
  patient_discharge_draft?: string | null;
  simplified_explanation?: string | null;
  clinical_review_flags: string[];
  reminder_candidates: string[];
  updated_at?: string | null;
}

export interface ReportStatusSummary {
  exists: boolean;
  status: ReportStatus;
  approved_at?: string | null;
  approved_by_id?: string | null;
  reminder_candidates_count: number;
}

export interface ConsultationWorkspace {
  visit: DoctorVisitListItem;
  transcript_stats: TranscriptStatsView;
  transcript_chunks: TranscriptChunk[];
  report_status: ReportStatusSummary;
  report_preview?: ReportPreview | null;
  available_actions: string[];
}

export interface BehavioralInsights {
  emotional_tone?: string;
  behavioral_observations?: string[];
  concerns?: string[];
  suggested_follow_ups?: string[];
  uncertainty_note?: string;
  [key: string]: unknown;
}

export interface TriageSummary {
  acuity_level?: string;
  key_symptoms?: string[];
  risk_flags?: string[];
  recommended_next_steps?: string[];
  uncertainty_note?: string;
  [key: string]: unknown;
}

export interface VisitReport {
  id: number;
  visit_id: string;
  status: "DRAFT" | "APPROVED";
  doctor_summary?: string | null;
  patient_discharge_draft?: string | null;
  simplified_explanation?: string | null;
  clinical_review_flags?: string[] | null;
  reminder_candidates?: string[] | null;
  approved_by_id?: string | number | null;
  approved_at?: string | null;
  created_at: string;
  updated_at: string;
}
