"""Série Mito ou Lei v3, PADRÃO APROVADO pela Letícia em 09/10/2026: lote do plano 15/10–02/11.

O modelo oficial está em `app/templates/mito_card.html` + `render_criativo.renderizar_mito_ou_lei`
(selo encaixado no topo do cartão). A proposta descartada (selo no canto) ficou no commit ea3263f.

Uso (de apps/api): python _saida_producao_1510/mito_v3.py [AAAA-MM-DD ...]
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from PIL import Image  # noqa: E402

from app.services.render_criativo import renderizar_mito_ou_lei  # noqa: E402
from conteudo import MITO_OU_LEI  # noqa: E402

AQUI = Path(__file__).resolve().parent
IDENTIDADE = {"cores": {"fundo_escuro": "#1E1814", "dourado": "#C9A962", "areia": "#E8DED1"}}


async def main(dias: list[str]) -> None:
    for dia, _k, af, ver, ex, ref, _tags in MITO_OU_LEI:
        if dias and dia not in dias:
            continue
        destino = AQUI / "pecas" / f"mito-{dia}-v3-topo.png"
        await renderizar_mito_ou_lei(af, ver, ex, ref, IDENTIDADE, str(destino))
        Image.open(destino).convert("RGB").save(destino.with_suffix(".jpg"), "JPEG", quality=92, optimize=True)
        destino.unlink()
        print("ok", dia)


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
