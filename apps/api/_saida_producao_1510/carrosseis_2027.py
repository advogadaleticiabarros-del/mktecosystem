"""Carrosséis da série "CLT em 2027" (pedido da Jessica em 16/11/2026: separar o que vira conteúdo dos artigos de 2027).
Formato v5 aprovado (capa Ouro editorial, checklist, fecho com retrato real da Dra.). Quartas às 12h, no lugar de
Manchetes avulsas (que voltam para a reserva). Base: decisão do STF de 12/11/2026 (ADIs 8.041 e 8.042), EC 141/2026,
Lei 15.371/2026. Sem "R$" nas peças. Reconferir a liminar antes de cada data (o Plenário ainda vai referendar).
Uso: DADOS=c2027 python carrossel_v5.py [chave ...]
"""
from carrosseis_jan_fev import FIM, M, X

BLOG = "advogadaleticiabarros.com.br/blog/"

# foto da página 5 (id Pexels em _fotos_pexels/<id>.jpg); capa em _fotos_pexels/original-<chave>.jpg (16/11/2026)
FOTO5 = {"hora-extra-42-horas": 9062772, "escala-42-horas": 29509530, "clt-2027": 19915766}


def C(data, chave, area, tag, titulo, capa, itens, checklist, fecho, legenda, fontes, perguntas, tags, pc):
    leg = (legenda + "\n\n❓ As perguntas que mais chegam aqui:\n" + "\n".join(f"📌 {p}" for p in perguntas)
           + f"\n\n📚 Fontes: {fontes}.\n\n🔖 Salva e {fecho[2]}" + FIM + tags)
    return {"chave": chave, "data": data, "area": area, "titulo": titulo, "carrossel": {
        "tag": tag, "area": area, "capa": capa, "itens": itens, "checklist": checklist, "fecho": fecho,
        "objetos": ["nenhum", "nenhum", "nenhum"], "foto5": None, "legenda": leg, "pc": pc}}


