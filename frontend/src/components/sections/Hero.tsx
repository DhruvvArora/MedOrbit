import { useState } from "react";
import HeroBlob from "../visuals/HeroBlob";
import { useAuth } from "../../context/AuthContext";
import { navigate } from "../../pages/Doctor/router";

export default function Hero() {
    const { user } = useAuth();
    const [isTransitioning, setIsTransitioning] = useState(false);

    const handleStartConsultation = () => {
        if (!user) {
            navigate("/login");
            return;
        }

        setIsTransitioning(true);

        setTimeout(() => {
            navigate("/live-consultation");
        }, 700);
    };

    return (
        <>
            {/* Full-screen overlay for transition — sits above everything during animation */}
            <div className={`hero-transition-overlay ${isTransitioning ? "hero-transition-overlay--active" : ""}`} />

            <section className="hero-section">
                <div className="hero-bg-glow hero-bg-glow-one" />
                <div className="hero-bg-glow hero-bg-glow-two" />

                {/* Text block fades out on click */}
                <div
                    className="hero-container"
                    style={{ opacity: isTransitioning ? 0 : 1, transition: "opacity 0.35s ease" }}
                >
                    <div className="hero-badge">
                        <span className="hero-badge-dot">●</span>
                        <span>AI-assisted Clinical and Behavioral Intelligence</span>
                    </div>

                    <h1 className="hero-title">
                        Where conversations become <span>clinical intelligence.</span>
                    </h1>

                    <p className="hero-subtitle">
                        MedOrbit listens during consultations, identifies relevant clinical and behavioral signals,
                        and converts them into usable summaries, reports, and care insights.
                    </p>
                </div>

                {/* Orb + instruction label — centered independently */}
                <div className="hero-orb-wrapper">
                    <div
                        className="hero-orb-click-target"
                        onClick={handleStartConsultation}
                        role="button"
                        tabIndex={0}
                        aria-label="Begin live consultation capture"
                        onKeyDown={(e) => e.key === "Enter" && handleStartConsultation()}
                    >
                        <HeroBlob isTransitioning={isTransitioning} />
                    </div>

                    <p
                        className="hero-orb-cta"
                        style={{ opacity: isTransitioning ? 0 : 1, transition: "opacity 0.25s ease" }}
                    >
                        Begin live consultation capture
                    </p>
                </div>
            </section>
        </>
    );
}
