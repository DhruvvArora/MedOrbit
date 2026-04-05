/* ─── Patient-facing view-model types ─────────────────────────
 *
 * These types are the ONLY shapes the patient UI should use.
 * Field names are intentionally patient-safe:
 *   - "approvedInstructions" (mapped from API "patient_discharge_draft")
 *   - "simplifiedExplanation"
 *   - "hasApprovedReport"
 *
 * The word "draft" MUST NOT appear in patient-facing UI or types.
 * ───────────────────────────────────────────────────────────── */

/* -- Visit -------------------------------------------------- */

export interface PatientVisitItem {
  visitId: number;
  title: string;
  status: string;
  startedAt: string | null;
  hasApprovedReport: boolean;
  simplifiedExplanation: string | null;
  /** Mapped from API field "patient_discharge_draft". */
  approvedInstructions: string | null;
}

/* -- Dashboard ---------------------------------------------- */

export interface PatientDashboardSummary {
  patientId: string;
  patientName: string;
  visitCount: number;
  pendingReportCount: number;
  pendingReminderCount: number;
  visits: PatientVisitItem[];
  recentReminders: PatientReminder[];
}

/* -- Reminder ----------------------------------------------- */

export type ReminderStatus = "PENDING" | "COMPLETED" | "SKIPPED";

export interface PatientReminder {
  id: number;
  visit_id: string;
  patient_id: string;
  title: string;
  status: ReminderStatus;
  due_at: string;
  completed_at: string | null;
  created_at: string;
  updated_at: string;
}

/* -- Chat --------------------------------------------------- */

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  isSupported?: boolean;
  safetyNote?: string;
}

export interface ExplainChatResponse {
  answer: string;
  is_supported: boolean;
  refusal_reason: string | null;
  safety_note: string;
}
