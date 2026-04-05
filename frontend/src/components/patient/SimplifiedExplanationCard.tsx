
interface Props {
  explanation: string;
}

export function SimplifiedExplanationCard({ explanation }: Props) {
  return (
    <section className="pt-card pt-explanation-card">
      <div className="pt-explanation-card__header">
        <span className="pt-icon">💡</span>
        <h3>What This Means for You</h3>
      </div>
      <div className="pt-explanation-content">{explanation}</div>
    </section>
  );
}
