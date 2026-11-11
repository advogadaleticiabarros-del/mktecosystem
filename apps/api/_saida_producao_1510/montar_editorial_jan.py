"""Monta o editorial do feed de 11/11/2026 a 31/01/2027 (pedido da Jessica em 10/11/2026) e gera editorial_jan.json
para aplicar_editorial_jan.py (roda no container). Roda aqui no Windows.

Grade semanal (docs/EDITORIAL_DO_FEED.md):
  seg 12h carrossel/estático · 19h Reels Mito ou Lei     ter 12h Manchete · 19h Reels Flagrante
  qua 12h carrossel/estático · 19h Reels Mito ou Lei     qui 12h carrossel/Manchete · 19h frase (papel claro)
  sex 12h Manchete · 19h Reels Flagrante                  sáb 12h carrossel/Manchete · 19h Reels Mito ou Lei
  dom 12h frase/estático · 15h30 Reels da Dra. (gravação dela)
Em dia de Flagrante, o estático Manchete do mesmo tema sai às 12h (par Manchete + Flagrante).

Uso: python montar_editorial_jan.py   → editorial_jan.json + envio_jan/ (arquivos para /app/media)
"""
import json
import re
import shutil
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
ESTILOS = RAIZ / "producao" / "estilos"
MOTION = ESTILOS / "papel-e-ouro" / "motion-diario"
ENVIO = AQUI / "envio_jan"
SCRATCH_RESERVA = Path(r"C:\Users\prosy\AppData\Local\Temp\claude\0720c4ab6a234b3c\d15d8cde-a713-4451-8e57-e48353233bdd\scratchpad\reserva.tsv")

# ---------- 12h: estáticos Manchete (já aprovados pela Jessica; a peça e a legenda estão em producao/estilos/manchete)
MANCHETE_12H = {
    "2026-11-13": "01-te-disseram", "2026-11-18": "09-exame", "2026-11-20": "04-cabelo", "2026-11-24": "13-doar-sangue",
    "2026-11-25": "06-preco", "2026-11-27": "33-licenca-180", "2026-11-30": "31-decimo-terceiro", "2026-12-01": "28-pensao",
    "2026-12-04": "23-salario-atrasado", "2026-12-07": "34-fim-6x1", "2026-12-09": "03-palavra", "2026-12-11": "08-revista",
    "2026-12-14": "05-amigo-secreto", "2026-12-16": "22-sem-carteira", "2026-12-18": "32-temporario",
    "2026-12-21": "30-ferias-natal", "2026-12-28": "12-avo", "2026-12-30": "02-caderno",
    # janeiro: par com o Flagrante do dia
    "2027-01-05": "18-ferias", "2027-01-08": "14-atestado", "2027-01-12": "15-holerite", "2027-01-15": "16-ponto",
    "2027-01-19": "20-experiencia", "2027-01-22": "25-sem-folga", "2027-01-26": "26-aviso-previo", "2027-01-29": "21-por-fora",
    # janeiro: demais dias
    "2027-01-02": "19-almoco", "2027-01-07": "24-fgts", "2027-01-11": "11-story", "2027-01-14": "07-estacionamento",
    "2027-01-18": "17-demissao", "2027-01-21": "10-banheiro", "2027-01-25": "27-lavar-banheiro", "2027-01-28": "29-guarda",
}

# ---------- frases Manchete já aprovadas na reserva do Orbit (papel claro): (dia, hora, data da pauta)
FRASES = [
    ("2026-11-12", "19:00", "2026-11-12"), ("2026-11-19", "19:00", "2026-11-17"), ("2026-11-26", "19:00", "2026-11-24"),
    ("2026-12-03", "19:00", "2026-12-01"), ("2026-12-10", "19:00", "2026-12-08"), ("2026-12-17", "19:00", "2026-12-15"),
    ("2027-01-03", "12:00", "2026-11-10"), ("2027-01-04", "12:00", "2026-11-14"), ("2027-01-06", "12:00", "2026-11-26"),
    ("2027-01-07", "19:00", "2026-12-24"), ("2027-01-09", "12:00", "2026-11-28"), ("2027-01-13", "12:00", "2026-12-29"),
    ("2027-01-14", "19:00", "2026-12-03"), ("2027-01-17", "12:00", "2026-12-31"), ("2027-01-21", "19:00", "2026-12-10"),
    ("2027-01-24", "12:00", "2026-11-19"), ("2027-01-28", "19:00", "2026-12-17"),
]

# ---------- outros estilos aprovados pela Jessica (Papel e Ouro, Verbete, Palavra de Ouro): legenda escrita agora
RODAPE = ("\n\nCada caso tem detalhes. Procure uma advogada de confiança.\n\n"
          "Esse é o perfil da Advogada Letícia Barros e aqui você encontra tudo sobre os seus direitos.\n\n"
          "Letícia Barros · OAB/ES 39.948\n\n")
