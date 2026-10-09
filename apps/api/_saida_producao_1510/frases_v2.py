"""Re-renderiza as frases no modelo fosco (09/10/2026): as 10 do lote e as 3 já agendadas."""
import asyncio, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent)); sys.path.insert(0, str(Path(__file__).resolve().parent))
from PIL import Image
from app.services.render_criativo import renderizar_frase_impacto
from conteudo import TEMAS
AQUI = Path(__file__).resolve().parent
IV = {"cores": {"fundo_escuro": "#231E1A", "dourado": "#C9A962", "areia": "#E8DED1"}}
FRASES = [(f"{t['chave']}-frase-v2.jpg", t["frase"]["html"]) for t in TEMAS] + [
    ("frase-pet-v2.jpg", "O pet também é da família. <em>E a lei agora reconhece isso no divórcio.</em>"),
    ("frase-abandono-v2.jpg", "Pagar pensão não é o mesmo que <em>estar presente.</em>"),
    ("frase-clt-v2.jpg", "Direito que você não conhece é <em>direito que você deixa de receber.</em>"),
]
async def main():
    for nome, html in FRASES:
        png = AQUI / "pecas" / nome.replace(".jpg", ".png")
        await renderizar_frase_impacto(html, IV, str(png))
        Image.open(png).convert("RGB").save(AQUI / "pecas" / nome, "JPEG", quality=92, optimize=True); png.unlink(); print("ok", nome)
asyncio.run(main())
