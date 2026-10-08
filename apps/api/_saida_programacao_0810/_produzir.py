"""Produz as artes que faltavam para a programação de 08 a 14/10/2026 e junta
todas as peças (novas e já prontas) em JPEG, com legenda, numa pasta só.

Uso (de apps/api): python _saida_programacao_0810/_produzir.py
"""
import asyncio
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import Image  # noqa: E402

from app.services.render_criativo import renderizar_frase_impacto, renderizar_pergunta  # noqa: E402

AQUI = Path(__file__).resolve().parent
ED = Path(r"C:\Users\prosy\Desktop\Editorial")
FRASES_VG = AQUI.parent / "_saida_frases_stf_violencia_genero"
SAIDA = AQUI / "pecas"
IV = {"cores": {"fundo_escuro": "#231E1A", "dourado": "#C9A962", "areia": "#E8DED1"}}
RODAPE = "\n\nSe essa é a sua situação, procure uma advogada de confiança."


def legenda_html(caminho: Path) -> str:
    s = caminho.read_text(encoding="utf-8")
    m = re.search(r'<div class="legenda">(.*?)</div>', s, re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()


def legendas_frases_vg() -> list[str]:
    s = (FRASES_VG / "legendas.txt").read_text(encoding="utf-8")
    partes = re.split(r"\nFrase \d — .*?\n", s)
    return [re.sub(r"^\s*Legenda:\s*", "", p).strip() for p in partes]


def jpeg(origem: Path, nome: str) -> str:
    destino = SAIDA / nome
    Image.open(origem).convert("RGB").save(destino, "JPEG", quality=92, optimize=True)
    return nome


NOVAS = {
    "frase-pet.png": ("frase", "O pet também é da família. <em>E a lei agora reconhece isso no divórcio.</em>"),
    "frase-abandono.png": ("frase", "Pagar pensão não é o mesmo que <em>estar presente.</em>"),
    "frase-clt.png": ("frase", "Direito que você não conhece é <em>direito que você deixa de receber.</em>"),
    "pergunta-clt.png": ("pergunta", "Cobri as férias de uma colega. Tenho direito ao salário dela?"),
}

LEGENDAS_NOVAS = {
    "frase-pet": (
        "🐾 Quem tem pet sabe: ele não é um objeto que fica com quem estiver com a chave de casa.\n\n"
        "Desde a Lei 15.392/2026, o pet que viveu a maior parte da vida durante o casamento ou a união "
        "estável é dos dois. Sem acordo, a regra é a guarda compartilhada, e as despesas são divididas.\n\n"
        "💛 Manda pra quem está se separando e tem medo de perder o companheiro de quatro patas."
        + RODAPE + "\n\n#GuardaDePet #DireitoDeFamília #Divórcio2026 #AdvogadaDeFamília #AdvogadaVitóriaES"
    ),
    "frase-abandono": (
        "💔 Tem pai que paga a pensão em dia e nunca pergunta como foi a escola.\n\n"
        "A Lei 15.240/2025 reconheceu o abandono afetivo como ato ilícito civil: presença, convivência e "
        "apoio nas decisões da vida do filho também são dever. Quando a ausência é sistemática, pode gerar "
        "indenização por dano moral.\n\n"
        "💛 Amor não se obriga por lei. Mas presença e cuidado, sim, têm consequência."
        + RODAPE + "\n\n#AbandonoAfetivo #DireitoDeFamília #Lei152402025 #AdvogadaDeFamília #AdvogadaVitóriaES"
    ),
    "frase-clt": (
        "💼 Muita gente trabalha anos sem saber de direitos simples, e deixa dinheiro pelo caminho.\n\n"
        "Cobrir as férias de um colega, fazer pausa quando digita o dia todo, não pagar pelo uniforme que "
        "estragou com o uso: tudo isso está na lei, e eu explico no carrossel de hoje à noite.\n\n"
        "💛 Ativa o sininho pra não perder."
        + RODAPE + "\n\n#DireitoTrabalhista #CLT #VocêSabia #DireitosDoTrabalhador #AdvogadaTrabalhista"
    ),
    "pergunta-clt": (
        "Essa dúvida chega muito pra mim.\n\n"
        "Quando você substitui um colega nas férias, licença ou afastamento, e essa substituição não é só "
        "um quebra-galho de algumas horas, você tem direito a receber o mesmo salário que ele recebe "
        "enquanto durar a substituição. É o que diz a Súmula 159 do TST.\n\n"
        "Guarde a prova: escala, e-mails, mensagens pedindo pra você cobrir, o período certinho.\n\n"
        "Já passou por isso? Me conta nos comentários."
        + RODAPE + "\n\n#DireitoTrabalhista #CLT #SalárioSubstituição #AdvogadaTrabalhista #AdvogadaVitóriaES"
    ),
}


async def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    tmp = AQUI / "_png"
    tmp.mkdir(exist_ok=True)
    for nome, (tipo, texto) in NOVAS.items():
        caminho = str(tmp / nome)
        if tipo == "frase":
            await renderizar_frase_impacto(texto, IV, caminho)
        else:
            await renderizar_pergunta(texto, IV, caminho)

    def carrossel(pasta: Path, prefixo: str) -> list[str]:
        return [jpeg(pasta / f"slide-{i}.png", f"{prefixo}-{i}.jpg") for i in range(1, 6)]

    lg_vg = legendas_frases_vg()
    plano = [
        # (data, hora, tipo, tema, imagens, legenda)
        ("2026-10-08", "19:00", "pergunta", "Assédio eleitoral no trabalho",
         [jpeg(ED / "2026-09/28-09-2026/pergunta/criativo.png", "relato-assedio.jpg")],
         legenda_html(ED / "2026-09/28-09-2026/pergunta/legenda.html")),

        ("2026-10-09", "12:00", "pergunta", "Guarda compartilhada de pet",
         [jpeg(ED / "2026-09/30-09-2026/pergunta/criativo.png", "pergunta-pet.jpg")],
         legenda_html(ED / "2026-09/30-09-2026/pergunta/legenda.html")),
        ("2026-10-09", "15:00", "frase", "Guarda compartilhada de pet",
         [jpeg(tmp / "frase-pet.png", "frase-pet.jpg")], LEGENDAS_NOVAS["frase-pet"]),
        ("2026-10-09", "20:00", "carrossel", "Guarda compartilhada de pet",
         carrossel(ED / "2026-09/30-09-2026/carrossel", "carrossel-pet"),
         legenda_html(ED / "2026-09/30-09-2026/carrossel/legenda.html")),
        ("2026-10-10", "19:00", "estatico", "Violência de gênero (STF)",
         [jpeg(FRASES_VG / "frase-01-familia-violencia-fora-de-casa.png", "estatico-vg-1.jpg")], lg_vg[0]),

        ("2026-10-11", "12:00", "pergunta", "Abandono afetivo",
         [jpeg(ED / "2026-10/02-10-2026/pergunta/criativo.png", "relato-abandono.jpg")],
         legenda_html(ED / "2026-10/02-10-2026/pergunta/legenda.html")),
        ("2026-10-11", "15:00", "frase", "Abandono afetivo",
         [jpeg(tmp / "frase-abandono.png", "frase-abandono.jpg")], LEGENDAS_NOVAS["frase-abandono"]),
        ("2026-10-11", "20:00", "carrossel", "Abandono afetivo",
         carrossel(ED / "2026-10/02-10-2026/carrossel", "carrossel-abandono"),
         legenda_html(ED / "2026-10/02-10-2026/carrossel/legenda.html")),
        ("2026-10-12", "19:00", "estatico", "Violência de gênero (STF)",
         [jpeg(FRASES_VG / "frase-02-familia-protecao-de-estranho.png", "estatico-vg-2.jpg")], lg_vg[1]),

        ("2026-10-13", "12:00", "pergunta", "3 direitos trabalhistas pouco conhecidos",
         [jpeg(tmp / "pergunta-clt.png", "pergunta-clt.jpg")], LEGENDAS_NOVAS["pergunta-clt"]),
        ("2026-10-13", "15:00", "frase", "3 direitos trabalhistas pouco conhecidos",
         [jpeg(tmp / "frase-clt.png", "frase-clt.jpg")], LEGENDAS_NOVAS["frase-clt"]),
        ("2026-10-13", "20:00", "carrossel", "3 direitos trabalhistas pouco conhecidos",
         carrossel(ED / "2026-10/04-10-2026/carrossel", "carrossel-clt"),
         legenda_html(ED / "2026-10/04-10-2026/carrossel/legenda.html")),
        ("2026-10-14", "19:00", "estatico", "Violência de gênero (STF)",
         [jpeg(FRASES_VG / "frase-03-familia-medida-protetiva-toda-mulher.png", "estatico-vg-3.jpg")], lg_vg[2]),
    ]
    itens = [{"data": d, "hora": h, "tipo": t, "tema": tema, "imagens": imgs, "legenda": leg}
             for d, h, t, tema, imgs, leg in plano]
    (AQUI / "plano.json").write_text(json.dumps(itens, ensure_ascii=False, indent=1), encoding="utf-8")

    # folha de contato para conferência
    capas = [(i["data"][8:] + "/10 " + i["hora"] + " " + i["tipo"], SAIDA / i["imagens"][0]) for i in itens]
    larg, alt, col = 270, 338, 7
    folha = Image.new("RGB", (col * (larg + 10), ((len(capas) + col - 1) // col) * (alt + 34)), "white")
    from PIL import ImageDraw
    d = ImageDraw.Draw(folha)
    for k, (rot, img) in enumerate(capas):
        x, y = (k % col) * (larg + 10), (k // col) * (alt + 34)
        folha.paste(Image.open(img).resize((larg, alt)), (x, y))
        d.text((x + 4, y + alt + 8), rot, fill="black")
    folha.save(AQUI / "folha.png")
    print(len(itens), "posts;", sum(len(i["imagens"]) for i in itens), "imagens")


asyncio.run(main())
