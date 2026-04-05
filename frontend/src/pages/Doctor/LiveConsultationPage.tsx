import { useEffect } from "react";
import { LiveTranscript } from "../../components/consultation/LiveTranscript";
import { LiveInsights } from "../../components/consultation/LiveInsights";
import { useDemoConsultation } from "../../hooks/useDemoConsultation";
import { navigate } from "./router";

/* Persist a minimal demo session so the review page can gracefully handle
   "no backend record" — it checks this key before hitting the API. */
export const DEMO_SESSION_KEY = "medorbit_demo_session";

export function LiveConsultationPage() {
  const { transcript, insights, status, stopConsultation, timer } = useDemoConsultation();

  const mins = Math.floor(timer / 60).toString().padStart(2, "0");
  const secs = (timer % 60).toString().padStart(2, "0");

  // Lock dark background for this screen only
  useEffect(() => {
    document.body.style.background = "#0b131e";
    return () => {
      document.body.style.background = "";
    };
  }, []);

  const handleEndConsultation = () => {
    stopConsultation();

    // Write a lightweight demo session into sessionStorage so the review
    // page can detect it and show a demo-safe state instead of an API error.
    const demoVisitId = `demo-${Date.now().toString(36)}`;
    const demoSession = {
      visitId: demoVisitId,
      chunks: transcript.map((c) => c.text),
      insights: insights.map((i) => i.content),
      durationSecs: timer,
      createdAt: new Date().toISOString(),
    };
    sessionStorage.setItem(DEMO_SESSION_KEY, JSON.stringify(demoSession));

    navigate(`/live-consultation/review`);
  };

  return (
    <div className="live-consultation-page">
      <header className="live-header">
        <div className="header-left">
          <div className={`status-indicator ${status === "listening" ? "pulsing" : ""}`} />
          <div>
            <h2>Live consultation capture</h2>
            <p className="live-header-sub">
              {status === "listening" ? "Transcript capturing in real time" : "Session complete"}
            </p>
          </div>
        </div>

        <div className="header-center">
          <span className="timer">{mins}:{secs}</span>
        </div>

        <div className="header-right">
          <button className="btn-end-session" onClick={handleEndConsultation}>
            End session &amp; review
          </button>
        </div>
      </header>

      <main className="live-workspace">
        <div className="left-panel">
          <LiveTranscript transcript={transcript} status={status} />
        </div>
        <div className="right-panel">
          <LiveInsights insights={insights} status={status} />
        </div>
      </main>

      <footer className="live-footer">
        <span className="trust-badge">
          AI observations are draft only · Clinician review required before any patient-facing output
        </span>
      </footer>
    </div>
  );
}
