// =========================================================== camada procedural (v2)
// Tudo é função do tempo t (determinístico): o quadro N sai igual em qualquer ordem de render.
const fx = document.getElementById('fx'), g = fx.getContext('2d');
function hash3(i, j, k) { let h = Math.imul(i | 0, 374761393) ^ Math.imul(j | 0, 668265263) ^ Math.imul(k | 0, 1440662683);
  h = Math.imul(h ^ (h >>> 13), 1274126177); return ((h ^ (h >>> 16)) >>> 0) / 4294967296; }
const rnd = (i, s = 0) => hash3(i, s, 977);
function vnoise(x, y, z) {
  const xi = Math.floor(x), yi = Math.floor(y), zi = Math.floor(z), xf = x - xi, yf = y - yi, zf = z - zi;
  const u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf), w = zf * zf * (3 - 2 * zf);
  const c = (a, b, d) => hash3(xi + a, yi + b, zi + d);
  const x00 = lerp(c(0,0,0), c(1,0,0), u), x10 = lerp(c(0,1,0), c(1,1,0), u), x01 = lerp(c(0,0,1), c(1,0,1), u), x11 = lerp(c(0,1,1), c(1,1,1), u);
  return lerp(lerp(x00, x10, v), lerp(x01, x11, v), w);
}
const fbm = (x, y, z) => (vnoise(x, y, z) * .55 + vnoise(x * 2.1, y * 2.1, z * 1.7) * .3 + vnoise(x * 4.3, y * 4.3, z * 2.9) * .15);
// energia da voz (0..1), um valor por quadro, calculada no Python a partir da narração
function energia(t) { const e = C.energia || []; if (!e.length) return 0; return e[clamp(Math.floor(t * 30), 0, e.length - 1)]; }
const OURO = '233,211,152';

function poeira(t, E) { // pó dourado em deriva, reage à voz
  const N = C.poeira ?? 220;
  for (let i = 0; i < N; i++) {
    const z = .25 + rnd(i, 1) * .75, ph = rnd(i, 2) * 6.283;
    const y = (((rnd(i, 3) * 1920 - t * (14 + 46 * z)) % 1920) + 1920) % 1920;
    const x = rnd(i, 4) * 1080 + Math.sin(t * .33 * (.6 + z) + ph) * 60 * z + (vnoise(i * .37, t * .25, 5) - .5) * 90 * z;
    const tw = .65 + .35 * Math.sin(t * (1.5 + 3 * rnd(i, 6)) + ph);
    const a = (.10 + .42 * z) * tw * (.55 + .95 * E), r = (.8 + 2.4 * z) * (1 + .7 * E);
    g.fillStyle = `rgba(${OURO},${a})`; g.beginPath(); g.arc(x, y, r, 0, 6.283); g.fill();
    if (z > .82) { g.fillStyle = `rgba(${OURO},${a * .16})`; g.beginPath(); g.arc(x, y, r * 4.5, 0, 6.283); g.fill(); }
  }
}

function explosoes(t) { // estouro de partículas + onda de choque nos impactos (carimbo, selo, pó formado)
  (C.bursts || []).forEach((b, ib) => {
    const dt = t - b.t; if (dt < 0 || dt > 1.5) return;
    const n = b.n ?? 70, sh = clamp(dt / .55);
    g.strokeStyle = `rgba(${OURO},${.55 * (1 - sh)})`; g.lineWidth = 6 * (1 - sh) + 1;
    g.beginPath(); g.arc(b.x, b.y, 30 + (b.raio ?? 420) * eOut(sh), 0, 6.283); g.stroke();
    for (let j = 0; j < n; j++) {
      const ang = rnd(j, ib * 31 + 7) * 6.283, v = 260 + 900 * Math.pow(rnd(j, ib * 31 + 8), 1.6), k = 3.4;
      const d = v * (1 - Math.exp(-k * dt)) / k, x = b.x + Math.cos(ang) * d, y = b.y + Math.sin(ang) * d + 140 * dt * dt;
      const a = Math.pow(1 - dt / 1.5, 1.6) * (.5 + .5 * rnd(j, ib + 99)), r = 1.4 + 3.2 * rnd(j, ib + 5);
      g.fillStyle = `rgba(${OURO},${a})`; g.beginPath(); g.arc(x, y, r, 0, 6.283); g.fill();
    }
  });
}

