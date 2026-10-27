"""Legenda e primeiro comentário da série 22 v2 (ângulo "vingança" pós-eleição, 27/10/2026). Reels animado, narração
com a voz clonada da Dra. (IA). Neutro (nenhum partido nem candidato), sem oferta de serviço, sem promessa, 5 hashtags.
A mesma legenda vale para o Reels 1 (gancho A, seguidores) e o 2 (gancho B, Trial Reels). Fatos no docstring de
serie_vinganca.py. Primeiro comentário com pergunta de opinião (nunca "conte seu caso", CED art. 42 I)."""
from legendas import ASSINATURA, LP  # noqa: F401  (assinatura e LP da v1, iguais)

LEGENDA = f"""Demitido por vingança depois da eleição? Isso tem nome na lei: dispensa discriminatória. E não importa em quem você votou.

O voto é secreto e ninguém pode perder o emprego por opinião política. No dia seguinte ao 2º turno, o Ministério Público do Trabalho recebeu 140 denúncias de assédio eleitoral, o maior número num único dia em 2026.

Quando a demissão é por esse motivo, a lei deixa o trabalhador escolher: voltar ao emprego, com os salários do período em que ficou afastado, ou receber em dobro a remuneração desse período. A indenização por dano moral pode ser pedida à parte.

❓ As perguntas que mais chegam aqui:
📌 A empresa pode me demitir porque postei sobre política? Demitir por causa da opinião política é discriminação. Ofensa à empresa ou a colegas é outra conversa, e cada caso é avaliado.
📌 Fui ameaçado de demissão antes da eleição. Isso é crime? Ameaçar para obrigar alguém a votar ou não votar em alguém é crime eleitoral (Código Eleitoral, art. 301).
📌 Onde denunciar? No site do MPT, em "Denuncie". A denúncia pode ser sigilosa.

✅ Antes de sair do grupo da empresa, guarde: mensagens, áudios, prints de grupos e de posts, e-mails, carta de dispensa e nomes de testemunhas.

👉 Passo a passo completo e formulário para pedir orientação: link na bio.

📚 Base: Constituição, arts. 5º, VIII, e 14; Lei 9.029/1995, arts. 1º e 4º; Convenção 111 da OIT; Resolução TSE 23.755/2026.

🔖 Salva e manda pra quem precisa saber.

{ASSINATURA}

#AssedioEleitoral #DireitoTrabalhista #DemissaoDiscriminatoria #DireitosDoTrabalhador #AdvogadaVitóriaES"""

PRIMEIRO_COMENTARIO = """📚 Base: Lei 9.029/1995, art. 4º (reintegração ou remuneração em dobro) e Constituição, art. 5º, VIII.
💬 Na sua opinião: política deveria ficar fora do ambiente de trabalho? Responde com sim ou não."""

TIKTOK = """Demitido por vingança depois da eleição? Isso é dispensa discriminatória, não importa em quem você votou. A lei prevê voltar ao emprego com os salários do período ou receber em dobro, além do dano moral. Guarde as provas antes de sair do grupo da empresa. Passo a passo no link do perfil. Cada caso tem detalhes. Dra. Letícia Barros, OAB/ES 39.948. Narração com IA.
#assedioeleitoral #direitotrabalhista #demissao #eleicoes2026 #clt"""

if __name__ == "__main__":
    print(len(LEGENDA), "caracteres; hashtags:", LEGENDA.count("#"), "| linha 1:", len(LEGENDA.splitlines()[0]),
          "| pc:", len(PRIMEIRO_COMENTARIO), "| tiktok:", len(TIKTOK))
