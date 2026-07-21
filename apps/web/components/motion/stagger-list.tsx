// apps/web/components/motion/stagger-list.tsx
"use client";

import { motion, useReducedMotion } from "framer-motion";

const CONTAINER_VARIANTS = {
  hidden: {},
  show: {
    transition: { staggerChildren: 0.08 },
  },
};

const ITEM_VARIANTS = {
  hidden: { opacity: 0, y: 12 },
  show: { opacity: 1, y: 0, transition: { duration: 0.35, ease: "easeOut" as const } },
};

export function StaggerList({
  children,
  className,
}: {
  children: React.ReactNode[];
  className?: string;
}) {
  const reduzirMovimento = useReducedMotion();

  if (reduzirMovimento) {
    return <div className={className}>{children}</div>;
  }

  return (
    <motion.div
      className={className}
      variants={CONTAINER_VARIANTS}
      initial="hidden"
      animate="show"
    >
      {children.map((child, indice) => (
        <motion.div key={indice} variants={ITEM_VARIANTS}>
          {child}
        </motion.div>
      ))}
    </motion.div>
  );
}
