"""Posts do Perfil da Empresa no Google (1 por artigo do blog), plano de SEO de 10/10/2026.

Gera as imagens 1200×900 (4:3, formato dos posts do Google) e `posts_google.json` para o banco do
artefato "Manual do Perfil no Google". Regras: sem telefone no texto (o Google rejeita), sem
"especialista", sem promessa de resultado; texto curto com o ponto principal no começo.

Uso (de apps/api): python _saida_producao_1510/posts_google.py
"""
import asyncio
import base64
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from PIL import Image  # noqa: E402
from playwright.async_api import async_playwright  # noqa: E402

AQUI = Path(__file__).resolve().parent
BLOG = "https://advogadaleticiabarros.com.br/blog/"

POSTS = [
    ("2026-10-11", "abandono-afetivo-indenizacao-lei-15240-2025", "capa-abandono-blog.png", "Abandono afetivo",
     "Abandono afetivo agora pode gerar indenização",
     "Abandono afetivo agora pode gerar indenização. A Lei 15.240/2025 reconheceu que a ausência de cuidado de um pai ou mãe é ato ilícito. No blog, explicamos o que muda e em que situações cabe indenização."),
    ("2026-10-12", "direitos-da-gestante-clt-guia-completo", "6991886.jpg", "Direitos da gestante",
     "Direitos da gestante CLT: o guia completo de 2026",
     "Grávida e com carteira assinada? Reunimos num só guia os direitos da gestante CLT em 2026: estabilidade, pré-natal, licença-maternidade, amamentação e salário-maternidade."),
    ("2026-10-15", "estabilidade-gestante-contrato-de-experiencia-e-temporario", "7990621.jpg", "Direitos da gestante",
     "Grávida no contrato de experiência tem estabilidade?",
     "Engravidou durante o contrato de experiência ou no trabalho temporário? Explicamos o que vale em 2026, incluindo a mudança do TST em março, e quais provas guardar."),
    ("2026-11-09", "13-salario-gestante-licenca-maternidade", "31627496.jpg", "Gestante e 13º",
     "A licença-maternidade não reduz o seu 13º",
     "Quem está de licença-maternidade recebe o 13º inteiro. Os meses de licença contam como trabalhados. No blog, explicamos quem paga e como conferir o contracheque."),
    ("2026-11-16", "voltei-da-licenca-maternidade-direitos-no-retorno", "original-amamentacao-trabalho.jpg", "Volta da licença",
     "Voltei da licença: meus direitos no retorno",
     "Voltou da licença-maternidade? Estabilidade, mesma função, pausas para amamentar e creche: o que a lei garante à mãe que volta ao trabalho."),
    ("2026-11-23", "alimentos-gravidicos-pensao-durante-a-gravidez", "original-alimentos-gravidicos.jpg", "Pensão na gravidez",
     "Grávida pode pedir pensão antes do bebê nascer",
     "A gestante pode pedir ao pai ajuda com as despesas da gravidez: são os alimentos gravídicos. Não precisa de DNA na gestação. No blog, explicamos o que cobrem e como reunir as provas."),
    ("2026-11-30", "salario-maternidade-quem-tem-direito-e-como-pedir", "28259754.jpg", "Salário-maternidade",
     "Salário-maternidade: quem tem direito e como pedir",
     "MEI, desempregada, doméstica ou adotante também podem ter direito ao salário-maternidade. No blog, explicamos quem recebe, quanto e como pedir pelo Meu INSS."),
]

HTML = """<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@600&family=Inter:wght@600;700&display=swap" rel="stylesheet">
<style>*{margin:0;box-sizing:border-box} body{width:1200px;height:900px;overflow:hidden;font-family:Inter,sans-serif;background:#1A1511}
.f{position:absolute;inset:0;background:url('%(foto)s') center %(pos)s/cover;filter:sepia(.15) saturate(.92) brightness(.9)}
.v{position:absolute;inset:0;background:linear-gradient(180deg,rgba(26,21,17,.25) 0%%,rgba(26,21,17,0) 35%%,rgba(26,21,17,.78) 70%%,rgba(26,21,17,.95) 100%%)}
.b{position:absolute;left:0;right:0;height:10px;background:linear-gradient(90deg,#8F7032,#E9D398,#C9A962,#E9D398,#8F7032)} .t{top:0} .r{bottom:0}
.c{position:absolute;left:70px;right:70px;bottom:70px}
.k{color:#E9D398;font-size:24px;font-weight:700;letter-spacing:5px;text-transform:uppercase}
.h{color:#FAF6F0;font-family:'EB Garamond',serif;font-weight:600;font-size:66px;line-height:1.05;margin-top:14px;text-wrap:balance}
.l{width:90px;height:2px;background:#C9A962;margin:26px 0 18px} .m{color:#E8DED1;font-size:22px;font-weight:600;letter-spacing:2px}
</style></head><body><div class="f"></div><div class="v"></div><div class="b t"></div><div class="b r"></div>
<div class="c"><div class="k">%(kicker)s</div><div class="h">%(titulo)s</div><div class="l"></div>
<div class="m">Leia no blog · Letícia Barros Advocacia · OAB/ES 39.948</div></div></body></html>"""


def uri(caminho: Path) -> str:
    im = Image.open(caminho).convert("RGB")
    im.thumbnail((1800, 1800))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=88)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


async def main() -> None:
    saida = []
    async with async_playwright() as p:
        nav = await p.chromium.launch()
        pg = await nav.new_page(viewport={"width": 1200, "height": 900})
        for data, slug, foto, kicker, titulo, texto in POSTS:
            arq = AQUI / "_fotos_pexels" / foto
            if not arq.exists():
                arq = AQUI / "pecas" / foto
            await pg.set_content(HTML % {"foto": uri(arq), "pos": "30%", "kicker": kicker, "titulo": titulo}, wait_until="networkidle")
            await pg.evaluate("document.fonts.ready")
            png = await pg.screenshot(type="jpeg", quality=86)
            destino = AQUI / "pecas" / f"google-post-{slug}.jpg"
            destino.write_bytes(png)
            saida.append({"data": data, "slug": slug, "titulo": titulo, "texto": texto, "link": f"{BLOG}{slug}.html",
                          "imagem": "data:image/jpeg;base64," + base64.b64encode(png).decode()})
            print("ok", destino.name, len(png) // 1024, "KB")
        await nav.close()
    (AQUI / "pecas" / "posts_google.json").write_text(json.dumps(saida, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    asyncio.run(main())
