import type { PatientReminder } from "../../types/patient";

interface Props {
  reminder: PatientReminder;
  onMarkComplete: (id: number) => void;
}

function formatDue(iso: string): string {
  try {
    return new Date(iso).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
    });
  } catch {
    return "";
  }
}

export function ReminderCard({ reminder, onMarkComplete }: Props) {
  const isCompleted = reminder.status === "COMPLETED";

  return (
    <div className={`pt-reminder-card ${isCompleted ? "pt-reminder-card--completed" : ""}`}>
      <div className="pt-reminder-card__info">
        <h4>{reminder.title}</h4>
        <p>Due: {formatDue(reminder.due_at)}</p>
      </div>

      {isCompleted ? (
        <span className="pt-reminder-done">✓ Done</span>
      ) : (
        <button className="pt-btn-sm" onClick={() => onMarkComplete(reminder.id)}>
          Complete
        </button>
      )}
    </div>
  );
}
