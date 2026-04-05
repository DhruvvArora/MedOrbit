
interface Props {
  title: string;
  subtitle?: string;
  actions?: React.ReactNode;
  children: React.ReactNode;
}

export function PatientShell({ title, subtitle, actions, children }: Props) {
  return (
    <div className="patient-shell">
      <header className="patient-shell__header">
        <div>
          <p className="patient-shell__eyebrow">Patient Portal</p>
          <h1>{title}</h1>
          {subtitle ? <p className="patient-shell__subtitle">{subtitle}</p> : null}
        </div>
        {actions ? <div className="patient-shell__actions">{actions}</div> : null}
      </header>
      {children}
    </div>
  );
}
