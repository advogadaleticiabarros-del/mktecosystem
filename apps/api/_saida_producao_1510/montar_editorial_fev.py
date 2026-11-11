"""Editorial de fevereiro de 2027 (pedido da Jessica em 11/11/2026: "pode fazer até o máximo que der, até fevereiro ou
março"). Mesma grade de docs/EDITORIAL_DO_FEED.md: 12h post todo dia, 19h Reels (Mito seg/qua/sáb, Flagrante
ter/sex). Gera editorial_fev.json para aplicar_editorial_jan.py (python aplicar_editorial_jan.py editorial_fev.json).

Uso: python montar_editorial_fev.py   → editorial_fev.json + envio_fev/"""
import json
import shutil
from pathlib import Path

import conteudo_dez
import conteudo_fev
import conteudo_nov
from montar_editorial_jan import ESTILOS, MOTION, RODAPE, SCRATCH_RESERVA

AQUI = Path(__file__).resolve().parent
ENVIO = AQUI / "envio_fev"

# Flagrante prontos (aprovados em 09/11/2026), terça e sexta 19h
FLAGRANTE = {"2027-02-02": ("09-sem-carteira", "Sem carteira assinada"), "2027-02-05": ("04-demissao", "Pedido de demissão"),
             "2027-02-09": ("31-story", "Story como prova"), "2027-02-12": ("11-fgts", "FGTS"),
             "2027-02-16": ("14-banheiro", "Controle de banheiro"), "2027-02-19": ("06-almoco", "Horário de almoço"),
             "2027-02-23": ("30-exame", "Exame preventivo"), "2027-02-26": ("27-preco", "Preço no caixa")}

MITO = {f"2027-{m[0][5:]}": f"{m[0][5:]}-{m[1]}" for m in conteudo_fev.MITO_OU_LEI}

# 12h: perguntas claras (texto e legenda já aprovados, peça da reserva do Orbit ganha a arte clara)
CLARAS = {"2027-02-01": "amamentacao-trabalho", "2027-02-03": "creche-empresa", "2027-02-08": "viagem-com-filhos",
          "2027-02-09": "racismo-trabalho", "2027-02-10": "alimentos-gravidicos", "2027-02-13": "gestante-insalubre",
          "2027-02-16": "assedio-moral", "2027-02-17": "dona-de-casa-inss", "2027-02-19": "trabalho-escravo",
          "2027-02-22": "hiv-trabalho", "2027-02-24": "aposentadoria-2027", "2027-02-26": "burnout-trabalho",
          "2027-02-27": "desempregada-gravida-inss"}

# 12h: acentos escuros (Palavra de Ouro e Papel e Ouro), espaçados na grade
TAGS = "#DireitoTrabalhista #DireitosDaMulher #DireitosDoTrabalhador #CLT #AdvogadaTrabalhista"
ACENTOS = {
    "2027-02-06": ("palavra-de-ouro/pecas/04-gravida.jpg", "Grávida não é motivo",
                   "Grávida não é motivo.\n\nA gravidez não é justo motivo para encerrar o contrato de trabalho. E a gestante tem "
                   "estabilidade da confirmação da gravidez até 5 meses depois do parto.\n\nSalve e mande para uma gestante.",
                   "CLT, art. 391; ADCT, art. 10, II, b", "Você conhece alguém que foi demitida grávida?"),
    "2027-02-12": ("palavra-de-ouro/pecas/02-salario.jpg", "Salário tem data",
                   "Salário tem data.\n\nO salário mensal deve ser pago até o 5º dia útil do mês seguinte. Atraso repetido "
                   "pode até permitir a rescisão indireta, a \"justa causa\" do patrão.\n\nSalve e mande para quem recebe "
                   "sempre atrasado.", "CLT, art. 459, § 1º; art. 483, d", "O seu salário cai no dia certo?"),
    "2027-02-15": ("palavra-de-ouro/pecas/03-assinar.jpg", "Assinar sem ler, não",
                   "Assinar sem ler, não.\n\nLeia tudo antes de assinar acordo, rescisão ou pedido de demissão. Se pressionarem, "
                   "peça uma cópia e tempo para ler.\n\nSalve e mande para quem vai assinar papel na empresa.",
                   "CLT, art. 477", "Já te pediram para assinar sem ler?"),
    "2027-02-20": ("palavra-de-ouro/pecas/06-burnout.jpg", "Burnout tem nome",
                   "Burnout tem nome.\n\nEstá na CID-11 como fenômeno ligado ao trabalho e, desde 2023, na lista oficial de "
                   "doenças relacionadas ao trabalho. Pode gerar afastamento pelo INSS.\n\nSalve e mande para quem está no limite.",
                   "CID-11 (QD85); Portaria GM/MS 1.999/2023", "Você conhece alguém que chegou nesse ponto?"),
    "2027-02-23": ("palavra-de-ouro/pecas/05-antes.jpg", "Pensão antes de nascer",
                   "Antes de nascer.\n\nA pensão pode ser pedida durante a gravidez: são os alimentos gravídicos. Depois do "
                   "parto, ela continua para o bebê.\n\nSalve e mande para uma gestante que está sozinha.",
                   "Lei 11.804/2008", "Você sabia que dá para pedir na gravidez?"),
    "2027-02-28": ("papel-e-ouro/pecas/fora-03-positivo.jpg", "Deu positivo: a estabilidade também",
                   "Deu positivo. A estabilidade também.\n\nA estabilidade da gestante vale da confirmação da gravidez até 5 "
                   "meses depois do parto, mesmo que a empresa ainda não saiba.\n\nGuarde o exame com a data.\n\nSalve e mande "
                   "para uma gestante.", "ADCT, art. 10, II, b; Súmula 244 do TST", "Quando você contou na empresa?"),
}


