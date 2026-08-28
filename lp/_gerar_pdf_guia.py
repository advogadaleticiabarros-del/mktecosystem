import asyncio
import base64
from pathlib import Path

from playwright.async_api import async_playwright

DIR = Path(__file__).parent
HTML_TEMPLATE = DIR / "guia-gestante-clt-pdf.html"
HTML_FINAL = DIR / "_guia-gestante-clt-pdf-final.html"
PDF_PATH = DIR / "guia-direitos-gestante-trabalhadora.pdf"

LOGO_PATH = Path(r"C:\tmp\mktecosystem\logo\logo-sem-fundo.png")
FOTO_CAPA_PATH = Path(r"C:\Users\prosy\Desktop\LETÍCIA\banco de imagens\pregnant-2640994_960_720.webp")


def data_uri(path: Path, mime: str) -> str:
    dados = base64.b64encode(path.read_bytes()).decode()
    return f"data:{mime};base64,{dados}"


async def main():
    html = HTML_TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("{{LOGO}}", data_uri(LOGO_PATH, "image/png"))
    html = html.replace("{{FOTO_CAPA}}", data_uri(FOTO_CAPA_PATH, "image/webp"))
    HTML_FINAL.write_text(html, encoding="utf-8")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f"file:///{HTML_FINAL.as_posix()}")
        await page.wait_for_timeout(700)
        await page.pdf(
            path=str(PDF_PATH),
            format="A4",
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
        )
        await browser.close()
    print(f"PDF gerado em {PDF_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