TEMAS = [
    C("2026-12-09", "hora-extra-42-horas", "Trabalhista", "Hora extra", "Hora extra com a jornada de 42 horas",
      ["Hora extra", "Hora extra", "vale mais a partir de 16/12", f"Menos horas, mesmo salário: {M}a sua hora sobe{X}.", "EC 141/2026"],
      [["Mesmo<br><em>salário</em>", f"A jornada cai para 42 horas e {M}o salário não pode diminuir{X}.", "EC 141/2026"],
       ["Divide<br>por <em>210</em>", f"O salário do mês era dividido por 220. {M}Com 42 horas, por 210{X}.", "Súmula 431 do TST"],
       ["Cerca de<br><em>4,8% a mais</em>", f"É quanto sobe a sua hora. {M}E a hora extra sobe junto{X}.", "Constituição, art. 7º, XVI"],
       ["A exceção dos<br><em>24 minutos</em>", f"Sem acordo até 15/12, o dia vai a 8h24 {M}sem extra nesses minutos{X}.", "STF, ADIs 8.041 e 8.042"],
       ["Confira<br>o <em>holerite</em>", "Em janeiro, compare:", ""]],
      ["Holerite de novembro e o de janeiro", "Valor de cada hora extra", "Horas pagas e horas do ponto"],
      ["Menos horas,<br>hora <em>mais cara</em>.", "O salário não diminui com a jornada.", "manda pra quem faz hora extra."],
      "A partir de 16/12, a sua hora de trabalho passa a valer mais. Arrasta pro lado e veja por quê. ⏰\n\n"
      "Com a jornada de 42 horas e o mesmo salário, a conta do mês deixa de ser dividida por 220 e passa a ser por 210. "
      "Cada hora sobe cerca de 4,8%, e a hora extra, que é calculada sobre ela, sobe junto.",
      "Emenda Constitucional 141/2026; Constituição, art. 7º, XVI; Súmula 431 do TST; STF, ADIs 8.041 e 8.042 (decisão de 12/11/2026)",
      ["Minha hora extra aumenta? Tende a aumentar, se o salário continuar o mesmo.",
       "E com 40 horas? A conta passa a ser por 200, a partir de 16/12/2027.",
       "Os 24 minutos a mais são extra? Sem acordo da categoria, não, até 15/12/2027."],
      "#HoraExtra #Fimda6x1 #DireitoTrabalhista #CLT #AdvogadaVitóriaES",
      f"📚 Base legal: EC 141/2026; Súmula 431 do TST.\n📖 A conta passo a passo: {BLOG}hora-extra-jornada-42-horas-como-calcular.html\n💬 Você faz hora extra?"),
    C("2026-12-16", "escala-42-horas", "Trabalhista", "Fim da 6x1", "Hoje começa a jornada de 42 horas",
      ["Fim da 6x1", "Hoje", "começa a jornada de 42 horas", f"E se a sua empresa {M}não mudar a escala{X}?", "EC 141/2026"],
      [["<em>2 folgas</em><br>por semana", f"A partir de hoje: até 42 horas {M}e dois dias de descanso{X}.", "EC 141/2026"],
       ["O STF<br><em>manteve</em>", f"O pedido de adiamento {M}não foi atendido{X}. A data é hoje.", "STF, ADIs 8.041 e 8.042"],
       ["Até <em>8h24</em><br>por dia", f"Sem acordo da categoria: 5 dias de até 8h24, {M}sem extra nos 24 minutos{X}.", "STF, decisão de 12/11/2026"],
       ["A vantagem<br><em>não some</em>", f"Benefício da convenção {M}não pode ser cortado pela empresa sozinha{X}.", "STF, decisão de 12/11/2026"],
       ["Não mudou?<br><em>Guarde</em>", "Comece a documentar hoje:", ""]],
      ["Foto da escala de dezembro", "Espelho de ponto", "Holerite de novembro"],
      ["Seis dias com uma<br>folga <em>acabou</em>.", "Com ou sem acordo, são duas folgas.", "manda pra quem trabalha na 6x1."],
      "Hoje, 16 de dezembro, começa a jornada de até 42 horas por semana, com dois dias de descanso. Arrasta pro lado. 📅\n\n"
      "O STF manteve a data. Sem acordo da categoria, a empresa pode fazer 5 dias de até 8h24, mas não pode manter seis "
      "dias de trabalho com uma folga. E o salário não pode diminuir.",
      "Emenda Constitucional 141/2026; STF, ADIs 8.041 e 8.042 (decisão de 12/11/2026)",
      ["O STF suspendeu o fim da 6x1? Não, manteve 16/12.",
       "A empresa pode reduzir meu salário? Não.",
       "E em empresa pequena? O calendário é o mesmo."],
      "#Fimda6x1 #Escala6x1 #DireitoTrabalhista #DireitosDoTrabalhador #AdvogadaVitóriaES",
      f"📚 Base legal: EC 141/2026; STF, ADIs 8.041 e 8.042.\n📖 O que fazer se a escala não mudar: {BLOG}escala-42-horas-16-de-dezembro-e-se-a-empresa-nao-mudar.html\n💬 A sua escala já mudou?"),
    C("2026-12-30", "clt-2027", "Trabalhista", "CLT em 2027", "O que muda na CLT em 2027",
      ["CLT em 2027", "2027", "o que muda para quem tem carteira", f"Jornada menor, {M}licença-paternidade maior{X}.", "EC 141 e Lei 15.371"],
      [["<em>42 horas</em><br>e 2 folgas", f"Desde 16/12/2026, {M}sem redução de salário{X}.", "EC 141/2026"],
       ["Pai com<br><em>10 dias</em>", f"A licença-paternidade dobra {M}a partir de 1º de janeiro{X}.", "Lei 15.371/2026"],
       ["Hora<br><em>mais cara</em>", f"Menos horas e o mesmo salário: {M}a hora extra sobe{X}.", "Súmula 431 do TST"],
       ["<em>40 horas</em><br>em dezembro", f"A segunda etapa chega {M}em 16/12/2027{X}.", "EC 141/2026"],
       ["Comece o ano<br><em>organizada</em>", "Guarde desde já:", ""]],
      ["Holerite de novembro de 2026", "Foto da sua escala", "Certidão do bebê, se for pai"],
      ["2027 começa com<br><em>mais direitos</em>.", "Saber é o primeiro passo para cobrar.", "manda pra quem trabalha de carteira assinada."],
      "O que muda na CLT em 2027? Arrasta pro lado e veja as datas certas. 🗓️\n\n"
      "O ano começa com a jornada de até 42 horas e duas folgas por semana, a licença-paternidade de 10 dias a partir de "
      "1º de janeiro e a hora extra calculada sobre uma hora mais cara. Em 16/12/2027, a jornada cai para 40 horas.",
      "Emenda Constitucional 141/2026; Lei 15.371/2026; Súmula 431 do TST",
      ["A 6x1 acabou? Sim, desde 16/12/2026.",
       "Quantos dias de licença-paternidade? 10 em 2027 e 15 em 2028.",
       "O salário pode cair com a jornada menor? Não."],
      "#CLT2027 #Fimda6x1 #LicençaPaternidade #DireitoTrabalhista #AdvogadaVitóriaES",
      f"📚 Base legal: EC 141/2026; Lei 15.371/2026.\n📖 O calendário completo: {BLOG}o-que-muda-na-clt-em-2027.html\n💬 Qual mudança mais mexe com você?"),
]
