import type { ChatMessage as ChatMessageType } from "../../types/patient";

interface Props {
  message: ChatMessageType;
}

export function ChatMessage({ message }: Props) {
  const isUser = message.role === "user";
  const isUnsupported = !isUser && message.isSupported === false;

  return (
    <div
      className={`pt-msg pt-msg--${message.role} ${isUnsupported ? "pt-msg--unsupported" : ""}`}
    >
      <div className="pt-msg__bubble">{message.content}</div>
      {isUnsupported ? (
        <span className="pt-msg__refusal">
          I can only answer based on your approved report.
        </span>
      ) : null}
    </div>
  );
}
