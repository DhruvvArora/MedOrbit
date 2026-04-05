import React from "react";

interface Props {
  title: string;
  subtitle?: string;
  rightSlot?: React.ReactNode;
  children: React.ReactNode;
}

export function PanelShell({ title, subtitle, rightSlot, children }: Props) {
  return (
    <section className="panel-shell">
      <header className="panel-shell__header">
        <div>
          <h3>{title}</h3>
          {subtitle ? <p>{subtitle}</p> : null}
        </div>
        {rightSlot ? <div>{rightSlot}</div> : null}
      </header>
      <div className="panel-shell__body">{children}</div>
    </section>
  );
}
