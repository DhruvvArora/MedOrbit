import React from "react";

const statConfig = [
  ["Total visits", "total"],
  ["Active", "active"],
  ["Draft reports", "draft_reports"],
  ["Approved", "approved_reports"],
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
