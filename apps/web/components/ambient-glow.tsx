"use client";

import { motion, useReducedMotion } from "framer-motion";

type OrbitNodeProps = {
  ring: number;
  size: number;
  duration: number;
  reverse?: boolean;
  offset?: number;
  tether?: boolean;
};

function OrbitNode({ ring, size, duration, reverse, offset = 0, tether }: OrbitNodeProps) {
  return (
    <div
      className="absolute left-1/2 top-1/2"
      style={{ width: ring, height: ring, marginLeft: -ring / 2, marginTop: -ring / 2, transform: `rotate(${offset}deg)` }}
    >
      <div
        className="absolute inset-0"
        style={{ animation: `orbit-spin ${duration}s linear infinite${reverse ? " reverse" : ""}` }}
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

export function AmbientGlow() {
  const reduzirMovimento = useReducedMotion();

  return (
    <motion.div
      className="pointer-events-none absolute inset-0 overflow-hidden"
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
      `}</style>

      <div className="absolute left-[38%] top-1/2 -translate-x-1/2 -translate-y-1/2">
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

        <OrbitNode ring={260} size={9} duration={20} offset={20} tether />
        <OrbitNode ring={260} size={5} duration={24} offset={190} reverse />
        <OrbitNode ring={420} size={6} duration={34} offset={80} reverse />
        <OrbitNode ring={420} size={4} duration={30} offset={250} />
        <OrbitNode ring={580} size={7} duration={48} offset={140} tether />
        <OrbitNode ring={580} size={4} duration={42} offset={320} reverse />
        <OrbitNode ring={720} size={5} duration={64} offset={60} />
        <OrbitNode ring={720} size={3.5} duration={58} offset={210} reverse tether />
      </div>
    </motion.div>
  );
}
