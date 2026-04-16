import { useEffect } from "react";
import { LiveTranscript } from "../../components/consultation/LiveTranscript";
import { LiveInsights } from "../../components/consultation/LiveInsights";
import { useLiveConsultation } from "../../hooks/useLiveConsultation";
import { navigate } from "./router";

export const DEMO_SESSION_KEY = "medorbit_demo_session";

export function LiveConsultationPage() {
  const {
    transcript,
    insights,
    status,
    stopConsultation,
    timer,
    interimText,
    error,
    isSupported,
    startConsultation,
  } = useLiveConsultation();

  const mins = Math.floor(timer / 60).toString().padStart(2, "0");
  const secs = (timer % 60).toString().padStart(2, "0");

  useEffect(() => {
    document.body.style.background = "";
    return () => {
      document.body.style.background = "";
    };
  }, []);

  const handleEndConsultation = () => {
    stopConsultation();

    const demoVisitId = `demo-${Date.now().toString(36)}`;
    const demoSession = {
      visitId: demoVisitId,
      chunks: transcript.map((chunk) => chunk.text),
      insights: insights.map((insight) => insight.content),
      durationSecs: timer,
      createdAt: new Date().toISOString(),
    };

    sessionStorage.setItem(DEMO_SESSION_KEY, JSON.stringify(demoSession));
    navigate("/live-consultation/review");
  };

  return (
    <div className="live-consultation-page">
      <header className="live-header">
        <div className="header-left">
          <div className={`status-indicator ${status === "listening" ? "pulsing" : ""}`} />
          <div>
            <h2>Live consultation capture</h2>
            <p className="live-header-sub">
              {error
                ? error
                : status === "listening"
                  ? "Microphone is active and transcript is updating live"
                  : status === "processing"
                    ? "Finishing session..."
                    : "Ready to capture"}
            </p>
          </div>
        </div>

        <div className="header-center">
          <span className="timer">
            {mins}:{secs}
          </span>
        </div>

        <div className="header-right" style={{ display: "flex", gap: "0.75rem" }}>
          {status !== "listening" ? (
            <button className="secondary-button" onClick={() => void startConsultation()}>
              {transcript.length > 0 ? "Restart recording" : "Start recording"}
            </button>
          ) : null}

          <button
            className="btn-end-session"
            onClick={handleEndConsultation}
            disabled={transcript.length === 0 && !error}
          >
            End session &amp; review
          </button>
        </div>
      </header>

      {!isSupported ? (
        <div className="panel-shell" style={{ padding: "1.25rem", marginBottom: "1rem" }}>
          <strong>Browser support required</strong>
          <p style={{ marginTop: "0.5rem" }}>
            Use Chrome or Edge for live microphone transcription in this MVP build.
          </p>
        </div>
      ) : null}

      <main className="live-workspace">
        <div className="left-panel">
          <LiveTranscript transcript={transcript} interimText={interimText} status={status} />
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