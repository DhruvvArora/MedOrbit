import React from "react";

interface Props {
  title: string;
  subtitle?: string;
  actions?: React.ReactNode;
  children: React.ReactNode;
}

export function DoctorShell({ title, subtitle, actions, children }: Props) {
  return (
    <div className="doctor-shell">
      <header className="doctor-shell__header">
        <div>
          <p className="eyebrow">Doctor workspace</p>
          <h1>{title}</h1>
          {subtitle ? <p className="doctor-shell__subtitle">{subtitle}</p> : null}
        </div>
        {actions ? <div className="doctor-shell__actions">{actions}</div> : null}
      </header>
      {children}
    </div>
  );
}