OUTROS = {
    "2027-01-01": ("verbete/pecas/01-leticia-barros.jpg", "Verbete: Letícia Barros",
                   "Letícia Barros: a advogada da mulher que trabalha.\n\n2027 começa e eu quero te lembrar por que este "
                   "perfil existe: para explicar, sem juridiquês, o que a lei garante para quem trabalha, para as gestantes "
                   "e para as famílias.\n\nAqui você encontra direito do trabalho, previdência e família, sempre com a "
                   "lei citada, para você conferir.\n\nSiga o perfil e compartilhe com quem precisa saber dos próprios direitos."
                   + RODAPE + "#DireitoTrabalhista #DireitosDaMulher #GestanteCLT #AdvogadaTrabalhista #VitóriaES",
                   "💬 Qual assunto você quer ver aqui em 2027?"),
    "2027-01-10": ("papel-e-ouro/pecas/clara-02-capa-nome.jpg", "Letícia Barros, a advogada da mulher que trabalha",
                   "Prazer, Letícia Barros.\n\nSou advogada em Vitória/ES e cuido de direito do trabalho, previdência e "
                   "família. Escolhi um público: a mulher que trabalha, a gestante, a mãe.\n\nAqui eu explico a lei em "
                   "linguagem simples, com o artigo citado, para você reconhecer quando um direito está sendo desrespeitado."
                   "\n\nSalve o perfil e compartilhe com uma amiga." + RODAPE
                   + "#DireitoTrabalhista #DireitosDaMulher #Gestante #AdvogadaTrabalhista #VitóriaES",
                   "💬 Me conta: você chegou aqui por qual assunto?"),
    "2027-01-16": ("papel-e-ouro/pecas/clara-05-gritar.jpg", "Assédio moral: gritar não é cobrar",
                   "Gritar não é cobrar.\n\nCobrar resultado faz parte do trabalho. Humilhar, expor na frente dos colegas e "
                   "repetir isso todo dia, não.\n\nO que vale saber:\n📌 Humilhação repetida pode configurar assédio moral\n"
                   "📌 A empresa responde pelo que o chefe faz\n📌 Anote datas, nomes de quem viu e guarde mensagens\n"
                   "📌 Procure ajuda: saúde mental também é direito" + RODAPE
                   + "#AssédioMoral #DireitoTrabalhista #SaúdeMental #DireitosDoTrabalhador #AdvogadaTrabalhista",
                   "📚 Base: CLT, art. 483; Código Civil, arts. 186 e 932, III.\n💬 Você já viu um chefe gritar com alguém na frente de todos?"),
    "2027-01-20": ("papel-e-ouro/pecas/clara-01-lei-tarjada.jpg", "Grávida? Leia esta linha do art. 391",
                   "Grávida? Leia esta linha.\n\n\"Não constitui justo motivo para a rescisão do contrato de trabalho da "
                   "mulher o fato de haver contraído matrimônio ou de encontrar-se em estado de gravidez.\" (CLT, art. 391)"
                   "\n\nA gravidez não é motivo para demitir. E a estabilidade vai da confirmação da gravidez até 5 meses "
                   "depois do parto.\n\nSalve e mande para uma gestante que você conhece." + RODAPE
                   + "#GestanteCLT #EstabilidadeDaGestante #DireitoTrabalhista #DireitosDaMulher #AdvogadaTrabalhista",
                   "📚 Base: CLT, art. 391; ADCT, art. 10, II, b.\n💬 Você conhece alguém que foi demitida grávida?"),
    "2027-01-23": ("papel-e-ouro/pecas/clara-07-rapidinho.jpg", "\"Doutora, é rapidinho\"",
                   "\"Doutora, é rapidinho.\"\n\nO áudio tinha 4 minutos. 😅\n\nE tudo bem: dúvida de direito raramente é "
                   "rapidinha, porque cada caso tem detalhes que mudam a resposta. Por isso eu explico aqui, com calma e "
                   "com a lei citada, as dúvidas que mais aparecem.\n\nSalve este perfil para quando a sua dúvida chegar."
                   + RODAPE + "#DireitoTrabalhista #AdvogadaTrabalhista #VidaDeAdvogada #DireitosDaMulher #VitóriaES",
                   "💬 Qual foi a sua última dúvida \"rapidinha\"?"),
    "2027-01-27": ("papel-e-ouro/pecas/clara-08-nunca-prometo.jpg", "Por que eu nunca prometo que você vai ganhar",
                   "Por que eu nunca vou te prometer que você vai ganhar?\n\nPorque advocacia informa o caminho, não garante "
                   "o resultado. Quem decide é o juiz, a partir das provas e da lei.\n\nO que eu posso fazer: explicar os "
                   "seus direitos, avaliar as provas com você e dizer com honestidade quais são as chances." + RODAPE
                   + "#AdvogadaTrabalhista #DireitoTrabalhista #ÉticaProfissional #DireitosDaMulher #VitóriaES",
                   "💬 Alguém já te prometeu ganhar uma causa?"),
    "2027-01-30": ("papel-e-ouro/pecas/fora-04-errata.jpg", "Errata: demitido também recebe 13º",
                   "Errata.\n\nOnde se lê: \"foi demitido, perdeu o 13º\".\nLeia-se: na dispensa sem justa causa, o 13º "
                   "proporcional é devido.\n\nO que vale saber:\n📌 1/12 do 13º para cada mês com 15 dias ou mais trabalhados\n"
                   "📌 Quem pede demissão também recebe o proporcional\n📌 Só a justa causa tira esse direito\n"
                   "📌 Confira o valor no termo de rescisão" + RODAPE
                   + "#13Salário #Rescisão #DireitoTrabalhista #DireitosDoTrabalhador #AdvogadaTrabalhista",
                   "📚 Base: Lei 4.090/1962, art. 3º; Súmula 157 do TST.\n💬 Você conferiu o 13º na sua rescisão?"),
    "2027-01-31": ("palavra-de-ouro/pecas/01-hora-extra.jpg", "Hora extra se paga",
                   "Hora extra se paga.\n\nCom adicional de, no mínimo, 50% sobre a hora normal. Não é favor, e não pode "
                   "virar \"banco\" sem acordo.\n\nO que vale saber:\n📌 Confira as horas extras no holerite todo mês\n"
                   "📌 Banco de horas precisa de acordo e tem prazo para compensar\n📌 Guarde mensagens de convocação fora "
                   "do horário" + RODAPE
                   + "#HoraExtra #DireitoTrabalhista #DireitosDoTrabalhador #CLT #AdvogadaTrabalhista",
                   "📚 Base: Constituição, art. 7º, XVI; CLT, art. 59.\n💬 Você confere as horas extras no holerite?"),
}

