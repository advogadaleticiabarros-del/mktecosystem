"""Rebalanceia o feed de 02/01 a 28/02/2027 com todos os formatos (pedido da Jessica em 11/11/2026: "está faltando
carrossel, precisamos de postagens durante a semana de todos os formatos e estilos ... balanceado até final de fevereiro").

Grade semanal (12h): seg e qua carrossel (melhores dias de carrossel do perfil) · ter e sex Manchete ou pergunta clara ·
qui pergunta clara ou Manchete (+ frase às 19h) · sáb peça de marca (Papel e Ouro, Verbete, Palavra de Ouro) · dom frase.
Reels (19h) não mudam. O que sobra vai para 01 a 12/03 às 12h; os 3 Flagrantes da reserva vão para 02, 05 e 09/03 às 19h.

Gera rebalancear_jan_fev.json com:
- "mover": peça já agendada (achada pelo nome do arquivo da arte) → novo dia/hora;
- "nova": carrossel novo (carrosseis_jan_fev.py) ou Flagrante de março.
Aplicar no container: python aplicar_rebalanceamento.py [--aplicar]
"""
import json
from pathlib import Path

import carrosseis_jan_fev as JF
from montar_editorial_jan import MOTION

AQUI = Path(__file__).resolve().parent

# (dia, hora, trecho do nome do arquivo da arte)
MOVER = [
    # sábados: peça de marca (claro e escuro alternados)
    ("2027-01-02", "12:00", "estatico-papel-e-ouro-clara-02"), ("2027-01-09", "12:00", "estatico-palavra-de-ouro-01-hora-extra"),
    ("2027-01-16", "12:00", "estatico-papel-e-ouro-clara-05"), ("2027-01-23", "12:00", "estatico-papel-e-ouro-clara-07"),
    ("2027-01-30", "12:00", "estatico-papel-e-ouro-fora-04"), ("2027-02-06", "12:00", "estatico-palavra-de-ouro-04-gravida"),
    ("2027-02-13", "12:00", "estatico-papel-e-ouro-clara-08"), ("2027-02-20", "12:00", "estatico-palavra-de-ouro-06-burnout"),
    ("2027-02-27", "12:00", "estatico-papel-e-ouro-clara-01"),
    # quintas 12h: pergunta clara em janeiro e fevereiro
    ("2027-01-07", "12:00", "clara-pergunta-amamentacao-trabalho"), ("2027-01-14", "12:00", "clara-pergunta-creche-empresa"),
    ("2027-01-21", "12:00", "clara-pergunta-gestante-insalubre"), ("2027-01-28", "12:00", "clara-pergunta-racismo-trabalho"),
    ("2027-02-04", "12:00", "clara-pergunta-alimentos-gravidicos"), ("2027-02-11", "12:00", "clara-pergunta-desempregada-gravida-inss"),
    ("2027-02-18", "12:00", "clara-pergunta-dona-de-casa-inss"), ("2027-02-25", "12:00", "clara-pergunta-hiv-trabalho"),
    # fevereiro: terça Manchete, sexta pergunta clara (janeiro mantém os pares Manchete + Flagrante)
    ("2027-02-02", "12:00", "estatico-manchete-19-"), ("2027-02-09", "12:00", "estatico-manchete-17-"),
    ("2027-02-16", "12:00", "estatico-manchete-24-"), ("2027-02-23", "12:00", "estatico-manchete-10-"),
    ("2027-02-05", "12:00", "clara-pergunta-viagem-com-filhos"), ("2027-02-12", "12:00", "clara-pergunta-assedio-moral"),
    ("2027-02-19", "12:00", "clara-pergunta-trabalho-escravo"), ("2027-02-26", "12:00", "clara-pergunta-aposentadoria-2027"),
    # domingos 12h e quintas 19h: frases em papel claro
    ("2027-01-03", "12:00", "frase-licenca-paternidade-2027"), ("2027-01-07", "19:00", "frase-temporaria-fim-de-ano"),
    ("2027-01-10", "12:00", "frase-aposentadoria-2027"), ("2027-01-14", "19:00", "frase-hiv-trabalho"),
    ("2027-01-17", "12:00", "frase-viagem-com-filhos"), ("2027-01-21", "19:00", "frase-assedio-moral"),
    ("2027-01-24", "12:00", "frase-dona-de-casa-inss"), ("2027-01-28", "19:00", "frase-desempregada-gravida-inss"),
    ("2027-01-31", "12:00", "frase-gestante-insalubre"),
    ("2027-02-04", "19:00", "frase-bebe-internado"), ("2027-02-07", "12:00", "frase-luto-2-dias"),
    ("2027-02-11", "19:00", "frase-pensao-18"), ("2027-02-14", "12:00", "frase-casamento-3-dias"),
    ("2027-02-18", "19:00", "frase-gestante-consultas"), ("2027-02-21", "12:00", "frase-doenca-ocupacional"),
    ("2027-02-25", "19:00", "frase-seguro-desemprego"), ("2027-02-28", "12:00", "frase-domestica-hora-extra"),
    # sobras: começo de março, 12h
    ("2027-03-01", "12:00", "clara-pergunta-burnout-trabalho"), ("2027-03-02", "12:00", "estatico-manchete-11-"),
    ("2027-03-03", "12:00", "frase-amamentacao-trabalho"), ("2027-03-04", "12:00", "estatico-palavra-de-ouro-02-salario"),
    ("2027-03-05", "12:00", "estatico-manchete-07-"), ("2027-03-06", "12:00", "estatico-papel-e-ouro-fora-03"),
    ("2027-03-07", "12:00", "frase-racismo-trabalho"), ("2027-03-08", "12:00", "estatico-manchete-27-"),
    ("2027-03-09", "12:00", "estatico-palavra-de-ouro-03-assinar"), ("2027-03-10", "12:00", "frase-gestante-troca-funcao"),
    ("2027-03-11", "12:00", "estatico-manchete-29-"), ("2027-03-12", "12:00", "estatico-palavra-de-ouro-05-antes"),
]

