import { DoctorShell } from "../../components/doctor/DoctorShell";
import { DEMO_SESSION_KEY } from "./LiveConsultationPage";
import { navigate } from "./router";
import { useAuth } from "../../context/AuthContext";

interface DemoSession {
  visitId: string;
  chunks: string[];
  insights: string[];
  durationSecs: number;
  createdAt: string;
}

function loadDemoSession(): DemoSession | null {
  try {
    const raw = sessionStorage.getItem(DEMO_SESSION_KEY);
    return raw ? (JSON.parse(raw) as DemoSession) : null;
  } catch {
    return null;
  }
}

export function DemoReviewPage() {
  const session = loadDemoSession();
  const { user } = useAuth();
  const dashboardPath =
    user?.role === "doctor" ? "/doctor/dashboard" : "/patient/dashboard";

  if (!session) {
    return (
      <DoctorShell
        title="Session Review"
        subtitle="No live session data found."
        actions={
          <button onClick={() => navigate("/live-consultation")}>
            Start new consultation
          </button>
        }
      >
        <div className="empty-state" style={{ padding: "2rem" }}>
          <strong>No session data</strong>
          <p>
            This page is reached after completing a live consultation capture. Return to the
            landing page and start a new session.
          </p>
          <button
            className="primary-button"
            style={{ marginTop: "1.5rem" }}
            onClick={() => navigate("/")}
          >
            Back to home
          </button>
        </div>
      </DoctorShell>
    );
  }

  const duration = `${Math.floor(session.durationSecs / 60)}m ${session.durationSecs % 60}s`;

  return (
    <DoctorShell
      title="Session Review"
      subtitle="Review the captured consultation before generating the clinical summary."
      actions={
        <>
          <button onClick={() => navigate("/")}>Back to home</button>
          <button
            className="primary-button"
            onClick={() => navigate(dashboardPath)}
          >
            Go to dashboard
          </button>
        </>
      }
    >
      <div className="workspace-grid">
        {/* Transcript panel */}
        <div className="panel-shell">
          <div className="panel-shell__header">
            <h3>Captured transcript</h3>
            <span className="status-badge status-badge--active">Live capture · {duration}</span>
          </div>
          <div className="panel-shell__body transcript-panel-body">
            <div className="transcript-list">
              {session.chunks.length === 0 ? (
                <div className="empty-state">
                  <strong>No transcript captured</strong>
                </div>
              ) : (
                session.chunks.map((chunk, i) => (
                  <div key={i} className="transcript-item transcript-item--system">
                    <p>{chunk}</p>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Insights panel */}
        <div className="panel-shell">
          <div className="panel-shell__header">
            <h3>AI draft observations</h3>
            <span className="status-badge status-badge--draft">Pending review</span>
          </div>
          <div className="panel-shell__body">
            <p className="panel-note" style={{ marginBottom: "1rem" }}>
              These observations are AI-generated drafts from the live session.
              They require clinician review before any patient-facing use.
            </p>
            {session.insights.length === 0 ? (
              <div className="empty-state">
                <strong>No insights captured</strong>
              </div>
            ) : (
              session.insights.map((insight, i) => (
                <div key={i} className="transcript-item">
                  <p>{insight}</p>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </DoctorShell>
  );
}
