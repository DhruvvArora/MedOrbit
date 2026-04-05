import { useAuth } from "../../context/AuthContext";

function navigateTo(path: string) {
  window.history.pushState({}, "", path);
  window.dispatchEvent(new PopStateEvent("popstate"));
}

export default function Navbar() {
  const { isAuthenticated, user, logout } = useAuth();

  return (
    <header className="navbar">
      <div className="navbar-inner">
        <div className="brand" onClick={() => navigateTo("/")} style={{ cursor: "pointer" }}>
          MedOrbit
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          {isAuthenticated && user ? (
            <>
              <button
                className="nav-cta"
                onClick={() => {
                  const target = user.role === "doctor"
                    ? "/doctor/dashboard"
                    : "/patient/dashboard";
                  navigateTo(target);
                }}
              >
                Dashboard
              </button>
              <button
                className="nav-cta"
                onClick={logout}
                style={{
                  background: "rgba(255,255,255,0.6)",
                  color: "var(--text-muted)",
                  backdropFilter: "blur(8px)",
                }}
              >
                Logout
              </button>
            </>
          ) : (
            <button className="nav-cta" onClick={() => navigateTo("/login")}>
              Login
            </button>
          )}
        </div>
      </div>
    </header>
  );
}