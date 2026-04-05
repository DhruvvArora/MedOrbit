import React, { useEffect, useRef } from "react";
import type { TranscriptChunk, TranscriptStatsView } from "../../types/doctor";
import { PanelShell } from "../shared/PanelShell";
import { EmptyState } from "../shared/EmptyState";

function speakerClass(role: TranscriptChunk["speaker_role"]) {
  if (role === "doctor") return "transcript-item transcript-item--doctor";
  if (role === "patient") return "transcript-item transcript-item--patient";
  return "transcript-item transcript-item--system";
}

export function TranscriptPanel({ chunks, stats }: { chunks: TranscriptChunk[]; stats: TranscriptStatsView }) {
  const endRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ block: "end" });
  }, [chunks.length]);

  return (
    <PanelShell
      title="Transcript"
      subtitle={stats.total_chunks > 0 ? `${stats.total_chunks} transcript entries` : "No transcript captured yet"}
      rightSlot={<span className="mini-muted">Manual Refresh</span>}
    >
      <div className="transcript-panel-body">
        {chunks.length === 0 ? (
          <EmptyState title="No transcript available" description="Start the visit or add transcript entries to populate this panel." />
        ) : (
          <div className="transcript-list">
            {chunks.map((chunk) => (
              <div key={chunk.id} className={speakerClass(chunk.speaker_role)}>
                <div className="transcript-item__meta">
                  <strong>{chunk.speaker_label || chunk.speaker_role}</strong>
                  <span>#{chunk.sequence_number}</span>
                </div>
                <p>{chunk.text}</p>
              </div>
            ))}
            <div ref={endRef} />
          </div>
        )}
      </div>
    </PanelShell>
  );
}