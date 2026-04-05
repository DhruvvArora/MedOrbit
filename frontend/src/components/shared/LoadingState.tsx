import React from "react";

export function LoadingState({ label = "Loading..." }: { label?: string }) {
  return (
    <div className="loading-state">
      <div className="loading-spinner" />
      <span>{label}</span>
    </div>
  );
}