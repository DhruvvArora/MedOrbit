import React, { useEffect, useState } from "react";
import { DoctorShell } from "../../components/doctor/DoctorShell";
import { VisitHeader } from "../../components/doctor/VisitHeader";
import { TranscriptPanel } from "../../components/doctor/TranscriptPanel";
import { AgentInsightPanel } from "../../components/doctor/AgentInsightPanel";
import { DraftReportPanel } from "../../components/doctor/DraftReportPanel";
import { WorkspaceActions } from "../../components/doctor/WorkspaceActions";
import { ErrorState } from "../../components/shared/ErrorState";
import { LoadingState } from "../../components/shared/LoadingState";
import { useAsyncResource } from "../../hooks/useAsyncResource";
import { doctorApi } from "../../lib/api/doctor";
import type { BehavioralInsights, TriageSummary } from "../../types/doctor";
import { navigate } from "./router";

export function DoctorWorkspacePage({ visitId }: { visitId: string }) {
  const { data, loading, refreshing, error, refresh } = useAsyncResource(() => doctorApi.getWorkspace(visitId), [visitId]);
  const [behavioral, setBehavioral] = useState<BehavioralInsights | null>(null);
  const [triage, setTriage] = useState<TriageSummary | null>(null);
  const [busy, setBusy] = useState(false);
  const [flashMessage, setFlashMessage] = useState<string | null>(null);
  const [flashTone, setFlashTone] = useState<"success" | "error">("success");

  useEffect(() => {
    if (!flashMessage) return;
    const timer = window.setTimeout(() => setFlashMessage(null), 3200);
    return () => window.clearTimeout(timer);
  }, [flashMessage]);

  async function runAction(action: () => Promise<unknown>, successMessage: string, refreshAfter = false) {
    setBusy(true);
    setFlashMessage(null);

    try {
      const result = await action();
      if (successMessage) {
        setFlashTone("success");
        setFlashMessage(successMessage);
      }
      if (refreshAfter) await refresh("soft");
      return result;
    } catch (err) {
      setFlashTone("error");
      setFlashMessage(err instanceof Error ? err.message : "Action failed");
      return null;
    } finally {
      setBusy(false);
    }
  }

  if (loading) return <LoadingState label="Loading consultation workspace..." />;
  if (error || !data) return <ErrorState message={error || "Workspace unavailable"} onRetry={() => void refresh("initial")} />;

  const canReview = data.report_status.exists;
  const canApprove = data.report_status.status === "draft";

  return (
    <DoctorShell
      title="Consultation workspace"
      subtitle="Raw transcript, AI drafts, and doctor approval are intentionally separated."
      actions={<button onClick={() => navigate("/doctor/dashboard")}>Back to dashboard</button>}
    >
      <VisitHeader visit={data.visit} />
      {flashMessage ? <div className={`flash-banner flash-banner--${flashTone}`}>{flashMessage}</div> : null}
      <WorkspaceActions
        canStart={data.visit.status === "scheduled"}
        canComplete={data.visit.status === "active"}
        canReview={canReview}
        canApprove={canApprove}
        busy={busy || refreshing}
        handlers={{
          onRefresh: () => void refresh("soft"),
          onRunBehavioral: () =>
            void runAction(async () => {
              const result = await doctorApi.runBehavioral(visitId);
              setBehavioral(result);
            }, "Behavioral draft refreshed."),
          onRunTriage: () =>
            void runAction(async () => {
              const result = await doctorApi.runTriage(visitId);
              setTriage(result);
            }, "Triage draft refreshed."),
          onRunOrchestration: () =>
            void runAction(() => doctorApi.runOrchestration(visitId), "Draft report generated or updated.", true),
          onOpenReview: () => navigate(`/doctor/visits/${visitId}/review`),
          onApprove: () => void runAction(() => doctorApi.approveReport(visitId), "Report approved.", true),
          onStartVisit: () => void runAction(() => doctorApi.startVisit(visitId), "Visit started.", true),
          onCompleteVisit: () => void runAction(() => doctorApi.completeVisit(visitId), "Visit completed.", true),
        }}
      />
      <div className="workspace-grid">
        <TranscriptPanel chunks={data.transcript_chunks} stats={data.transcript_stats} />
        <AgentInsightPanel behavioral={behavioral} triage={triage} />
      </div>
      <DraftReportPanel
        reportStatus={data.report_status}
        reportPreview={data.report_preview}
        onOpenReview={() => navigate(`/doctor/visits/${visitId}/review`)}
      />
    </DoctorShell>
  );
}