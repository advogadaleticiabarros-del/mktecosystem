"""Reel #12 — Direitos da gestante (a partir do vídeo do NotebookLM, 09/10/2026).

Corta os melhores trechos da narração (fatos conferidos: ADCT art. 10 II b; STF Tema 497;
CLT art. 392 §4º; Lei 11.770/2008), põe as ilustrações num cartão central com zoom
contínuo e desenha por cima, quadro a quadro (Playwright), cabeçalho da marca, títulos
animados por parte, legenda palavra a palavra, selos dos números, barra de progresso,
flash nos cortes e o fechamento com CTA impessoal.

Uso: py montar.py
"""
import asyncio
import base64
import json
import subprocess
from pathlib import Path

from playwright.async_api import async_playwright

AQUI = Path(__file__).resolve().parent
SRC = Path(r"C:\Users\prosy\Desktop\Direitos_da_Gestante_no_Brasil.mp4")
FF = Path(r"C:\Users\prosy\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin")
ASSETS = Path(r"C:\Users\prosy\mktecosystem\apps\api\app\assets")
FPS = 30
OUTRO = 3.2
VID = dict(x=40, y=640, w=1000, h=540)

# (início, fim) no vídeo original, agrupados por parte do roteiro.
PARTES = [
    {"kicker": "Direitos da gestante", "titulo": "Grávida? <em>E agora?</em>", "trechos": [(25.45, 29.95)]},
    {"kicker": "01 · Estabilidade", "titulo": "Ninguém pode te demitir <em>sem justa causa</em>", "trechos": [(59.40, 71.55)]},
    {"kicker": "02 · O detalhe", "titulo": "Vale mesmo se a empresa <em>não sabia</em>", "trechos": [(91.45, 101.05), (104.45, 106.15)]},
    {"kicker": "03 · Pré-natal", "titulo": "Consultas e exames <em>sem desconto</em>", "trechos": [(125.70, 133.70), (147.70, 154.00)]},
    {"kicker": "04 · Licença-maternidade", "titulo": "<em>120 dias</em>, ou 180 na Empresa Cidadã", "trechos": [(192.55, 196.55), (197.58, 205.70)]},
    {"kicker": "", "titulo": "Informação <em>é poder</em>.", "trechos": [(368.95, 370.45)]},
]
# Selos que "saltam" quando a narração fala o número (tempo no vídeo original).
SELOS = [(70.04, "5 meses após o parto"), (98.26, "Não sabia? Vale igual"), (130.02, "Mínimo de 6 consultas"),
         (152.86, "Sem desconto"), (193.74, "120 dias"), (204.32, "180 dias")]
CORRIGE = {"validez": "vale desde", "-natal": "pré-natal", "pré": ""}
DESTAQUES = {"grávida", "emprego", "demissão", "justa", "causa", "concepção", "cinco", "meses", "parto", "não", "soubesse",
             "empregador", "seis", "consultas", "exames", "descontado", "salário", "120", "180", "dias", "cidadã", "poder"}


def ff(*args: str) -> None:
    subprocess.run([str(FF / "ffmpeg.exe"), "-v", "error", "-y", *args], check=True)


