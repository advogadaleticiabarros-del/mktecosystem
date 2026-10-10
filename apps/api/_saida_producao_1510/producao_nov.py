"""Frases v2 e Mito ou Lei v3 dos planos mensais (conteudo_nov.py, conteudo_dez.py), no modelo aprovado. MES=dez para dezembro.

Uso (de apps/api): python _saida_producao_1510/producao_nov.py [frases] [mitos]
Carrosséis: DADOS=nov python _saida_producao_1510/carrossel_v5.py · Perguntas: pergunta_v6.py <chave ...>
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from PIL import Image  # noqa: E402

from app.services.render_criativo import renderizar_frase_impacto, renderizar_mito_ou_lei  # noqa: E402
import importlib, os  # noqa: E402
_MES = importlib.import_module("conteudo_" + os.environ.get("MES", "nov"))
MITO_OU_LEI, TEMAS = _MES.MITO_OU_LEI, _MES.TEMAS

AQUI = Path(__file__).resolve().parent
IV_FRASE = {"cores": {"fundo_escuro": "#231E1A", "dourado": "#C9A962", "areia": "#E8DED1"}}
IV_MITO = {"cores": {"fundo_escuro": "#1E1814", "dourado": "#C9A962", "areia": "#E8DED1"}}


def jpg(png: Path) -> None:
    Image.open(png).convert("RGB").save(png.with_suffix(".jpg"), "JPEG", quality=92, optimize=True)
    png.unlink()


async def main(partes: set[str]) -> None:
    if not partes or "frases" in partes:
        for t in TEMAS:
            png = AQUI / "pecas" / f"{t['chave']}-frase-v2.png"
            await renderizar_frase_impacto(t["frase"]["html"], IV_FRASE, str(png))
            jpg(png)
            print("ok frase", t["chave"])
    if not partes or "mitos" in partes:
        for dia, _k, af, ver, ex, ref, *_ in MITO_OU_LEI:
            png = AQUI / "pecas" / f"mito-{dia}-v3-topo.png"
            await renderizar_mito_ou_lei(af, ver, ex, ref, IV_MITO, str(png))
            jpg(png)
            print("ok mito", dia)


if __name__ == "__main__":
    asyncio.run(main(set(sys.argv[1:])))
