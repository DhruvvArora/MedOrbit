import React from "react";
import type { BehavioralInsights, TriageSummary } from "../../types/doctor";
import { PanelShell } from "../shared/PanelShell";
import { EmptyState } from "../shared/EmptyState";
import { StatusBadge } from "../shared/StatusBadge";

interface Props {
  behavioral: BehavioralInsights | null;
  triage: TriageSummary | null;
}

function renderList(items: unknown, fallback: string) {
  if (!Array.isArray(items) || items.length === 0) return <p>{fallback}</p>;
  return (
    <ul className="bullet-list">
      {items.map((item, index) => (
        <li key={`${String(item)}-${index}`}>{String(item)}</li>
      ))}
    </ul>
  );
}

export function AgentInsightPanel({ behavioral, triage }: Props) {
  return (
    <div className="stack-grid">
      <PanelShell
        title="Behavioral Insights"
        subtitle="Draft observations for clinician review"
        rightSlot={<StatusBadge tone="draft">Draft</StatusBadge>}
      >
        {!behavioral ? (
          <EmptyState title="Behavioral Analysis not available" description="Run analysis once enough transcript context is available." />
        ) : (
          <div className="agent-content">
            <p><strong>Emotional tone:</strong> {behavioral.emotional_tone || "Not specified"}</p>
            <div>
              <h4>Observations</h4>
              {renderList(behavioral.behavioral_observations, "No structured observations returned yet.")}
            </div>
            <div>
              <h4>Concerns</h4>
              {renderList(behavioral.concerns, "No concerns surfaced.")}
            </div>
            <div>
              <h4>Suggested follow-ups</h4>
              {renderList(behavioral.suggested_follow_ups, "No follow-up prompts suggested yet.")}
            </div>
            {behavioral.uncertainty_note ? <p className="panel-note">{behavioral.uncertainty_note}</p> : null}
          </div>
        )}
      </PanelShell>

      <PanelShell
        title="Clinical Triage"
        subtitle="Draft prioritization for clinician review"
        rightSlot={<StatusBadge tone="draft">Draft</StatusBadge>}
      >
        {!triage ? (
          <EmptyState title="Triage summary not available" description="Run triage once relevant symptoms or concerns are documented." />
        ) : (
          <div className="agent-content">
            <p><strong>Acuity level:</strong> {triage.acuity_level || "Not specified"}</p>
            <div>
              <h4>Key symptoms</h4>
              {renderList(triage.key_symptoms, "No symptoms extracted yet.")}
            </div>
            <div>
              <h4>Risk flags</h4>
              {renderList(triage.risk_flags, "No explicit risk flags returned.")}
            </div>
            <div>
              <h4>Recommended next steps</h4>
              {renderList(triage.recommended_next_steps, "No suggested next steps yet.")}
            </div>
            {triage.uncertainty_note ? <p className="panel-note">{triage.uncertainty_note}</p> : null}
          </div>
        )}
      </PanelShell>
    </div>
  );
}
