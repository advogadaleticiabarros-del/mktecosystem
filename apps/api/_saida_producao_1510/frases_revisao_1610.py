"""Revisão das frases do feed (16/10/2026): menos "não", leitura simples. Aprovadas pela Letícia na página de revisão.
Renderiza as imagens novas (mesmo card dourado v2) em pecas/. A subida é feita por subir_frases_1610.py, dentro do container.
Uso (de apps/api): python _saida_producao_1510/frases_revisao_1610.py
"""
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from PIL import Image  # noqa: E402

from app.services.render_criativo import renderizar_frase_impacto  # noqa: E402

AQUI = Path(__file__).resolve().parent
IV = {"cores": {"fundo_escuro": "#231E1A", "dourado": "#C9A962", "areia": "#E8DED1"}}

# id da peça: (arquivo da imagem, frase com o destaque dourado em <em>)
APROVADAS = {
    "008e857d-28a0-4d61-8c3f-8688f4a0b2c0": ("cancer-inss-frase-v2.jpg", "Tratar a doença e manter o sustento: <em>a lei protege os dois.</em>"),
    "d10b0c8c-dc75-4376-a64e-4f8924351525": (None, "Mãe que adota também é mãe. <em>E tem a mesma licença.</em>"),
    "704234e9-fa10-4067-b1d3-18cd7ee3b2aa": (None, "O banco pode encerrar a conta. <em>Seu dinheiro continua sendo seu.</em>"),
    "57bfbf8f-ce65-4b0c-ac6b-1ceb08aa2e32": (None, "A pensão pertence à criança. <em>É direito dela.</em>"),
    "60464f4b-f21a-4d0e-8e9d-29f5d7de88a1": (None, "Voltou ao trabalho? <em>O tempo de amamentar continua garantido.</em>"),
    "e2ab00b0-49a9-41f8-831d-ad32ad2050c0": (None, "Trabalhar e cuidar do filho: <em>a lei ajuda a conciliar os dois.</em>"),
    "dccec0f0-4989-4b21-b7d6-0ed999ce97c8": (None, "Cada mês de trabalho <em>conta para a sua aposentadoria.</em>"),
    "3e4469a7-c793-4b55-b980-6d03e110c9a1": (None, "Mesmo desempregada, <em>a maternidade continua protegida.</em>"),
    "6262a7b6-8593-4bd3-9dbf-d08990709f10": (None, "Burnout é doença. <em>E tem proteção na lei.</em>"),
    "bfc6f9bd-e97a-4805-ae2b-4355a328aecd": (None, "Respeito no trabalho <em>é direito seu.</em>"),
    "2c01e626-5e07-4e48-bde8-5a4a4dcdd465": (None, "Na festa da firma, <em>o respeito continua valendo.</em>"),
    "a2a633bc-a53d-4cac-89df-1e16e88242bf": (None, "Entender o contracheque <em>protege o seu dinheiro.</em>"),
}


def arquivo(pid: str, imagens: dict) -> str:
    return APROVADAS[pid][0] or imagens[pid].split("/media/")[1].split("?")[0]


async def main():
    imagens = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    for pid, (_, html) in APROVADAS.items():
        nome = arquivo(pid, imagens)
        png = AQUI / "pecas" / nome.replace(".jpg", ".png")
        await renderizar_frase_impacto(html, IV, str(png))
        Image.open(png).convert("RGB").save(AQUI / "pecas" / nome, "JPEG", quality=92, optimize=True)
        png.unlink()
        print("ok", nome)


if __name__ == "__main__":
    asyncio.run(main())
