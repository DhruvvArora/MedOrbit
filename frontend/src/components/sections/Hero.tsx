import HeroBlob from "../visuals/HeroBlob";

export default function Hero() {
    return (
        <section className="hero-section">
            <div className="hero-bg-glow hero-bg-glow-one" />
            <div className="hero-bg-glow hero-bg-glow-two" />

            <div className="hero-container">
                <div className="hero-badge">
                    <span className="hero-badge-dot">●</span>
                    <span>AI-assisted clinical and behavioral intelligence</span>
                </div>

                <h1 className="hero-title">
                    Where conversations become <span>clinical intelligence.</span>
                </h1>

                <p className="hero-subtitle">
                    MedOrbit listens during consultations, identifies relevant clinical and behavioral signals,
                    and converts them into usable summaries, reports, and care insights.
                </p>
            </div>

            {/* Blob sits outside hero-container so it's not clipped or doubled */}
            <div style={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                width: "100%",
                overflow: "hidden",
                marginTop: "1rem",
            }}>
                <HeroBlob />
            </div>
        </section>
    );
}
