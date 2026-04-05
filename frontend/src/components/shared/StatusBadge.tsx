import React from "react";

interface Props {
  tone: "neutral" | "draft" | "approved" | "warning" | "active";
  children: React.ReactNode;
}

export function StatusBadge({ tone, children }: Props) {
  return <span className={`status-badge status-badge--${tone}`}>{children}</span>;
}
