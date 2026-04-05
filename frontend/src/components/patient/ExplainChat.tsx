import React, { useState, useRef, useEffect } from "react";
import type { ChatMessage as ChatMessageType } from "../../types/patient";
import { ChatMessage } from "./ChatMessage";
import { patientApi } from "../../lib/api/patient";

interface Props {
  visitId: string;
  hasApprovedReport: boolean;
}

export function ExplainChat({ visitId, hasApprovedReport }: Props) {
  const [messages, setMessages] = useState<ChatMessageType[]>([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSend() {
    const text = input.trim();
    if (!text || sending) return;

    const userMsg: ChatMessageType = { role: "user", content: text };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setSending(true);

    try {
      const res = await patientApi.sendChatMessage(visitId, text);
      const assistantMsg: ChatMessageType = {
        role: "assistant",
        content: res.answer,
        isSupported: res.is_supported,
        safetyNote: res.safety_note,
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Sorry, something went wrong. Please try again.",
          isSupported: true,
        },
      ]);
    } finally {
      setSending(false);
    }
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  return (
    <section className="pt-card pt-chat">
      <div className="pt-chat__header">
        <span className="pt-icon">💬</span>
        <h3>Ask About Your Report</h3>
      </div>

      <p className="pt-chat__disclaimer">
        This assistant answers questions based on your doctor-approved report only.
        It cannot provide new diagnoses or medical advice.
      </p>

      {!hasApprovedReport ? (
        <div className="pt-chat__disabled">
          Chat will be available once your doctor approves the report for this visit.
        </div>
      ) : (
        <>
          <div className="pt-chat__messages">
            {messages.length === 0 ? (
              <p className="pt-chat__empty">
                Ask a question about your care instructions and we'll explain it in simple terms.
              </p>
            ) : (
              messages.map((msg, i) => <ChatMessage key={i} message={msg} />)
            )}
            <div ref={bottomRef} />
          </div>

          <div className="pt-chat__input-row">
            <input
              className="pt-chat__input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask a question about your report..."
              disabled={sending}
            />
            <button
              className="pt-btn-primary pt-btn-sm"
              onClick={handleSend}
              disabled={sending || !input.trim()}
            >
              {sending ? "..." : "Ask"}
            </button>
          </div>

          <p className="pt-chat__safety">
            ⚠ AI assistant. Not a substitute for professional medical advice.
            For emergencies, call 911.
          </p>
        </>
      )}
    </section>
  );
}
