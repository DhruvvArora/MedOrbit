import type { ReactNode } from "react";
import { useAuth } from "../../context/AuthContext";

interface Props {
  title: string;
  subtitle?: string;
  actions?: ReactNode;
  children: ReactNode;
}

function navigateTo(path: string) {
  window.history.pushState({}, "", path);
  window.dispatchEvent(new PopStateEvent("popstate"));
}

export function DoctorShell({ title, subtitle, actions, children }: Props) {
  const { logout, user } = useAuth();

  const dashboardPath =
    user?.role === "doctor" ? "/doctor/dashboard" : "/patient/dashboard";

  const workspaceLabel =
    user?.role === "doctor"
      ? "Doctor workspace"
      : "Consultation workspace";

  return (
    <div className="doctor-shell">
      <header className="doctor-shell__header">
        <div>
          <p className="eyebrow">
            <span
              className="doctor-shell__brand"
              onClick={() => navigateTo("/")}
              style={{ cursor: "pointer", marginRight: "8px" }}
            >
              MedOrbit
            </span>
            {workspaceLabel}
          </p>
          <h1>{title}</h1>
          {subtitle ? <p className="doctor-shell__subtitle">{subtitle}</p> : null}
        </div>

        <div
          className="doctor-shell__actions"
          style={{ display: "flex", gap: "8px", alignItems: "center" }}
        >
          <button onClick={() => navigateTo("/")}>Home</button>
          <button className="primary-button" onClick={() => navigateTo(dashboardPath)}>
            Dashboard
          </button>
          {actions}
          <button onClick={logout}>Logout</button>
        </div>
      </header>

      {children}
    </div>
  );
}