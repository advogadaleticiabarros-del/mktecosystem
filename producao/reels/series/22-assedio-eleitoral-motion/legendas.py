"""Legenda e primeiro comentário da série 22 (27/10/2026): Reels animado, narração com a voz clonada da Dra. (IA).
Neutro (nenhum partido nem candidato), sem oferta de serviço, sem promessa, 5 hashtags. Fatos no docstring de serie.py.
Link da página com o passo a passo e o formulário: na bio (UTM instagram/reels) e no TIKTOK abaixo."""

LP = "https://advogadaleticiabarros.com.br/lp/demissao-por-voto.html"

ASSINATURA = """Cada caso tem detalhes. Se esse é o seu caso, procure uma advogada de confiança.

Dra. Letícia Barros · Direito Trabalhista · Vitória/ES · OAB/ES 39.948
Esse é o perfil da Advogada Letícia Barros e aqui você encontra tudo sobre Direito Trabalhista.
Atualizado em outubro de 2026.
🔊 Narração produzida com inteligência artificial."""

LEGENDAS = {
    1: {"titulo": "Reels: demissão por causa do voto (assédio eleitoral)",
        "legenda": f"""Demitido por causa do seu voto? Isso é dispensa discriminatória, e a lei protege qualquer trabalhador, não importa em quem votou.

O voto é secreto e ninguém pode perder direitos por opinião política. Um dia depois do 2º turno, o Ministério Público do Trabalho recebeu 140 denúncias de assédio eleitoral, o maior número num único dia em 2026.

Quando a demissão é por esse motivo, a lei prevê que o trabalhador escolha entre voltar ao emprego, com os salários do período em que ficou afastado, ou receber em dobro a remuneração desse período. A indenização por dano moral pode ser pedida à parte.

❓ As perguntas que mais chegam aqui:
📌 A empresa pode me demitir porque postei sobre política? Demitir por causa da opinião política é discriminação. Ofensa à empresa ou a colegas é outra conversa, e cada caso é avaliado.
📌 Fui ameaçado de demissão antes da eleição. Isso é crime? Ameaçar para obrigar alguém a votar ou não votar em alguém é crime eleitoral (Código Eleitoral, art. 301).
📌 Onde denunciar? No site do MPT, em "Denuncie". A denúncia pode ser sigilosa.

✅ Guarde agora: mensagens, áudios, prints de grupos e de posts, e-mails, carta de dispensa e nomes de testemunhas.

👉 Passo a passo completo e formulário para pedir orientação: link na bio.

📚 Base: Constituição, arts. 5º, VIII, e 14; Lei 9.029/1995, arts. 1º e 4º; Convenção 111 da OIT; Resolução TSE 23.755/2026.

🔖 Salva e manda pra quem precisa saber.

{ASSINATURA}

#AssedioEleitoral #DireitoTrabalhista #DemissaoDiscriminatoria #DireitosDoTrabalhador #AdvogadaVitóriaES""",
        "pc": """📚 Base: Lei 9.029/1995, art. 4º (reintegração ou remuneração em dobro) e Constituição, art. 5º, VIII.
💬 No seu trabalho falaram de política nessa eleição? Como foi?"""},
}

TIKTOK = f"""Demitido por causa do voto? Isso é dispensa discriminatória, não importa em quem você votou. A lei prevê voltar ao emprego com os salários do período ou receber em dobro, além do dano moral. Guarde as provas. Passo a passo no link do perfil. Cada caso tem detalhes. Dra. Letícia Barros, OAB/ES 39.948. Narração com IA.
#assedioeleitoral #direitotrabalhista #demissao #eleicoes2026 #clt"""

if __name__ == "__main__":
    for n, l in LEGENDAS.items():
        print(len(l["legenda"]), "caracteres; hashtags:", l["legenda"].count("#"), "| pc:", len(l["pc"]))
    print("tiktok:", len(TIKTOK))