function soco(t) { // punch-in: micro-zoom elástico na palavra-chave (quebra de padrão)
  let s = 0;
  for (const p of (C.punches || [])) { const dt = t - p; if (dt >= 0 && dt < 1.2) s += .05 * Math.exp(-dt * 4.2) * (1 - Math.exp(-dt * 28)); }
  return 1 + s;
}

// pó de ouro que forma palavra, número ou imagem: pontos amostrados do desenho final
function pontosDe(d) {
  const oc = document.createElement('canvas'), W = 1080, H = d.img ? 1080 : Math.ceil(d.size * 1.5);
  oc.width = W; oc.height = H; const o = oc.getContext('2d');
  let w = 0, h = 0;
  if (d.img) { const im = d._im; const sc = d.size / Math.max(im.width, im.height); w = im.width * sc; h = im.height * sc; o.drawImage(im, 0, 0, w, h); }
  else { o.font = `${d.peso ?? 700} ${d.size}px 'EB Garamond'`; o.textBaseline = 'top'; w = o.measureText(d.texto).width; h = d.size * 1.15;
    o.fillStyle = '#fff'; o.fillText(d.texto, 0, d.size * .05); }
  const px = o.getImageData(0, 0, W, H).data, passo = d.passo ?? Math.max(4, Math.round(d.size / 34)), pts = [];
  for (let y = 0; y < H; y += passo) for (let x = 0; x < W; x += passo) if (px[(y * W + x) * 4 + 3] > 128) pts.push([x - w / 2, y - h / 2]);
  d._pts = pts; d._w = w; d._h = h;
}
function desenharPo(d, t, opCena) {
  const a0 = d.at, dur = d.durPo ?? 1.15, n = d._pts.length;
  if (t < a0) return;
  const sai = d.ate != null ? clamp((t - d.ate) / .5) : 0;
  for (let i = 0; i < n; i++) {
    const [tx, ty] = d._pts[i], atraso = rnd(i, 41) * .38;
    const k = eInOut((t - a0 - atraso) / dur);
    const ang = rnd(i, 42) * 6.283, raio = 500 + 700 * rnd(i, 43);
    const sx = d.x + Math.cos(ang) * raio, sy = d.y + Math.sin(ang) * raio * 1.2;
    const gira = Math.sin(k * Math.PI) * 140 * (rnd(i, 44) - .5);
    let x = lerp(sx, d.x + tx, k) + gira, y = lerp(sy, d.y + ty, k) - gira * .6;
    if (sai > 0) { y -= eOut(sai) * (120 + 260 * rnd(i, 45)); x += (rnd(i, 46) - .5) * 160 * sai; }
    const brilho = .55 + .45 * Math.sin(t * 6 + i * .7);
    const a = clamp(k * 1.6) * (1 - sai) * opCena * (k >= 1 ? .3 + .35 * brilho : .9);
    g.fillStyle = `rgba(${OURO},${a})`; g.fillRect(x - 1.6, y - 1.6, 3.2, 3.2);
  }
  // desenho nítido por cima quando o pó assenta (legibilidade)
  const nit = clamp((t - a0 - dur - .1) / .45) * (1 - sai) * opCena;
  if (nit > 0) {
    g.save(); g.globalAlpha = nit;
    if (d.img) g.drawImage(d._im, d.x - d._w / 2, d.y - d._h / 2, d._w, d._h);
    else {
      g.font = `${d.peso ?? 700} ${d.size}px 'EB Garamond'`; g.textBaseline = 'top';
      const gr = g.createLinearGradient(d.x - d._w / 2, 0, d.x + d._w / 2, 0), sh = ((t * .45) % 1.6) - .3;
      gr.addColorStop(0, '#B8943F'); gr.addColorStop(clamp(sh - .12, 0, 1), '#E2C77F'); gr.addColorStop(clamp(sh, 0, 1), '#FFF4D2');
      gr.addColorStop(clamp(sh + .12, 0, 1), '#E2C77F'); gr.addColorStop(1, '#B8943F');
      g.shadowColor = 'rgba(0,0,0,.55)'; g.shadowBlur = 40; g.shadowOffsetY = 10; g.fillStyle = gr;
      g.fillText(d.texto, d.x - d._w / 2, d.y - d._h / 2 + d.size * .05);
    }
    g.restore();
  }
}

