export function LogoMark({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 40 40" className={className} fill="none" aria-hidden="true">
      <circle
        cx="20"
        cy="20"
        r="16"
        stroke="var(--primary)"
        strokeWidth="2"
        strokeLinecap="round"
        strokeDasharray="82 18"
        strokeDashoffset="4"
      />
      <circle cx="20" cy="4" r="2.6" fill="var(--primary)" />
    </svg>
  );
}
