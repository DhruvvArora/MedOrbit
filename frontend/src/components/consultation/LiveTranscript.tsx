import { useEffect, useRef } from "react";
import type { TranscriptChunk } from "../../hooks/useDemoConsultation";

interface LiveTranscriptProps {
  transcript: TranscriptChunk[];
  status: "idle" | "listening" | "processing" | "stopped";
}

export function LiveTranscript({ transcript, status }: LiveTranscriptProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to newest chunk
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [transcript]);

  return (
    <div className="live-transcript">
      {/* Live status bar at top of transcript panel */}
      <div className="transcript-status-bar">
        {status === "listening" && (
          <>
            <span className="transcript-pulse-dot" />
            <span>Capturing conversation…</span>
          </>
        )}
        {status === "processing" && (
          <>
            <span className="transcript-pulse-dot transcript-pulse-dot--processing" />
            <span>Processing session…</span>
          </>
        )}
        {status === "stopped" && <span>Session ended</span>}
      </div>

      <div className="transcript-chunks">
        {transcript.length === 0 && status === "listening" && (
          <div className="transcript-empty-hint">Listening for conversation…</div>
        )}

        {transcript.map((chunk, i) => (
          <div key={chunk.id} className="transcript-chunk" style={{ animationDelay: `${i * 0.05}s` }}>
            <span className="transcript-chunk-time">
              {chunk.timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" })}
            </span>
            <p className="transcript-chunk-text">{chunk.text}</p>
          </div>
        ))}

        <div ref={bottomRef} />
      </div>
    </div>
  );
}
