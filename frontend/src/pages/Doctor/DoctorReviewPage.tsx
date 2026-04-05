import React, { useState } from "react";
import { DoctorShell } from "../../components/doctor/DoctorShell";
import { ReviewEditor } from "../../components/doctor/ReviewEditor";
import { ErrorState } from "../../components/shared/ErrorState";
import { LoadingState } from "../../components/shared/LoadingState";
import { useAsyncResource } from "../../hooks/useAsyncResource";
import { doctorApi } from "../../lib/api/doctor";
import type { VisitReport } from "../../types/doctor";
import { navigate } from "./router";

export function DoctorReviewPage({ visitId }: { visitId: string }) {
  const { data, loading, error, refresh, setData } = useAsyncResource(() => doctorApi.getReport(visitId), [visitId]);
  const [saving, setSaving] = useState(false);
  const [flashMessage, setFlashMessage] = useState<string | null>(null);

  async function doSave(payload: Partial<VisitReport>) {
    setSaving(true);
    try {
      const next = await doctorApi.updateReport(visitId, payload);
      setData(next);
      setFlashMessage("Draft saved.");
    } catch (err) {
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
      setFlashMessage("Report approved. Patient-safe outputs can now be consumed downstream.");
    } catch (err) {
      setFlashMessage(err instanceof Error ? err.message : "Unable to approve report");
    } finally {
      setSaving(false);
    }
  }

  async function doGenerateReminders() {
    setSaving(true);
    try {
      const items = await doctorApi.generateReminders(visitId);
      setFlashMessage(`Generated ${items.length} reminders from the approved report.`);
      await refresh();
    } catch (err) {
      setFlashMessage(err instanceof Error ? err.message : "Unable to generate reminders");
    } finally {
      setSaving(false);
    }
  }

  if (loading) return <LoadingState label="Loading doctor review screen..." />;
  if (error || !data) return <ErrorState message={error || "Review screen unavailable"} onRetry={() => void refresh()} />;

  return (
    <DoctorShell
      title="Review, edit, and approve"
      subtitle="This is the doctor-controlled layer before patient-safe release."
      actions={<button onClick={() => navigate(`/doctor/visits/${visitId}/workspace`)}>Back to workspace</button>}
    >
      {flashMessage ? <div className="flash-banner">{flashMessage}</div> : null}
      <ReviewEditor
        report={data}
        onSave={doSave}
        onApprove={doApprove}
        onGenerateReminders={doGenerateReminders}
        saving={saving}
      />
    </DoctorShell>
  );
}
