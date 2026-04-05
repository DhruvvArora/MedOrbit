
interface Props {
  tone: "approved" | "pending" | "info";
  children: React.ReactNode;
}

const ICONS: Record<string, string> = {
  approved: "✓",
  pending: "⏳",
  info: "ℹ",
};

export function CareStatusBanner({ tone, children }: Props) {
  return (
    <div className={`pt-banner pt-banner--${tone}`}>
      <span>{ICONS[tone]}</span>
      <span>{children}</span>
    </div>
  );
}
