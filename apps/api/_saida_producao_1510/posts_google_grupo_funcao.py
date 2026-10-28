"""Capas do blog (1200x630) e posts do Perfil da Empresa (1200x900) do grupo "O que a empresa pode exigir" (27/10/2026)."""
import asyncio, base64, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent)); sys.path.insert(0, str(Path(__file__).resolve().parent))
from PIL import Image
from playwright.async_api import async_playwright
from artigos_grupo_funcao import ARTIGOS, B
from posts_google import HTML, uri

AQUI = Path(__file__).resolve().parent
def capa_blog(a):
    im = Image.open(AQUI / "_fotos_pexels" / a["foto"]).convert("RGB")
    W, H = im.size
    h = int(W * 630 / 1200)
    y = max(0, min(H - h, int(a["cy"] * H - h / 2)))
    im.crop((0, y, W, y + h)).resize((1200, 630), Image.LANCZOS).save(
        AQUI / "pecas" / f"capa-{a['slug']}.jpg", "JPEG", quality=85, optimize=True, progressive=True)


async def main():
    saida = []
    async with async_playwright() as p:
        nav = await p.chromium.launch(); pg = await nav.new_page(viewport={"width": 1200, "height": 900})
        for a in ARTIGOS:
            capa_blog(a)
            kicker = a["kicker"]
            await pg.set_content(HTML % {"foto": uri(AQUI / "_fotos_pexels" / a["foto"]), "pos": f"{int(a['cy'] * 100)}%",
                                         "kicker": kicker, "titulo": a["titulo"]}, wait_until="networkidle")
            await pg.evaluate("document.fonts.ready")
            png = await pg.screenshot(type="jpeg", quality=86)
            (AQUI / "pecas" / f"google-post-{a['slug']}.jpg").write_bytes(png)
            saida.append({"data": a["data"], "slug": a["slug"], "titulo": a["titulo"], "texto": a["post_google"],
                          "link": f"{B}{a['slug']}.html", "imagem": "data:image/jpeg;base64," + base64.b64encode(png).decode()})
            print("ok", a["slug"])
        await nav.close()
    (AQUI / "pecas" / "posts_google_grupo_funcao.json").write_text(json.dumps(saida, ensure_ascii=False), encoding="utf-8")

asyncio.run(main())
