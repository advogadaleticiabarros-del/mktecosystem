// Interação do editor: selecionar, arrastar, redimensionar, escrever, painel, desfazer e salvar.
// O desenho fica em peca.js; o documento em memória é a única verdade e cada gesto termina em registrar().
const OURO = "#C9A962", AREIA = "#EFE6D9", TAMANHO_MINIMO = 22, ENCOSTO = 6;
const CORES = [["Ouro com brilho", OURO_BRILHO, FOIL], ["Ouro", OURO, OURO], ["Areia", AREIA, AREIA], ["Branco", "#FFFFFF", "#FFFFFF"], ["Café", "#231E1A", "#231E1A"]];
const FUNDOS = [["Café", "#231E1A"], ["Café escuro", "#1E1814"], ["Papel", "#EFE6D9"]];
const $ = (s) => document.querySelector(s);
const palco = $("#palco"), area = $("#palco-area"), escalaEl = $("#palco-escala"), selecao = $("#selecao");

let nomePeca = null, doc = null, selecionado = null, escala = 1, editando = null;
let historico = [], posicao = 0, temporizador = null, salvamento = Promise.resolve();

const urlPeca = () => `/api/pecas/${encodeURIComponent(nomePeca)}`;
const urlFoto = (a) => `${urlPeca()}/fotos/${a}`;
const atual = () => doc.elementos.find((e) => e.id === selecionado) || null;
const noDe = (id) => palco.querySelector(`[data-id="${CSS.escape(id)}"]`);
const arred = (v) => Math.round(v * 100) / 100;

function situacao(texto, erro = false) {
  const s = $("#situacao");
  s.textContent = texto;
  s.classList.toggle("erro", erro);
}

function avisar(texto) {
  const a = $("#aviso");
  a.textContent = texto;
  a.hidden = false;
  clearTimeout(avisar.t);
  avisar.t = setTimeout(() => { a.hidden = true; }, 5000);
}

async function pedir(caminho, opcoes) {
  const r = await fetch(caminho, opcoes);
  const dados = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(dados.erro || "Não consegui falar com o editor. A janela preta continua aberta?");
  return dados;
}

// --- salvar e desfazer ---

function salvarJa() {
  clearTimeout(temporizador);
  temporizador = null;
  const nome = urlPeca(), corpo = JSON.stringify(doc);
  salvamento = salvamento.then(() => pedir(nome, { method: "PUT", body: corpo, headers: { "Content-Type": "application/json" } }))
    .then(() => { if (!temporizador) situacao("Salvo"); })
    .catch((erro) => situacao(erro.message, true));
  return salvamento;
}

function registrar() {
  const agora = JSON.stringify(doc);
  if (agora === historico[posicao]) return;
  historico = historico.slice(0, posicao + 1);
  historico.push(agora);
  if (historico.length > 200) historico.shift();
  posicao = historico.length - 1;
  botoesHistorico();
  situacao("Salvando…");
  clearTimeout(temporizador);
  temporizador = setTimeout(salvarJa, 300);
}

function botoesHistorico() {
  $("#desfazer").disabled = posicao === 0;
  $("#refazer").disabled = posicao >= historico.length - 1;
}

function andarHistorico(passo) {
  const nova = posicao + passo;
  if (nova < 0 || nova >= historico.length) return;
  posicao = nova;
  doc = JSON.parse(historico[posicao]);
  if (!atual()) selecionado = null;
  redesenhar();
  botoesHistorico();
  situacao("Salvando…");
  clearTimeout(temporizador);
  temporizador = setTimeout(salvarJa, 300);
}

// --- desenho ---

function ajustarEscala() {
  const margem = 24, h = area.clientHeight - margem * 2, l = area.clientWidth - margem * 2;
  escala = Math.min(h / doc.altura, l / doc.largura);
  escalaEl.style.transform = `scale(${escala})`;
  escalaEl.style.left = (area.clientWidth - doc.largura * escala) / 2 + "px";
  escalaEl.style.top = (area.clientHeight - doc.altura * escala) / 2 + "px";
  moldura();
}

function redesenhar() {
  desenharPeca(doc, palco, urlFoto);
  pecaCarregada(doc, palco).then(moldura);
  ajustarEscala();
  montarPainel();
  montarCamadas();
}

function redesenharElemento(e) {
  const velho = noDe(e.id);
  if (velho) velho.replaceWith(desenharElemento(e, urlFoto));
  moldura();
}

