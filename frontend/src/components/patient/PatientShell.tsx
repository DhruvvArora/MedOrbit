import { useAuth } from "../../context/AuthContext";

interface Props {
  title: string;
  subtitle?: string;
  actions?: React.ReactNode;
  children: React.ReactNode;
}

function navigateTo(path: string) {
  window.history.pushState({}, "", path);
  window.dispatchEvent(new PopStateEvent("popstate"));
}

export function PatientShell({ title, subtitle, actions, children }: Props) {
  const { logout } = useAuth();

  return (
    <div className="patient-shell">
      <header className="patient-shell__header">
        <div>
          <p className="patient-shell__eyebrow">
            <span
              onClick={() => navigateTo("/")}
              style={{
                cursor: "pointer",
                marginRight: "8px",
                fontWeight: 700,
                color: "var(--teal-deep)",
              }}
            >
              MedOrbit
            </span>
            Patient Portal
          </p>
          <h1>{title}</h1>
          {subtitle ? <p className="patient-shell__subtitle">{subtitle}</p> : null}
        </div>

        <div
          className="patient-shell__actions"
          style={{ display: "flex", gap: "8px", alignItems: "center" }}
        >
          <button onClick={() => navigateTo("/")}>Home</button>
          <button className="primary-button" onClick={() => navigateTo("/patient/dashboard")}>
            Dashboard
          </button>
          {actions}
          <button
            onClick={logout}
            style={{
              padding: "8px 16px",
              border: "1px solid rgba(31,36,33,0.12)",
              borderRadius: "12px",
              background: "rgba(255,255,255,0.5)",
              backdropFilter: "blur(4px)",
              color: "var(--text-muted)",
              fontSize: "0.85rem",
              fontWeight: 600,
              cursor: "pointer",
              transition: "all 0.2s",
            }}
          >
            Logout
          </button>
        </div>
      </header>
      {children}
    </div>
  );
}