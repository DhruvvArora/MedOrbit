import React from "react";
import type { DoctorVisitListItem } from "../../types/doctor";
import { StatusBadge } from "../shared/StatusBadge";

export function VisitHeader({ visit }: { visit: DoctorVisitListItem }) {
  return (
    <section className="visit-header-card">
      <div>
        <p className="eyebrow">Visit workspace</p>
        <h2>{visit.title || "Consultation visit"}</h2>
        <p>{visit.patient_name}</p>
      </div>
      <div className="visit-header-card__meta">
        <StatusBadge tone={visit.status === "active" ? "active" : "neutral"}>{visit.status}</StatusBadge>
        <StatusBadge tone="neutral">{visit.type === "virtual" ? "Virtual" : "In person"}</StatusBadge>
        <StatusBadge tone={visit.report_status === "approved" ? "approved" : visit.report_status === "draft" ? "draft" : "warning"}>
          {visit.report_status === "none" ? "report pending" : `${visit.report_status} report`}
        </StatusBadge>
      </div>
    </section>
  );
}
