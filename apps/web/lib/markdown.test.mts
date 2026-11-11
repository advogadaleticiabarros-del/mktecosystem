// Teste do leitor de Markdown: node --experimental-strip-types lib/markdown.test.mts
import { markdownParaHtml, emLinha } from "./markdown.ts";
import { readFileSync } from "node:fs";
import assert from "node:assert";
assert.equal(emLinha("a **b** *c* `d` <x>"), "a <strong>b</strong> <em>c</em> <code>d</code> &lt;x&gt;");
assert.equal(markdownParaHtml("| a | b |\n| --- | --- |\n| 1 | 2 |"), '<div class="tabela"><table><thead><tr><th>a</th><th>b</th></tr></thead><tbody><tr><td>1</td><td>2</td></tr></tbody></table></div>');
assert.equal(markdownParaHtml("- um\n- dois"), "<ul><li>um</li><li>dois</li></ul>");
assert.equal(markdownParaHtml("## T\n\ntexto\ncontinua"), "<h2>T</h2>\n<p>texto continua</p>");
assert.ok(markdownParaHtml("![x](https://a/b.jpg)").includes('<img src="https://a/b.jpg"'));
const h = markdownParaHtml(readFileSync(new URL("../../../docs/CADERNO_DA_MARCA.md", import.meta.url), "utf8"));
console.log("ok", h.length, (h.match(/<table>/g)||[]).length, "tabelas", (h.match(/<h2>/g)||[]).length, "seções");
