import { useEffect, useState } from "react";
import Navbar from "./components/layout/Navbar";
import Hero from "./components/sections/Hero";
import "./index.css";
import "./styles/theme.css";
import "./styles/doctor.css";
import { parseRoute } from "./pages/Doctor/router";
import { DoctorDashboardPage } from "./pages/Doctor/DoctorDashboardPage";
import { DoctorWorkspacePage } from "./pages/Doctor/DoctorWorkspacePage";
import { DoctorReviewPage } from "./pages/Doctor/DoctorReviewPage";

function App() {
  const [path, setPath] = useState(window.location.pathname);

  useEffect(() => {
    const listener = () => setPath(window.location.pathname);
    window.addEventListener("popstate", listener);
    return () => window.removeEventListener("popstate", listener);
  }, []);

  const isDoctorPath = path.startsWith("/doctor");

  if (isDoctorPath) {
    const route = parseRoute(path);

    return (
      <div className="app-shell doctor-app-shell">
        {route.name === "doctor-dashboard" ? <DoctorDashboardPage /> : null}
        {route.name === "doctor-workspace" ? (
          <DoctorWorkspacePage visitId={route.visitId} />
        ) : null}
        {route.name === "doctor-review" ? (
          <DoctorReviewPage visitId={route.visitId} />
        ) : null}
      </div>
    );
  }

  return (
    <div className="app-shell">
      <Navbar />
      <main>
        <Hero />
      </main>
    </div>
  );
}

export default App;