function moldura() {
  const n = selecionado && noDe(selecionado);
  selecao.hidden = !n;
  if (!n) return;
  const q = n.getBoundingClientRect(), base = area.getBoundingClientRect();
  Object.assign(selecao.style, { left: q.left - base.left + "px", top: q.top - base.top + "px", width: q.width + "px", height: q.height + "px" });
}

function selecionar(id) {
  if (selecionado === id) return;
  selecionado = id;
  moldura();
  montarPainel();
  montarCamadas();
}

// --- escrever no texto ---

function comecarEdicao(id) {
  const e = doc.elementos.find((x) => x.id === id);
  if (!e || e.tipo !== "texto") return;
  const n = noDe(id);
  editando = id;
  n.contentEditable = "true";
  n.focus();
  document.getSelection().selectAllChildren(n);
  document.getSelection().collapseToEnd();
  selecao.style.display = "none";
  montarPainel();
  n.addEventListener("blur", () => terminarEdicao(n, e), { once: true });
  n.addEventListener("keydown", (ev) => {
    ev.stopPropagation();
    if (ev.key === "Escape") n.blur();
    if (ev.key === "Enter") { ev.preventDefault(); document.execCommand("insertLineBreak"); }
  });
  n.addEventListener("paste", (ev) => {
    ev.preventDefault();
    document.execCommand("insertText", false, ev.clipboardData.getData("text/plain"));
  });
}

function terminarEdicao(n, e) {
  const html = limparTexto(n.innerHTML).replace(/(<br>)+$/, "");
  editando = null;
  selecao.style.display = "";
  if (n.textContent.trim()) e.html = html;
  else avisar("O texto não pode ficar vazio. Para tirar, use Excluir.");
  redesenharElemento(e);
  montarPainel();
  registrar();
}

// --- arrastar e redimensionar ---

function encostos(ignorar) {
  const xs = [96, doc.largura / 2, doc.largura - 96], ys = [96, doc.altura / 2, doc.altura - 96];
  const base = palco.getBoundingClientRect();
  for (const n of palco.querySelectorAll(".el")) {
    if (n.dataset.id === ignorar) continue;
    const q = n.getBoundingClientRect();
    xs.push((q.left - base.left) / escala, (q.right - base.left) / escala);
    ys.push((q.top - base.top) / escala, (q.bottom - base.top) / escala);
  }
  return { xs, ys };
}

function encostar(pontos, alvos, delta) {
  let melhor = null;
  for (const p of pontos) for (const a of alvos) {
    const d = a - (p + delta);
    if (Math.abs(d) <= ENCOSTO && (!melhor || Math.abs(d) < Math.abs(melhor.d))) melhor = { d, a };
  }
  return melhor;
}

function mostrarGuia(el, propriedade, valor) {
  el.hidden = valor === null;
  if (valor === null) return;
  const q = palco.getBoundingClientRect(), base = area.getBoundingClientRect();
  el.style[propriedade] = (propriedade === "left" ? q.left - base.left : q.top - base.top) + valor * escala + "px";
}

function arrastar(ev, e) {
  const n = noDe(e.id), x0 = e.x, y0 = e.y, cx = ev.clientX, cy = ev.clientY;
  const q0 = n.getBoundingClientRect(), base = palco.getBoundingClientRect();
  const caixa = { l: (q0.left - base.left) / escala, r: (q0.right - base.left) / escala, t: (q0.top - base.top) / escala, b: (q0.bottom - base.top) / escala };
  const alvos = encostos(e.id);
  let moveu = false;
  const mover = (m) => {
    let dx = (m.clientX - cx) / escala, dy = (m.clientY - cy) / escala;
    if (!moveu && Math.hypot(dx, dy) * escala < 3) return;
    moveu = true;
    const ex = m.altKey ? null : encostar([caixa.l, (caixa.l + caixa.r) / 2, caixa.r], alvos.xs, dx);
    const ey = m.altKey ? null : encostar([caixa.t, (caixa.t + caixa.b) / 2, caixa.b], alvos.ys, dy);
    if (ex) dx += ex.d;
    if (ey) dy += ey.d;
    mostrarGuia($("#guia-x"), "left", ex ? ex.a : null);
    mostrarGuia($("#guia-y"), "top", ey ? ey.a : null);
    e.x = arred(x0 + dx);
    e.y = arred(y0 + dy);
    n.style.left = e.x + "px";
    n.style.top = e.y + "px";
    moldura();
  };
  soltarDepois(mover, () => {
    mostrarGuia($("#guia-x"), "left", null);
    mostrarGuia($("#guia-y"), "top", null);
    montarPainel();
    registrar();
  });
}

