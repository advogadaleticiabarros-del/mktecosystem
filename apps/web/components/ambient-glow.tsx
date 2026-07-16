export function AmbientGlow() {
  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden" aria-hidden="true">
      <div className="absolute -left-24 top-1/4 h-[420px] w-[420px] animate-[spin_40s_linear_infinite] rounded-full border border-primary/20" />
      <div className="absolute -left-40 top-1/3 h-[560px] w-[560px] animate-[spin_60s_linear_infinite_reverse] rounded-full border border-primary/10" />
      <div className="absolute left-10 top-1/2 h-2 w-2 animate-pulse rounded-full bg-primary shadow-[0_0_20px_6px_var(--primary)]" />
      <div className="absolute left-52 top-1/4 h-1.5 w-1.5 animate-pulse rounded-full bg-primary shadow-[0_0_16px_4px_var(--primary)] [animation-delay:0.6s]" />
    </div>
  );
}
