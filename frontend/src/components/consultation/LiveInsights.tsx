import type { AIInsight } from "../../hooks/useDemoConsultation";

interface LiveInsightsProps {
  insights: AIInsight[];
  status: "idle" | "listening" | "processing" | "stopped";
}

export function LiveInsights({ insights, status }: LiveInsightsProps) {
  const tags = insights.filter((i) => i.type === "tag");
  const observations = insights.filter((i) => i.type === "observation");

  return (
    <div className="live-insights">
      <div className="insights-header">
        <div className="recording-dot" />
        <span>Live analysis</span>
        <span className="insights-badge">AI draft</span>
      </div>

      <div className="insights-scroll">
        {insights.length === 0 ? (
          <div className="insights-empty">
            <div className="insights-empty-dots">
              <span />
              <span />
              <span />
            </div>
            <p>Capturing conversation context…</p>
          </div>
        ) : (
          <>
            {tags.length > 0 && (
              <div className="insights-section">
                <h4 className="insights-section-label">Detected signals</h4>
                <div className="tags-container">
                  {tags.map((t) => (
                    <span key={t.id} className="insight-tag">
                      {t.content}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {observations.length > 0 && (
              <div className="insights-section">
                <h4 className="insights-section-label">Draft observations</h4>
                {observations.map((o) => (
                  <div key={o.id} className="insight-card">
                    <span className="insight-card-label">AI draft · pending review</span>
                    <p>{o.content}</p>
                  </div>
                ))}
              </div>
            )}
          </>
        )}

        {status === "stopped" && (
          <div className="insights-session-end">
            Session ended — full analysis available in review.
          </div>
        )}
      </div>
    </div>
  );
}