def pauta_da_pergunta(chave):
    for mod in (conteudo_nov, conteudo_dez):
        for t in mod.TEMAS:
            if t["chave"] == chave:
                return t["data"]
    raise KeyError(chave)


def main():
    ENVIO.mkdir(exist_ok=True)
    acoes = []
    reserva = [l.split("\t") for l in SCRATCH_RESERVA.read_text(encoding="utf-8").splitlines() if l.strip()]
    for dia, chave in CLARAS.items():
        pauta = pauta_da_pergunta(chave)
        ids = [r[0] for r in reserva if r[1] == "pergunta" and r[2] == pauta and "v=manchete1" in r[4]]
        assert len(ids) == 1, (chave, ids)
        arq = f"clara-pergunta-{chave}.jpg"
        shutil.copy(ESTILOS / "manchete" / "pecas" / arq, ENVIO / arq)
        acoes.append({"acao": "agendar", "dia": dia, "hora": "12:00", "piece_id": ids[0], "formato": "post",
                      "status": "pronto", "nova_imagem": arq})
    for t in conteudo_fev.FRASES_EXTRA:
        nome = f"fev-{t['data'][5:]}-frase-{t['chave']}"
        arq = f"estatico-{nome}.jpg"
        shutil.copy(ESTILOS / "manchete" / "pecas" / f"{nome}.jpg", ENVIO / arq)
        acoes.append({"acao": "nova", "dia": t["data"], "hora": "12:00", "tipo": "frase", "formato": "post",
                      "titulo": "Frase: " + t["frase"]["html"].replace("<em>", "").replace("</em>", "")[:180],
                      "area": t["area"], "arquivo": arq, "estilo": "frase-papel", "legenda": t["legenda"],
                      "primeiro_comentario": t["primeiro_comentario"]})
    for dia, (caminho, titulo, leg, base, perg) in ACENTOS.items():
        arq = "estatico-" + caminho.replace("/pecas/", "-").replace("/", "-")
        shutil.copy(ESTILOS / caminho, ENVIO / arq)
        acoes.append({"acao": "nova", "dia": dia, "hora": "12:00", "tipo": "estatico", "formato": "post", "titulo": titulo,
                      "area": "Trabalhista", "arquivo": arq, "estilo": caminho.split("/")[0],
                      "legenda": leg + RODAPE + TAGS, "primeiro_comentario": f"📚 Base: {base}.\n💬 {perg}"})
    for dia, (ep, tema) in FLAGRANTE.items():
        pasta = MOTION / ep
        video, capa = f"flagrante-{ep}-v2.mp4", f"flagrante-{ep}-capa-textura.jpg"
        shutil.copy(pasta / f"{ep}-v2.mp4", ENVIO / video)
        shutil.copy(pasta / "capa-textura.jpg", ENVIO / capa)
        l = json.loads((pasta / "legenda.json").read_text(encoding="utf-8"))
        acoes.append({"acao": "nova", "dia": dia, "hora": "19:00", "tipo": "reels", "formato": "reels",
                      "titulo": f"Reels Flagrante: {tema}", "area": "Trabalhista", "video": video, "capa": capa,
                      "estilo": "flagrante", "episodio": ep, "legenda": l["legenda"],
                      "primeiro_comentario": l.get("primeiro_comentario", "")})
    for dia, nome in MITO.items():
        pasta = MOTION / "mito-lei" / nome
        if not (pasta / f"{nome}-v3.mp4").exists() or not (pasta / "capa-moldura-viva.jpg").exists():
            print("FALTA VÍDEO OU CAPA", nome)
            continue
        video, capa = f"mito-lei-{nome}-v3.mp4", f"mito-lei-{nome}-capa-moldura-viva.jpg"
        shutil.copy(pasta / f"{nome}-v3.mp4", ENVIO / video)
        shutil.copy(pasta / "capa-moldura-viva.jpg", ENVIO / capa)
        l = json.loads((pasta / "legenda.json").read_text(encoding="utf-8"))
        acoes.append({"acao": "nova", "dia": dia, "hora": "19:00", "tipo": "reels", "formato": "reels",
                      "titulo": "Mito ou Lei: " + l["legenda"].split("?", 1)[0], "area": "Trabalhista", "video": video,
                      "capa": capa, "estilo": "mito-ou-lei", "legenda": l["legenda"],
                      "primeiro_comentario": l.get("primeiro_comentario", "")})
    dias12 = sorted(a["dia"] for a in acoes if a["hora"] == "12:00")
    assert len(dias12) == len(set(dias12)) == 28, (len(dias12), len(set(dias12)))
    (AQUI / "editorial_fev.json").write_text(json.dumps(acoes, ensure_ascii=False, indent=1), encoding="utf-8")
    from collections import Counter
    print(len(acoes), Counter(a["acao"] for a in acoes), "arquivos:", len(list(ENVIO.iterdir())))


if __name__ == "__main__":
    main()
