"use client";

import { useState } from "react";

export function ImageCarousel({ imagens, alt }: { imagens: string[]; alt: string }) {
  const [ativo, setAtivo] = useState(0);
  const carrossel = imagens.length > 1;

  return (
    <div>
      <div
        className="editorial-image-frame"
        data-carousel={carrossel}
        onScroll={(e) => {
          if (!carrossel) return;
          const el = e.currentTarget;
          const indice = Math.round(el.scrollLeft / el.clientWidth);
          setAtivo(indice);
        }}
      >
        {imagens.map((src, i) => (
          // eslint-disable-next-line @next/next/no-img-element
          <img key={src + i} src={src} alt={`${alt} ${i + 1}`} loading="lazy" />
        ))}
      </div>
      {carrossel && (
        <div className="editorial-dots">
          {imagens.map((_, i) => (
            <span key={i} className="editorial-dot" data-active={i === ativo} />
          ))}
        </div>
      )}
    </div>
  );
}
