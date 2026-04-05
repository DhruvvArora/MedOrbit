import type { PatientVisitItem } from "../../types/patient";

interface Props {
  visit: PatientVisitItem;
  onClick: () => void;
}

function formatDate(iso: string | null): string {
  if (!iso) return "";
  try {
    return new Date(iso).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  } catch {
    return "";
  }
}

export function PatientVisitCard({ visit, onClick }: Props) {
  return (
    <article className="pt-card pt-visit-card" onClick={onClick} role="button" tabIndex={0}>
      <div className="pt-visit-card__top">
        <div>
          <h3>{visit.title}</h3>
          {visit.startedAt ? (
            <p className="pt-visit-card__meta">{formatDate(visit.startedAt)}</p>
          ) : null}
        </div>
        <span className={`pt-badge pt-badge--${visit.hasApprovedReport ? "approved" : "pending"}`}>
          {visit.hasApprovedReport ? "✓ Approved" : "⏳ Under Review"}
        </span>
      </div>

      {visit.hasApprovedReport ? (
        <p className="pt-visit-card__link">View your care details →</p>
      ) : (
        <p className="pt-visit-card__body">
          Your doctor is reviewing the report for this visit. Check back soon.
        </p>
      )}
    </article>
  );
}
