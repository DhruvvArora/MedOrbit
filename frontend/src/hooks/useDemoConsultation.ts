import { useState, useEffect, useRef } from "react";

const generateId = () => Math.random().toString(36).substr(2, 9);

/* ── Simulated conversation chunks ─────────────────────────────────────────
   Chunks are shown as progressive blocks of captured dialogue — no speaker
   labelling at this stage; that happens post-session in review.
────────────────────────────────────────────────────────────────────────── */
const SIMULATED_CHUNKS: { text: string; delayMs: number }[] = [
  {
    text: "Patient presents reporting a persistent cough that has been ongoing for approximately three weeks. States it is worse at night and is disrupting sleep.",
    delayMs: 700,
  },
  {
    text: "Also experiencing mild shortness of breath when climbing stairs. No reported fever or chills. Reports feeling generally fatigued.",
    delayMs: 1400,
  },
  {
    text: "No recent change in medication. Patient mentions stress at work as a possible contributing factor. No family history of respiratory illness flagged.",
    delayMs: 1600,
  },
  {
    text: "Discussion around potential triggers — dust exposure at home, a recent cold approximately four weeks ago. No smoker. No known allergies.",
    delayMs: 1700,
  },
  {
    text: "Clinical notes: Cough duration three weeks, nocturnal pattern. Dyspnoea on exertion. Patient otherwise systemically well.",
    delayMs: 1800,
  },
];

export interface TranscriptChunk {
  id: string;
  text: string;
  timestamp: Date;
}

export interface AIInsight {
  id: string;
  type: "tag" | "observation";
  content: string;
}

export function useDemoConsultation() {
  const [transcript, setTranscript] = useState<TranscriptChunk[]>([]);
  const [insights, setInsights] = useState<AIInsight[]>([]);
  const [status, setStatus] = useState<"idle" | "listening" | "processing" | "stopped">("listening");
  const [timer, setTimer] = useState(0);

  const chunkIndex = useRef(0);
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Live timer
  useEffect(() => {
    if (status !== "listening") return;
    const interval = setInterval(() => setTimer((t) => t + 1), 1000);
    return () => clearInterval(interval);
  }, [status]);

  // Chunk-based transcript reveal
  useEffect(() => {
    if (status !== "listening") return;

    function pushNextChunk() {
      if (chunkIndex.current >= SIMULATED_CHUNKS.length) {
        setStatus("processing");
        return;
      }

      const chunk = SIMULATED_CHUNKS[chunkIndex.current];

      timeoutRef.current = setTimeout(() => {
        setTranscript((prev) => [
          ...prev,
          { id: generateId(), text: chunk.text, timestamp: new Date() },
        ]);

        // Stagger-release AI signals alongside chunks
        if (chunkIndex.current === 0) {
          setInsights((prev) => [
            ...prev,
            { id: generateId(), type: "tag", content: "Symptom: Cough" },
          ]);
        }
        if (chunkIndex.current === 1) {
          setInsights((prev) => [
            ...prev,
            { id: generateId(), type: "tag", content: "Duration: ~3 weeks" },
            { id: generateId(), type: "tag", content: "Symptom: Shortness of breath" },
          ]);
        }
        if (chunkIndex.current === 2) {
          setInsights((prev) => [
            ...prev,
            { id: generateId(), type: "tag", content: "Fatigue reported" },
          ]);
        }
        if (chunkIndex.current === 3) {
          setInsights((prev) => [
            ...prev,
            {
              id: generateId(),
              type: "observation",
              content:
                "Draft observation: Nocturnal cough with exertional dyspnoea, onset 3 weeks. No fever. Systemically well. Possible post-viral or environmental trigger.",
            },
          ]);
        }

        chunkIndex.current += 1;
        pushNextChunk();
      }, chunk.delayMs);
    }

    pushNextChunk();

    return () => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
    };
  }, [status]);

  const stopConsultation = () => {
    setStatus("stopped");
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
  };

  return { transcript, insights, status, timer, stopConsultation };
}
