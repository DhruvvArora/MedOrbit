import { useEffect, useState } from "react";
import Navbar from "./components/layout/Navbar";
import Hero from "./components/sections/Hero";
import "./index.css";
import "./styles/theme.css";
import "./styles/doctor.css";
import "./styles/patient.css";
import "./styles/auth.css";
import { parseRoute } from "./pages/Doctor/router";
import { DoctorDashboardPage } from "./pages/Doctor/DoctorDashboardPage";
import { DoctorWorkspacePage } from "./pages/Doctor/DoctorWorkspacePage";
import { DoctorReviewPage } from "./pages/Doctor/DoctorReviewPage";
import { LiveConsultationPage } from "./pages/Doctor/LiveConsultationPage";
import { DemoReviewPage } from "./pages/Doctor/DemoReviewPage";
import { parsePatientRoute } from "./pages/Patient/router";
import { PatientDashboardPage } from "./pages/Patient/PatientDashboardPage";
import { PatientVisitDetailPage } from "./pages/Patient/PatientVisitDetailPage";
import { ProtectedRoute } from "./components/auth/ProtectedRoute";
import { LoginPage } from "./pages/Auth/LoginPage";
import { RegisterPage } from "./pages/Auth/RegisterPage";

function App() {
  const [path, setPath] = useState(window.location.pathname);

  useEffect(() => {
    const listener = () => setPath(window.location.pathname);
    window.addEventListener("popstate", listener);
    return () => window.removeEventListener("popstate", listener);
  }, []);

  const isDoctorPath = path.startsWith("/doctor");
  const isPatientPath = path.startsWith("/patient");
  const isLoginPath = path === "/login";
  const isRegisterPath = path === "/register";

  /* ── Auth Pages ───────────────────────────────────────── */
  if (isLoginPath) {
    return (
      <div className="app-shell">
        <LoginPage />
      </div>
    );
  }

  if (isRegisterPath) {
    return (
      <div className="app-shell">
        <RegisterPage />
      </div>
    );
  }

  /* ── Doctor Routes (Protected) ────────────────────────── */
  if (isDoctorPath) {
    const route = parseRoute(path);

    return (
      <ProtectedRoute requiredRole="doctor">
        <div className="app-shell doctor-app-shell">
          {route.name === "doctor-dashboard" ? <DoctorDashboardPage /> : null}
          {route.name === "doctor-workspace" ? (
            <DoctorWorkspacePage visitId={route.visitId} />
          ) : null}
          {route.name === "doctor-review" ? (
            <DoctorReviewPage visitId={route.visitId} />
          ) : null}
          {route.name === "doctor-live-consultation" ? (
            <LiveConsultationPage />
          ) : null}
          {route.name === "doctor-live-consultation-review" ? (
            <DemoReviewPage />
          ) : null}
        </div>
      </ProtectedRoute>
    );
  }

  /* ── Patient Routes (Protected) ───────────────────────── */
  if (isPatientPath) {
    const route = parsePatientRoute(path);

    return (
      <ProtectedRoute requiredRole="patient">
        <div className="app-shell patient-app-shell">
          {route.name === "patient-dashboard" ? <PatientDashboardPage /> : null}
          {route.name === "patient-visit-detail" ? (
            <PatientVisitDetailPage visitId={route.visitId} />
          ) : null}
        </div>
      </ProtectedRoute>
    );
  }

  /* ── Landing Page (Public) ────────────────────────────── */
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