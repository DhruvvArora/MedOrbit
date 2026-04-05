import React from "react";
import type { ReportPreview, ReportStatusSummary } from "../../types/doctor";
import { PanelShell } from "../shared/PanelShell";
import { EmptyState } from "../shared/EmptyState";
import { StatusBadge } from "../shared/StatusBadge";

export function DraftReportPanel({ reportStatus, reportPreview, onOpenReview }: {
  reportStatus: ReportStatusSummary;
  reportPreview?: ReportPreview | null;
  onOpenReview: () => void;
}) {
  const tone = reportStatus.status === "approved" ? "approved" : reportStatus.status === "draft" ? "draft" : "warning";
  const label = reportStatus.status === "none" ? "no report" : reportStatus.status;

  return (
    <PanelShell
      title="Draft Report"
      subtitle="Review and refine the report before final approval."
      rightSlot={<StatusBadge tone={tone}>{label}</StatusBadge>}
    >
      {!reportPreview ? (
        <EmptyState
          title="No draft report yet"
          description="Generate a draft once enough transcript context is available."
        />
      ) : (
        <>
          <div className="report-preview">
            <div>
              <h4>Doctor summary</h4>
              <p>{reportPreview.doctor_summary || "No doctor summary yet."}</p>
            </div>
            <div>
              <h4>Patient explanation draft</h4>
              <p>{reportPreview.simplified_explanation || "No patient-facing explanation yet."}</p>
            </div>
            <div>
              <h4>Reminder candidates</h4>
              {reportPreview.reminder_candidates.length > 0 ? (
                <ul className="bullet-list">
                  {reportPreview.reminder_candidates.map((item, index) => <li key={`${item}-${index}`}>{item}</li>)}
                </ul>
              ) : (
                <p>No reminder candidates yet.</p>
              )}
            </div>
          </div>

          <div className="panel-actions">
            <button className="primary-button" onClick={onOpenReview}>
              Review Report
            </button>
          </div>
        </>
      )}
    </PanelShell>
  );
}