# ---------- Reels Flagrante prontos e nunca publicados (aprovados em 09/11/2026), terça e sexta 19h
FLAGRANTE = {"2026-12-04": ("10-salario-atrasado", "Salário atrasado"), "2027-01-05": ("05-ferias", "Férias"),
             "2027-01-08": ("01-atestado", "Atestado do posto"), "2027-01-12": ("02-holerite", "Holerite"),
             "2027-01-15": ("03-ponto", "Folha de ponto"), "2027-01-19": ("07-experiencia", "Contrato de experiência"),
             "2027-01-22": ("12-sem-folga", "Sem folga"), "2027-01-26": ("13-aviso-previo", "Aviso prévio"),
             "2027-01-29": ("08-por-fora", "Salário por fora")}

# ---------- Reels Mito ou Lei novos de janeiro (mito_lei.py + conteudo_jan.py), 19h
MITO_JAN = {"2027-01-13": "01-13-demitido-13", "2027-01-16": "01-16-atestado-13", "2027-01-18": "01-18-mamografia-falta",
            "2027-01-20": "01-20-cancer-inss", "2027-01-23": "01-23-medida-protetiva-trabalho",
            "2027-01-25": "01-25-licenca-adotante", "2027-01-27": "01-27-penhora-salario", "2027-01-30": "01-30-casamento-70"}

# ---------- Reels gravados pela Dra.: domingo 15h30 (melhor alcance de Reels no domingo, dados do perfil)
# ficam PAUSADOS até a versão no motor moderno ser aprovada (a Jessica achou a edição antiga feia, 10/11/2026)
DRA_DOMINGO = [("2026-11-15", "limbo previdenciário (1/2)"), ("2026-11-22", "limbo previdenciário, quem paga"),
               ("2026-11-29", "Série Hora extra (1/3)"), ("2026-12-06", "Série Hora extra (2/3)"),
               ("2026-12-13", "Série Hora extra (3/3)"), ("2026-12-20", "Reels: pediu demissão? A multa do 477"),
               ("2026-12-27", "Reels: conselhos da advogada")]
HORA_DRA = "15:30"

MOVER = [("Mito ou Lei: BPC dá direito a 13º", "2027-01-07", "2027-01-06", "19:00")]


