import React from "react";
import { useAsyncResource } from "../../hooks/useAsyncResource";
import { patientApi } from "../../lib/api/patient";
import { PatientShell } from "../../components/patient/PatientShell";
import { PatientVisitList } from "../../components/patient/PatientVisitList";
import { ReminderList } from "../../components/patient/ReminderList";
import { LoadingState } from "../../components/shared/LoadingState";
import { ErrorState } from "../../components/shared/ErrorState";
import { navigate } from "./router";

export function PatientDashboardPage() {
  const { data, loading, refreshing, error, refresh, setData } = useAsyncResource(
    () => patientApi.getDashboard(),
    [],
  );

  if (loading) return <LoadingState label="Loading your care overview..." />;
  if (error || !data) {
    return (
      <ErrorState
        message={error || "Dashboard unavailable"}
        onRetry={() => void refresh("initial")}
      />
    );
  }

  /* Optimistic reminder mark-complete */
  async function handleMarkComplete(id: number) {
    if (!data) return;
    // Optimistic update
    setData({
      ...data,
      recentReminders: data.recentReminders.map((r) =>
        r.id === id ? { ...r, status: "COMPLETED" as const } : r,
      ),
    });

    try {
      await patientApi.updateReminderStatus(id, "COMPLETED");
    } catch {
      // Revert on failure
      void refresh("soft");
    }
  }

  const pendingReminders = data.recentReminders.filter((r) => r.status === "PENDING");

  return (
    <PatientShell
      title={`Welcome back, ${data.patientName.split(" ")[0]} 👋`}
      subtitle="Here's your care overview"
      actions={
        <button onClick={() => void refresh("soft")} disabled={refreshing}>
          {refreshing ? "Refreshing..." : "Refresh"}
        </button>
      }
    >
      {/* ── Stats ──────────────────────────────────────── */}
      <div className="pt-stats-grid">
        <div className="pt-stat-card">
          <span>Visits</span>
          <strong>{data.visitCount}</strong>
        </div>
        <div className="pt-stat-card">
          <span>Under Review</span>
          <strong>{data.pendingReportCount}</strong>
        </div>
        <div className="pt-stat-card">
          <span>Care Tasks</span>
          <strong>{pendingReminders.length}</strong>
        </div>
      </div>

      {/* ── Visits ─────────────────────────────────────── */}
      <div className="pt-section-title">
        <span className="pt-icon">📅</span> Your Visits
      </div>
      <PatientVisitList
        visits={data.visits}
        onOpenVisit={(visitId) => navigate(`/patient/visits/${visitId}`)}
      />

      {/* ── Reminders ──────────────────────────────────── */}
      {data.recentReminders.length > 0 ? (
        <>
          <div className="pt-section-title">
            <span className="pt-icon">📋</span> Upcoming Care Tasks
          </div>
          <ReminderList
            reminders={data.recentReminders}
            onMarkComplete={handleMarkComplete}
            title="All Tasks"
          />
        </>
      ) : null}
    </PatientShell>
  );
}
