"""Cria no editor a peça grito-D-editorial, com os mesmos valores de producao/estilos/palavra-de-ouro/gerar.py.
Não mexe na peça do estilo. Uso: python importar_grito_d.py (recusa se a peça já existir)."""
import io
from pathlib import Path

from PIL import Image

from acervo import Acervo

AQUI = Path(__file__).resolve().parent
FOTO = AQUI.parent / "estilos" / "palavra-de-ouro" / "fotos" / "10675499.jpg"
OURO, AREIA = "#C9A962", "#EFE6D9"
NOME = "grito-D-editorial"


def foto_tratada():
    """Comprime só as altas luzes da pele (teto=205 de gerar.foto_grito): o preto continua preto."""
    f = Image.open(FOTO).convert("L").point(lambda v: v if v < 110 else 110 + (v - 110) * 95 / 145).convert("RGB")
    b = io.BytesIO()
    f.save(b, "JPEG", quality=95)
    return b.getvalue()


def documento(foto):
    radial = "radial-gradient(ellipse 54% 50% at 58% 54%,#000 58%,transparent 100%)"
    texto = lambda id, x, y, html, fonte, tamanho, cor=AREIA, **e: {"id": id, "nome": e.pop("nome", id), "tipo": "texto", "x": x, "y": y, "html": html, "fonte": fonte, "tamanho": tamanho, "cor": cor, **e}
    return {"largura": 1080, "altura": 1440, "fundo": "#231E1A", "elementos": [
        {"id": "faixa-topo", "nome": "Faixa do topo", "tipo": "retangulo", "x": 0, "y": 0, "largura": 1080, "altura": 6, "cor": OURO},
        {"id": "faixa-base", "nome": "Faixa do rodapé", "tipo": "retangulo", "x": 0, "y": 1434, "largura": 1080, "altura": 6, "cor": OURO},
        {"id": "foto", "nome": "Foto", "tipo": "imagem", "x": 300, "y": 310, "largura": 740, "altura": 952, "arquivo": foto, "mistura": "screen",
         "sepia": 0.14, "pb": True, "mascara_caixa": "linear-gradient(#000 88%,transparent)", "mascara_foto": radial},
        texto("gritar", 9, 1348, "GRITAR", "EB Garamond", 270, "ouro-brilho", nome="GRITAR", peso=500, entrelinha=1, espacamento=0.015, rotacao=-90),
        texto("assunto", 320, 96, "ASSÉDIO MORAL", "Inter", 32, OURO, nome="Assunto", peso=600, espacamento=0.12),
        texto("area", 766.3125, 104, "Direito do Trabalho", "Inter", 24, nome="Área", peso=500),
        texto("frase", 320, 153, "não é <i>cobrar.</i>", "EB Garamond", 132, nome="Frase", peso=500, entrelinha=1.02, espacamento=-0.015, cor_destaque=OURO),
        texto("apoio", 320, 305.625, "Cobrar resultados é legítimo.<br>Humilhar trabalhadores, não.", "Inter", 32, nome="Apoio", entrelinha=1.34),
        texto("ressalva", 320, 405.375, "Abuso repetido pode configurar assédio moral.", "Inter", 26, nome="Ressalva", entrelinha=1.35),
        {"id": "fio", "nome": "Fio da assinatura", "tipo": "retangulo", "x": 320, "y": 1261.21875, "largura": 664, "altura": 2, "cor": OURO},
        texto("nome", 320, 1279.21875, "LETÍCIA BARROS", "Inter", 24, nome="Nome", peso=600, entrelinha=1.35, espacamento=0.12),
        texto("oab", 320, 1311.609375, "Advocacia · OAB/ES 39.948", "Inter", 24, nome="OAB", peso=500, entrelinha=1.35),
    ]}


if __name__ == "__main__":
    Acervo(AQUI).criar(NOME, documento("foto.jpg"), {"foto.jpg": foto_tratada()})
    print(NOME)
