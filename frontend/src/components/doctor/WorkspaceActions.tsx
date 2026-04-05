import React from "react";

export interface WorkspaceActionHandlers {
  onRefresh: () => void;
  onRunBehavioral: () => void;
  onRunTriage: () => void;
  onRunOrchestration: () => void;
  onOpenReview: () => void;
  onApprove: () => void;
  onStartVisit: () => void;
  onCompleteVisit: () => void;
}

export function WorkspaceActions({
  canStart,
  canComplete,
  canReview,
  canApprove,
  handlers,
  busy,
}: {
  canStart: boolean;
  canComplete: boolean;
  canReview: boolean;
  canApprove: boolean;
  handlers: WorkspaceActionHandlers;
  busy: boolean;
}) {
  return (
    <div className="workspace-actions">
      <button onClick={handlers.onRefresh} disabled={busy}>Refresh</button>
      <button onClick={handlers.onRunBehavioral} disabled={busy}>Generate Behavioral Insights</button>
      <button onClick={handlers.onRunTriage} disabled={busy}>Generate Triage Draft</button>
      <button className="primary-button" onClick={handlers.onRunOrchestration} disabled={busy}>
        {busy ? "Working..." : "Generate Report"}
      </button>

      {canReview ? <button onClick={handlers.onOpenReview} disabled={busy}>Review Report</button> : null}
      {canApprove ? <button onClick={handlers.onApprove} disabled={busy}>Approve report</button> : null}
      {canStart ? <button onClick={handlers.onStartVisit} disabled={busy}>Start visit</button> : null}
      {canComplete ? <button onClick={handlers.onCompleteVisit} disabled={busy}>Complete visit</button> : null}
    </div>
  );
}