def legendas_manchete():
    txt = (ESTILOS / "manchete" / "legendas.md").read_text(encoding="utf-8")
    out = {}
    for bloco in re.split(r"^## ", txt, flags=re.M)[1:]:
        nome, corpo = bloco.split("\n", 1)
        alt = re.search(r"\*\*Texto alternativo:\*\*\s*(.+)", corpo)
        leg = re.search(r"\*\*Legenda:\*\*\s*\n(.+?)\n\*\*Primeiro comentário:\*\*", corpo, re.S)
        com = re.search(r"\*\*Primeiro comentário:\*\*\s*\n(.+)", corpo, re.S)
        out[nome.strip()] = {"alt": alt.group(1).strip() if alt else "", "legenda": leg.group(1).strip(),
                             "primeiro_comentario": com.group(1).strip() if com else ""}
    return out


def titulo_manchete(alt, leg):
    """Título no calendário do Orbit: o tema, que abre o texto alternativo ("Estabilidade da gestante: ...")."""
    tema = alt.split(":", 1)[0].strip() if alt else leg.split("\n", 1)[0].strip()
    return f"Manchete: {tema}"[:200]


def main():
    ENVIO.mkdir(exist_ok=True)
    acoes = []
    legs = legendas_manchete()
    usados = set()
    for dia, nome in MANCHETE_12H.items():
        chave = f"manchete-{nome}"
        assert chave not in usados, chave
        usados.add(chave)
        arq = f"estatico-{chave}.jpg"
        shutil.copy(ESTILOS / "manchete" / "pecas" / f"{chave}.jpg", ENVIO / arq)
        l = legs[chave]
        acoes.append({"acao": "nova", "dia": dia, "hora": "12:00", "tipo": "estatico", "formato": "post",
                      "titulo": titulo_manchete(l["alt"], l["legenda"]), "area": "Trabalhista", "arquivo": arq, "estilo": "manchete",
                      "legenda": l["legenda"], "primeiro_comentario": l["primeiro_comentario"], "alt": l["alt"]})
    for dia, (caminho, titulo, leg, com) in OUTROS.items():
        arq = "estatico-" + caminho.replace("/pecas/", "-").replace("/", "-")
        shutil.copy(ESTILOS / caminho, ENVIO / arq)
        acoes.append({"acao": "nova", "dia": dia, "hora": "12:00", "tipo": "estatico", "formato": "post", "titulo": titulo,
                      "area": "Trabalhista", "arquivo": arq, "estilo": caminho.split("/")[0], "legenda": leg,
                      "primeiro_comentario": com})
    reserva = [l.rstrip("\n").split("\t") for l in SCRATCH_RESERVA.read_text(encoding="utf-8").splitlines() if l.strip()]
    for dia, hora, pauta in FRASES:
        ids = [r[0] for r in reserva if r[1] == "frase" and r[2] == pauta and "v=manchete1" in r[4]]
        assert len(ids) == 1, (pauta, ids)
        acoes.append({"acao": "agendar", "dia": dia, "hora": hora, "piece_id": ids[0], "formato": "post", "status": "pronto"})
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
    for dia, nome in MITO_JAN.items():
        pasta = MOTION / "mito-lei" / nome
        video, capa = f"mito-lei-{nome}-v3.mp4", f"mito-lei-{nome}-capa-moldura-viva.jpg"
        if not (pasta / f"{nome}-v3.mp4").exists():
            print("FALTA VÍDEO", nome)
            continue
        shutil.copy(pasta / f"{nome}-v3.mp4", ENVIO / video)
        shutil.copy(pasta / "capa-moldura-viva.jpg", ENVIO / capa)
        l = json.loads((pasta / "legenda.json").read_text(encoding="utf-8"))
        acoes.append({"acao": "nova", "dia": dia, "hora": "19:00", "tipo": "reels", "formato": "reels",
                      "titulo": "Mito ou Lei: " + l["legenda"].split("?", 1)[0], "area": "Trabalhista", "video": video,
                      "capa": capa, "estilo": "mito-ou-lei", "legenda": l["legenda"],
                      "primeiro_comentario": l.get("primeiro_comentario", "")})
    for dia, trecho in DRA_DOMINGO:
        acoes.append({"acao": "dra", "dia": dia, "hora": HORA_DRA, "titulo_contem": trecho, "status": "pausado",
                      "capa": f"dra-capa-{dia}.jpg"})
    for titulo, de, para, hora in MOVER:
        acoes.append({"acao": "mover", "titulo": titulo, "de": de, "para": para, "hora": hora})
    ordem = {"mover": 0, "dra": 1, "agendar": 2, "nova": 3}  # o Limbo sai da terça/sexta antes do Flagrante entrar
    acoes.sort(key=lambda a: ordem[a["acao"]])
    (AQUI / "editorial_jan.json").write_text(json.dumps(acoes, ensure_ascii=False, indent=1), encoding="utf-8")
    from collections import Counter
    print(len(acoes), Counter(a["acao"] for a in acoes), "arquivos:", len(list(ENVIO.iterdir())))


if __name__ == "__main__":
    main()
