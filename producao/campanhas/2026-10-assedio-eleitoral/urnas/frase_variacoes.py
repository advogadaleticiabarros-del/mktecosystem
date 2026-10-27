"""Variações da frase com o ângulo pós-eleição: represália pelo voto (27/10/2026).

Pedido: "me dê mais variações da frase, principalmente porque já acabou a eleição, esse efeito está em represália à
escolha do candidato e ligado à vingança". Mesmo modelo da frase v3 (`frase_estatico_v.py`): foto real de urna sob
véu café e crédito. Neutras (nenhum lado) e sem promessa de resultado (OAB).

Saída: ../frase-estatico/pecas/assedio-eleitoral-frase-var-N.jpg
"""
import asyncio

import frase_estatico_v as base
import urnas
from app.services.render_criativo import _env, _fotografar, _logo_data_uri

# (frase, tamanho da fonte, foto, foco da foto). Sem a foto "luz": a tela mostra "PRESIDENTE", que depois da eleição
# pode ser lido como indireta a um lado. A "ue2020" é clara e pede véu mais escuro (VEU).
FRASES = [
    ("A eleição acabou.<br><em>O seu direito, não.</em>", 84, "confirma", (0.70, 0.5)),
    ("Discordar do seu voto é direito de qualquer um.<br><em>Demitir por ele, não.</em>", 66, "teclado", (0.62, 0.5)),
    ("O resultado da eleição não é motivo de demissão.<br><em>Vingança também não.</em>", 64, "teclado", (0.35, 0.5)),
    ("Represália pelo voto tem nome na lei:<br><em>dispensa discriminatória.</em>", 68, "ue2020", (0.50, 0.60)),
    ("Ninguém pode pagar com o emprego<br><em>pelo voto que deu.</em>", 72, "confirma", (0.55, 0.5)),
    ("A urna fechou no domingo.<br><em>A porta da empresa não pode fechar por isso.</em>", 64, "teclado", (0.45, 0.5)),
    ("Demitir por vingança eleitoral não é gestão.<br><em>É discriminação.</em>", 68, "confirma", (0.85, 0.5)),
    ("Seu voto foi secreto.<br><em>A represália por ele é proibida.</em>", 72, "ue2020", (0.40, 0.55)),
]


VEU = {"ue2020": (.93, .8)}


def html(frase: str, tamanho: int, foto: str, foco: tuple[float, float]) -> str:
    h = _env.get_template("frase_impacto.html").render(
        frase=frase, fundo="#231E1A", dourado="#C9A962", areia="#E8DED1", tamanho_fonte=tamanho,
        nome_conta="Letícia Barros", oab="OAB/ES 39.948", logo_src=_logo_data_uri())
    h = h.replace('<div class="mancha"></div>', base.camada(foto, foco, *VEU.get(foto, (.86, .6))), 1)
    return h.replace('<div class="grao"></div>', '<div class="grao"></div>' + base.CREDITO.format(urnas.credito(foto)), 1)


async def main():
    base.SAIDA.mkdir(exist_ok=True)
    for i, (frase, tamanho, foto, foco) in enumerate(FRASES, 1):
        png = base.SAIDA / f"assedio-eleitoral-frase-var-{i}.png"
        await _fotografar(html(frase, tamanho, foto, foco), str(png))
        print("ok", base.v1.jpg(png))


if __name__ == "__main__":
    asyncio.run(main())
