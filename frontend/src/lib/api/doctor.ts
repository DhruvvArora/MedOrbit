import { apiFetch } from "./http";
import type {
  BehavioralInsights,
  ConsultationWorkspace,
  DoctorDashboardSummary,
  TriageSummary,
  VisitReport,
} from "../../types/doctor";

export const doctorApi = {
  getDashboard: () => apiFetch<DoctorDashboardSummary>("/doctor/dashboard-summary"),
  getWorkspace: (visitId: string) => apiFetch<ConsultationWorkspace>(`/doctor/visits/${visitId}/workspace`),
  getReport: (visitId: string) => apiFetch<VisitReport>(`/visits/${visitId}/report`),
  runBehavioral: (visitId: string) => apiFetch<BehavioralInsights>(`/visits/${visitId}/agents/behavioral/run`, { method: "POST" }),
  runTriage: (visitId: string) => apiFetch<TriageSummary>(`/visits/${visitId}/agents/clinical-triage/run`, { method: "POST" }),
  runOrchestration: (visitId: string) => apiFetch<VisitReport>(`/visits/${visitId}/orchestration/run`, { method: "POST" }),
  updateReport: (visitId: string, payload: Partial<VisitReport>) =>
    apiFetch<VisitReport>(`/visits/${visitId}/report`, { method: "PATCH", body: JSON.stringify(payload) }),
  approveReport: (visitId: string) => apiFetch<VisitReport>(`/visits/${visitId}/report/approve`, { method: "POST" }),
  generateReminders: (visitId: string) => apiFetch<unknown[]>(`/visits/${visitId}/reminders/generate`, { method: "POST" }),
  startVisit: (visitId: string) => apiFetch(`/visits/${visitId}/start`, { method: "POST" }),
  completeVisit: (visitId: string) => apiFetch(`/visits/${visitId}/complete`, { method: "POST" }),
};
