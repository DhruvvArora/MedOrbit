import React from "react";
import type { DoctorVisitListItem } from "../../types/doctor";
import { StatusBadge } from "../shared/StatusBadge";

function reportTone(status: DoctorVisitListItem["report_status"]) {
  if (status === "approved") return "approved" as const;
  if (status === "draft") return "draft" as const;
  return "neutral" as const;
}

export function DoctorVisitCard({ visit, onOpen }: { visit: DoctorVisitListItem; onOpen: (visitId: string) => void }) {
  return (
    <article className="visit-card">
      <div className="visit-card__top">
        <div>
          <h3>{visit.title || "Untitled visit"}</h3>
          <p>{visit.patient_name}</p>
        </div>
        <div className="visit-card__badges">
          <StatusBadge tone={visit.status === "active" ? "active" : "neutral"}>{visit.status}</StatusBadge>
          <StatusBadge tone={reportTone(visit.report_status)}>{visit.report_status === "none" ? "no report" : visit.report_status}</StatusBadge>
        </div>
      </div>
      <div className="visit-card__meta">
        <span>{visit.type === "virtual" ? "Virtual" : "In person"}</span>
        <span>{visit.transcript_chunk_count} transcript chunks</span>
      </div>
      <button onClick={() => onOpen(visit.id)} className="primary-button">Open workspace</button>
    </article>
  );
}