def b64(p: Path) -> str:
    mime = "image/png" if p.suffix == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def cortar() -> tuple[list[dict], float]:
    """Gera um clipe por trecho (zoom contínuo, sem a marca do NotebookLM) e a linha do tempo."""
    pasta = AQUI / "clipes"
    pasta.mkdir(exist_ok=True)
    linha, t, lista = [], 0.0, []
    for ip, parte in enumerate(PARTES):
        inicio_parte = t
        for it, (a, b) in enumerate(parte["trechos"]):
            dur = round(b - a, 3)
            frames = int(round(dur * FPS))
            destino = pasta / f"p{ip}_{it}.mp4"
            z0 = 1.0 if it == 0 else 1.03
            ff("-ss", str(a), "-t", str(dur), "-i", str(SRC),
               "-vf", f"crop=1215:656:24:0,fps={FPS},scale=2000:-2,"
                      f"zoompan=z='{z0}+0.07*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={VID['w']}x{VID['h']}:fps={FPS},"
                      "eq=saturation=0.92",
               "-af", f"afade=t=in:d=0.04,afade=t=out:st={dur - 0.05}:d=0.05,aresample=48000",
               "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "192k", "-ac", "2", str(destino))
            lista.append(destino)
            linha.append({"parte": ip, "ini_src": a, "fim_src": b, "ini": t, "fim": t + dur})
            t += dur
        parte["ini"], parte["fim"] = inicio_parte, t
    (pasta / "lista.txt").write_text("".join(f"file '{p.as_posix()}'\n" for p in lista), encoding="utf-8")
    ff("-f", "concat", "-safe", "0", "-i", str(pasta / "lista.txt"), "-c", "copy", str(AQUI / "miolo.mp4"))
    return linha, t


def legendas(linha: list[dict]) -> list[dict]:
    """Palavras da transcrição levadas para o tempo do Reel, em blocos de até ~26 caracteres."""
    r = json.loads((AQUI / "transcricao.json").read_text(encoding="utf-8"))
    palavras = [w for s in r["segments"] for w in s["words"]]
    saida = []
    for tr in linha:
        bloco = []
        for w in palavras:
            if w["start"] >= tr["ini_src"] - 0.05 and w["start"] < tr["fim_src"] - 0.03 and w["end"] <= tr["fim_src"] + 0.15:
                txt = w["word"].strip()
                txt = CORRIGE.get(txt, txt)
                if not txt:
                    continue
                ini = tr["ini"] + max(0.0, w["start"] - tr["ini_src"])
                fim = tr["ini"] + min(tr["fim_src"], w["end"]) - tr["ini_src"]
                chave = txt.lower().strip(".,?!")
                p = {"t": txt, "a": round(ini, 3), "b": round(fim, 3), "d": chave in DESTAQUES}
                bloco.append(p)
        # quebra em linhas curtas
        atual, n = [], 0
        for p in bloco:
            if atual and (n + len(p["t"]) > 26 or atual[-1]["t"][-1] in ".?!"):
                saida.append(atual)
                atual, n = [], 0
            atual.append(p)
            n += len(p["t"]) + 1
        if atual:
            saida.append(atual)
    return [{"a": b[0]["a"], "b": b[-1]["b"] + 0.25, "w": b} for b in saida]


def selos(linha: list[dict]) -> list[dict]:
    out = []
    for t_src, texto in SELOS:
        for tr in linha:
            if tr["ini_src"] <= t_src <= tr["fim_src"]:
                out.append({"a": tr["ini"] + t_src - tr["ini_src"], "texto": texto})
    return out


HTML = r"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;0,700;1,600;1,700&family=Inter:wght@500;600;700;800;900&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; } html { font-variant-numeric: lining-nums; }
body { width:1080px; height:1920px; overflow:hidden; background:transparent; font-family:'Inter',sans-serif; }
#fundo { position:absolute; inset:0; background: radial-gradient(ellipse at 50% 38%, #3D332A 0%, #2A231E 55%, #1A1511 100%); }
#fundo .marca { position:absolute; width:1300px; left:50%; top:52%; transform:translate(-50%,-50%); opacity:.04; }
#fundo .grao { position:absolute; inset:0; opacity:.12; mix-blend-mode:overlay; background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='g'><feTurbulence type='fractalNoise' baseFrequency='1.3' numOctaves='2' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/></filter><rect width='100%25' height='100%25' filter='url(%23g)'/></svg>"); }
.faixa { position:absolute; left:0; right:0; height:14px; background:linear-gradient(90deg,#8E6E2E,#E9D398 30%,#C9A962 55%,#F4E6BC 75%,#9C7B3A); }
#cab { position:absolute; top:196px; left:60px; right:60px; display:flex; justify-content:space-between; font-size:24px; font-weight:700; letter-spacing:5px; text-transform:uppercase; color:#E8DED1; }
#cab .d { color:#C9A962; }
#barra { position:absolute; top:248px; left:60px; right:60px; height:6px; border-radius:3px; background:#E8DED126; overflow:hidden; }
#barra i { display:block; height:100%; background:linear-gradient(90deg,#B8943F,#E9D398); border-radius:3px; }
#topo { position:absolute; left:60px; right:60px; top:300px; height:310px; display:flex; flex-direction:column; justify-content:flex-end; align-items:center; text-align:center; }
#kicker { display:inline-block; font-size:24px; font-weight:800; letter-spacing:4px; text-transform:uppercase; color:#231E1A; background:#C9A962; padding:9px 18px; border-radius:6px; margin-bottom:22px; }
#titulo { font-family:'Cormorant Garamond',serif; font-weight:700; font-size:84px; line-height:1.0; color:#FAF6F0; text-wrap:balance; }
#titulo em { font-style:italic; color:#E2C77F; }
#moldura { position:absolute; left:34px; top:634px; width:1012px; height:552px; border-radius:30px; border:3px solid #C9A962; box-shadow:0 30px 80px rgba(0,0,0,.55), 0 0 0 10px rgba(201,169,98,.10); }
#flash { position:absolute; left:40px; top:640px; width:1000px; height:540px; border-radius:26px; background:#FFF6DC; opacity:0; }
#selo { position:absolute; right:40px; top:1120px; transform-origin:85% 50%; font-size:40px; font-weight:900; letter-spacing:1px; text-transform:uppercase; color:#231E1A;
  background:linear-gradient(180deg,#F4E6BC,#C9A962); padding:16px 28px; border-radius:16px; box-shadow:0 18px 40px rgba(0,0,0,.5); opacity:0; }
#leg { position:absolute; left:50px; right:50px; top:1250px; text-align:center; font-size:62px; font-weight:900; line-height:1.18; color:#FFFFFF;
  text-shadow:0 4px 0 #1A1511, 0 0 18px rgba(0,0,0,.55); }
#leg span { display:inline-block; margin:0 10px; transform-origin:50% 60%; }
#leg span.d { color:#E9D398; }
#leg span.on { transform:scale(1.07); color:#F4E6BC; }
#perfil { position:absolute; left:0; right:0; top:1440px; display:flex; justify-content:center; align-items:center; gap:14px; font-size:26px; font-weight:700; color:#E8DED1cc; }
#perfil img { width:46px; height:46px; border-radius:50%; border:2px solid #C9A962; object-fit:cover; }
#fim { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; opacity:0;
  background: radial-gradient(ellipse at 50% 42%, #3D332A 0%, #231E1A 60%, #1A1511 100%); }
#fim img.logo { width:230px; margin-bottom:40px; }
#fim .f1 { font-family:'Cormorant Garamond',serif; font-weight:700; font-size:88px; line-height:1.02; color:#FAF6F0; padding:0 80px; }
#fim .f1 em { font-style:italic; color:#E2C77F; }
#fim .f2 { margin-top:36px; font-size:36px; font-weight:600; color:#E8DED1; }
#fim .btn { margin-top:44px; font-size:34px; font-weight:800; color:#231E1A; background:#C9A962; padding:20px 40px; border-radius:999px; }
#fim .oab { margin-top:52px; font-size:26px; font-weight:700; letter-spacing:5px; text-transform:uppercase; color:#C9A962; }
</style></head><body>
<div id="fundo"><img class="marca" src="__LOGO__"><div class="grao"></div><div class="faixa" style="top:0"></div><div class="faixa" style="bottom:0"></div></div>
<div id="cab"><span>Letícia Barros · Advocacia</span><span class="d">Trabalhista</span></div>
<div id="barra"><i></i></div>
<div id="topo"><div id="kicker"></div><div id="titulo"></div></div>
<div id="moldura"></div><div id="flash"></div><div id="selo"></div>
<div id="leg"></div>
<div id="perfil"><img src="__PERFIL__"><span>@adv.leticiabarros2</span></div>
<div id="fim"><img class="logo" src="__LOGO__">
  <div class="f1">Salve e mande para <em>uma gestante</em>.</div>
  <div class="f2">Cada caso tem detalhes.</div>
  <div class="btn">Procure uma advogada de confiança</div>
  <div class="oab">Letícia Barros · OAB/ES 39.948</div></div>
<script>
const D = __DADOS__;
const ease = x => 1 - Math.pow(1 - Math.min(Math.max(x,0),1), 3);
const pop = x => { x = Math.min(Math.max(x,0),1); const c = 1.70158; return 1 + (c+1)*Math.pow(x-1,3) + c*Math.pow(x-1,2); };
let parteAtual = -1, blocoAtual = -1;
window.render = (t, soFundo) => {
  document.getElementById('fundo').style.display = soFundo ? 'block' : 'none';
  for (const id of ['cab','barra','topo','moldura','flash','selo','leg','perfil','fim'])
    document.getElementById(id).style.visibility = soFundo ? 'hidden' : 'visible';
  if (soFundo) return;
  document.querySelector('#barra i').style.width = (100 * Math.min(t / D.total, 1)) + '%';
  // parte (título animado)
  const ip = D.partes.findIndex(p => t >= p.ini && t < p.fim);
  const p = D.partes[ip < 0 ? D.partes.length - 1 : ip];
  if (ip !== parteAtual && ip >= 0) {
    parteAtual = ip;
    document.getElementById('kicker').textContent = p.kicker;
    document.getElementById('kicker').style.display = p.kicker ? 'inline-block' : 'none';
    document.getElementById('titulo').innerHTML = p.titulo;
  }
  const k = ip === 0 ? 1 : ease((t - p.ini) / 0.35);
  const topo = document.getElementById('topo');
  topo.style.opacity = k; topo.style.transform = `translateY(${(1 - k) * 40}px)`;
  // flash nos cortes
  const corte = D.cortes.reduce((m, c) => (t >= c && t - c < m ? t - c : m), 9);
  document.getElementById('flash').style.opacity = corte < 0.14 ? 0.35 * (1 - corte / 0.14) : 0;
  // selo
  const s = D.selos.filter(s => t >= s.a && t < s.a + 1.8).pop();
  const selo = document.getElementById('selo');
  if (s) { const x = (t - s.a); selo.textContent = s.texto; selo.style.opacity = Math.min(1, x / 0.08) * (x > 1.55 ? (1.8 - x) / 0.25 : 1);
           selo.style.transform = `rotate(-4deg) scale(${0.6 + 0.4 * pop(x / 0.32)})`; } else selo.style.opacity = 0;
  // legenda palavra a palavra
  const ib = D.leg.findIndex(b => t >= b.a - 0.05 && t < b.b);
  const leg = document.getElementById('leg');
  if (ib !== blocoAtual) { blocoAtual = ib; leg.innerHTML = ib < 0 ? '' : D.leg[ib].w.map(w => `<span class="${w.d ? 'd' : ''}">${w.t}</span>`).join(' '); }
  if (ib >= 0) D.leg[ib].w.forEach((w, i) => leg.children[i].classList.toggle('on', t >= w.a && t < w.b + 0.05));
  // fechamento
  const f = (t - D.fimFala) / 0.4;
  document.getElementById('fim').style.opacity = ease(f);
};
</script></body></html>"""


async def desenhar(dados: dict, total: float) -> None:
    pasta = AQUI / "overlay"
    pasta.mkdir(exist_ok=True)
    for velho in pasta.glob("*.png"):
        velho.unlink()
    html = (HTML.replace("__DADOS__", json.dumps(dados, ensure_ascii=False))
            .replace("__LOGO__", b64(ASSETS / "logo-leticia.png")).replace("__PERFIL__", b64(ASSETS / "perfil-leticia.jpg")))
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1920})
        await page.set_content(html, wait_until="networkidle")
        await page.evaluate("document.fonts.ready")
        await page.evaluate("render(0, true)")
        await page.screenshot(path=str(AQUI / "fundo.png"))
        n = int(round(total * FPS))
        for i in range(n):
            await page.evaluate(f"render({i / FPS:.4f}, false)")
            await page.screenshot(path=str(pasta / f"{i:05d}.png"), omit_background=True)
            if i % 300 == 0:
                print("overlay", i, "/", n, flush=True)
        await browser.close()


def compor(total: float, fala: float) -> Path:
    mascara = AQUI / "mascara.png"
    from PIL import Image, ImageDraw
    m = Image.new("L", (VID["w"], VID["h"]), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, VID["w"] - 1, VID["h"] - 1], radius=26, fill=255)
    m.save(mascara)
    saida = AQUI.parent / "reel.mp4"
    ff("-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i", str(AQUI / "fundo.png"),
       "-i", str(AQUI / "miolo.mp4"),
       "-loop", "1", "-i", str(mascara),
       "-framerate", str(FPS), "-i", str(AQUI / "overlay" / "%05d.png"),
       "-filter_complex",
       f"[1:v]tpad=stop_mode=clone:stop_duration={OUTRO}[v];[2:v]format=gray[m];[v][m]alphamerge[vr];"
       f"[0:v][vr]overlay={VID['x']}:{VID['y']}:shortest=0:eof_action=pass[b];[b][3:v]overlay=0:0:eof_action=pass,format=yuv420p[out];"
       f"[1:a]apad=pad_dur={OUTRO},highpass=f=70,loudnorm=I=-14:TP=-1.5:LRA=11[a]",
       "-map", "[out]", "-map", "[a]", "-t", f"{total:.3f}", "-r", str(FPS),
       "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-profile:v", "high", "-movflags", "+faststart",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(saida))
    return saida


async def main() -> None:
    linha, fala = cortar()
    total = round(fala + OUTRO, 3)
    partes = [{"kicker": p["kicker"], "titulo": p["titulo"], "ini": p["ini"], "fim": p["fim"]} for p in PARTES]
    partes[-1]["fim"] = total + 1
    dados = {"total": total, "fimFala": fala - 0.1, "partes": partes, "leg": legendas(linha), "selos": selos(linha),
             "cortes": [tr["ini"] for tr in linha[1:]]}
    (AQUI / "linha_do_tempo.json").write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")
    print("fala", round(fala, 2), "total", total)
    await desenhar(dados, total)
    print("ok", compor(total, fala))


if __name__ == "__main__":
    asyncio.run(main())
