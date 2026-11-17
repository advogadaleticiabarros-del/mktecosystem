"""Série 23 · Novos Reels 3 (16/11/2026): dois Reels gravados pela Dra. Letícia, um tema cada, estilo inteiro com banco.
R1 (IMG_2092) Intermitente: o 13º, as férias e o 1/3 já vêm no pagamento de cada período.
   Base: CLT art. 452-A §1º (convocação com 3 dias corridos), §2º (1 dia útil para responder; silêncio = recusa),
   §6º (ao fim de cada período: remuneração, férias proporcionais + 1/3, 13º proporcional, DSR e adicionais).
   Cortes: "e o FGTS" (FGTS não vem na diária: o empregador deposita à parte, §8º); "nada mais o trabalhador vai ter
   direito de receber" (exagero); "não tem direito a férias" (o descanso de 1 mês a cada 12 continua, §9º);
   "danoso" e "atendimento" da abertura (opinião e caso de cliente). Gancho repete a fala do 13º.
R2 (IMG_2093) Intermitente de fachada: todo dia, por anos, subordinado e sem poder recusar -> o contrato pode ser
   questionado; a diária vira salário e 13º, férias e FGTS são cobrados à parte.
   Base: CLT art. 443 §3º e art. 452-A (Lei 13.467/2017); art. 9º (nulidade do ato que desvirtua a CLT); há julgados
   que afastam o intermitente sem alternância real. Sem promessa de resultado ("pode ser questionado").
   Cortes: "quando ele não tem ameaça..." (frase invertida), trecho final truncado ("o que isso desse com o terceiro").
"""
from pathlib import Path

VIDEOS = Path(__file__).resolve().parents[1] / "work" / "videos"
VEL = 1.05
BR = Path(r"C:\Users\prosy\Desktop\NOVOS REELS\3")
SRC = BR / "IMG_2092.MOV"
FONTES = {1: BR / "IMG_2092.MOV", 2: BR / "IMG_2093.MOV"}
VOCABULARIO = ("contrato intermitente, décimo terceiro, férias, um terço, diária, convocação, bico, FGTS, CLT, "
               "artigo 443, subordinado, alternância, jurisprudência, julgados, Judiciário, Letícia Barros")

FALAS = {
    1: [(72.80, 76.75, "o trabalhador fica esperando receber o décimo terceiro e não tem"),
        (27.80, 32.50, "a grande maioria das pessoas não sabem e entram com um contrato intermitente"),
        (40.40, 48.70, "ele é convocado com três dias e pode recusar a convocação com até 24 horas, então ele não precisa "
                       "ir mas ele não receberia por esse dia."),
        # "né" entre 53,25 e 53,70 (medido no envelope do áudio): sai
        (49.22, 53.07, "Esse contrato ele é o antigo extra, é o antigo bico", "fixo"),
        (53.72, 63.00, "que a gente fazia, era convocado para ir trabalhar e recebia por hora, recebia pelo dia trabalhado. "
                       "Esse é o contrato intermitente, agora ele tem um nome.", "fixo"),
        # "O contrato intermitente, ele retira," (63,58 a 66,5) é começo falso: entra a partir do "não é que" (66,52)
        (66.52, 80.85, "não é que ele retira direito de trabalhador, mas só que lá no final do ano "
                       "agora que é período de décimo terceiro o trabalhador fica esperando receber o décimo terceiro e não "
                       "tem porque ele recebe já está incluso lá no valor da diária,", "fixo"),
        (81.25, 83.45, "assim como também ele não tem direito", "fixo"),
        (84.42, 91.88, "a receber o valor da férias, não tem direito a receber um terço de férias porque no valor do dia, "
                       "no valor daquela hora já está inserido.", "fixo"),
        (100.21, 106.47, "se o dia de trabalho for 150 reais, esse dia ele engloba décimo terceiro, férias", "fixo"),  # "então" (99,90-100,20) sai
        (112.45, 115.40, "Meu nome é Letícia Barros e aqui nesse perfil falo sobre seus direitos.")],
    2: [(15.55, 21.93, "trabalhou ele durante anos, vamos colocar 3, 4 anos, todos os dias, e aí chegava no final do ano, "
                       "não tinha décimo terceiro", "fixo"),  # gancho (a mesma fala volta no 3º trecho)
        # "o que que acontece nesse caso" sai (repetição); a pergunta vai na tela
        (3.31, 9.68, "o trabalhador trabalhou em contrato intermitente, não sabia que era "
                     "contrato intermitente, ia trabalhar todos os dias,", "fixo"),
        (15.55, 24.28, "trabalhou ele durante anos, vamos colocar 3, 4 anos, todos os dias, e aí chegava no final do ano, "
                       "não tinha décimo terceiro, chegava no final do ano, não tinha férias", "fixo"),
        # "né" entre 29,85 e 29,95 (envelope do áudio): sai
        (25.62, 29.80, "tendo esse trabalhador as provas de que ele era subordinado,", "fixo"),
        (30.05, 42.30, "dessa não alternância de períodos que ele sempre trabalhou todos os dias, tendo ele essa comprovação, "
                       "testemunhas que provem que ele ia trabalhar, esse contrato pode ser questionado,", "fixo"),
        # hesitação entre "443" e "parágrafo" (80,6 a 82,05) e "da" arrastado de "depois da mudança de 2017" saem;
        # a Reforma de 2017 vai na tela
        (70.62, 80.58, "Claro que como o contrato intermitente ele é regularizado dentro da CLT, ele está previsto no "
                       "artigo 443,", "fixo"),
        (82.08, 84.27, "parágrafo 3 da CLT,", "fixo"),
        (89.70, 95.30, "existe muita jurisprudência, existe muito juiz que entende como válido o contrato intermitente,"),
        (96.30, 100.10, "mas também existem alguns julgados,"),
        # termina em "recusar": o "a" arrastado (124,4 a 125,5) antes de "ir trabalhar" sai
        (112.95, 123.98, "a gente pode sim levar ao judiciário pra gente discutir, inclusive quando esse trabalhador "
                         "vai todos os dias, quando esse trabalhador ele é subordinado, quando esse trabalhador não pode "
                         "se recusar", "fixo"),
        # "e aí o que que aconteceria?" sai (repetição); a pergunta vai na tela
        (50.95, 69.95, "Receberia esse valor que você recebeu na diária, você receberia os reflexos dele, então esse seria "
                       "o seu salário e não englobaria aí 13º, férias, FGTS, então você poderia cobrar na justiça essa "
                       "diferença."),
        (163.30, 166.10, "Meu nome é Letícia Barros e aqui nesse perfil falo sobre seus direitos.")],
}
