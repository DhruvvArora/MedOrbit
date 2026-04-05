"use client";

import { useEffect, useRef } from "react";

export default function HeroBlob({ isTransitioning: _isTransitioning }: { isTransitioning?: boolean }) {
  const wrapRef = useRef<HTMLDivElement>(null);
  const cellRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let animFrameId: number;
    let renderer: any;
    let cleanupFns: (() => void)[] = [];

    import("three").then((THREE) => {
      const wrap = wrapRef.current;
      const cell = cellRef.current;
      if (!wrap || !cell) return;

      // Scene
      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 1000);
      camera.position.z = 4;

      renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
      const cellSize = Math.min(wrap.offsetWidth, wrap.offsetHeight) || 400;
      renderer.setSize(cellSize, cellSize);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

      // Ensure canvas stays within bounds
      renderer.domElement.style.display = "block";
      renderer.domElement.style.maxWidth = "100%";
      renderer.domElement.style.maxHeight = "100%";

      cell.appendChild(renderer.domElement);

      // Geometry
      const geometry = new THREE.IcosahedronGeometry(1.2, 16);
      const positionAttribute = geometry.attributes.position;
      const vertex = new THREE.Vector3();
      const originalPositions: any[] = [];
      for (let i = 0; i < positionAttribute.count; i++) {
        vertex.fromBufferAttribute(positionAttribute, i);
        originalPositions.push(vertex.clone());
      }

      // Material — navy + teal glow wireframe
      const material = new THREE.MeshPhysicalMaterial({
        color: 0x1b365d,
        emissive: 0x2db5a8,
        emissiveIntensity: 0.2,
        roughness: 0.1,
        metalness: 0.1,
        clearcoat: 0.8,
        clearcoatRoughness: 0.2,
        wireframe: true,
        transparent: true,
        opacity: 0.35,
        side: THREE.DoubleSide,
      });

      const blob = new THREE.Mesh(geometry, material);
      scene.add(blob);

      const core = new THREE.Object3D();
      scene.add(core);

      scene.add(new THREE.AmbientLight(0xffffff, 1.5));

      // Noise — same formula as original hero-canvas.js
      const noise = (x: number, y: number, z: number) =>
        Math.sin(x * 2.5) * Math.cos(y * 2.5) * Math.sin(z * 2.5);

      let time = 0;
      let hovering = false;
      let targetRotX = 0;
      let targetRotY = 0;
      let currentRotX = 0;
      let currentRotY = 0;
      let wrapRect: DOMRect | null = null;

      const render = () => {
        time += 0.02;

        const pos = blob.geometry.attributes.position;
        for (let i = 0; i < pos.count; i++) {
          const v = originalPositions[i];
          const n = noise(
            v.x + time * 0.5,
            v.y + time * 0.3,
            v.z + time * 0.4
          );
          const d = 1 + n * 0.15;
          pos.setXYZ(i, v.x * d, v.y * d, v.z * d);
        }
        pos.needsUpdate = true;

        if (!hovering) {
          targetRotY += 0.005;
          targetRotX += 0.002;
        }

        currentRotX += (targetRotX - currentRotX) * 0.08;
        currentRotY += (targetRotY - currentRotY) * 0.08;

        blob.rotation.x = currentRotX;
        blob.rotation.y = currentRotY;
        core.rotation.x = currentRotX * 0.5;
        core.rotation.y = currentRotY * 0.5;

        renderer.render(scene, camera);
        animFrameId = requestAnimationFrame(render);
      };

      // Mouse interaction
      const onMouseEnter = () => {
        hovering = true;
        wrapRect = wrap.getBoundingClientRect();
      };
      const onMouseMove = (e: MouseEvent) => {
        if (!hovering || !wrapRect) return;
        const mx = (e.clientX - wrapRect.left) / wrapRect.width - 0.5;
        const my = (e.clientY - wrapRect.top) / wrapRect.height - 0.5;
        targetRotY = mx * Math.PI * 1.2;
        targetRotX = my * Math.PI * 1.2;
      };
      const onMouseLeave = () => {
        hovering = false;
        targetRotX = currentRotX;
        targetRotY = currentRotY;
      };
      const onResize = () => {
        if (!wrap) return;
        if (hovering) wrapRect = wrap.getBoundingClientRect();
        const size = Math.min(wrap.offsetWidth, wrap.offsetHeight);
        renderer.setSize(size, size);
      };
      const onScroll = () => {
        if (hovering && wrap) wrapRect = wrap.getBoundingClientRect();
      };

      wrap.addEventListener("mouseenter", onMouseEnter);
      wrap.addEventListener("mousemove", onMouseMove);
      wrap.addEventListener("mouseleave", onMouseLeave);
      window.addEventListener("resize", onResize, { passive: true });
      window.addEventListener("scroll", onScroll, { passive: true });

      cleanupFns = [
        () => wrap.removeEventListener("mouseenter", onMouseEnter),
        () => wrap.removeEventListener("mousemove", onMouseMove),
        () => wrap.removeEventListener("mouseleave", onMouseLeave),
        () => window.removeEventListener("resize", onResize),
        () => window.removeEventListener("scroll", onScroll),
      ];

      setTimeout(() => {
        animFrameId = requestAnimationFrame(render);
      }, 100);
    });

    return () => {
      cancelAnimationFrame(animFrameId);
      cleanupFns.forEach((fn) => fn());
      if (renderer) {
        renderer.dispose();
        const cell = cellRef.current;
        if (cell && renderer.domElement && cell.contains(renderer.domElement)) {
          cell.removeChild(renderer.domElement);
        }
      }
    };
  }, []);

  return (
    <div
      ref={wrapRef}
      style={{
        width: "100%",
        height: "100%",
        overflow: "hidden",
      }}
    >
      <div ref={cellRef} style={{ width: "100%", height: "100%" }} />
    </div>
  );
}