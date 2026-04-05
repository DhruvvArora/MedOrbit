import { useCallback, useEffect, useRef, useState } from "react";

const generateId = () => Math.random().toString(36).slice(2, 11);

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

type ConsultationStatus = "idle" | "listening" | "processing" | "stopped";

interface SpeechRecognitionAlternativeLike {
  transcript: string;
  confidence: number;
}

interface SpeechRecognitionResultLike {
  isFinal: boolean;
  length: number;
  0: SpeechRecognitionAlternativeLike;
}

interface SpeechRecognitionEventLike extends Event {
  resultIndex: number;
  results: ArrayLike<SpeechRecognitionResultLike>;
}

interface SpeechRecognitionLike extends EventTarget {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  maxAlternatives: number;
  onresult: ((event: SpeechRecognitionEventLike) => void) | null;
  onerror: ((event: Event & { error?: string }) => void) | null;
  onend: (() => void) | null;
  start(): void;
  stop(): void;
  abort(): void;
}

interface WindowWithSpeech extends Window {
  SpeechRecognition?: new () => SpeechRecognitionLike;
  webkitSpeechRecognition?: new () => SpeechRecognitionLike;
}

function getSpeechRecognitionCtor() {
  const speechWindow = window as WindowWithSpeech;
  return speechWindow.SpeechRecognition || speechWindow.webkitSpeechRecognition || null;
}

function buildInsights(chunks: TranscriptChunk[]): AIInsight[] {
  const combined = chunks.map((chunk) => chunk.text).join(" ").toLowerCase();
  const tags: string[] = [];

  const addTag = (condition: boolean, label: string) => {
    if (condition && !tags.includes(label)) tags.push(label);
  };

  addTag(/\bcough\b/.test(combined), "Symptom: Cough");
  addTag(/\bpain\b/.test(combined), "Symptom: Pain");
  addTag(/\bfatigue|tired|exhausted\b/.test(combined), "Fatigue reported");
  addTag(/\bshortness of breath|breathless|breathing\b/.test(combined), "Breathing concern");
  addTag(/\bfever\b/.test(combined), "Fever mentioned");
  addTag(/\bstress|anxious|anxiety\b/.test(combined), "Stress/anxiety mentioned");
  addTag(/\bsleep|insomnia|night\b/.test(combined), "Sleep disruption");
  addTag(/\bmedication|medicine\b/.test(combined), "Medication discussed");
  addTag(/\ballergy|allergies\b/.test(combined), "Allergies mentioned");

  const nextInsights: AIInsight[] = tags.map((tag) => ({
    id: `tag-${tag}`,
    type: "tag",
    content: tag,
  }));

  if (chunks.length >= 2) {
    const recentText = chunks
      .slice(-3)
      .map((chunk) => chunk.text)
      .join(" ");

    const clipped =
      recentText.length > 240 ? `${recentText.slice(0, 237).trim()}...` : recentText;

    nextInsights.push({
      id: "observation-latest",
      type: "observation",
      content: `Draft observation: ${clipped}`,
    });
  }

  return nextInsights;
}

export function useLiveConsultation() {
  const [transcript, setTranscript] = useState<TranscriptChunk[]>([]);
  const [insights, setInsights] = useState<AIInsight[]>([]);
  const [status, setStatus] = useState<ConsultationStatus>("idle");
  const [timer, setTimer] = useState(0);
  const [interimText, setInterimText] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSupported, setIsSupported] = useState(true);

  const recognitionRef = useRef<SpeechRecognitionLike | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const shouldRestartRef = useRef(false);

  const stopMediaTracks = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
  }, []);

  const stopConsultation = useCallback(() => {
    shouldRestartRef.current = false;
    setInterimText("");
    setStatus("processing");

    if (recognitionRef.current) {
      try {
        recognitionRef.current.stop();
      } catch {
        // ignore stop race
      }
    }

    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== "inactive") {
      try {
        mediaRecorderRef.current.stop();
      } catch {
        // ignore stop race
      }
    }

    stopMediaTracks();

    window.setTimeout(() => {
      setStatus("stopped");
    }, 300);
  }, [stopMediaTracks]);

  const startConsultation = useCallback(async () => {
    const SpeechRecognitionCtor = getSpeechRecognitionCtor();

    if (!navigator.mediaDevices?.getUserMedia || !window.MediaRecorder || !SpeechRecognitionCtor) {
      setIsSupported(false);
      setError("Live microphone transcription is supported best in Chrome or Edge.");
      setStatus("stopped");
      return;
    }

    setIsSupported(true);
    setError(null);
    setTranscript([]);
    setInsights([]);
    setTimer(0);
    setInterimText("");

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
      });

      streamRef.current = stream;

      const recorder = new MediaRecorder(stream);
      mediaRecorderRef.current = recorder;
      audioChunksRef.current = [];

      recorder.ondataavailable = (event: BlobEvent) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      recorder.start(1000);

      const recognition = new SpeechRecognitionCtor();
      recognitionRef.current = recognition;
      shouldRestartRef.current = true;

      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = "en-US";
      recognition.maxAlternatives = 1;

      recognition.onresult = (event) => {
        let nextInterim = "";
        const finalizedTexts: string[] = [];

        for (let i = event.resultIndex; i < event.results.length; i += 1) {
          const result = event.results[i];
          const text = result[0]?.transcript?.trim();

          if (!text) continue;

          if (result.isFinal) {
            finalizedTexts.push(text);
          } else {
            nextInterim += `${text} `;
          }
        }

        setInterimText(nextInterim.trim());

        if (finalizedTexts.length > 0) {
          setTranscript((previous) => {
            const additions = finalizedTexts.map((text) => ({
              id: generateId(),
              text,
              timestamp: new Date(),
            }));

            const nextTranscript = [...previous, ...additions];
            setInsights(buildInsights(nextTranscript));
            return nextTranscript;
          });

          setInterimText("");
        }
      };

      recognition.onerror = (event) => {
        const code = event.error || "unknown";

        if (code === "not-allowed") {
          setError("Microphone permission was blocked. Allow mic access and try again.");
          shouldRestartRef.current = false;
          stopMediaTracks();
          setStatus("stopped");
          return;
        }

        if (code === "no-speech") {
          return;
        }

        setError(`Live transcription error: ${code}`);
      };

      recognition.onend = () => {
        if (shouldRestartRef.current) {
          try {
            recognition.start();
          } catch {
            // ignore restart races
          }
        }
      };

      recognition.start();
      setStatus("listening");
    } catch {
      setError("Unable to access the microphone. Check browser permissions and device input.");
      setStatus("stopped");
      stopMediaTracks();
    }
  }, [stopMediaTracks]);

  useEffect(() => {
    if (status !== "listening") return;

    const interval = window.setInterval(() => {
      setTimer((current) => current + 1);
    }, 1000);

    return () => window.clearInterval(interval);
  }, [status]);

  useEffect(() => {
    void startConsultation();

    return () => {
      shouldRestartRef.current = false;

      if (recognitionRef.current) {
        try {
          recognitionRef.current.abort();
        } catch {
          // ignore
        }
      }

      if (mediaRecorderRef.current && mediaRecorderRef.current.state !== "inactive") {
        try {
          mediaRecorderRef.current.stop();
        } catch {
          // ignore
        }
      }

      stopMediaTracks();
    };
  }, [startConsultation, stopMediaTracks]);

  return {
    transcript,
    insights,
    status,
    timer,
    interimText,
    error,
    isSupported,
    startConsultation,
    stopConsultation,
  };
}