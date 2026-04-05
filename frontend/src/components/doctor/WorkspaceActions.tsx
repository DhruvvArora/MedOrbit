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
      <div className="workspace-actions__group">
        <button onClick={handlers.onRefresh} disabled={busy}>Refresh workspace</button>
        <button onClick={handlers.onRunBehavioral} disabled={busy}>Run behavioral analysis</button>
        <button onClick={handlers.onRunTriage} disabled={busy}>Run triage analysis</button>
        <button className="primary-button" onClick={handlers.onRunOrchestration} disabled={busy}>
          {busy ? "Working..." : "Run orchestration"}
        </button>
      </div>

      <div className="workspace-actions__group">
        <button onClick={handlers.onOpenReview} disabled={!canReview || busy}>Open review / edit</button>
        <button onClick={handlers.onApprove} disabled={!canApprove || busy}>Approve report</button>
        {canStart ? <button onClick={handlers.onStartVisit} disabled={busy}>Start visit</button> : null}
        {canComplete ? <button onClick={handlers.onCompleteVisit} disabled={busy}>Complete visit</button> : null}
      </div>
    </div>
  );
}