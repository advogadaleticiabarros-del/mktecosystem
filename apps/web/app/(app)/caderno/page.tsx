import { readFileSync } from "node:fs";
import path from "node:path";
import { AppShell } from "@/components/app-shell";
import { markdownParaHtml } from "@/lib/markdown";

/* Caderno da marca (pedido da Jessica em 10/11/2026: "salve todo o contexto lá no Orbit"): identidade, voz, estilos,
   Reels, quadros, grade e o editorial do feed. Lido dos documentos do repositório na hora do build, então
   basta atualizar docs/CADERNO_DA_MARCA.md ou docs/EDITORIAL_DO_FEED.md e publicar o web. */
const DOCS = path.join(process.cwd(), "..", "..", "docs");
const ler = (nome: string) => {
  try {
    return markdownParaHtml(readFileSync(path.join(DOCS, nome), "utf8"));
  } catch {
    return `<p>Documento ${nome} não encontrado no build.</p>`;
  }
};

export default function CadernoPage() {
  const caderno = ler("CADERNO_DA_MARCA.md");
  const editorial = ler("EDITORIAL_DO_FEED.md");
  return (
    <AppShell title="Caderno da marca" description="Identidade, voz, estilos, Reels, quadros e editorial do feed">
      <nav className="mb-6 flex flex-wrap gap-2 text-sm">
        <a href="#caderno" className="rounded-full border px-4 py-1.5 hover:bg-muted">Caderno</a>
        <a href="#editorial" className="rounded-full border px-4 py-1.5 hover:bg-muted">Editorial do feed</a>
      </nav>
      <article id="caderno" className="caderno" dangerouslySetInnerHTML={{ __html: caderno }} />
      <hr className="my-12" />
      <article id="editorial" className="caderno" dangerouslySetInnerHTML={{ __html: editorial }} />
    </AppShell>
  );
}
