"use client";

import { useEffect, useRef } from "react";
import { motion, useMotionValue, useReducedMotion, useSpring } from "framer-motion";

type OrbitNodeProps = {
  ring: number;
  size: number;
  duration: number;
  reverse?: boolean;
  offset?: number;
  tether?: boolean;
  reduzirMovimento?: boolean;
};

function OrbitNode({ ring, size, duration, reverse, offset = 0, tether, reduzirMovimento }: OrbitNodeProps) {
  return (
    <div
      className="absolute left-1/2 top-1/2"
      style={{ width: ring, height: ring, marginLeft: -ring / 2, marginTop: -ring / 2, transform: `rotate(${offset}deg)` }}
    >
      <div
        className="absolute inset-0"
        style={
          reduzirMovimento
            ? undefined
            : { animation: `orbit-spin ${duration}s linear infinite${reverse ? " reverse" : ""}` }
        }
      >
        <div
          className="absolute left-1/2 top-0 -translate-x-1/2 -translate-y-1/2 rounded-full bg-primary"
          style={{ width: size, height: size, boxShadow: `0 0 ${size * 4}px ${size}px var(--primary)` }}
        >
          {tether && (
            <span
              className="absolute left-1/2 top-full -translate-x-1/2 bg-gradient-to-b from-primary/50 to-transparent"
              style={{ width: 1, height: size * 3 }}
            />
          )}
        </div>
      </div>
    </div>
  );
}

type ShootingStarProps = {
  top: string;
  left: string;
  angle: number;
  length: number;
  duration: number;
  delay: number;
};

function ShootingStar({ top, left, angle, length, duration, delay }: ShootingStarProps) {
  return (
    <div
      className="absolute h-px"
      style={{
        top,
        left,
        width: length,
        transform: `rotate(${angle}deg)`,
        transformOrigin: "left center",
        animation: `shooting-star ${duration}s ease-in ${delay}s infinite`,
        opacity: 0,
      }}
    >
      <div
        className="h-px w-full"
        style={{
          background: "linear-gradient(90deg, transparent, var(--primary) 65%, color-mix(in srgb, var(--primary) 60%, white) 100%)",
        }}
      />
      <div
        className="absolute right-0 top-1/2 -translate-y-1/2 rounded-full"
        style={{
          width: 3,
          height: 3,
          background: "color-mix(in srgb, var(--primary) 60%, white)",
          boxShadow: "0 0 8px 2px var(--primary)",
        }}
      />
    </div>
  );
}

const ESTRELAS: ShootingStarProps[] = [
  { top: "14%", left: "8%", angle: 22, length: 110, duration: 6, delay: 0.5 },
  { top: "62%", left: "72%", angle: 18, length: 90, duration: 7.5, delay: 3 },
  { top: "30%", left: "55%", angle: 26, length: 130, duration: 8.5, delay: 5.5 },
  { top: "78%", left: "20%", angle: 20, length: 100, duration: 6.8, delay: 1.8 },
  { top: "8%", left: "68%", angle: 24, length: 80, duration: 7.2, delay: 7 },
];

export function AmbientGlow({ anchorLeft = "38%" }: { anchorLeft?: string }) {
  const reduzirMovimento = useReducedMotion() ?? false;
  const containerRef = useRef<HTMLDivElement>(null);

  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);
  const parallaxX = useSpring(mouseX, { stiffness: 60, damping: 20, mass: 0.6 });
  const parallaxY = useSpring(mouseY, { stiffness: 60, damping: 20, mass: 0.6 });

  useEffect(() => {
    if (reduzirMovimento) return;
    function handlePointerMove(event: PointerEvent) {
      const container = containerRef.current;
      if (!container) return;
      const rect = container.getBoundingClientRect();
      const relativeX = (event.clientX - rect.left) / rect.width - 0.5;
      const relativeY = (event.clientY - rect.top) / rect.height - 0.5;
      mouseX.set(relativeX * 22);
      mouseY.set(relativeY * 22);
    }
    window.addEventListener("pointermove", handlePointerMove);
    return () => window.removeEventListener("pointermove", handlePointerMove);
  }, [reduzirMovimento, mouseX, mouseY]);

  return (
    <motion.div
      ref={containerRef}
      className="pointer-events-none absolute inset-0"
      aria-hidden="true"
      initial={reduzirMovimento ? false : { opacity: 0, scale: 0.85 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.9, ease: "easeOut" }}
    >
      <style>{`
        @keyframes orbit-spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        @keyframes shooting-star {
          0% { opacity: 0; transform: translate(0, 0) rotate(var(--angle, 0deg)); }
          6% { opacity: 1; }
          18% { opacity: 0; transform: translate(160px, 90px) rotate(var(--angle, 0deg)); }
          100% { opacity: 0; }
        }
      `}</style>

      {!reduzirMovimento &&
        ESTRELAS.map((estrela, indice) => <ShootingStar key={indice} {...estrela} />)}

      <motion.div
        className="pointer-events-none absolute top-1/2 -translate-x-1/2 -translate-y-1/2"
        style={{ left: anchorLeft, x: parallaxX, y: parallaxY }}
      >
        <div
          className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 rounded-full"
          style={{
            width: 64,
            height: 64,
            background: "radial-gradient(circle at 35% 30%, color-mix(in srgb, var(--primary) 70%, white), var(--primary) 60%, color-mix(in srgb, var(--primary) 70%, black) 100%)",
            boxShadow: "0 0 90px 22px color-mix(in srgb, var(--primary) 50%, transparent)",
          }}
        />

        <div
          className="absolute left-1/2 top-1/2 h-[260px] w-[260px] -translate-x-1/2 -translate-y-1/2 rounded-full border border-primary/30"
        />
        <div
          className="absolute left-1/2 top-1/2 h-[420px] w-[420px] -translate-x-1/2 -translate-y-1/2 rounded-full border border-primary/20"
        />
        <div
          className="absolute left-1/2 top-1/2 h-[580px] w-[580px] -translate-x-1/2 -translate-y-1/2 rounded-full border border-primary/12"
        />
        <div
          className="absolute left-1/2 top-1/2 h-[720px] w-[720px] -translate-x-1/2 -translate-y-1/2 rounded-full border border-primary/8"
        />

        <OrbitNode ring={260} size={9} duration={20} offset={20} tether reduzirMovimento={reduzirMovimento} />
        <OrbitNode ring={260} size={5} duration={24} offset={190} reverse reduzirMovimento={reduzirMovimento} />
        <OrbitNode ring={420} size={6} duration={34} offset={80} reverse reduzirMovimento={reduzirMovimento} />
        <OrbitNode ring={420} size={4} duration={30} offset={250} reduzirMovimento={reduzirMovimento} />
        <OrbitNode ring={580} size={7} duration={48} offset={140} tether reduzirMovimento={reduzirMovimento} />
        <OrbitNode ring={580} size={4} duration={42} offset={320} reverse reduzirMovimento={reduzirMovimento} />
        <OrbitNode ring={720} size={5} duration={64} offset={60} reduzirMovimento={reduzirMovimento} />
        <OrbitNode ring={720} size={3.5} duration={58} offset={210} reverse tether reduzirMovimento={reduzirMovimento} />
      </motion.div>
    </motion.div>
  );
}