function redimensionar(ev, e) {
  const q = noDe(e.id).getBoundingClientRect();
  const cx = q.left + q.width / 2, cy = q.top + q.height / 2, r0 = Math.max(Math.hypot(ev.clientX - cx, ev.clientY - cy), 1);
  const inicio = { tamanho: e.tamanho, largura: e.largura, altura: e.altura }, x0 = ev.clientX, y0 = ev.clientY;
  soltarDepois((m) => {
    const fator = Math.hypot(m.clientX - cx, m.clientY - cy) / r0;
    if (e.tipo === "retangulo") {
      e.largura = Math.max(1, Math.round(inicio.largura + (m.clientX - x0) / escala));
      e.altura = Math.max(1, Math.round(inicio.altura + (m.clientY - y0) / escala));
    } else if (e.tipo === "imagem") {
      e.largura = Math.round(inicio.largura * fator);
      e.altura = Math.round(inicio.altura * fator);
    } else {
      e.tamanho = Math.max(TAMANHO_MINIMO, Math.round(inicio.tamanho * fator));
      if (inicio.largura) e.largura = Math.round(inicio.largura * fator);
    }
    redesenharElemento(e);
  }, () => { montarPainel(); registrar(); });
}

function soltarDepois(mover, soltar) {
  const fim = () => {
    window.removeEventListener("pointermove", mover);
    window.removeEventListener("pointerup", fim);
    soltar();
  };
  window.addEventListener("pointermove", mover);
  window.addEventListener("pointerup", fim);
}

palco.addEventListener("pointerdown", (ev) => {
  const n = ev.target.closest(".el");
  if (!n || n.isContentEditable) return;
  if (ev.button !== 0) return;
  selecionar(n.dataset.id);
  arrastar(ev, atual());
});
palco.addEventListener("dragstart", (ev) => ev.preventDefault());
palco.addEventListener("dblclick", (ev) => {
  const n = ev.target.closest(".el");
  if (n) comecarEdicao(n.dataset.id);
});
$("#alca").addEventListener("pointerdown", (ev) => {
  ev.preventDefault();
  ev.stopPropagation();
  if (atual()) redimensionar(ev, atual());
});
area.addEventListener("pointerdown", (ev) => {
  if (ev.target === area) {
    if (editando) document.activeElement.blur();
    selecionar(null);
  }
});

// --- painel ---

function campo(rotulo, entrada) {
  const l = document.createElement("label");
  l.className = "campo";
  const s = document.createElement("span");
  s.textContent = rotulo;
  l.append(s, entrada);
  return l;
}

function numero(rotulo, valor, aoMudar, { min, passo = 1, vazio = false } = {}) {
  const i = document.createElement("input");
  i.type = "number";
  i.step = passo;
  if (min !== undefined) i.min = min;
  i.value = valor ?? "";
  if (vazio) i.placeholder = "automática";
  i.addEventListener("input", () => { if (i.value !== "" && (min === undefined || +i.value >= min)) aoMudar(+i.value); });
  i.addEventListener("change", () => {
    if (i.value === "" && vazio) aoMudar(null);
    else if (i.value === "" || (min !== undefined && +i.value < min)) { i.value = min ?? 0; aoMudar(+i.value); if (min === TAMANHO_MINIMO) avisar(`Nada abaixo de ${TAMANHO_MINIMO} px: é regra do manual de conteúdo.`); }
    registrar();
  });
  return campo(rotulo, i);
}

function escolha(rotulo, valor, opcoes, aoMudar) {
  const s = document.createElement("select");
  for (const [texto, v] of opcoes) s.add(new Option(texto, v, false, String(v) === String(valor)));
  s.addEventListener("change", () => { aoMudar(s.value); registrar(); });
  return campo(rotulo, s);
}

function botao(texto, aoClicar) {
  const b = document.createElement("button");
  b.textContent = texto;
  b.addEventListener("click", aoClicar);
  return b;
}

