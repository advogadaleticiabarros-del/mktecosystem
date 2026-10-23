"""Gera lp/checklist-2027-empresas.pdf (material da LP de empresas) a partir de checklist-2027-empresas-pdf.html.

Uso: py lp/_gerar_pdf_checklist_empresas.py  (precisa do playwright com chromium)
"""
import asyncio
import base64
import sys
from pathlib import Path

from playwright.async_api import async_playwright

DIR = Path(__file__).parent
TEMPLATE = DIR / "checklist-2027-empresas-pdf.html"
FINAL = DIR / "_checklist-2027-empresas-final.html"
PDF = DIR / "checklist-2027-empresas.pdf"
LOGO = DIR.parent / "logo" / "logo-sem-fundo.png"


async def main(previa: bool) -> None:
    logo = "data:image/png;base64," + base64.b64encode(LOGO.read_bytes()).decode()
    FINAL.write_text(TEMPLATE.read_text(encoding="utf-8").replace("{{LOGO}}", logo), encoding="utf-8")
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 794, "height": 1123})
        await page.goto(FINAL.as_uri())
        await page.wait_for_timeout(1200)
        await page.pdf(path=str(PDF), format="A4", print_background=True,
                       margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        if previa:  # imagens das páginas para conferir antes de publicar
            for i in range(5):
                await page.screenshot(path=str(DIR / f"_previa-checklist-{i + 1}.png"), full_page=True,
                                      clip={"x": 0, "y": i * 1123, "width": 794, "height": 1123})
        await browser.close()
    print("PDF gerado em", PDF)


if __name__ == "__main__":
    asyncio.run(main("--previa" in sys.argv))
