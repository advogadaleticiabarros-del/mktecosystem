"use client";

import { useEffect, useState } from "react";
import { motion, useMotionValue, useReducedMotion, useSpring } from "framer-motion";

export function CursorGlow() {
  const reduzirMovimento = useReducedMotion() ?? false;
  const [visivel, setVisivel] = useState(false);

  const cursorX = useMotionValue(-999);
  const cursorY = useMotionValue(-999);
  const seguidorX = useSpring(cursorX, { stiffness: 140, damping: 22, mass: 0.4 });
  const seguidorY = useSpring(cursorY, { stiffness: 140, damping: 22, mass: 0.4 });

  useEffect(() => {
    if (reduzirMovimento) return;
    function handlePointerMove(event: PointerEvent) {
      cursorX.set(event.clientX);
      cursorY.set(event.clientY);
      setVisivel(true);
    }
    function handlePointerLeave() {
      setVisivel(false);
    }
    window.addEventListener("pointermove", handlePointerMove);
    window.addEventListener("pointerleave", handlePointerLeave);
    return () => {
      window.removeEventListener("pointermove", handlePointerMove);
      window.removeEventListener("pointerleave", handlePointerLeave);
    };
  }, [reduzirMovimento, cursorX, cursorY]);

  if (reduzirMovimento) return null;

  return (
    <motion.div
      className="pointer-events-none fixed left-0 top-0 z-0 rounded-full"
      aria-hidden="true"
      style={{
        x: seguidorX,
        y: seguidorY,
        translateX: "-50%",
        translateY: "-50%",
        width: 380,
        height: 380,
        background:
          "radial-gradient(circle, color-mix(in srgb, var(--primary) 35%, transparent) 0%, color-mix(in srgb, var(--primary) 12%, transparent) 45%, transparent 72%)",
      }}
      animate={{ opacity: visivel ? 1 : 0 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
    />
  );
}
