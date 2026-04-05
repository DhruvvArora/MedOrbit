
interface Props {
  /** Mapped from patient_discharge_draft – labelled patient-safe. */
  approvedInstructions: string;
}

export function ApprovedReportSection({ approvedInstructions }: Props) {
  return (
    <section className="pt-card pt-report-section">
      <div className="pt-report-section__header">
        <span className="pt-badge pt-badge--approved">✓ Doctor-Approved</span>
        <h3>Your Approved Care Instructions</h3>
      </div>
      <div className="pt-report-content">{approvedInstructions}</div>
    </section>
  );
}
