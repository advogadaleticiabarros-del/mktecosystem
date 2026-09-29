"use client";

function textoPuroDoHtml(html: string): string {
  if (typeof window === "undefined") return html;
  const container = document.createElement("div");
  container.innerHTML = html;
  return container.textContent?.trim() ?? "";
}

export function ArtigoLeitura({ html, titulo }: { html: string; titulo?: string }) {
  const texto = textoPuroDoHtml(html);

  return (
    <div>
      {titulo && (
        <div style={{ fontSize: 19, fontWeight: 700, marginTop: 12, marginBottom: 8 }}>
          {titulo}
        </div>
      )}
      <div
        style={{
          fontSize: 15,
          lineHeight: 1.6,
          color: "var(--foreground)",
          whiteSpace: "pre-wrap",
        }}
      >
        {texto || "Texto do artigo ainda não disponível."}
      </div>
    </div>
  );
}
