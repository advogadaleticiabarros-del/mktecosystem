"""Capas dos 4 artigos de novembro/2026 (renderizador oficial do blog: foto pura 1200×630)."""
import asyncio, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent)); sys.path.insert(0, str(Path(__file__).resolve().parent))
from app.services.render_artigo_blog import renderizar_capa_artigo
from artigos_nov import ARTIGOS
AQUI = Path(__file__).resolve().parent
IV = {"cores": {"fundo_escuro": "#231E1A", "dourado": "#C9A962", "areia": "#E8DED1"}}
async def main():
    for a in ARTIGOS:
        destino = AQUI / "pecas" / f"capa-{a['slug']}.png"
        await renderizar_capa_artigo(titulo=a["titulo"], categoria="", identidade_visual=IV, caminho_saida=str(destino),
                                     foto_path=str(AQUI / "_fotos_pexels" / f"{a['foto']}.jpg"))
        print("ok", destino.name)
asyncio.run(main())
