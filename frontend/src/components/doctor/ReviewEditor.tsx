import React, { useEffect, useMemo, useState } from "react";
import type { VisitReport } from "../../types/doctor";
import { PanelShell } from "../shared/PanelShell";
import { StatusBadge } from "../shared/StatusBadge";

interface Props {
  report: VisitReport;
  onSave: (payload: Partial<VisitReport>) => Promise<void>;
  onApprove: () => Promise<void>;
  onGenerateReminders: () => Promise<void>;
  saving: boolean;
}

export function ReviewEditor({ report, onSave, onApprove, onGenerateReminders, saving }: Props) {
  const [doctorSummary, setDoctorSummary] = useState("");
  const [patientDraft, setPatientDraft] = useState("");
  const [patientExplanation, setPatientExplanation] = useState("");
  const [flags, setFlags] = useState("");
  const [reminders, setReminders] = useState("");

  useEffect(() => {
    setDoctorSummary(report.doctor_summary || "");
    setPatientDraft(report.patient_discharge_draft || "");
    setPatientExplanation(report.simplified_explanation || "");
    setFlags((report.clinical_review_flags || []).join("\n"));
    setReminders((report.reminder_candidates || []).join("\n"));
  }, [report]);

  const canEdit = report.status === "DRAFT";
  const badgeTone = report.status === "APPROVED" ? "approved" : "draft";

  const savePayload = useMemo(
    () => ({
      doctor_summary: doctorSummary,
      patient_discharge_draft: patientDraft,
      simplified_explanation: patientExplanation,
      clinical_review_flags: flags.split("\n").map((item) => item.trim()).filter(Boolean),
      reminder_candidates: reminders.split("\n").map((item) => item.trim()).filter(Boolean),
    }),
    [doctorSummary, patientDraft, patientExplanation, flags, reminders]
  );

  return (
    <PanelShell
      title="Doctor review and approval"
      subtitle="Editable doctor-authored layer. This is the only place approval can happen."
      rightSlot={<StatusBadge tone={badgeTone}>{report.status.toLowerCase()}</StatusBadge>}
    >
      <div className="editor-grid">
        <label>
          <span>Doctor summary</span>
          <textarea value={doctorSummary} onChange={(e) => setDoctorSummary(e.target.value)} disabled={!canEdit || saving} rows={5} />
        </label>
        <label>
          <span>Patient discharge draft</span>
          <textarea value={patientDraft} onChange={(e) => setPatientDraft(e.target.value)} disabled={!canEdit || saving} rows={5} />
        </label>
        <label>
          <span>Patient explanation</span>
          <textarea value={patientExplanation} onChange={(e) => setPatientExplanation(e.target.value)} disabled={!canEdit || saving} rows={5} />
        </label>
        <label>
          <span>Clinical review flags (one per line)</span>
          <textarea value={flags} onChange={(e) => setFlags(e.target.value)} disabled={!canEdit || saving} rows={5} />
        </label>
        <label>
          <span>Reminder candidates (one per line)</span>
          <textarea value={reminders} onChange={(e) => setReminders(e.target.value)} disabled={!canEdit || saving} rows={5} />
        </label>
      </div>

      <div className="panel-actions">
        {canEdit ? (
          <button className="primary-button" disabled={saving} onClick={() => void onSave(savePayload)}>
            {saving ? "Saving..." : "Save edits"}
          </button>
        ) : null}

        {canEdit ? (
          <button disabled={saving} onClick={() => void onApprove()}>
            {saving ? "Processing..." : "Approve final report"}
          </button>
        ) : null}

        {report.status === "APPROVED" ? (
          <button disabled={saving} onClick={() => void onGenerateReminders()}>
            {saving ? "Generating..." : "Generate reminders from approved report"}
          </button>
        ) : null}
      </div>
    </PanelShell>
  );
}