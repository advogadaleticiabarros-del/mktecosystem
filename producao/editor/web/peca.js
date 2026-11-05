// Desenha uma peça a partir do documento. É o único desenho: o editor e a exportação usam esta mesma função,
// então a imagem baixada sai igual à tela. Valores visuais vêm de producao/estilos/palavra-de-ouro/base.py.
const OURO_BRILHO = "ouro-brilho";
const FOIL = "linear-gradient(112deg,#a57a2c 0%,#dcbc6a 14%,#f9efc2 27%,#d2aa54 41%,#a67c2e 56%,#ebd590 70%,#fcf4cc 80%,#bb923f 100%)";
const GRAO = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='900' height='900'%3E%3Cfilter id='n'%3E"
  + "%3CfeTurbulence type='fractalNoise' baseFrequency='.95' numOctaves='3' stitchTiles='stitch'/%3E"
  + "%3CfeColorMatrix values='0 0 0 0 .9 0 0 0 0 .9 0 0 0 0 .9 0 0 0 .9 0'/%3E%3C/filter%3E"
  + "%3Crect width='900' height='900' filter='url(%23n)'/%3E%3C/svg%3E";

// Só <i> e <br> sobrevivem: colar texto de outro lugar não traz estilo nem código junto.
function limparTexto(html) {
  const saida = document.createElement("div");
  const copiar = (origem, destino) => {
    for (const no of origem.childNodes) {
      if (no.nodeType === Node.TEXT_NODE) destino.append(no.textContent);
      else if (no.nodeType === Node.ELEMENT_NODE) {
        const tag = no.tagName;
        if (tag === "BR") destino.append(document.createElement("br"));
        else if (tag === "I" || tag === "EM") copiar(no, destino.appendChild(document.createElement("i")));
        else {
          // Enter no campo de texto vira <div>: cada um é uma linha nova.
          if ((tag === "DIV" || tag === "P") && destino.childNodes.length) destino.append(document.createElement("br"));
          copiar(no, destino);
        }
      }
    }
  };
  copiar(new DOMParser().parseFromString(html, "text/html").body, saida);
  return saida.innerHTML;
}

function filtroDaFoto(e) {
  return `${e.pb === false ? "" : "grayscale(1) "}sepia(${e.sepia ?? 0}) brightness(${e.brilho ?? 1}) contrast(${e.contraste ?? 1})`;
}

function montarTexto(n, e) {
  n.innerHTML = limparTexto(e.html);
  Object.assign(n.style, {
    fontFamily: `'${e.fonte}',${e.fonte === "Inter" ? "sans-serif" : "serif"}`,
    fontSize: e.tamanho + "px",
    fontWeight: e.peso ?? 400,
    lineHeight: e.entrelinha ?? "normal",
    letterSpacing: (e.espacamento ?? 0) + "em",
    textAlign: e.alinhamento ?? "left",
    width: e.largura ? e.largura + "px" : "max-content",
    whiteSpace: e.largura ? "normal" : "nowrap",
  });
  if (e.cor === OURO_BRILHO) {
    Object.assign(n.style, { background: FOIL, webkitBackgroundClip: "text", backgroundClip: "text", color: "transparent", padding: ".12em .1em .16em 0", caretColor: "#E8DED1" });
  } else {
    n.style.color = e.cor;
  }
  for (const i of n.querySelectorAll("i")) {
    i.style.fontWeight = e.peso_destaque ?? 400;
    if (e.cor_destaque === OURO_BRILHO) {
      // O respiro evita cortar o traço inclinado do itálico.
      Object.assign(i.style, { background: FOIL, webkitBackgroundClip: "text", backgroundClip: "text", color: "transparent", padding: "0 .08em .1em 0", marginRight: "-.08em", caretColor: "#E8DED1" });
    } else if (e.cor_destaque) {
      i.style.color = e.cor_destaque;
    }
  }
}

function montarImagem(n, e, urlFoto) {
  Object.assign(n.style, { width: e.largura + "px", height: e.altura + "px", overflow: "hidden", mixBlendMode: e.mistura ?? "normal" });
  if (e.mascara_caixa) { n.style.webkitMaskImage = e.mascara_caixa; n.style.maskImage = e.mascara_caixa; }
  const img = document.createElement("img");
  img.src = urlFoto(e.arquivo);
  img.draggable = false;
  Object.assign(img.style, { width: "100%", display: "block", filter: filtroDaFoto(e) });
  if (e.mascara_foto) { img.style.webkitMaskImage = e.mascara_foto; img.style.maskImage = e.mascara_foto; }
  n.append(img);
}

// Luz: brilho redondo que some nas bordas. O canto redondo também faz o clique valer só dentro do círculo.
function montarLuz(n, e) {
  Object.assign(n.style, {
    width: e.largura + "px", height: e.altura + "px", borderRadius: "50%", opacity: e.intensidade ?? 0.5, mixBlendMode: e.mistura ?? "screen",
    background: `radial-gradient(closest-side,${e.cor},transparent)`,
  });
}

function desenharPeca(doc, palco, urlFoto) {
  palco.replaceChildren();
  Object.assign(palco.style, {
    width: doc.largura + "px", height: doc.altura + "px", position: "relative", overflow: "hidden", background: doc.fundo,
    isolation: "isolate", fontVariantNumeric: "lining-nums", fontKerning: "normal",
  });
  const grao = document.createElement("div");
  grao.className = "grao";
  Object.assign(grao.style, { position: "absolute", inset: 0, zIndex: -1, pointerEvents: "none", background: `url("${GRAO}")`, mixBlendMode: "screen", opacity: 0.03 });
  palco.append(grao);
  for (const e of doc.elementos) palco.append(desenharElemento(e, urlFoto));
}

function desenharElemento(e, urlFoto) {
  const n = document.createElement("div");
  n.dataset.id = e.id;
  n.className = "el el-" + e.tipo;
  Object.assign(n.style, { position: "absolute", left: e.x + "px", top: e.y + "px", transformOrigin: "0 0", transform: e.rotacao ? `rotate(${e.rotacao}deg)` : "" });
  if (e.tipo === "texto") montarTexto(n, e);
  else if (e.tipo === "imagem") montarImagem(n, e, urlFoto);
  else if (e.tipo === "luz") montarLuz(n, e);
  else Object.assign(n.style, { width: e.largura + "px", height: e.altura + "px", background: e.cor === OURO_BRILHO ? FOIL : e.cor });
  return n;
}

// Fontes e fotos carregadas: só depois disso a imagem pode ser tirada.
async function pecaCarregada(doc, palco) {
  const pedidos = doc.elementos.filter((e) => e.tipo === "texto").flatMap((e) => [
    `${e.peso ?? 400} ${e.tamanho}px '${e.fonte}'`,
    `italic ${e.peso_destaque ?? 400} ${e.tamanho}px '${e.fonte}'`,
  ]);
  await Promise.all(pedidos.map((f) => document.fonts.load(f).catch(() => null)));
  await document.fonts.ready;
  await Promise.all([...palco.querySelectorAll("img")].map((i) => i.decode().catch(() => null)));
}
