import WireBlob from "../visuals/WireBlob";

export default function Hero() {
    return (
        <section className="hero-section">
            <div className="hero-bg-glow hero-bg-glow-one" />
            <div className="hero-bg-glow hero-bg-glow-two" />

            <div className="hero-container">
                <div className="hero-badge">
                    <span className="hero-badge-dot">●</span>
                    <span>AI-assisted clinical conversation intelligence</span>
                </div>

                <h1 className="hero-title">
                    Listen with <span>clarity.</span>
                </h1>

                <p className="hero-subtitle">
                    Hearity captures relevant clinical context from doctor-patient
                    conversations and turns it into usable, structured insight.
                </p>

                <WireBlob />
            </div>
        </section>
    );
}