FLAGRANTE_MARCO = {"2027-03-02": ("16-guarda", "Guarda compartilhada"), "2027-03-05": ("20-pausa-banheiro", "Pausa no banheiro"),
                   "2027-03-09": ("28-estacionamento", "Furto no estacionamento")}


def main():
    acoes = [{"acao": "mover", "dia": d, "hora": h, "midia": m} for d, h, m in MOVER]
    chaves = {}
    for d, h, m in MOVER:
        assert (d, h) not in chaves, ("vaga repetida", d, h)
        chaves[(d, h)] = m
    assert len({m for _, _, m in MOVER}) == len(MOVER), "arte repetida"
    for t in JF.TEMAS:
        c = t["carrossel"]
        assert (t["data"], "12:00") not in chaves, ("carrossel em vaga ocupada", t["data"])
        acoes.append({"acao": "nova", "dia": t["data"], "hora": "12:00", "tipo": "carrossel", "formato": "carrossel",
                      "titulo": t["titulo"], "area": t["area"], "estilo": "carrossel-ouro-editorial",
                      "imagens": [f"carrossel-{t['chave']}-v5-{i}.jpg" for i in range(1, 8)],
                      "legenda": c["legenda"], "primeiro_comentario": c["pc"]})
    for dia, (ep, tema) in FLAGRANTE_MARCO.items():
        l = json.loads((MOTION / ep / "legenda.json").read_text(encoding="utf-8"))
        acoes.append({"acao": "nova", "dia": dia, "hora": "19:00", "tipo": "reels", "formato": "reels",
                      "titulo": f"Reels Flagrante: {tema}", "area": "Trabalhista", "video": f"flagrante-{ep}-v2.mp4",
                      "capa": f"flagrante-{ep}-capa-textura.jpg", "estilo": "flagrante", "episodio": ep,
                      "legenda": l["legenda"], "primeiro_comentario": l.get("primeiro_comentario", "")})
    (AQUI / "rebalancear_jan_fev.json").write_text(json.dumps(acoes, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(acoes), "ações:", sum(a["acao"] == "mover" for a in acoes), "mover,", sum(a["acao"] == "nova" for a in acoes), "novas")


if __name__ == "__main__":
    main()
