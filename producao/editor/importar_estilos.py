"""Traz para o editor as peças dos estilos de producao/estilos, com os textos editáveis.

Roda o gerar.py de cada estilo como ele é, mas intercepta o Playwright e o PIL: no momento da foto da peça,
lê cada bloco de texto (posição, fonte, cor) e o esconde; a foto sem os textos, já com o acabamento dourado,
vira o fundo. Nada é gravado em producao/estilos: as peças prontas continuam como estão.
Uso: python importar_estilos.py [estilo ...]   (peça que já existe no editor é pulada, nunca sobrescrita)"""
import io
import os
import runpy
import sys
from pathlib import Path

from PIL import Image
from playwright.async_api._generated import Page

from acervo import Acervo, PecaInvalida

AQUI = Path(__file__).resolve().parent
ESTILOS = AQUI.parent / "estilos"
# Lotes que não são o gerar.py do estilo: nome → (pasta do estilo, script, argumentos).
LOTES = {"manchete-dez": ("manchete", "conteudo_planejado.py", ["dez"]),
         "manchete-nov": ("manchete", "conteudo_planejado.py", ["nov", "nov-11-1", "nov-11-2", "nov-11-3", "nov-12"])}
GERADORES = {"palavra-de-ouro": "gerar.py", "verbete": "gerar.py", "papel-e-ouro": "gerar.py", "objeto-em-cena": "gerar.py", "manchete": "gerar.py"}
NAO_IMPORTAR = {"palavra-de-ouro-grito-D-editorial"}  # já está no editor, com os ajustes da Jessica

