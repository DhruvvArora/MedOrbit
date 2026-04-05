import React from "react";

const statConfig = [
  ["Total Visits", "total"],
  ["In progress", "active"],
  ["Drafts ready", "draft_reports"],
  ["Approved Reports", "approved_reports"],
] as const;

export function DoctorDashboardStats({ counts }: { counts: Record<string, number> }) {
  return (
    <div className="stats-grid">
      {statConfig.map(([label, key]) => (
        <article key={key} className="stat-card">
          <span>{label}</span>
          <strong>{counts[key] ?? 0}</strong>
        </article>
      ))}
    </div>
  );
}