function seletorCor(rotulo, valor, cores, aoMudar) {
  const caixa = document.createElement("div");
  const t = document.createElement("span");
  t.className = "dica";
  t.textContent = rotulo;
  const linha = document.createElement("div");
  linha.className = "cores";
  for (const [nome, v, amostra] of cores) {
    const b = document.createElement("button");
    b.className = "cor" + (v === valor ? " ativa" : "");
    b.title = nome;
    b.setAttribute("aria-label", nome);
    b.style.background = amostra ?? v;
    b.addEventListener("click", () => { aoMudar(v); registrar(); montarPainel(); });
    linha.append(b);
  }
  const livre = document.createElement("input");
  livre.type = "color";
  livre.title = "Outra cor";
  livre.setAttribute("aria-label", `${rotulo}: outra cor`);
  livre.value = /^#[0-9a-f]{6}$/i.test(valor || "") ? valor : "#C9A962";
  livre.addEventListener("input", () => aoMudar(livre.value));
  livre.addEventListener("change", () => { registrar(); montarPainel(); });
  linha.append(livre);
  caixa.append(t, linha);
  return caixa;
}

function posicaoCampos(e) {
  const d = document.createElement("div");
  d.className = "dois";
  const muda = (k) => (v) => { e[k] = v; redesenharElemento(e); };
  d.append(numero("Horizontal (X)", e.x, muda("x")), numero("Vertical (Y)", e.y, muda("y")));
  return d;
}

function painelTexto(e) {
  const p = $("#painel"), muda = (k) => (v) => { e[k] = v; redesenharElemento(e); };
  const destacar = botao("Destacar trecho selecionado", () => document.execCommand("italic"));
  destacar.addEventListener("mousedown", (ev) => ev.preventDefault());
  destacar.disabled = editando !== e.id;
  const dica = document.createElement("p");
  dica.className = "dica";
  dica.textContent = editando === e.id
    ? "Selecione um trecho e clique para deixá-lo em itálico e na cor de destaque. Clique fora para terminar."
    : "Clique duas vezes no texto para escrever.";
  p.append(dica, destacar);
  const dois = document.createElement("div");
  dois.className = "dois";
  dois.style.marginTop = "10px";
  dois.append(
    numero("Tamanho", e.tamanho, muda("tamanho"), { min: TAMANHO_MINIMO }),
    numero("Largura da caixa", e.largura, muda("largura"), { min: 40, vazio: true }),
  );
  p.append(dois);
  p.append(escolha("Fonte", e.fonte, [["EB Garamond (títulos)", "EB Garamond"], ["Inter (textos)", "Inter"]], muda("fonte")));
  p.append(escolha("Peso", e.peso ?? 400, [["Normal", 400], ["Médio", 500], ["Forte", 600]], (v) => muda("peso")(+v)));
  p.append(seletorCor("Cor do texto", e.cor, CORES, muda("cor")));
  p.append(seletorCor("Cor do destaque (itálico)", e.cor_destaque, CORES.slice(1), muda("cor_destaque")));
  p.append(escolha("Alinhamento", e.alinhamento ?? "left", [["Esquerda", "left"], ["Centro", "center"], ["Direita", "right"]], muda("alinhamento")));
  const finos = document.createElement("div");
  finos.className = "dois";
  finos.append(
    numero("Entrelinha", typeof e.entrelinha === "number" ? e.entrelinha : 1.2, muda("entrelinha"), { min: 0.7, passo: 0.02 }),
    numero("Espaço entre letras", e.espacamento ?? 0, muda("espacamento"), { passo: 0.005 }),
  );
  p.append(finos, numero("Girar (graus)", e.rotacao ?? 0, muda("rotacao"), { passo: 90 }));
}

function painelImagem(e) {
  const p = $("#painel"), muda = (k) => (v) => { e[k] = v; redesenharElemento(e); };
  p.append(botao("Trocar foto", () => pedirFoto("trocar")));
  const pb = document.createElement("input");
  pb.type = "checkbox";
  pb.checked = e.pb !== false;
  pb.addEventListener("change", () => { e.pb = pb.checked; redesenharElemento(e); registrar(); });
  const l = document.createElement("label");
  l.className = "campo";
  l.style.marginTop = "10px";
  l.append(pb, "Preto e branco");
  const dica = document.createElement("p");
  dica.className = "dica";
  dica.textContent = "Foto da Dra. fica sempre com a cor original, sem preto e branco.";
  const dois = document.createElement("div");
  dois.className = "dois";
  dois.append(
    numero("Brilho", e.brilho ?? 1, muda("brilho"), { min: 0.2, passo: 0.05 }),
    numero("Contraste", e.contraste ?? 1, muda("contraste"), { min: 0.2, passo: 0.05 }),
    numero("Largura", e.largura, muda("largura"), { min: 20 }),
    numero("Altura", e.altura, muda("altura"), { min: 20 }),
  );
  p.append(l, dica, dois, numero("Girar (graus)", e.rotacao ?? 0, muda("rotacao"), { passo: 90 }));
}

