/* Markdown simples → HTML, para mostrar no Orbit os documentos do repositório (Caderno da marca, editorial).
   Cobre o que esses documentos usam: títulos, parágrafos, listas, tabelas, imagens, links, negrito, itálico, código
   e linha horizontal. O texto é escapado antes de virar HTML. */

const escapar = (s: string) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

export function emLinha(texto: string): string {
  let s = escapar(texto);
  s = s.replace(/`([^`]+)`/g, "<code>$1</code>");
  s = s.replace(/!\[([^\]]*)\]\(([^)\s]+)\)/g, '<img src="$2" alt="$1" loading="lazy">');
  s = s.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noreferrer">$1</a>');
  s = s.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  s = s.replace(/(^|[^*])\*([^*\s][^*]*)\*/g, "$1<em>$2</em>");
  return s;
}

const celulas = (linha: string) => linha.trim().replace(/^\||\|$/g, "").split("|").map((c) => c.trim());

export function markdownParaHtml(md: string): string {
  const linhas = md.replace(/\r/g, "").split("\n");
  const out: string[] = [];
  let i = 0;
  while (i < linhas.length) {
    const l = linhas[i];
    if (!l.trim()) { i++; continue; }
    const t = l.match(/^(#{1,4})\s+(.*)$/);
    if (t) { out.push(`<h${t[1].length}>${emLinha(t[2])}</h${t[1].length}>`); i++; continue; }
    if (/^---+\s*$/.test(l)) { out.push("<hr>"); i++; continue; }
    if (l.trim().startsWith("|") && i + 1 < linhas.length && /^\s*\|?\s*:?-{3,}/.test(linhas[i + 1])) {
      const cab = celulas(l);
      i += 2;
      const corpo: string[][] = [];
      while (i < linhas.length && linhas[i].trim().startsWith("|")) corpo.push(celulas(linhas[i++]));
      out.push(`<div class="tabela"><table><thead><tr>${cab.map((c) => `<th>${emLinha(c)}</th>`).join("")}</tr></thead><tbody>${
        corpo.map((r) => `<tr>${r.map((c) => `<td>${emLinha(c)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`);
      continue;
    }
    const lista = l.match(/^(\s*)([-*]|\d+\.)\s+/);
    if (lista) {
      const ordenada = /\d/.test(lista[2]);
      const itens: string[] = [];
      while (i < linhas.length && /^\s*([-*]|\d+\.)\s+/.test(linhas[i])) {
        let item = linhas[i].replace(/^\s*([-*]|\d+\.)\s+/, "");
        i++;
        while (i < linhas.length && /^\s{2,}\S/.test(linhas[i]) && !/^\s*([-*]|\d+\.)\s+/.test(linhas[i])) item += " " + linhas[i++].trim();
        itens.push(`<li>${emLinha(item)}</li>`);
      }
      out.push(ordenada ? `<ol>${itens.join("")}</ol>` : `<ul>${itens.join("")}</ul>`);
      continue;
    }
    if (l.startsWith(">")) {
      const bloco: string[] = [];
      while (i < linhas.length && linhas[i].startsWith(">")) bloco.push(linhas[i++].replace(/^>\s?/, ""));
      out.push(`<blockquote>${emLinha(bloco.join(" "))}</blockquote>`);
      continue;
    }
    const par: string[] = [];
    while (i < linhas.length && linhas[i].trim() && !/^(#{1,4}\s|---+\s*$|\||>|\s*([-*]|\d+\.)\s+)/.test(linhas[i])) par.push(linhas[i++].trim());
    if (par.length) out.push(`<p>${emLinha(par.join(" "))}</p>`);
    else i++;
  }
  return out.join("\n");
}
