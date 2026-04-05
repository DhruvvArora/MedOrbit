import type { PatientVisitItem } from "../../types/patient";
import { PatientVisitCard } from "./PatientVisitCard";
import { EmptyState } from "../shared/EmptyState";

interface Props {
  visits: PatientVisitItem[];
  onOpenVisit: (visitId: number) => void;
}

export function PatientVisitList({ visits, onOpenVisit }: Props) {
  if (visits.length === 0) {
    return (
      <EmptyState
        title="No visits yet"
        description="Your doctor will share your care details here after your next appointment."
      />
    );
  }

  return (
    <div className="pt-visit-list">
      {visits.map((v) => (
        <PatientVisitCard
          key={v.visitId}
          visit={v}
          onClick={() => onOpenVisit(v.visitId)}
        />
      ))}
    </div>
  );
}