function painelRetangulo(e) {
  const p = $("#painel"), muda = (k) => (v) => { e[k] = v; redesenharElemento(e); };
  p.append(seletorCor("Cor", e.cor, CORES.slice(1), muda("cor")));
  const dois = document.createElement("div");
  dois.className = "dois";
  dois.append(numero("Largura", e.largura, muda("largura"), { min: 1 }), numero("Espessura", e.altura, muda("altura"), { min: 1 }));
  p.append(dois);
}

function montarPainel() {
  const p = $("#painel"), e = atual();
  p.replaceChildren();
  if (!e) {
    const dica = document.createElement("p");
    dica.className = "dica";
    dica.style.marginTop = "12px";
    dica.textContent = "Clique em um elemento da arte para alterá-lo. Clique duas vezes em um texto para escrever. Tudo é salvo sozinho.";
    p.append(dica, seletorCor("Cor do fundo", doc.fundo, FUNDOS, (v) => { doc.fundo = v; palco.style.background = v; }));
    return;
  }
  const titulo = document.createElement("h2");
  titulo.textContent = e.nome || e.id;
  p.append(titulo);
  ({ texto: painelTexto, imagem: painelImagem, retangulo: painelRetangulo })[e.tipo](e);
  p.append(posicaoCampos(e));
  const linha = document.createElement("div");
  linha.className = "linha";
  linha.append(botao("Para frente", () => mudarOrdem(e, 1)), botao("Para trás", () => mudarOrdem(e, -1)), botao("Duplicar", duplicar), botao("Excluir", excluir));
  p.append(linha);
}

function montarCamadas() {
  const c = $("#camadas");
  c.replaceChildren();
  for (const e of [...doc.elementos].reverse()) {
    const b = botao(e.nome || e.id, () => selecionar(e.id));
    if (e.id === selecionado) b.className = "ativa";
    c.append(b);
  }
}

// --- comandos ---

function novoId(base) {
  let n = 1;
  while (doc.elementos.some((e) => e.id === `${base}-${n}`)) n++;
  return `${base}-${n}`;
}

function adicionar(e) {
  doc.elementos.push(e);
  selecionado = e.id;
  redesenhar();
  registrar();
}

function mudarOrdem(e, passo) {
  const i = doc.elementos.indexOf(e), j = i + passo;
  if (j < 0 || j >= doc.elementos.length) return;
  doc.elementos.splice(i, 1);
  doc.elementos.splice(j, 0, e);
  redesenhar();
  registrar();
}

function duplicar() {
  const e = atual();
  if (e) adicionar({ ...e, id: novoId(e.tipo), nome: `${e.nome || e.id} (cópia)`, x: e.x + 24, y: e.y + 24 });
}

function excluir() {
  const e = atual();
  if (!e) return;
  doc.elementos.splice(doc.elementos.indexOf(e), 1);
  selecionado = null;
  redesenhar();
  registrar();
}

let modoFoto = "nova";
function pedirFoto(modo) {
  modoFoto = modo;
  $("#arquivo-foto").value = "";
  $("#arquivo-foto").click();
}

$("#arquivo-foto").addEventListener("change", async (ev) => {
  const arquivo = ev.target.files[0];
  if (!arquivo) return;
  situacao("Enviando foto…");
  try {
    await salvamento;
    const foto = await pedir(`${urlPeca()}/foto`, { method: "POST", body: arquivo });
    const e = atual();
    if (modoFoto === "trocar" && e && e.tipo === "imagem") {
      e.arquivo = foto.arquivo;
      e.altura = Math.round(e.largura * foto.altura / foto.largura);
      redesenhar();
      registrar();
    } else {
      const largura = 600;
      adicionar({ id: novoId("foto"), nome: arquivo.name.slice(0, 40), tipo: "imagem", x: 240, y: 400, largura, altura: Math.round(largura * foto.altura / foto.largura), arquivo: foto.arquivo, pb: true, sepia: 0.14, contraste: 1.06 });
    }
  } catch (erro) {
    situacao(erro.message, true);
  }
});

$("#novo-texto").addEventListener("click", () => adicionar({ id: novoId("texto"), nome: "Texto novo", tipo: "texto", x: 96, y: 620, html: "Texto novo", fonte: "Inter", tamanho: 36, peso: 400, cor: AREIA, entrelinha: 1.34 }));
$("#nova-foto").addEventListener("click", () => pedirFoto("nova"));
$("#novo-fio").addEventListener("click", () => adicionar({ id: novoId("fio"), nome: "Fio", tipo: "retangulo", x: 96, y: 720, largura: 888, altura: 2, cor: OURO }));
$("#desfazer").addEventListener("click", () => andarHistorico(-1));
$("#refazer").addEventListener("click", () => andarHistorico(1));

