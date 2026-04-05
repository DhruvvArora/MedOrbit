import React, { useEffect, useState } from "react";
import { DoctorShell } from "../../components/doctor/DoctorShell";
import { ReviewEditor } from "../../components/doctor/ReviewEditor";
import { ErrorState } from "../../components/shared/ErrorState";
import { LoadingState } from "../../components/shared/LoadingState";
import { useAsyncResource } from "../../hooks/useAsyncResource";
import { doctorApi } from "../../lib/api/doctor";
import type { VisitReport } from "../../types/doctor";
import { navigate } from "./router";

export function DoctorReviewPage({ visitId }: { visitId: string }) {
  const { data, loading, refreshing, error, refresh, setData } = useAsyncResource(() => doctorApi.getReport(visitId), [visitId]);
  const [saving, setSaving] = useState(false);
  const [flashMessage, setFlashMessage] = useState<string | null>(null);
  const [flashTone, setFlashTone] = useState<"success" | "error">("success");

  useEffect(() => {
    if (!flashMessage) return;
    const timer = window.setTimeout(() => setFlashMessage(null), 3200);
    return () => window.clearTimeout(timer);
  }, [flashMessage]);

  async function doSave(payload: Partial<VisitReport>) {
    setSaving(true);
    try {
      const next = await doctorApi.updateReport(visitId, payload);
      setData(next);
      setFlashTone("success");
      setFlashMessage("Draft saved.");
    } catch (err) {
      setFlashTone("error");
      setFlashMessage(err instanceof Error ? err.message : "Unable to save report");
    } finally {
      setSaving(false);
    }
  }

  async function doApprove() {
    setSaving(true);
    try {
      const next = await doctorApi.approveReport(visitId);
      setData(next);
      setFlashTone("success");
      setFlashMessage("Report approved. Patient-safe outputs can now be consumed downstream.");
    } catch (err) {
      setFlashTone("error");
      setFlashMessage(err instanceof Error ? err.message : "Unable to approve report");
    } finally {
      setSaving(false);
    }
  }

  async function doGenerateReminders() {
    setSaving(true);
    try {
      const items = await doctorApi.generateReminders(visitId);
      setFlashTone("success");
      setFlashMessage(`Generated ${items.length} reminders from the approved report.`);
      await refresh("soft");
    } catch (err) {
      setFlashTone("error");
      setFlashMessage(err instanceof Error ? err.message : "Unable to generate reminders");
    } finally {
      setSaving(false);
    }
  }

  if (loading) return <LoadingState label="Loading doctor review screen..." />;
  if (error || !data) return <ErrorState message={error || "Review screen unavailable"} onRetry={() => void refresh("initial")} />;

  return (
    <DoctorShell
      title="Review and Approve"
      subtitle="Review the draft, make edits, and approve the final version."
      actions={
        <button onClick={() => navigate(`/doctor/visits/${visitId}/workspace`)} disabled={refreshing}>
          Back to workspace
        </button>
      }
    >
      {flashMessage ? <div className={`flash-banner flash-banner--${flashTone}`}>{flashMessage}</div> : null}
      <ReviewEditor
        report={data}
        onSave={doSave}
        onApprove={doApprove}
        onGenerateReminders={doGenerateReminders}
        saving={saving || refreshing}
      />
    </DoctorShell>
  );
}