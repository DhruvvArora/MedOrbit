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
      <button onClick={handlers.onRefresh}>Refresh workspace</button>
      <button onClick={handlers.onRunBehavioral} disabled={busy}>Run behavioral analysis</button>
      <button onClick={handlers.onRunTriage} disabled={busy}>Run triage analysis</button>
      <button onClick={handlers.onRunOrchestration} disabled={busy}>Run orchestration</button>
      <button onClick={handlers.onOpenReview} disabled={!canReview}>Open review / edit</button>
      <button onClick={handlers.onApprove} disabled={!canApprove || busy}>Approve report</button>
      {canStart ? <button onClick={handlers.onStartVisit}>Start visit</button> : null}
      {canComplete ? <button onClick={handlers.onCompleteVisit}>Complete visit</button> : null}
    </div>
  );
}
