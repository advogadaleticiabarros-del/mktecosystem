"""Frase v2 e estático "5 provas" da campanha de assédio eleitoral (27/10/2026).

Fatos em ../BRIEFING.md. Frase no gerador oficial (`renderizar_frase_impacto`); o estático usa o mesmo acabamento
fosco da frase (moldura, grão, vinheta, logo como marca d'água, assinatura) com um checklist de 5 itens.
Uso (de apps/api): py ../../producao/campanhas/2026-10-assedio-eleitoral/frase-estatico/gerar.py
Saída: ./pecas/*.jpg
"""
import asyncio
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
API = AQUI.parents[3] / "apps" / "api"
sys.path.insert(0, str(API))

from PIL import Image  # noqa: E402

from app.services.render_criativo import _fotografar, _logo_data_uri, renderizar_frase_impacto  # noqa: E402

IV = {"cores": {"fundo_escuro": "#231E1A", "dourado": "#C9A962", "areia": "#E8DED1"}}
SAIDA = AQUI / "pecas"

FRASE = "Seu voto é secreto.<br><em>Seu emprego não pode depender dele.</em>"

PROVAS = [
    ("Prints completos", "com data, hora, quem mandou e o nome do grupo."),
    ("A conversa exportada", "WhatsApp › Mais › Exportar conversa, com mídia."),
    ("Os áudios baixados", "salve cada arquivo, não só o print da tela."),
    ("A carta de dispensa", "e o termo de rescisão, com a data da demissão."),
    ("Os nomes das testemunhas", "quem viu ou ouviu, com contato e o que presenciou."),
]

ESTATICO = """<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600;1,700&family=Inter:wght@500;600;700&display=swap" rel="stylesheet">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; font-variant-numeric: lining-nums; font-feature-settings: "lnum" 1; }
  .card { width: 1080px; height: 1350px; position: relative; overflow: hidden; font-family: 'Inter', sans-serif;
    color: #E8DED1; background: radial-gradient(ellipse at 60% 22%, #3B3129 0%, #2A231E 55%, #1F1915 100%); }
  .card::before { content: ''; position: absolute; inset: 36px; border: 1.5px solid #C9A9628c; border-radius: 18px; z-index: 5; }
  .vinheta { position: absolute; inset: 0; z-index: 1; background: radial-gradient(ellipse at 50% 50%, transparent 52%, rgba(0,0,0,.32) 100%); }
  .grao { position: absolute; inset: 0; z-index: 6; opacity: .14; mix-blend-mode: overlay;
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='g'><feTurbulence type='fractalNoise' baseFrequency='1.4' numOctaves='2' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/></filter><rect width='100%25' height='100%25' filter='url(%23g)'/></svg>"); }
  .marca { position: absolute; z-index: 1; width: 1050px; right: -380px; bottom: -300px; opacity: .06; }
  .topo { position: absolute; top: 96px; left: 112px; right: 112px; z-index: 4; display: flex; justify-content: space-between;
    font-size: 22px; font-weight: 600; letter-spacing: 4px; text-transform: uppercase; color: #C9A962; }
  .topo span:last-child { text-align: right; }
  .miolo { position: absolute; top: 206px; left: 112px; right: 112px; z-index: 4; text-align: center; }
  .kicker { font-size: 24px; font-weight: 700; letter-spacing: 5px; text-transform: uppercase; color: #C9A962; }
  h1 { font-family: 'EB Garamond', serif; font-weight: 700; font-size: 70px; line-height: 1.04; color: #FAF6F0; margin-top: 16px; white-space: nowrap; }
  h1 em { font-style: italic; color: #C9A962; }
  .lista { margin-top: 36px; background: rgba(250,246,240,.055); border: 1.5px solid #C9A96259; border-radius: 20px;
    padding: 16px 40px; text-align: left; }
  .item { display: flex; gap: 28px; align-items: flex-start; padding: 18px 0; border-bottom: 1px solid #C9A96233; }
  .item:last-child { border-bottom: 0; }
  .n { flex: 0 0 56px; height: 56px; border-radius: 50%; border: 1.5px solid #C9A962; color: #C9A962;
    font-family: 'EB Garamond', serif; font-weight: 700; font-size: 32px; display: flex; align-items: center; justify-content: center; }
  .t b { display: block; font-family: 'EB Garamond', serif; font-weight: 700; font-size: 38px; color: #FAF6F0; line-height: 1.1; }
  .t span { display: block; font-size: 26px; line-height: 1.35; color: #E8DED1; margin-top: 4px; }
  .pilula { display: inline-block; margin-top: 32px; background: #C9A962; color: #231E1A; border-radius: 30px;
    padding: 16px 36px; font-size: 25px; font-weight: 700; letter-spacing: 1px; }
  .assinatura { position: absolute; left: 0; right: 0; bottom: 84px; z-index: 4; display: flex; flex-direction: column; align-items: center; gap: 10px; }
  .linha-ass { display: flex; align-items: center; gap: 22px; }
  .fio { width: 110px; height: 1.5px; background: linear-gradient(90deg, transparent, #C9A962); }
  .fio.dir { background: linear-gradient(90deg, #C9A962, transparent); }
  .assinatura img { width: 50px; height: 50px; object-fit: contain; }
  .nome { font-size: 23px; font-weight: 600; letter-spacing: 6px; text-transform: uppercase; }
  .oab { font-size: 22px; font-weight: 600; letter-spacing: 4px; color: #C9A962; }
</style></head><body>
<div class="card">
  <img class="marca" src="{logo}" alt=""><div class="vinheta"></div>
  <div class="topo"><span>Letícia Barros<br>Advocacia</span><span>Direito do<br>Trabalho</span></div>
  <div class="miolo">
    <div class="kicker">Demitido por causa do voto?</div>
    <h1>5 provas para guardar <em>agora</em></h1>
    <div class="lista">{itens}</div>
    <div class="pilula">Passo a passo completo no link da bio</div>
  </div>
  <div class="assinatura">
    <div class="linha-ass"><div class="fio"></div><img src="{logo}" alt="Letícia Barros"><span class="nome">Letícia Barros · Advocacia</span><div class="fio dir"></div></div>
    <span class="oab">OAB/ES 39.948</span>
  </div>
  <div class="grao"></div>
</div></body></html>"""


def html_estatico() -> str:
    itens = "".join(f'<div class="item"><div class="n">{i}</div><div class="t"><b>{a}</b><span>{b}</span></div></div>'
                    for i, (a, b) in enumerate(PROVAS, 1))
    return ESTATICO.replace("{logo}", _logo_data_uri()).replace("{itens}", itens)


def jpg(png: Path) -> Path:
    destino = png.with_suffix(".jpg")
    Image.open(png).convert("RGB").save(destino, "JPEG", quality=92, optimize=True)
    png.unlink()
    return destino


async def main():
    SAIDA.mkdir(exist_ok=True)
    frase = SAIDA / "assedio-eleitoral-frase-v2.png"
    await renderizar_frase_impacto(FRASE, IV, str(frase))
    print("ok", jpg(frase))
    est = SAIDA / "assedio-eleitoral-estatico-provas-v1.png"
    await _fotografar(html_estatico(), str(est))
    print("ok", jpg(est))


if __name__ == "__main__":
    asyncio.run(main())
