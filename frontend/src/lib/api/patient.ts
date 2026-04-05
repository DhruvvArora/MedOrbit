import { apiFetch } from "./http";
import type {
  PatientDashboardSummary,
  PatientVisitItem,
  PatientReminder,
  ExplainChatResponse,
} from "../../types/patient";

/* ─── API-to-view-model mapping ──────────────────────────────
 *
 * The backend returns `patient_discharge_draft` (DB column name).
 * Patient-facing code MUST NOT expose the word "draft".
 * We map it to `approvedInstructions` at the API boundary.
 * ───────────────────────────────────────────────────────────── */

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function mapVisit(raw: any): PatientVisitItem {
  return {
    visitId: raw.visit_id,
    title: raw.title ?? "Visit",
    status: raw.status,
    startedAt: raw.started_at ?? null,
    hasApprovedReport: raw.has_approved_report,
    simplifiedExplanation: raw.simplified_explanation ?? null,
    approvedInstructions: raw.patient_discharge_draft ?? null,
  };
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function mapDashboard(raw: any): PatientDashboardSummary {
  return {
    patientId: raw.patient_id,
    patientName: raw.patient_name,
    visitCount: raw.visit_count,
    pendingReportCount: raw.pending_report_count,
    pendingReminderCount: raw.pending_reminder_count,
    visits: (raw.visits ?? []).map(mapVisit),
    recentReminders: raw.recent_reminders ?? [],
  };
}

/* ─── Patient API ────────────────────────────────────────────── */

export const patientApi = {
  getDashboard: async (): Promise<PatientDashboardSummary> => {
    const raw = await apiFetch<unknown>("/patient/dashboard-summary");
    return mapDashboard(raw);
  },

  getVisitDetail: async (visitId: string): Promise<PatientVisitItem> => {
    const raw = await apiFetch<unknown>(`/patient/visits/${visitId}`);
    return mapVisit(raw);
  },

  getReminders: () =>
    apiFetch<PatientReminder[]>("/patient/reminders"),

  updateReminderStatus: (reminderId: number, newStatus: string) =>
    apiFetch<PatientReminder>(`/patient/reminders/${reminderId}/status`, {
      method: "PATCH",
      body: JSON.stringify({ status: newStatus }),
    }),

  sendChatMessage: (visitId: string, message: string) =>
    apiFetch<ExplainChatResponse>(
      `/patient/visits/${visitId}/explain-chat`,
      { method: "POST", body: JSON.stringify({ message }) },
    ),
};
