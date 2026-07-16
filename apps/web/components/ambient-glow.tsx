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
  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden" aria-hidden="true">
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
            width: 46,
            height: 46,
            background: "radial-gradient(circle at 35% 30%, var(--color-dourado-light, #d4bc7d), var(--primary) 60%, var(--color-dourado-dark, #b8943f) 100%)",
            boxShadow: "0 0 60px 14px color-mix(in srgb, var(--primary) 45%, transparent)",
          }}
        />

        <div
          className="absolute left-1/2 top-1/2 h-[220px] w-[220px] -translate-x-1/2 -translate-y-1/2 rounded-full border border-primary/25"
        />
        <div
          className="absolute left-1/2 top-1/2 h-[380px] w-[380px] -translate-x-1/2 -translate-y-1/2 rounded-full border border-primary/15"
        />
        <div
          className="absolute left-1/2 top-1/2 h-[540px] w-[540px] -translate-x-1/2 -translate-y-1/2 rounded-full border border-primary/10"
        />

        <OrbitNode ring={220} size={8} duration={22} offset={20} tether />
        <OrbitNode ring={220} size={4} duration={26} offset={190} reverse />
        <OrbitNode ring={380} size={5} duration={38} offset={80} reverse />
        <OrbitNode ring={380} size={3} duration={34} offset={250} />
        <OrbitNode ring={540} size={6} duration={55} offset={140} tether />
        <OrbitNode ring={540} size={3.5} duration={48} offset={320} reverse />
      </div>
    </div>
  );
}
