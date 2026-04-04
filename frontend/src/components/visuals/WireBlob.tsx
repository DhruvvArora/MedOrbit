export default function WireBlob() {
    return (
        <div className="wireblob-wrap">
            <svg
                className="wireblob"
                viewBox="0 0 600 600"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
            >
                <g opacity="0.9">
                    {Array.from({ length: 26 }).map((_, i) => {
                        const scale = 1 - i * 0.018;
                        const rotate = i * 7;

                        return (
                            <path
                                key={i}
                                d="M300 90C390 70 490 130 520 235C548 333 503 455 392 507C286 556 156 532 96 428C43 335 56 205 149 135C194 101 245 94 300 90Z"
                                transform={`translate(300 300) rotate(${rotate}) scale(${scale}) translate(-300 -300)`}
                            />
                        );
                    })}
                </g>
            </svg>
        </div>
    );
}