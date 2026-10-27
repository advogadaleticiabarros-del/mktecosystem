"""Legendas da campanha "Demissão pelo voto?" (27/10/2026): carrossel no Instagram e no Facebook, primeiros
comentários e instruções dos Stories. Mesma estrutura do método SEO/IA de conteudo_nov.py. Tom neutro: sem partido,
sem candidato, sem oferta de serviço (OAB, Provimento 205/2021). Fatos em ../BRIEFING.md.
"""

LP = "https://advogadaleticiabarros.com.br/lp/demissao-por-voto.html"
UTM = "?utm_source={fonte}&utm_medium={meio}&utm_campaign=assedio-eleitoral-2026"
LINK_STORIES = LP + UTM.format(fonte="instagram", meio="stories")
LINK_FB = LP + UTM.format(fonte="facebook", meio="post")

TAGS = "#AssédioEleitoral #DemissãoDiscriminatória #DireitoTrabalhista #DireitosDoTrabalhador #AdvogadaVitóriaES"

FECHO = """Cada caso tem detalhes. Se esse é o seu caso, procure uma advogada de confiança.

Dra. Letícia Barros · Advogada · Vitória/ES · OAB/ES 39.948
Esse é o perfil da Advogada Letícia Barros e aqui você encontra tudo sobre Direito Trabalhista.
Atualizado em outubro de 2026."""

CORPO = """Demissão por causa do voto é dispensa discriminatória, e a lei protege o trabalhador. Não importa em quem você votou. 🗳️

O MPT recebeu 1.939 denúncias de assédio eleitoral no trabalho até o 2º turno, um recorde, e mais 140 só no dia seguinte à eleição. A Constituição garante que ninguém perde direitos por convicção política, e a Lei 9.029/1995 proíbe demitir por discriminação. Se a demissão foi por isso, a pessoa pode escolher entre voltar ao emprego, com os salários do período, ou receber em dobro a remuneração desse tempo, além de indenização por dano moral.

📌 O que fazer agora:
✅ Salve mensagens, áudios e prints com data, hora e quem mandou
✅ Exporte a conversa do WhatsApp antes de sair do grupo da empresa
✅ Guarde a carta de dispensa e anote nomes de testemunhas
✅ Denuncie em sigilo no site do MPT ou no sindicato

⚠️ Faltar ao trabalho para ir a uma manifestação pode gerar falta e desconto. O que a lei proíbe é demitir por causa do voto, da opinião ou de participar de ato fora do horário.

❓ As perguntas que mais chegam aqui:
📌 A empresa pode descobrir em quem eu votei? O voto é secreto. Ninguém é obrigado a contar nem a provar.
📌 E se o motivo foi um post meu nas redes? Opinião política não é motivo de demissão. Ofensa à empresa ou a colegas é outra discussão, avaliada caso a caso.
📌 Ameaça antes do voto também é proibida? Sim. Coagir alguém a votar ou não votar em um candidato é crime eleitoral.

📚 Fontes: CF, art. 5º, VIII, e art. 14; Lei 9.029/1995, arts. 1º e 4º; Convenção 111 da OIT; Resolução TSE 23.755/2026; Código Eleitoral, art. 301; MPT (balanço de 26/10/2026)."""

LEGENDA_IG = (CORPO + "\n\n🔗 O passo a passo completo, com as provas que valem, está no link dos Stories de hoje.\n\n"
              "🔖 Salva para ter à mão e manda para quem está passando por isso.\n\n" + FECHO + "\n\n" + TAGS)

PC_IG = ("📚 Base legal: Lei 9.029/1995, arts. 1º e 4º; CF, art. 5º, VIII.\n"
         "💬 Você acha que as pessoas sabem que o voto não pode custar o emprego?")

LEGENDA_FB = (CORPO + "\n\n🔗 O passo a passo completo está no primeiro comentário.\n\n"
              "🔖 Compartilhe com quem precisa saber disso.\n\n" + FECHO + "\n\n" + TAGS)

PC_FB = ("Passo a passo completo: o que a lei garante, quais provas servem e como guardar:\n" + LINK_FB)


def instrucao_story(n: int) -> str:
    base = (f"Story {n} de 8 da sequência \"Demissão pelo voto?\". Postar as 8 em sequência, na ordem, pelo app do Instagram.\n\n"
            "No Instagram: + > Story > escolher esta imagem (sem cortar) > Seu story.")
    if n == 2:
        base += ("\n\nAntes de publicar: adesivo ENQUETE no espaço vazio abaixo de \"Você já viu isso acontecer?\".\n"
                 "Pergunta: Você já viu isso acontecer? · Opções: Sim / Não")
    if n == 8:
        base += (f"\n\nAntes de publicar: adesivo LINK no espaço vazio entre \"Toque no link abaixo\" e \"Cada caso tem detalhes\".\n"
                 f"Link: {LINK_STORIES}\nTexto do adesivo: Passo a passo completo\n"
                 "Depois: adicionar os 8 a um destaque chamado \"Seus direitos\" (ou \"Voto e emprego\").")
    return base