# Devolve os blocos de texto e marca cada um com data-ed-oculto para sumir da foto do fundo.
EXTRAIR = r"""() => {
const tela = document.querySelector('.c') || document.body, base = tela.getBoundingClientRect();
const FONTES = ['EB Garamond', 'Playfair Display', 'Inter'];
const hex = (c) => { const m = c.match(/[\d.]+/g); if (!m) return null;
  return '#' + m.slice(0, 3).map((v) => (+v).toString(16).padStart(2, '0')).join('').toUpperCase(); };
const bloco = (n) => { while (n && n !== tela && getComputedStyle(n).display === 'inline') n = n.parentElement; return n; };
const vistos = new Set(), saida = [];
const caminhar = document.createTreeWalker(tela, NodeFilter.SHOW_TEXT);
while (caminhar.nextNode()) {
  const t = caminhar.currentNode;
  if (!t.textContent.trim() || t.parentElement.closest('svg,style,script')) continue;
  const b = bloco(t.parentElement);
  if (b && b !== tela && !vistos.has(b)) vistos.add(b);
}
const angulo = (n) => { let a = 0;
  for (let e = n; e && e !== tela; e = e.parentElement) { const m = getComputedStyle(e).transform;
    if (m && m !== 'none') { const v = m.match(/-?[\d.e]+/g).map(Number); a += Math.round(Math.atan2(v[1], v[0]) * 180 / Math.PI); } }
  return a; };
for (const b of vistos) {
  if ([...vistos].some((o) => o !== b && o.contains(b))) continue;
  const s = getComputedStyle(b), q = b.getBoundingClientRect();
  if (s.visibility === 'hidden' || +s.opacity === 0 || !q.width) continue;
  // Texto atrás de outra camada (letras atrás do retrato) fica no fundo, para não passar na frente da foto.
  const coberto = [...b.getClientRects()].some((r) => { const p = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
    return p && !b.contains(p) && !p.contains(b); });
  if (coberto) continue;
  const fonte = FONTES.find((f) => s.fontFamily.includes(f));
  const rot = angulo(b);
  if (!fonte || ![0, -90, 90].includes(rot)) continue;
  const tamanho = parseFloat(s.fontSize);
  const caixa = s.textTransform === 'uppercase' ? (x) => x.toUpperCase() : (x) => x;
  let destaque = null, marca = null;
  const html = (n) => [...n.childNodes].map((c) => {
    if (c.nodeType === 3) return caixa(c.textContent).replace(/&/g, '&amp;').replace(/</g, '&lt;');
    if (c.nodeType !== 1 || c.closest('svg')) return '';
    if (c.tagName === 'BR') return '<br>';
    const cs = getComputedStyle(c);
    if (cs.display !== 'inline' && c !== n) return '';
    if (cs.fontStyle === 'italic' && s.fontStyle !== 'italic') { destaque = destaque || cs; return '<i>' + html(c) + '</i>'; }
    if (cs.verticalAlign === 'super' || parseFloat(cs.fontSize) < tamanho * 0.8) return '<sup>' + html(c) + '</sup>';
    if (+cs.fontWeight >= +s.fontWeight + 200) return '<b>' + html(c) + '</b>';
    if (hex(cs.color) !== hex(s.color) && cs.backgroundClip !== 'text') { marca = marca || hex(cs.color); return '<mark>' + html(c) + '</mark>'; }
    return html(c);
  }).join('');
  let texto = html(b).replace(/\s+/g, ' ').replace(/ ?<br> ?/g, '<br>').trim();
  const todoItalico = s.fontStyle === 'italic';
  if (todoItalico) texto = '<i>' + texto + '</i>';
  if (!texto) continue;
  const ouro = s.backgroundClip === 'text' || s.webkitBackgroundClip === 'text';
  const pad = ouro ? { l: 0, t: 0 } : { l: parseFloat(s.paddingLeft) + parseFloat(s.borderLeftWidth), t: parseFloat(s.paddingTop) + parseFloat(s.borderTopWidth) };
  const largura = b.clientWidth - parseFloat(s.paddingLeft) - parseFloat(s.paddingRight), altura = b.clientHeight;
  let x = q.left - base.left + pad.l, y = q.top - base.top + pad.t;
  // Bloco com imagem dentro (assinatura com logo): a posição é a do texto, não a da caixa toda.
  if (b.querySelector('img,svg') && !rot) {
    const r = document.createRange(), nos = [...b.childNodes].filter((c) => c.nodeType === 3 && c.textContent.trim());
    r.setStartBefore(nos[0]); r.setEndAfter(nos[nos.length - 1]);
    const rr = r.getBoundingClientRect(), lhPx = s.lineHeight === 'normal' ? rr.height : parseFloat(s.lineHeight);
    x = rr.left - base.left; y = rr.top - base.top - (lhPx - rr.height) / 2;
  }
  if (rot === -90) { x = q.left - base.left + pad.t; y = q.bottom - base.top - pad.l; }
  if (rot === 90) { x = q.right - base.left - pad.t; y = q.top - base.top + pad.l; }
  const lh = s.lineHeight === 'normal' ? 'normal' : Math.round(parseFloat(s.lineHeight) / tamanho * 1000) / 1000;
  const cor = ouro ? 'ouro-brilho' : hex(s.color);
  const destCor = destaque && (destaque.backgroundClip === 'text' || destaque.webkitBackgroundClip === 'text') ? 'ouro-brilho' : destaque && hex(destaque.color);
  saida.push({ tipo: 'texto', x: Math.round(x * 100) / 100, y: Math.round(y * 100) / 100, html: texto, fonte, tamanho,
    cor, peso: +s.fontWeight, entrelinha: lh, espacamento: Math.round(parseFloat(s.letterSpacing || 0) / tamanho * 10000) / 10000 || 0,
    alinhamento: ['center', 'right', 'end'].includes(s.textAlign) ? (s.textAlign === 'end' ? 'right' : s.textAlign) : 'left',
    largura: s.whiteSpace === 'nowrap' ? null : Math.ceil(largura) + 1, rotacao: rot || null,
    cor_destaque: todoItalico ? null : (destCor && destCor !== cor ? destCor : null),
    peso_destaque: todoItalico ? +s.fontWeight : (destaque ? +destaque.fontWeight : null),
    cor_marca: marca, _altura: altura });
  b.setAttribute('data-ed-oculto', '');
}
const estilo = document.createElement('style');
estilo.id = 'ed-oculto';
estilo.textContent = '[data-ed-oculto]{color:transparent!important;-webkit-text-fill-color:transparent!important;text-shadow:none!important}'
  + '[data-ed-oculto][style*=clip],[data-ed-oculto].f{background:none!important}';
document.head.append(estilo);
for (const b of document.querySelectorAll('[data-ed-oculto]')) if (getComputedStyle(b).backgroundClip === 'text') b.style.setProperty('background', 'none', 'important');
return saida;
}"""


