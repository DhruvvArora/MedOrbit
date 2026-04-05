import type { PatientReminder } from "../../types/patient";
import { ReminderCard } from "./ReminderCard";

interface Props {
  reminders: PatientReminder[];
  onMarkComplete: (id: number) => void;
  title?: string;
}

export function ReminderList({
  reminders,
  onMarkComplete,
  title = "Your Care Tasks",
}: Props) {
  /* Sort: pending first, then completed */
  const sorted = [...reminders].sort((a, b) => {
    if (a.status === "PENDING" && b.status !== "PENDING") return -1;
    if (a.status !== "PENDING" && b.status === "PENDING") return 1;
    return 0;
  });

  return (
    <section className="pt-card" style={{ marginBottom: "1.25rem" }}>
      <div className="pt-section-title">
        <span className="pt-icon">📋</span>
        {title}
      </div>

      {sorted.length === 0 ? (
        <p style={{ color: "var(--pt-muted)", fontSize: "0.95rem" }}>
          No care tasks right now. You're all set! 🎉
        </p>
      ) : (
        <div className="pt-reminder-list">
          {sorted.map((r) => (
            <ReminderCard key={r.id} reminder={r} onMarkComplete={onMarkComplete} />
          ))}
        </div>
      )}
    </section>
  );
}
