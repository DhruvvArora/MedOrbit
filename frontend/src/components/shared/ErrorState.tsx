import React from "react";

export function ErrorState({ message, onRetry }: { message: string; onRetry?: () => void }) {
  return (
    <div className="error-state">
      <strong>Something needs attention</strong>
      <p>{message}</p>
      {onRetry ? <button onClick={onRetry}>Try again</button> : null}
    </div>
  );
}