def _limpar(t):
    e = {k: v for k, v in t.items() if v is not None and not k.startswith("_")}
    if e["tamanho"] < 22:  # o manual não aceita; peças antigas com menos ficam no limite e o aviso sai no relatório
        e["tamanho_original"] = e["tamanho"]
        e["tamanho"] = 22
    return e


def documento(textos, fundo="fundo.jpg"):
    elementos = [{"id": "fundo", "nome": "Fundo (foto e acabamento)", "tipo": "imagem", "x": 0, "y": 0, "largura": 1080,
                  "altura": 1440, "arquivo": fundo, "pb": False}]
    for i, t in enumerate(textos, 1):
        e = _limpar(t)
        nome = e["html"].replace("<br>", " ").replace("<i>", "").replace("</i>", "")
        elementos.append({"id": f"texto-{i}", "nome": nome[:30], **e})
    return {"largura": 1080, "altura": 1440, "fundo": "#231E1A", "elementos": elementos}


def importar(estilo, acervo, so=()):
    capturas, pendente = {}, []
    tirar_foto, gravar = Page.screenshot, Image.Image.save

    async def foto_sem_texto(self, *a, **k):
        pendente.append(await self.evaluate(EXTRAIR))
        return await tirar_foto(self, *a, **k)

    def interceptar(img, destino, *a, **k):
        caminho = Path(str(destino)) if isinstance(destino, (str, Path)) else None
        if caminho is None:
            return gravar(img, destino, *a, **k)
        if pendente and img.size == (1080, 1440):
            capturas[caminho.stem] = (pendente.pop(), img.copy())
        # o resto (grade, tira) não é gravado: nada em producao/estilos muda

    pasta_estilo, script, args = LOTES.get(estilo, (estilo, GERADORES.get(estilo), []))
    pasta = ESTILOS / pasta_estilo
    Page.screenshot, Image.Image.save = foto_sem_texto, interceptar
    argv, cwd = sys.argv, Path.cwd()
    os.environ["EDITOR_IMPORTA"] = "1"  # o lote pula peça já gravada; aqui ela precisa ser refeita para a captura
    try:
        sys.argv = [str(pasta / script), *(args or []), *so]
        sys.path.insert(0, str(pasta))
        runpy.run_path(str(pasta / script), run_name="__main__")
    finally:
        Page.screenshot, Image.Image.save = tirar_foto, gravar
        os.environ.pop("EDITOR_IMPORTA", None)
        sys.argv = argv
        sys.path.remove(str(pasta))
        for m in ("base",):
            sys.modules.pop(m, None)
    feitos = []
    for nome, (textos, fundo) in capturas.items():
        peca = nome if nome.startswith(pasta_estilo) else f"{pasta_estilo}-{nome}"
        if peca in NAO_IMPORTAR or peca in acervo.nomes():
            continue
        b = io.BytesIO()
        fundo.convert("RGB").save(b, "JPEG", quality=95)
        try:
            acervo.criar(peca, documento(textos), {"fundo.jpg": b.getvalue()})
        except PecaInvalida as erro:
            print(f"{peca}: não importada ({erro})")
            continue
        pequenos = [t for t in textos if t["tamanho"] < 22]
        feitos.append((peca, len(textos), len(pequenos)))
    return feitos


if __name__ == "__main__":
    acervo = Acervo(AQUI)
    for estilo in sys.argv[1:] or [*GERADORES, *LOTES]:
        for peca, n, pequenos in importar(estilo, acervo):
            print(f"{peca}: {n} textos" + (f", {pequenos} abaixo de 22 px ajustados" if pequenos else ""))