$("#baixar").addEventListener("click", async () => {
  const b = $("#baixar");
  b.disabled = true;
  situacao("Gerando imagem…");
  try {
    if (temporizador) salvarJa();
    await salvamento;
    const { arquivo } = await pedir(`${urlPeca()}/exportar`, { method: "POST" });
    const a = document.createElement("a");
    a.href = `/api/saidas/${arquivo}`;
    a.download = arquivo;
    a.click();
    situacao("Salvo");
    avisar(`Imagem pronta: ${arquivo}. Veja na pasta Downloads.`);
  } catch (erro) {
    situacao(erro.message, true);
  } finally {
    b.disabled = false;
  }
});

$("#nova-versao").addEventListener("click", async () => {
  const sugestao = nomePeca.normalize("NFD").replace(/[^A-Za-z0-9_-]/g, "") + "-v2";
  const novo = prompt("Nome da nova versão. A peça atual continua como está.", sugestao);
  if (!novo) return;
  try {
    if (temporizador) salvarJa();
    await salvamento;
    await pedir(`${urlPeca()}/copia`, { method: "POST", body: JSON.stringify({ nome: novo }) });
    await listarPecas(novo);
    await abrirPeca(novo);
  } catch (erro) {
    avisar(erro.message);
  }
});

$("#voltar-original").addEventListener("click", async () => {
  if (!confirm("Voltar esta peça ao original? As alterações podem ser recuperadas com Desfazer enquanto o editor estiver aberto.")) return;
  try {
    clearTimeout(temporizador);
    temporizador = null;
    await salvamento;
    doc = await pedir(`${urlPeca()}/restaurar`, { method: "POST" });
    selecionado = null;
    redesenhar();
    registrar();
  } catch (erro) {
    avisar(erro.message);
  }
});

window.addEventListener("keydown", (ev) => {
  if (editando || ev.target.matches("input,select,textarea")) return;
  const ctrl = ev.ctrlKey || ev.metaKey, tecla = ev.key.toLowerCase();
  if (ctrl && tecla === "z") { ev.preventDefault(); andarHistorico(ev.shiftKey ? 1 : -1); return; }
  if (ctrl && tecla === "y") { ev.preventDefault(); andarHistorico(1); return; }
  const e = atual();
  if (!e) return;
  if (ctrl && tecla === "d") { ev.preventDefault(); duplicar(); return; }
  if (ev.key === "Delete" || ev.key === "Backspace") { ev.preventDefault(); excluir(); return; }
  const passo = ev.shiftKey ? 10 : 1;
  const setas = { ArrowLeft: [-passo, 0], ArrowRight: [passo, 0], ArrowUp: [0, -passo], ArrowDown: [0, passo] }[ev.key];
  if (setas) {
    ev.preventDefault();
    e.x = arred(e.x + setas[0]);
    e.y = arred(e.y + setas[1]);
    redesenharElemento(e);
    montarPainel();
    registrar();
  }
});

window.addEventListener("resize", () => doc && ajustarEscala());
window.addEventListener("beforeunload", () => {
  if (temporizador) fetch(urlPeca(), { method: "PUT", body: JSON.stringify(doc), keepalive: doc && JSON.stringify(doc).length < 60000 });
});

// --- abrir ---

async function listarPecas(escolhida) {
  const nomes = await pedir("/api/pecas");
  const s = $("#peca");
  s.replaceChildren(...nomes.map((n) => new Option(n, n, false, n === escolhida)));
  return nomes;
}

async function abrirPeca(nome) {
  if (temporizador) salvarJa();
  await salvamento;
  nomePeca = nome;
  doc = await pedir(urlPeca());
  historico = [JSON.stringify(doc)];
  posicao = 0;
  selecionado = null;
  $("#peca").value = nome;
  redesenhar();
  botoesHistorico();
  situacao("Salvo");
}

$("#peca").addEventListener("change", (ev) => abrirPeca(ev.target.value));

(async () => {
  try {
    const nomes = await listarPecas();
    if (nomes.length) await abrirPeca(nomes[0]);
    else situacao("Nenhuma peça no editor ainda.", true);
  } catch (erro) {
    situacao(erro.message, true);
  }
})();
