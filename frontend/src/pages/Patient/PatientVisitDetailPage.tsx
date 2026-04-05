import React, { useState, useCallback } from "react";
import { useAsyncResource } from "../../hooks/useAsyncResource";
import { patientApi } from "../../lib/api/patient";
import { PatientShell } from "../../components/patient/PatientShell";
import { CareStatusBanner } from "../../components/patient/CareStatusBanner";
import { ApprovedReportSection } from "../../components/patient/ApprovedReportSection";
import { SimplifiedExplanationCard } from "../../components/patient/SimplifiedExplanationCard";
import { ReminderList } from "../../components/patient/ReminderList";
import { ExplainChat } from "../../components/patient/ExplainChat";
import { LoadingState } from "../../components/shared/LoadingState";
import { ErrorState } from "../../components/shared/ErrorState";
import { navigate } from "./router";
import type { PatientReminder } from "../../types/patient";

interface Props {
  visitId: string;
}

export function PatientVisitDetailPage({ visitId }: Props) {
  const {
    data: visit,
    loading,
    error,
    refresh,
  } = useAsyncResource(() => patientApi.getVisitDetail(visitId), [visitId]);

  const {
    data: allReminders,
    setData: setReminders,
    refresh: refreshReminders,
  } = useAsyncResource(() => patientApi.getReminders(), []);

  /* Filter reminders to this visit */
  const visitReminders: PatientReminder[] = (allReminders ?? []).filter(
    (r) => String(r.visit_id) === String(visitId),
  );

  /* Optimistic reminder mark-complete */
  async function handleMarkComplete(id: number) {
    if (!allReminders) return;

    setReminders(
      allReminders.map((r) =>
        r.id === id ? { ...r, status: "COMPLETED" as const } : r,
      ),
    );

    try {
      await patientApi.updateReminderStatus(id, "COMPLETED");
    } catch {
      void refreshReminders("soft");
    }
  }

  if (loading) return <LoadingState label="Loading your care details..." />;
  if (error || !visit) {
    return (
      <ErrorState
        message={error || "Visit details unavailable"}
        onRetry={() => void refresh("initial")}
      />
    );
  }

  return (
    <PatientShell
      title={visit.title}
      subtitle={visit.startedAt
        ? new Date(visit.startedAt).toLocaleDateString("en-US", {
          weekday: "long",
          month: "long",
          day: "numeric",
          year: "numeric",
        })
        : undefined}
      actions={
        <button onClick={() => navigate("/patient/dashboard")}>
          ← Back to Dashboard
        </button>
      }
    >
      {/* ── Status Banner ──────────────────────────────── */}
      {visit.hasApprovedReport ? (
        <CareStatusBanner tone="approved">
          This report has been reviewed and approved by your doctor.
        </CareStatusBanner>
      ) : (
        <CareStatusBanner tone="pending">
          Your doctor is still reviewing this report. Check back soon.
        </CareStatusBanner>
      )}

      {/* ── Approved Report ────────────────────────────── */}
      {visit.hasApprovedReport && visit.approvedInstructions ? (
        <ApprovedReportSection
          approvedInstructions={visit.approvedInstructions}
        />
      ) : null}

      {/* ── Simplified Explanation ─────────────────────── */}
      {visit.hasApprovedReport && visit.simplifiedExplanation ? (
        <SimplifiedExplanationCard
          explanation={visit.simplifiedExplanation}
        />
      ) : null}

      {/* ── Reminders ──────────────────────────────────── */}
      {visit.hasApprovedReport ? (
        <ReminderList
          reminders={visitReminders}
          onMarkComplete={handleMarkComplete}
        />
      ) : null}

      {/* ── Explain Chat ───────────────────────────────── */}
      <ExplainChat
        visitId={visitId}
        hasApprovedReport={visit.hasApprovedReport}
      />
    </PatientShell>
  );
}
