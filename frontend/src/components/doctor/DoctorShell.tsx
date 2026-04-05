import React from "react";
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

export function DoctorShell({ title, subtitle, actions, children }: Props) {
  const { logout, user } = useAuth();
  const homePath = user?.role === "doctor" ? "/doctor/dashboard" : "/patient/dashboard";

  return (
    <div className="doctor-shell">
      <header className="doctor-shell__header">
        <div>
          <p className="eyebrow">
            <span
              className="doctor-shell__brand"
              onClick={() => navigateTo(homePath)}
              style={{ cursor: "pointer", marginRight: "8px" }}
            >
              MedOrbit
            </span>
            {user?.role === "doctor" ? "Doctor workspace" : "Consultation workspace"}
          </p>
          <h1>{title}</h1>
          {subtitle ? <p className="doctor-shell__subtitle">{subtitle}</p> : null}
        </div>
        <div className="doctor-shell__actions" style={{ display: "flex", gap: "8px", alignItems: "center" }}>
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