// máscara de tinta dourada (ruído que escorre) para a transição 'tinta'
const mc = document.createElement('canvas'); mc.width = 108; mc.height = 192; const mg = mc.getContext('2d'); const mdata = mg.createImageData(108, 192);
async function tinta(c, k) {
  const seed = c.a * 13.7, thr = lerp(-.15, 1.15, eInOut(k));
  for (let y = 0; y < 192; y++) for (let x = 0; x < 108; x++) {
    const n = fbm(x * .045 + seed, y * .045, seed) * .7 + (y / 192) * .3;
    const v = clamp((thr - n) / .05);
    const o = (y * 108 + x) * 4; mdata.data[o] = mdata.data[o + 1] = mdata.data[o + 2] = 255; mdata.data[o + 3] = v * 255;
    if (v > .02 && v < .98) { // borda incandescente
      const gx = x * 10 + 5, gy = y * 10 + 5, a = (1 - Math.abs(v - .5) * 2) * .85;
      g.fillStyle = `rgba(255,236,190,${a})`; g.fillRect(gx - 4, gy - 4, 8, 8);
      g.fillStyle = `rgba(${OURO},${a * .22})`; g.beginPath(); g.arc(gx, gy, 18, 0, 6.283); g.fill();
    }
  }
  mg.putImageData(mdata, 0, 0);
  const url = mc.toDataURL(); const im = new Image(); im.src = url; await im.decode().catch(() => {});
  c._div.style.webkitMaskImage = c._div.style.maskImage = `url(${url})`;
  c._div.style.webkitMaskSize = c._div.style.maskSize = '100% 100%';
}
function luz(k) { // clarão dourado que varre a tela na diagonal
  const x = lerp(-500, 1580, eInOut(k)), gr = g.createLinearGradient(x - 420, 0, x + 420, 400);
  gr.addColorStop(0, 'rgba(255,240,200,0)'); gr.addColorStop(.5, `rgba(255,240,200,${.75 * Math.sin(k * Math.PI)})`); gr.addColorStop(1, 'rgba(255,240,200,0)');
  g.fillStyle = gr; g.fillRect(0, 0, 1080, 1920);
}

// verificador da área limpa do Reels: lista o que invade topo (270), base (672), laterais (65)
// Mede as letras/cartões (não a caixa do contêiner) e só depois que a cena e o elemento assentaram.
function caixa(n, d) {
  if (d.tipo === 'texto') {
    let L = 1e9, T = 1e9, R = -1e9, B = -1e9;
    n.querySelectorAll('.lin > span').forEach(sp => { const r = sp.getBoundingClientRect(); L = Math.min(L, r.left); T = Math.min(T, r.top); R = Math.max(R, r.right); B = Math.max(B, r.bottom); });
    return { left: L, top: T, right: R, bottom: B, width: R - L };
  }
  const f = n.firstElementChild;
  if (f && (f.classList.contains('cartao') || f.classList.contains('papel') || ['IMG', 'svg', 'DIV'].includes(f.tagName))) return f.getBoundingClientRect();
  const r = document.createRange(); r.selectNodeContents(n); return r.getBoundingClientRect();
}
function checar(t) {
  const prob = [], palco = document.getElementById('palco'), tfPalco = palco.style.transform;
  palco.style.transform = ''; // o soco é momentâneo: confere o enquadramento base
  C.cenas.forEach((c, ic) => {
    if (c._div.style.visibility !== 'visible') return;
    const prox = C.cenas[ic + 1];
    if (t < c.a + (c.tdur ?? T) + .05 || (prox && t >= prox.a)) return;
    c._els.forEach(([n, d]) => {
      if (d.livre || t < (d.at ?? 0) + (d.dur ?? .55) + .5 || (d.ate != null && t > d.ate)) return;
      if (d.tipo === 'po') { if (!d._pts) return;
        const L = d.x - d._w / 2, R = d.x + d._w / 2, Tp = d.y - d._h / 2, B = d.y + d._h / 2;
        if (Tp < 268 || B > 1250 || L < 63 || R > 1017) prob.push({ t, cena: ic, el: d.texto || 'imagem', box: [L, Tp, R, B].map(Math.round) });
        return; }
      if (parseFloat(n.style.opacity || 1) < .5) return;
      const r = caixa(n, d); if (!r.width) return;
      const fora = [];
      if (r.top < 268) fora.push('topo'); if (r.bottom > 1250) fora.push('base');
      if (r.left < 63) fora.push('esquerda'); if (r.right > 1017) fora.push('direita');
      if (fora.length) prob.push({ t, cena: ic, el: (n.textContent || d.tipo || '').trim().slice(0, 40), fora, box: [r.left, r.top, r.right, r.bottom].map(Math.round) });
    });
  });
  palco.style.transform = tfPalco;
  return prob;
}
